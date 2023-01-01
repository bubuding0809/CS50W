import { getCookie } from './utils.js'

document.addEventListener('DOMContentLoaded', () => {
    const follow_btn = document.querySelector('.follow-btn');
    follow_btn.onclick = event => {
        follower_handler(event);
    }
})

function follower_handler(event) {
    const follow_btn = event.target
    const user_id = follow_btn.dataset.userId;
    const username = follow_btn.dataset.username;
    console.log('Toggling follow for ' + username);

    fetch(`/profile/${user_id}/toggle_follow`, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(response => {
        console.log(response);

        //update DOM
        console.log(follow_btn.innerText)
        if (follow_btn.innerText === 'FOLLOW') {
            follow_btn.innerText = 'Unfollow';
        } else {
            follow_btn.innerText = 'follow';
        }
        document.querySelector('.follower-count').innerHTML = response.follower_count;
    })
    .catch(error => {
        console.log(error);
    });
}