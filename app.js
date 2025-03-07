const fs = require('fs');
const express = require('express');
const app = express();
const path = require('path');

// Create logs directory if it doesn't exist
const LOG_DIR = 'logs';
if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}

// Setup logging function with timestamp
function log(level, message) {
    const timestamp = new Date().toISOString();
    const logMessage = `${timestamp} - ${level.toUpperCase()} - ${message}`;
    
    console.log(logMessage);
    
    // Also log to file
    const today = new Date().toISOString().split('T')[0];
    const logFile = path.join(LOG_DIR, `server_${today}.log`);
    
    fs.appendFileSync(logFile, logMessage + '\n');
}

// Error logging with stack trace
function logError(message, error) {
    log('error', `${message}: ${error.message}`);
    if (error.stack) {
        console.error(error.stack);
        // Also log stack trace to file
        const today = new Date().toISOString().split('T')[0];
        const logFile = path.join(LOG_DIR, `server_${today}.log`);
        fs.appendFileSync(logFile, `${error.stack}\n`);
    }
}

// Date utilities for consistency with Python
const dateUtils = {
    formatDate: (date) => {
        const options = { month: 'short', day: 'numeric', year: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    },
    
    formatTime: (date) => {
        return date.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    },
    
    getCurrentDate: () => {
        return new Date();
    },
    
    getFormattedDate: () => {
        return dateUtils.formatDate(dateUtils.getCurrentDate());
    },
    
    getFormattedTime: () => {
        return dateUtils.formatTime(dateUtils.getCurrentDate());
    }
};

// Load configuration
function loadConfig() {
    try {
        const configData = fs.readFileSync('config.json', 'utf8');
        const config = JSON.parse(configData);
        log('info', 'Configuration loaded successfully');
        return config;
    } catch (error) {
        logError('Error loading config file', error);
        // Return default values if config file cannot be loaded
        return {
            "data": {
                "output_json_path": "output.json"
            },
            "server": {
                "port": 8080
            },
            "refresh": {
                "interval_seconds": 20
            }
        };
    }
}

// Load configuration
const config = loadConfig();
const jsonFilePath = config.data.output_json_path;
const refreshInterval = config.refresh.interval_seconds * 1000; // Convert to milliseconds

// Function to safely read JSON file
function readJsonFile() {
    try {
        const rawData = fs.readFileSync(jsonFilePath, 'utf8');
        
        try {
            const data = JSON.parse(rawData);
            
            // Verify if data has the expected structure
            if (data && data.data && Array.isArray(data.data)) {
                log('info', `Data loaded with ${data.data.length} entries`);
                
                // If metadata is missing, add it
                if (!data.metadata) {
                    const now = new Date();
                    data.metadata = {
                        last_updated: now.toISOString(),
                        date: dateUtils.formatDate(now),
                        time: dateUtils.formatTime(now),
                        count: data.data.length
                    };
                    log('info', 'Added missing metadata to data');
                }
                
                return data;
            } else {
                log('warning', 'Invalid data format in JSON file');
                return { 
                    data: [],
                    metadata: {
                        last_updated: new Date().toISOString(),
                        date: dateUtils.getFormattedDate(),
                        time: dateUtils.getFormattedTime(),
                        count: 0
                    }
                };
            }
        } catch (parseError) {
            logError('Error parsing JSON data', parseError);
            return { 
                data: [],
                metadata: {
                    last_updated: new Date().toISOString(),
                    date: dateUtils.getFormattedDate(),
                    time: dateUtils.getFormattedTime(),
                    count: 0
                }
            };
        }
    } catch (error) {
        logError('Error reading the JSON file', error);
        return { 
            data: [],
            metadata: {
                last_updated: new Date().toISOString(),
                date: dateUtils.getFormattedDate(),
                time: dateUtils.getFormattedTime(),
                count: 0
            }
        };
    }
}

// Initially read the JSON file
let jsonData = readJsonFile();
let lastReadTime = Date.now();

// Update jsonData at the interval specified in config
const refreshIntervalId = setInterval(() => { 
    try {
        const newData = readJsonFile();
        
        // Only update if we got valid data
        if (newData && newData.data && newData.data.length > 0) {
            jsonData = newData;
            lastReadTime = Date.now();
            log('info', `Data refreshed at ${dateUtils.getFormattedTime()}`);
        } else {
            log('warning', 'Refresh attempt returned empty or invalid data');
        }
    } catch (error) {
        logError('Error refreshing data', error);
    }
}, refreshInterval);

// Health check endpoint
app.get('/health', (req, res) => {
    const uptime = process.uptime();
    const formattedUptime = {
        days: Math.floor(uptime / 86400),
        hours: Math.floor((uptime % 86400) / 3600),
        minutes: Math.floor((uptime % 3600) / 60),
        seconds: Math.floor(uptime % 60)
    };

    const status = {
        status: 'UP',
        uptime: formattedUptime,
        lastDataRefresh: new Date(lastReadTime).toISOString(),
        dataEntries: jsonData && jsonData.data ? jsonData.data.length : 0,
        timestamp: new Date().toISOString(),
        metadata: jsonData.metadata || {}
    };
    res.json(status);
});

// API endpoint to serve the data
app.use('/api/arrivals', (req, res) => {
    try {
        // Force reload the JSON data to ensure we have the latest changes
        try {
            const latestData = readJsonFile();
            if (latestData && latestData.data && latestData.data.length > 0) {
                jsonData = latestData;
                lastReadTime = Date.now();
            }
        } catch (error) {
            logError('Error reading latest data', error);
        }

        // Check if we have data to return
        if (!jsonData || !jsonData.data || jsonData.data.length === 0) {
            log('warning', 'No data available to serve');
        }

        // Simply return the data as is
        res.json(jsonData);
    } catch (error) {
        logError('Error serving API request', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: 'An error occurred while processing your request'
        });
    }
});

// Static files and web server setup
app.use('/', express.static('public'));

// Error handling middleware
app.use((err, req, res, next) => {
    logError('Express error', err);
    res.status(500).json({ 
        error: 'Internal server error',
        message: 'An error occurred while processing your request'
    });
});

// Start the server
const port = config.server.port;
const server = app.listen(port, () => {
    log('info', `SF Moving Resources board started on port ${port}`);
    log('info', `Data refreshes every ${config.refresh.interval_seconds} seconds`);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
    logError('Uncaught exception', error);
    // Keep the server running despite uncaught exceptions
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
    logError('Unhandled promise rejection', { message: reason.toString() });
    // Keep the server running despite unhandled promise rejections
});

// Handle process termination gracefully
process.on('SIGINT', () => {
    log('info', 'Server shutting down...');
    clearInterval(refreshIntervalId);
    server.close(() => {
        log('info', 'Server stopped');
        process.exit(0);
    });
});