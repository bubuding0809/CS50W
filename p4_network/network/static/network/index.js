import {getCookie} from './utils.js';

// Load all posts when document is loaded
document.addEventListener('DOMContentLoaded', () => {

    // Find all like buttons and add like_handler to them
    document.querySelectorAll('.like-btn').forEach( e => {
        e.addEventListener('click', like_handler);
    });

    // Find all edit buttons and add edit_handler to them
    document.querySelectorAll('.edit-btn').forEach(e => {
        e.addEventListener('click', edit_handler);
    })
});

function like_handler(event) {
    const post_id = parseInt(event.target.dataset.id);
    console.log(post_id)
    console.log(`toggling like status for post ${post_id}`)

    fetch(`/posts/${post_id}/toggle_like`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(response => {
        console.log(response);

        // Update like counter with new like count
        const like_counter_span = document.querySelector(`#liked-id-${post_id}`).firstChild;
        like_counter_span.innerText = response.like_count
    });
}

function edit_handler(event) {
    console.log('Editing')
    const post_id = event.target.dataset.id;
    const edit_button = event.target
    const post_content = document.querySelector(`#post-content-${post_id}`);

    const edit_area = document.createElement('textarea');
    edit_area.className = 'form-control mb-3'
    edit_area.rows = 5
    edit_area.cols = 120
    edit_area.id = `post-edit-${post_id}`
    edit_area.value = post_content.innerHTML;
 
    post_content.replaceWith(edit_area);
    edit_button.innerHTML = 'save';


    const save_edit_callback = () => {
        save_edit_handler(post_id, edit_button, save_edit_callback)
    }

    edit_button.removeEventListener('click', edit_handler);
    edit_button.addEventListener('click', save_edit_callback);

    edit_area.addEventListener('keyup', event => {
        if (event.key === 'Enter' && event.shiftKey) return;

        if (event.key === 'Enter') {
            // Call save_edit_handler
            save_edit_handler(post_id, edit_button, save_edit_callback);
        }
        
        if (event.key === 'Escape') {
            // Cancel editing operation
            edit_area.replaceWith(post_content)
            edit_button.innerHTML = 'edit'

            edit_button.removeEventListener('click', save_edit_callback);
            edit_button.addEventListener('click', edit_handler);

        }
    })
}

function save_edit_handler(post_id, edit_button, save_edit_callback) {
    console.log('Saving')
    const new_content = document.querySelector(`#post-edit-${post_id}`);

    fetch(`/posts/${post_id}/edit_post`, {
        method: 'PUT',
        body: JSON.stringify({
            new_content: new_content.value.trim()
        }),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(response => {
        console.log(response);

        const content = document.createElement('p');
        content.id = `post-content-${post_id}`;
        content.style.whiteSpace = 'pre-line';
        content.innerHTML = response.new_content;
        new_content.replaceWith(content);
        edit_button.innerHTML = 'edit';
    })
    .catch(error => {
        console.log(error);
    }) 

    edit_button.removeEventListener('click', save_edit_callback);
    edit_button.addEventListener('click', edit_handler);
}
