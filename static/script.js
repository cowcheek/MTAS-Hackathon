document.getElementById('submitButton').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const fileInput = document.getElementById('fileInput');
    const responseArea = document.getElementById('responseOutput');

    const formData = new FormData();
    formData.append('query', query);

    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        // if (data.results) {
        //     responseArea.innerHTML = ''; // Clear previous results
        //     data.results.forEach((result) => {
        //         console.log(result);

        //         const errorText = document.createElement('p');
        //         errorText.innerHTML = `<strong>Error:</strong> ${result.error}`;
        //         responseArea.appendChild(errorText);

        //         const ticketDetails = document.createElement('p');
        //         ticketDetails.innerHTML = `
        //             <strong>Ticket ID:</strong> ${result.matched_ticket.ticket_id}<br>
        //             <strong>Description:</strong> ${result.matched_ticket.description}<br>
        //             <strong>Solution:</strong> ${result.matched_ticket.solution}
        //         `;
        //         responseArea.appendChild(ticketDetails);
        //         responseArea.appendChild(document.createElement('hr')); // Separator
        //     });
        // } else {
        //     responseArea.innerHTML = 'No results found.';
        // }
        responseArea.innerHTML = 'No results found.';
    } catch (error) {
        console.error('Error:', error);
        responseArea.innerHTML = 'An error occurred while processing your request.';
    }
});

document.getElementById('copyButton').addEventListener('click', () => {
    const responseText = document.getElementById('responseArea').innerText;
    navigator.clipboard.writeText(responseText).then(() => {
        alert('Response copied to clipboard!');
    });
});
