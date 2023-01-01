document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  if (!localStorage.getItem('mailbox')) {
    load_mailbox('inbox')
    window.location.reload()
  } else {
    load_mailbox(localStorage.getItem('mailbox'));
  }
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#reply-body').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Enable Sender field
  document.querySelector('#compose-recipients').disabled = false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
 
  //Fetch mailbox content
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(
      email => show_email(email, mailbox));
  });

  localStorage.setItem('mailbox', mailbox)
}

function send_email() {
    // POST form data to /emails route to send email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then (result => {
      console.log(result);
    });

    localStorage.setItem('mailbox', 'sent')
    windows.location.reload()
    return false;
}

function show_email(email, mailbox) {
  // Create main email div
  const email_div = document.createElement('div');
  email_div.className = "d-flex justify-content-between border border-dark p-1 px-2 mb-1 rounded";
  email_div.id = 'email-item';  

  // Create sender and subject div
  const sender_subject_div = document.createElement('div');
  sender_subject_div.id = 'email-link'
  if (mailbox === 'sent') {
    sender_subject_div.innerHTML = `<b>${email.recipients}</b> Subject: ${email.subject}`;
  } else {
    sender_subject_div.innerHTML = `<b>${email.sender}</b> Subject: ${email.subject}`;
  }
  email_div.append(sender_subject_div);

  // time stamp and archive button div
  const time_stamp_archive_div = document.createElement('div')

  // Create time stamp div
  const timestamp_div = document.createElement('span');
  timestamp_div.innerHTML = email.timestamp;
  timestamp_div.className = 'px-3'
  time_stamp_archive_div.append(timestamp_div);

  // Create archive button if mailbox is not sent
  if (mailbox !== 'sent') {
    const archive_button = document.createElement('i');
    archive_button.id = "archive-button"
    archive_button.style.display = 'inline-block'
    if (!email.archived) {
      archive_button.className = 'bi bi-archive';
    } else {
      archive_button.className = 'bi bi-archive-fill';
    }
    archive_button.addEventListener('click', () => archive_email(email.id, email.archived, mailbox));    
   
    // Add event listener to archive button to allow archiving
    time_stamp_archive_div.append(archive_button);
  }

  // Add the time_stamp_archive_div to email div
  email_div.append(time_stamp_archive_div);

  // add event listener to sender_subject_div to allow click
  sender_subject_div.addEventListener('click', () => load_email(email.id));

  // turn email block background to gray if email has been read
  if (email.read === true) {
    email_div.style.backgroundColor = '#D3D3D3';
  }

  // Append completed main email div to email-view
  document.querySelector('#emails-view').append(email_div);
}

function load_email(id) {
  // Enable display for email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Fetch email data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    document.querySelector('#email-sender').innerHTML = '<b>From: </b>' + email.sender;
    document.querySelector('#email-recipient').innerHTML = '<b>To: </b>' + email.recipients;
    document.querySelector('#email-subject').innerHTML = '<b>Subject: </b>' + email.subject;
    document.querySelector('#email-timestamp').innerHTML = '<b>From: </b>' + email.timestamp;
    document.querySelector('#email-details').innerHTML = email.body;

    // Set email to read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
  });

  // Enable reply button
  document.querySelector('#reply-button').onclick = () => compose_reply(id);
}

function compose_reply(id) {
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    //Prefill recipients
    const recipients = document.querySelector('#compose-recipients');
    recipients.value = email.sender;
    recipients.disabled = true;

    // Prefill subject
    if (!email.subject.startsWith('Re')){
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = email.subject
    }

    // Prefill reply-body
    const reply_body_p = document.querySelector('#reply-body');
    reply_body_p.innerText = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`
    reply_body_p.style.display = 'block';
    document.querySelector('#compose-body').placeholder = 'Reply...'
  })
}

function archive_email(id, is_archived, mailbox) {
  console.log('toggling archive status');

  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // if email is not archived, archive it
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !is_archived
      })
    });
    localStorage.setItem('mailbox', mailbox)
    window.location.reload()
  });
}