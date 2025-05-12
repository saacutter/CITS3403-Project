function sendRequest(url) {
    // Make the request to the designated route
    var request = new XMLHttpRequest();
    request.open('POST', url + username, true);
    request.onload = () => {
        // Ensure that the request was successful
        if (request.status == 200) {
            // Extract the button div from the page
            let btnDiv = (addBtn || removeBtn)?.closest('div');

            // Remove the relevant button from the page and add the opposite button
            if (addBtn) {
                addBtn.remove();
                btnDiv.insertAdjacentHTML('beforeend', `
                    <button class="p-2 w-full text-lg font-bold border-none bg-red-500 hover:bg-red-700 transition m-auto" id="remove-friend">Unfollow User</button>
                `);
            } else {
                removeBtn.remove();
                btnDiv.insertAdjacentHTML('beforeend', `
                    <button class="p-2 w-full text-lg font-bold border-none bg-gray-500 hover:bg-gray-600 transition m-auto" id="add-friend">Follow User</button>
                `);
            }

            // Reattach event listeners for the new buttons
            addBtn = document.querySelector('#add-friend');
            removeBtn = document.querySelector('#remove-friend');
            attachListeners();
        }
    };
    request.send();
}

function attachListeners() {
    // If the button is for adding users, add the user
    if (addBtn) {
        addBtn.addEventListener("click", () => {
            sendRequest("/add_friend/");
        });
    }

    // If the button is for removing users, remove the user
    if (removeBtn) {
        removeBtn.addEventListener("click", () => {
            sendRequest("/remove_friend/");
        });
    }
}

// Initial setup of page
let addBtn = document.querySelector('#add-friend');
let removeBtn = document.querySelector('#remove-friend');
const username = document.querySelectorAll('h1')[1].innerHTML;
attachListeners();