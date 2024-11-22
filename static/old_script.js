document.getElementById('submitButton').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const fileInput = document.getElementById('fileInput');
    const responseOutput = document.getElementById('responseOutput');
    const responseArea = document.getElementById('responseArea');

    const formData = new FormData();
    
    if (query) {
        formData.append('query', query);
    }

    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        // Check if the response is an array with matched_ticket objects
        if (Array.isArray(data) && data.length > 0) {
            const ticket = data[0].matched_ticket;
            responseOutput.innerHTML = `
                <div class="match">
                    <p><strong>Ticket ID:</strong> <a href="${ticket.ticket_id}" target="_blank">${ticket.ticket_id}</a></p>
                    <p><strong>Solution:</strong> ${ticket.solution}</p>
                    <p><strong>Solution Team:</strong> ${ticket.solution_team}</p>
                    <p><strong>Solution Component:</strong> ${ticket.solution_component}</p>
                </div>
            `;
        } else {
            responseOutput.innerHTML = 'No matches found.';
        }

        responseArea.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        responseOutput.innerHTML = 'An error occurred while processing your request.';
        responseArea.style.display = 'block';
    }
});

document.getElementById('copyButton').addEventListener('click', () => {
    const responseText = document.getElementById('responseOutput').innerText;
    navigator.clipboard.writeText(responseText).then(() => {
        alert('Response copied to clipboard!');
    });
});
