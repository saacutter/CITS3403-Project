const file = document.querySelector('#file');
const inputFields = document.querySelectorAll('#upload-input');

// See if the file has a file uploaded and disable any subsequent inputs
file.addEventListener('change', () => {
    // Adjust the ability of the input fields based on if a file has been uploaded or not
    if (file.files.length == 0) {
        for (let i = 2; i < inputFields.length - 1; i++) { // Starts after the file input and ends before the submit button
            inputFields[i].disabled = false; // Enable all fields
        }
    } else {
        for (let i = 2; i < inputFields.length - 1; i++) { // Starts after the file input and ends before the submit button
            inputFields[i].disabled = true; // Disable all fields
        }
    }
});

// Add the event listener to every input field
for (let i = 0; i < inputFields.length; i++) {
    inputFields[i].addEventListener('change', () => {
        // Check if all of the input fields are empty
        let allEmpty = true;
        for (let i = 0; i < inputFields.length; i++) {
            if (inputFields[i].value != "") {
                allEmpty = false;
                break;
            }
        }
        
        // Disable the file field if any of of the input fields have content and re-enable otherwise
        if (allEmpty) {
            file.disabled = false;
        } else {
            file.disabled = true;
        }
    });
}