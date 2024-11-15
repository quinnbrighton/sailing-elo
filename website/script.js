async function loadSailorData() {
    try {
        // Fetch the CSV file
        const response = await fetch('skipperrank.csv');
        const csvData = await response.text();

        // Parse CSV data
        const rows = csvData.split('\n').slice(1); // Skip the header row
        const tableBody = document.querySelector('#sailorTable tbody');

        // Loop through each row and create table rows
        rows.forEach(row => {
            const columns = row.split(',');

            // Only process if the row has data
            if (columns.length > 1) {
                const tr = document.createElement('tr');
                columns.forEach(column => {
                    const td = document.createElement('td');
                    td.textContent = column;
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            }
        });
    } catch (error) {
        console.error('Error loading CSV data:', error);
    }
}

function displaySailors(sailors) {
    const sailorList = document.querySelector('#sailorList'); // Make sure this exists in your HTML
    sailors.forEach(sailor => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = sailor.url;
        link.textContent = sailor.name;
        listItem.appendChild(link);
        sailorList.appendChild(listItem);
    });
}

// Function to fetch and parse the CSV data
async function loadRedirectData() {
    try {
        const response = await fetch('name_to_website.csv'); // Update the path if needed
        const data = await response.text();
        const rows = data.split('\n').slice(1); // Skip the header row

        const sailors = rows.map(row => {
            const [name, url] = row.split(',');
            return { name: name.trim(), url: url.trim() };
        });

        displaySailors(sailors); // Call the function to display sailors
    } catch (error) {
        console.error('Error loading redirect data:', error);
    }
}

// Call the functions to load and display sailor data
loadSailorData();
loadRedirectData();