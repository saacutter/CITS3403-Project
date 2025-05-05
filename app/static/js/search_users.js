const input = document.querySelector('input');
const usersDiv = document.querySelector('#retrievedUsers');

// Make a request to the database whenever the input value changes
input.addEventListener('change', () => {
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
    request.open('GET', '/get_like/' + value, true);
    request.onload = () => {
        // Ensure that the request was successful
        if (request.status == 200) {
            // Parse the result
            users = JSON.parse(request.responseText);
            
            // Display an error message if no users matching the name was found
            if (users[0].username == null) {
                usersDiv.insertAdjacentHTML('beforeend', '<h3 class="center">No users were found!</h3>');
                return;
            } 

            // Add a div to represent each user retrieved
            for (let i = 0; i < users.length; i++) {
                console.log(users[i]);
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
    usersDiv.insertAdjacentHTML('beforeend', `
        <div class="container-flex center white-bg rounded-border search-user">
            <img src="${src}" alt="Profile Picture">
            <p>${user.username}</p>
        </div>
    `); 
    /* Adapted from: 
        https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
        https://stackoverflow.com/questions/805107/how-can-i-assign-a-multiline-string-literal-to-a-variable
    */
}