// Adapted from https://www.chartjs.org/docs/latest/charts/doughnut.html

const canvas = document.querySelector('canvas').getContext('2d');
const gamesPlayed = document.querySelector('#totalGames').innerHTML;
const wins = document.querySelector('#wins').innerHTML;
const losses = document.querySelector('#losses').innerHTML;
const draws = document.querySelector('#draws').innerHTML;

if (gamesPlayed > 0) {
    // Create a chart depicting rate of each result
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                data: [+((wins / gamesPlayed)*100).toFixed(2), +((losses / gamesPlayed)*100).toFixed(2), +((draws / gamesPlayed)*100).toFixed(2)],
                backgroundColor: ['#4CAF50', '#f4473c', '#e0e0e0'],
                borderWidth: 5
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }, 
            cutout: '70%',
        }
    });
} else {
    // Create an empty chart (since there are no games to go off)
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            datasets: [{
                label: 'Not Enough Data',
                data: [1],
                backgroundColor: ['#e0e0e0'],
                borderWidth: 5
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            cutout: '70%'
        }
    });
}