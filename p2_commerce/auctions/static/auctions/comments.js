const auction_id = parseInt(JSON.parse(document.querySelector('#auction_id').textContent));
let counter = 1;
const quantity = 5;

document.addEventListener('DOMContentLoaded', load_comments)

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load_comments();
    }
};

function create_comment(comment){
    const comment_div = document.createElement('div');
    comment_div.className = 'd-flex align-items-center py-2'

    const profile_image_div = document.createElement('div')
    profile_image_div.className = 'flex-shrink-0'
    if (comment.profile_image != null) {
        profile_image_div.innerHTML = `<img class="rounded-circle" src=${comment.profile_image} alt="Profile Image" width="50px">`
    } else {
        profile_image_div.innerHTML = `<img class="rounded-circle" src="/media/images/No_image_available.svg.png" alt="Profile Image" width="50px">`

    }
    comment_div.append(profile_image_div)

    const info_div = document.createElement('div')
    info_div.className = "flex-grow-1 ms-3"
    info_div.innerHTML = `<div><strong>${comment.user}</strong><small>${comment.time_diff}</small></div>`
    info_div.innerHTML += comment.comment
    comment_div.append(info_div)
    
    document.querySelector('#comment_list').append(comment_div);
}

function load_comments() {
    // Set start and end comment numbers, and update counter
    const start = counter;
    const end = start + quantity;
    counter = end + 1;

    //Use custom API to get comments
    fetch(`/list_comments/${auction_id}?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        data.forEach(create_comment);
    });
}