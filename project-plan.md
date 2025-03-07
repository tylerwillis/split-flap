# San Francisco Moving Resources Split-Flap Board

## Project Overview
This project adapts an existing subway split-flap display to show information about services and goods for people moving to San Francisco. The adaptation preserves the engaging split-flap animation while changing the data source and visual elements to represent marketplace listings.

## Current Project Structure
1. **Data Fetching**: Python script fetches subway data from transit API and outputs to `output.json`
2. **Data Serving**: Node.js server reads `output.json` and serves it through an API endpoint
3. **Frontend Display**: HTML/CSS/JS creates an animated split-flap board showing subway information
4. **Data Structure**: Current data includes route_id, last_stop_name, arrival_time, and service_status

## Adaptation Plan

### 1. Data Source Change
1. **Replace Python Script**: Create a new script to read from a manually curated CSV
2. **CSV Structure**: 
   ```
   type,offer,date_posted,notes
   ```
3. **JSON Output Mapping**: 
   - `route_id` → `type` (category of service/good)
   - `last_stop_name` → `offer` (what's being offered)
   - `arrival_time` → `date_posted` (when it was posted)
   - `service_status` → `notes` (additional information)
   - `current_stop` → Can be repurposed for location or kept as "San Francisco"

### 2. Frontend Modifications
1. **Header Changes**: Update headers from "Route/Destination/ETA/Status" to "Type/Offer/Date Posted/Notes"
2. **Icon Images**: Create placeholder icons for different categories (housing, services, items, etc.) that can be replaced later
3. **CSS Updates**: Modify custom.css to include the new category icons
4. **Status Indicators**: Repurpose status indicators to show:
   - Green indicator ("A" status) for "Open" offers
   - Red indicator ("B" status) for "Application Required" offers

### 3. Visual Styling Updates
1. **Color Scheme**: Update colors to reflect a San Francisco theme
2. **Page Title**: Change to "San Francisco Moving Resources" or similar
3. **Branding**: Add placeholder for San Francisco-related logo/branding that can be replaced later

## Implementation Steps

### Step 1: Create CSV Parser ✅
1. Created a new Python script (`sf_resources.py`) that:
   - Reads the CSV file with resource listings
   - Formats the data into the expected JSON structure
   - Writes to output.json
   - Runs on a schedule to refresh data (every 5 minutes)
   - Added a feature to create a sample CSV if none exists

2. Created a sample CSV structure (`sf_resources.csv`):
   ```csv
   type,offer,date_posted,notes,status
   Housing,2BR Apartment in Mission,2023-08-15,Pet friendly,Open
   Service,Moving assistance,2023-09-01,Available weekends,Application Required
   ...
   ```

3. Implementation Notes:
   - The script automatically creates a sample CSV file if none exists
   - Date formatting converts YYYY-MM-DD to "X days" or "Today" for better display
   - Added sorting to show most recent listings first
   - Includes status field to determine if an item is "Open" or "Application Required"

### Step 2: Update Server Code ✅
1. Modified `app.js` to:
   - Map the new data fields correctly (type, offer, date_posted, notes)
   - Updated refresh interval to 5 minutes (300000ms)
   - Changed status code mappings:
     - 'A' status (green) for "Open" offers
     - 'B' status (red) for "Application Required" offers

2. Implementation Notes:
   - Added status detection based on keywords in notes
   - Added logging to show when data is refreshed
   - Updated console message to show "SF Moving Resources board started"

### Step 3: Update Frontend Display ✅
1. Modified `index.html` to:
   - Updated column headers to "Type/Offer/Posted/Notes"
   - Changed page title to "San Francisco Moving Resources"
   - Updated descriptions in template to match the new data structure
   - Set a fixed title rather than fetching from API

2. Created placeholder category icons:
   - Added CSS-based category indicators with distinct colors for each type
   - Each category has its own color and displays its name as text
   - Created 10 different category styles: Housing, Service, Item, Event, Job, Resource, Transport, Storage, Education, Financial

3. Updated `custom.js` to include new category types in the image drum:
   ```javascript
   sf.display.ImageDrum = function() {
     return [
       ' ', 'Housing', 'Service', 'Item', 'Event', 'Job', 
       'Resource', 'Transport', 'Storage', 'Education', 'Financial'
     ];
   };
   ```

4. Updated `custom.css` to:
   - Replace subway route images with colored blocks for each category
   - Added text labels for each category type
   - Updated status indicator colors to green for "Open" and red for "Application Required"
   - Added San Francisco theme colors to headers and background

### Step 4: Testing & Deployment ✅
1. Created a sample `output.json` file with our marketplace data structure:
   - Formatted dates as "Today", "1 day", "X days" for better readability
   - Included all our category types to test the display
   - Populated with sample data from our CSV file
   - Structured to match the expected format for the app.js server

2. Verified the Node.js server is working:
   - Server running on port 8080
   - Serving the updated HTML/CSS/JS files
   - Processing our new data format correctly

## Project Completion

The San Francisco Moving Resources Split-Flap Board has been successfully adapted from a subway display to a marketplace listing board. All the planned changes have been implemented:

1. **Data Source**: Created the Python script and CSV structure for marketplace listings
2. **Server Logic**: Updated app.js to handle the new data format and status indicators
3. **Frontend**: Modified all HTML, CSS, and JS files to display the new content
4. **Visual Style**: Added color-coded placeholder icons and SF-themed styling

## How to Use

1. **Adding Listings**: Edit the `sf_resources.csv` file to add, remove, or update listings
2. **Running the Application**:
   - Run `node app.js` to start the server
   - The Python script (`sf_resources.py`) will generate the output.json file from the CSV data
   - Access the application at http://localhost:8080 in your browser
   - The display will automatically refresh every 5 minutes

## Notes for Future Customization
- **Icons**: All category icons are placeholders with colored blocks and text. These can be replaced with proper icon images by updating the CSS file.
- **Color Scheme**: The current color scheme uses a neutral gray background with category-colored icons. This can be further customized.
- **Data Refresh**: Data refreshes every 5 minutes; this can be adjusted in both app.js and sf_resources.py.
- **CSV Structure**: You can modify sf_resources.csv to add your own listings. The script will read any changes on its next refresh cycle.

## Fixing Readability Issues

Based on user feedback and testing, several readability issues have been identified that need to be addressed:

### Identified Issues
1. **Text Readability**: The white text on black split-flap cards is hard to read
2. **Row Size**: The rows are too small, making the content appear crowded
3. **Date Display**: The "Posted" section isn't correctly rendering dates from the CSV
4. **Overall Contrast**: The current color scheme needs improvement for better visibility

### Implementation Plan
1. **Return to Yellow Text on Black Background** ✅
   - Restored the traditional yellow-on-black color scheme for split-flap cards
   - Removed CSS filters that were converting yellow to white
   - Darkened the background to #14202A for better contrast

2. **Increase Row Size and Spacing** ✅
   - Increased row height from 60px to 85px for better visibility
   - Added 15px margin between rows for better separation
   - Increased split-flap card size from 25px × 40px to 32px × 50px
   - Enlarged category icons to match new dimensions
   - Added subtle borders and enhanced shadows for better definition
   - Increased font sizes throughout for better readability

3. **Fix the "Posted" Date Display** ✅
   - Updated Python script to format dates as MM/DD/YY instead of "days ago"
   - Modified output.json to use MM/DD/YY date format
   - Updated app.js to properly handle and display dates
   - Added logging to verify proper data loading

4. **Improve Overall Contrast and Definition** ✅
   - Darkened the background to #0f1a24 for even better contrast
   - Added stronger borders to split-flap cards and headers
   - Made column headers bolder with letter spacing for better readability
   - Added text shadow to the title for emphasis
   - Enhanced the board container with a subtle blue tint and inner glow
   - Added a border around the board for better definition
   - Improved the time display with a darker background and bolder text

### Readability Improvements Completion

All readability issues have been successfully addressed, resulting in a much more legible and visually appealing display:

1. **Text Display**: The yellow text on black background provides optimal contrast and readability, true to traditional split-flap displays
2. **Layout**: Larger rows and elements with proper spacing make scanning the information much easier
3. **Date Format**: Dates now display in a standard MM/DD/YY format that's easy to understand
4. **Visual Hierarchy**: Enhanced contrast between elements, clear headers, and a professional color scheme make the information well-organized and easy to process

The board now provides a much better user experience while maintaining the engaging split-flap animation that gives it character.

## Debugging and Fixes

During testing, we identified and fixed several issues to ensure proper display functionality:

### Display Issues Fixed

1. **Character Rendering Problem** ✅
   - **Issue**: Split-flap characters were not displaying correctly (showing random characters)
   - **Root Cause**: Our changes affected the character mapping and sprite sheet alignment
   - **Solution**:
     - Added `sf.display.AlphabetDrum = sf.display.FullDrum` to ensure proper character set
     - Removed background-size scaling to preserve sprite sheet alignment
     - Returned to original character card dimensions (25px × 40px)
     - Kept enhanced styling like borders and shadows

2. **Status Indicator Alignment** ✅
   - **Issue**: Status indicators (green/red dots) were appearing below content instead of aligned
   - **Root Cause**: Our row height changes affected the positioning of status elements
   - **Solution**:
     - Added `position: relative` to row elements to create positioning context
     - Used absolute positioning for status indicators with `position: absolute`
     - Added `right: 0` and `top: 50%` to align status dots properly
     - Used `transform: translateY(-50%)` for precise vertical centering

3. **Row Spacing Optimization** ✅
   - **Issue**: Needed to balance row size with proper spacing
   - **Solution**:
     - Returned to the original 60px row height for better compatibility
     - Maintained 15px margins between rows for clear separation
     - Adjusted vertical alignment of elements for consistent appearance

These fixes have resulted in a stable, visually appealing display that properly shows all marketplace listings while maintaining the traditional split-flap animation effect. 