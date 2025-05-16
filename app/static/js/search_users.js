const input = document.querySelector('input');
const usersDiv = document.querySelector('#retrievedUsers');

// Make a request to the database whenever the input value changes
input.addEventListener('input', () => {
    // Clear the div to remove elements already there
    let children = usersDiv.children;
    if (children.length > 0) {
        for (let i = 0; i < children.length; i++) {
            usersDiv.removeChild(children[i]);
        }
    }

    // Extract the value that has been input
    let value = input.value;

    // Make the request to the designated route
    var request = new XMLHttpRequest();
    request.open('POST', '/get_like/' + value, true);
    request.onload = () => {
        // Ensure that the request was successful
        if (request.status == 200) {
            // Parse the result
            users = JSON.parse(request.responseText);
            
            // Display an error message if no users matching the name was found
            if (users[0].username == null) {
                let error = document.querySelector('#retrievedUsers h1');
                if (error == null) {
                    usersDiv.insertAdjacentHTML('beforeend', '<h1 class="center text-lg text-white">No users were found!</h1>');
                }
                return;
            } 

            // Add a div to represent each user retrieved
            for (let i = 0; i < users.length; i++) {
                addUserDiv(users[i]);
            }
        } else {
            return;
        }
    };
    request.send();
});

function addUserDiv(user) {
    let src = user.profile_picture.startsWith('http') ? user.profile_picture : `/uploads/${user.profile_picture}`;
    let timeFormatted = moment(user.last_login).format('LLL');
    usersDiv.insertAdjacentHTML('beforeend', `
        <div id="${user.username}" class="container-flex w-1/2 items-center h-20 center white-bg rounded-border search-user">
            <a href="/user/${user.username}"><img src="${src}" alt="Profile Picture"></a>
            <div class="container flex-col text-left">
                <p class="text-xl font-bold">${user.username}</p>
                <p class="text-sm text-gray-500">Last active ${timeFormatted}</p>
            </div>
            <button style="margin-left: auto; margin-right: 1em;" onclick="add_friend('${user.username}')">Follow User</button>
        </div>
    `); 
    /* Adapted from: 
        https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
        https://stackoverflow.com/questions/805107/how-can-i-assign-a-multiline-string-literal-to-a-variable
    */
}

function add_friend(username) {
    // Extract the div with the username
    let user = document.querySelector(`#${username}`);

    // Make a request to the designated route
    var request = new XMLHttpRequest();
    request.open('POST', '/add_friend/' + username, true);
    request.onload = () => {
        // If the request status is 200, remove the "add friend" button from the div to prevent errors
        if (request.status == 200) {
            let button = user.querySelector('button');
            user.removeChild(button);
            
            // Add a paragraph to show that the friend request was sent
            user.insertAdjacentHTML('beforeend', '<p style="margin-right: 1em; width: 10em;">Following</p>');
        } else if (request.status == 400) {
            // Return if there is already an error message
            let error = document.querySelector(`#${username}-error`);
            if (error) {
                return;
            }

            // Insert an error message if the user is already added
            let header = document.querySelector('header');
            header.insertAdjacentHTML('afterend', `
                <div class="center error rounded-border-px mt-5" id="${username}-error">
                    <p>The user ${username} could not be followed.</p>
                </div>
            `);

            // Remove the error message after 5 seconds
            let body = document.querySelector('body');
            setTimeout(() => {
                body.removeChild(document.querySelector(".error"));
            }, 5000);
        }
    };
    request.send();
}