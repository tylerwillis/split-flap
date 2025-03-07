# San Francisco Moving Resources Split-Flap Board

## Project Overview
This project adapts an existing subway split-flap display to showcase information about services and goods for people moving to San Francisco. The adaptation maintains the engaging split-flap animation while updating the data source and visual elements to represent marketplace listings.

## Current Project Structure
1. **Data Fetching**: Python script fetches data from a CSV file and outputs to `output.json`
2. **Data Serving**: Node.js server reads `output.json` and serves it through an API endpoint
3. **Frontend Display**: HTML/CSS/JS creates an animated split-flap board showing marketplace information
4. **Data Structure**: Current data includes type, offer, date_posted, notes, and status

## Data Handling
- **Data Source**: CSV file (`sf_resources.csv`) manually curated with marketplace listings.
- **Data Processing**: Python script (`sf_resources.py`) converts CSV data to JSON format.
- **Data Serving**: Node.js server (`app.js`) serves JSON data through an API endpoint.

## Frontend Display
- HTML/CSS/JS creates an animated split-flap board displaying marketplace information.
- Auto-refreshes every 20 seconds to display the latest data.

## Adaptation Plan

### 1. Data Source Change
1. **Replace Python Script**: Create a new script to read from a manually curated CSV
2. **CSV Structure**: 
   ```
   type,offer,date_posted,notes,status
   ```
3. **JSON Output Mapping**: 
   - `route_id` → `type` (category of service/good)
   - `last_stop_name` → `offer` (what's being offered)
   - `arrival_time` → `date_posted` (when it was posted)
   - `service_status` → `notes` (additional information)
   - `current_stop` → Kept as "San Francisco"

### 2. Frontend Modifications
1. **Header Changes**: Update headers from "Route/Destination/ETA/Status" to "Type/Offer/Date Posted/Notes"
2. **Icon Images**: Create placeholder icons for different categories (housing, services, items, etc.)
3. **CSS Updates**: Modify custom.css to include the new category icons
4. **Status Indicators**: Repurpose status indicators to show:
   - Green indicator ("A" status) for "Open" offers
   - Red indicator ("B" status) for "Application Required" offers

### 3. Visual Styling Updates
1. **Color Scheme**: Update colors to reflect a San Francisco theme
2. **Page Title**: Change to "San Francisco Moving Resources"
3. **Branding**: Add San Francisco-related branding elements

## Implementation Steps (Completed on March 7th, 2025)

### Step 1: Data Source and CSV Parser ✅
- Created Python script (`sf_resources.py`) to:
  - Read and format CSV data into JSON.
  - Automatically generate a sample CSV if none exists.
  - Format dates clearly ("Today", "X days ago").
  - Sort entries to prioritize recent listings.

- Created a sample CSV structure (`sf_resources.csv`):
  ```csv
  type,offer,date_posted,notes,status
  Housing,2BR Apartment in Mission,2023-08-15,Pet friendly,Open
  Service,Moving assistance,2023-09-01,Available weekends,Application Required
  ...
  ```

- Implementation Notes:
  - The script automatically creates a sample CSV file if none exists
  - Date formatting converts YYYY-MM-DD to "X days" or "Today" for better display
  - Added sorting to show most recent listings first
  - Includes status field to determine if an item is "Open" or "Application Required"

### Step 2: Server Logic Updates ✅
- Modified Node.js server (`app.js`) to:
  - Correctly map new data fields (type, offer, date_posted, notes).
  - Update refresh interval to 5 minutes (now adjusted to 20 seconds).
  - Implement status indicators (green for "Open", red for "Application Required").

- Implementation Notes:
  - Added status detection based on keywords in notes
  - Added logging to show when data is refreshed
  - Updated console message to show "SF Moving Resources board started"

### Step 3: Frontend Display Enhancements ✅
- Updated `index.html` to:
  - Reflect new data structure with clear headers ("Type/Offer/Date Posted/Notes").
  - Include placeholder category icons with distinct colors.
  - Adjust sorting order to ascending (`order: 'asc'`) to align with backend sorting.

- Created placeholder category icons:
  - Added CSS-based category indicators with distinct colors for each type
  - Each category has its own color and displays its name as text
  - Created 10 different category styles: Housing, Service, Item, Event, Job, Resource, Transport, Storage, Education, Financial

- Updated `custom.js` to include new category types in the image drum:
  ```javascript
  sf.display.ImageDrum = function() {
    return [
      ' ', 'Housing', 'Service', 'Item', 'Event', 'Job', 
      'Resource', 'Transport', 'Storage', 'Education', 'Financial'
    ];
  };
  ```

- Updated `custom.css` to:
  - Replace subway route images with colored blocks for each category
  - Add text labels for each category type
  - Update status indicator colors to green for "Open" and red for "Application Required"
  - Add San Francisco theme colors to headers and background

### Step 4: Visual and UX Improvements ✅
- Enhanced readability and visual appeal:
  - Restored traditional yellow-on-black color scheme.
  - Increased row size and spacing for better readability.
  - Improved date display format to MM/DD/YY.
  - Enhanced overall contrast and definition.

- Implemented specific improvements:
  - Darkened the background to #0f1a24 for better contrast
  - Added stronger borders to split-flap cards and headers
  - Made column headers bolder with letter spacing for better readability
  - Added text shadow to the title for emphasis
  - Enhanced the board container with a subtle blue tint and inner glow
  - Added a border around the board for better definition
  - Improved the time display with a darker background and bolder text

### Step 5: Debugging and Fixes ✅
- Addressed and resolved:
  - Character rendering issues.
  - Status indicator alignment.
  - Row spacing optimization.

1. **Character Rendering Problem** ✅
   - **Issue**: Split-flap characters were not displaying correctly (showing random characters)
   - **Root Cause**: Changes affected the character mapping and sprite sheet alignment
   - **Solution**:
     - Added `sf.display.AlphabetDrum = sf.display.FullDrum` to ensure proper character set
     - Removed background-size scaling to preserve sprite sheet alignment
     - Returned to original character card dimensions (25px × 40px)
     - Kept enhanced styling like borders and shadows

2. **Status Indicator Alignment** ✅
   - **Issue**: Status indicators (green/red dots) were appearing below content instead of aligned
   - **Root Cause**: Row height changes affected the positioning of status elements
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

### Step 6: Interactive and Ambient Enhancements ✅
- Redesigned interactive elements:
  - Enlarged and enhanced "Join the Group Chat" button.
  - Added authentic airport ambiance sound with toggle functionality.
  - Improved browser compatibility and autoplay handling.

- **Chat Button Redesign**:
  - Increased font size from 16px to 24px
  - Expanded padding and border thickness
  - Added enhanced visual effects (glow, hover animations)
  - Improved button positioning and spacing

- **Airport Ambiance**:
  - Added authentic airport background sound (sfo.mp3) to enhance the airport arrival board experience
  - Implemented a stylish "Turn On/Off Ambiance" button
  - Button matches the design language of the chat button
  - Button dynamically changes text and icon based on sound state
  - Handles browser autoplay restrictions gracefully
  - Visual feedback indicates current sound state

- **Browser Compatibility**:
  - Implemented robust detection of browser autoplay capabilities
  - Added graceful fallback when autoplay is blocked
  - Improved error handling for audio playback issues
  - Added console logging for debugging and user alerts for critical issues

### Step 7: Layout and Alignment Refinements ✅
- **Column Alignment**: Meticulously adjusted the positioning of all column headers to align perfectly with their respective data columns
- **Container Width**: Increased the container width from 1700px to 1900px to ensure proper spacing and prevent overlap
- **Status Indicators**: Repositioned status indicators to prevent overlap with the Notes text
- **Responsive Adjustments**: Fine-tuned positioning across elements for a cohesive, professional appearance

## Recent Activities and Learnings (March 7th, 2025)
- Adjusted sorting logic in `sf_resources.py` to handle future dates and prioritize recent entries.
- Modified frontend sorting order in `public/index.html` from 'desc' to 'asc' for consistency.
- Implemented debugging outputs to verify sorting behavior.
- Confirmed successful data processing and sorting through repeated server restarts.
- Documented sorting logic clearly in the README for future reference.

## How to Use
1. **Adding Listings**: Edit the `sf_resources.csv` file to add, remove, or update listings
2. **Running the Application**:
   - Run `node app.js` to start the server
   - The Python script (`sf_resources.py`) will generate the output.json file from the CSV data
   - Access the application at http://localhost:8080 in your browser
   - The display will automatically refresh every 20 seconds

## Notes for Future Customization
- **Icons**: All category icons are placeholders with colored blocks and text. These can be replaced with proper icon images by updating the CSS file.
- **Color Scheme**: The current color scheme uses yellow text on black background for split-flap cards. This can be further customized.
- **Data Refresh**: Data refreshes every 20 seconds; this can be adjusted in both app.js and sf_resources.py.
- **CSV Structure**: You can modify sf_resources.csv to add your own listings. The script will read any changes on its next refresh cycle.

## Future Improvement Ideas
1. **Mobile Responsiveness**: Adapting the display for smaller screens
2. **Data Filtering**: Adding the ability to filter resources by category
3. **Animation Speed**: Allowing users to adjust the speed of the split-flap animation
4. **Dark/Light Mode**: Adding a toggle for different visual themes
5. **Audio Options**: Providing multiple ambient sound options
6. **Accessibility Features**: Enhancing screen reader support and keyboard navigation
7. **Localization**: Adding support for multiple languages
8. **User Accounts**: Adding authentication for personalized resource tracking 