// Main JavaScript file for the Flask app

function fetchData() {
    const responseElement = document.getElementById('api-response');
    responseElement.textContent = 'Loading...';
    
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            responseElement.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            responseElement.textContent = 'Error: ' + error.message;
        });
}

// Add some interactivity
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask app loaded successfully!');
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});