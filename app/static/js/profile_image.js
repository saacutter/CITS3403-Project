const fileInput = document.querySelector('#image-file');
const profilePicture = document.querySelector('#profile-picture-edit');
const oldFile = profilePicture.src; // Keep a copy of the original source for later use
const fileReader = new FileReader(); // Adapted from https://stackoverflow.com/questions/69595046/how-to-set-image-source-as-input-file-using-javascript

fileInput.addEventListener('change', () => {
    // Change the profile icon dynamically based on if the image has been removed or added
    if (fileInput.files.length == 0) {
        profilePicture.src = oldFile; // Set the image so that cancelling an upload request reverts the source
    } else {
        // Ensure that the 
        // Set the image source to be whatever is uploaded by the user
        fileReader.onload = (event) => {
            profilePicture.src = event.target.result;
        }
        fileReader.readAsDataURL(fileInput.files[0]);
    }
});