const friendsDiv = document.querySelector('#friends > div');
const buttons = friendsDiv.querySelectorAll('button');

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', () => {
        // Find the closest div
        let friend = buttons[i].closest('div');

        // Make the request to the designated route
        var request = new XMLHttpRequest();
        request.open('POST', '/remove_friend/' + friend.id, true);
        request.onload = () => {
            // Ensure that the request was successful
            if (request.status == 200) {
                // Remove the friend from the page
                friendsDiv.removeChild(friend);

                // Check if the user has any friends left and render the appropriate text
                if (friendsDiv.querySelectorAll('div').length == 0) {
                    let heading = document.querySelector('#friends h1');
                    heading.insertAdjacentHTML('afterend', `
                        <p class="text-white text-med">This user has no friends.</p>
                    `);
                }
            }
        };
        request.send();
    });
}