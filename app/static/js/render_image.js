const fileInput = document.querySelector('#image-file') || document.querySelector('#preview-file');
const image = document.querySelector('#profile-picture-edit') || document.querySelector('#preview-edit');
const oldFile = image.src; // Keep a copy of the original source for later use
const fileReader = new FileReader(); // Adapted from https://stackoverflow.com/questions/69595046/how-to-set-image-source-as-input-file-using-javascript

fileInput.addEventListener('change', () => {
    // Change the profile icon dynamically based on if the image has been removed or added
    if (fileInput.files.length == 0) {
        image.src = oldFile; // Set the image so that cancelling an upload request reverts the source
    } else {
        // Set the image source to be whatever is uploaded by the user
        fileReader.onload = (event) => {
            image.src = event.target.result;
        }
        fileReader.readAsDataURL(fileInput.files[0]);
    }
});