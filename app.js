const fs = require('fs');
const express = require('express');
const app = express();

const jsonFilePath = 'output.json'; // Path to the JSON file with SF resources data

// Function to read JSON file
function readJsonFile() {
    try {
        const data = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
        console.log(`Data loaded with ${data.length} entries`);
        return data;
    } catch (error) {
        console.error('Error reading the JSON file:', error);
        return []; // Return an empty array in case of an error
    }
}

// Initially read the JSON file
let jsonData = readJsonFile();

// Update jsonData every 5 minutes (300000 milliseconds)
setInterval(() => { 
    jsonData = readJsonFile();
    console.log('Data refreshed at ' + new Date().toLocaleTimeString());
}, 300000);

app.use('/api/arrivals', (req, res) => {
    let r = { data: [] };

    // Convert the object values to an array and then iterate
    Object.values(jsonData).forEach((entry, index) => {
        if (index <= 45) { // Display up to 45 results
            // Get the days ago value
            let daysAgo = entry.arrival_time;
            
            // Ensure the days ago is formatted properly for display
            let data = {
                line: entry.route_id,          // Category type (Housing, Service, etc.)
                stop: entry.current_stop,      // Location (San Francisco)
                terminal: entry.last_stop_name, // Offer description
                scheduled: daysAgo,            // Days ago the post was made
                remarks: entry.service_status   // Notes
            };

            // Determine status based on resource status (Open or Application Required)
            let itemStatus = '';
            
            // Extract status from notes or service_status field
            const notesLower = entry.service_status.toLowerCase();
            
            if (notesLower.includes('application required') || 
                notesLower.includes('apply') ||
                notesLower.includes('contact') ||
                notesLower.includes('interview')) {
                data.status = 'B'; // Red status for items requiring application
                itemStatus = 'Application Required';
            } else {
                data.status = 'A'; // Green status for open items
                itemStatus = 'Open';
            }
            
            // Add formatted status to the data
            data.itemStatus = itemStatus;

            r.data.push(data);
        }
    });

    res.json(r);
});

// Static files and web server setup remain unchanged
app.use('/', express.static('public'));

const port = process.env.PORT || 8080;
app.listen(port);
console.log('SF Moving Resources board started on port ' + port);