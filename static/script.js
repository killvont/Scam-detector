// Handle the scam description form submission
document.getElementById('scamForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('description').value;
    const resultDiv = document.getElementById('result');

    resultDiv.innerHTML = '<p class="loading">Processing...</p>'; // Show loading message

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        resultDiv.innerHTML = `<p class="success">Prediction: ${data.prediction}</p>`;
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
    }
});

// Handle the link scanning form submission
document.getElementById('linkForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const link = document.getElementById('linkInput').value;
    const linkResultDiv = document.getElementById('linkResult');

    linkResultDiv.innerHTML = '<p class="loading">Scanning...</p>'; // Show loading message

    try {
        const response = await fetch('/scan_listing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ link })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        linkResultDiv.innerHTML = `<p class="success">Scan Result: ${data.result || 'No issues found'}</p>`;
    } catch (error) {
        console.error('Error:', error);
        linkResultDiv.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
    }
});
