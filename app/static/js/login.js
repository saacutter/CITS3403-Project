// Identify the 'signup' button and listen for clicks
let suButton = document.querySelector('#signup-btn');
suButton.addEventListener('click', () => {
    // Hide the login panel
    disableInputs(login.querySelectorAll('button, input'));
    login.style.display = "none"; 

    // Show the signup panel
    signup.style.display = "block";
    enableInputs(signup.querySelectorAll('button, input'));

    // Update the route and title to reflect the current view
    window.history.replaceState({}, "Tournament Manager | Sign Up", "/signup");
});

let liButton = document.querySelector('#login-btn');
liButton.addEventListener('click', () => {
    // Hide the signup panel
    disableInputs(signup.querySelectorAll('button, input'));
    signup.style.display = "none";

    // Show the login panel
    login.style.display = "block";
    enableInputs(login.querySelectorAll('button, input'));

    // Update the route and title to reflect the current view
    window.history.replaceState({}, "Tournament Manager | Log In", "/login");
});

function disableInputs(elements) {
    for (let i = 0; i < elements.length; i++) {
        elements[i].setAttribute('disabled', 'true');
    }
}

function enableInputs(elements) {
    for (let i = 0; i < elements.length; i++) {
        elements[i].removeAttribute('disabled');
    }
}