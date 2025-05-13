const tournamentsDiv = document.querySelector('#tournaments');
const tournamentButtons = tournamentsDiv.querySelectorAll('button');

for (let i = 0; i < tournamentButtons.length; i++) {
    tournamentButtons[i].addEventListener('click', () => {
        // Find the closest div
        let tournament = tournamentButtons[i].closest('.tournament-card').querySelector('div');
        let tDiv = tournamentButtons[i].closest('#tournament');

        // Make the request to the designated route
        var request = new XMLHttpRequest();
        request.open('POST', '/delete_tournament/' + tournament.id, true);
        request.onload = () => {
            // Ensure that the request was successful
            if (request.status == 200) {
                // Remove the tournament from the page
                tournamentsDiv.removeChild(tDiv);

                // Check if the user has any tournaments left and render the appropriate text
                if (tournamentsDiv.querySelectorAll('div').length == 0) {
                    let heading = document.querySelector('#tournaments').previousElementSibling;
                    heading.insertAdjacentHTML('afterend', `
                        <p class="text-white text-med">This user has not competed in any tournaments yet.</p>
                    `);
                }
            }
        };
        request.send();
    });
}