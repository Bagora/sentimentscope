document.getElementById('sentimentForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const userInput = document.getElementById('userInput').value;

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server error, please try again later.');
        }
        return response.json();
    })
    .then(data => {
        // Clear any previous error messages
        document.getElementById('error-message').classList.add('hidden');

        let positivePercent = (data.scores.pos * 100).toFixed(2);
        let neutralPercent = (data.scores.neu * 100).toFixed(2);
        let negativePercent = (data.scores.neg * 100).toFixed(2);

        // Display the results in respective boxes
        document.getElementById('positive-percent').innerText = positivePercent;
        document.getElementById('positive-text').innerText = data.text_parts.positive || "No positive sentiment detected.";

        document.getElementById('neutral-percent').innerText = neutralPercent;
        document.getElementById('neutral-text').innerText = data.text_parts.neutral || "No neutral sentiment detected.";

        document.getElementById('negative-percent').innerText = negativePercent;
        document.getElementById('negative-text').innerText = data.text_parts.negative || "No negative sentiment detected.";
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Display error message
        const errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.innerText = error.message;
        errorMessageDiv.classList.remove('hidden');
    });
});

// Keyboard control for 'Enter' key submission
document.getElementById('userInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('sentimentForm').dispatchEvent(new Event('submit'));
    }
});