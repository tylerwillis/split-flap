# San Francisco Moving Resources Split-Flap Board

## Project Overview
This project adapts an existing subway split-flap display to showcase information about services and goods for people moving to San Francisco. The adaptation maintains the engaging split-flap animation while updating the data source and visual elements to represent marketplace listings.

## Project Structure

### Data Handling
- **Data Source**: CSV file (`sf_resources.csv`) manually curated with marketplace listings.
- **Data Processing**: Python script (`sf_resources.py`) converts CSV data to JSON format.
- **Data Serving**: Node.js server (`app.js`) serves JSON data through an API endpoint.

### Frontend Display
- HTML/CSS/JS creates an animated split-flap board displaying marketplace information.
- Auto-refreshes every 20 seconds to display the latest data.

## Implementation Steps (Completed on March 7th, 2025)

### Step 1: Data Source and CSV Parser
- Created Python script (`sf_resources.py`) to:
  - Read and format CSV data into JSON.
  - Automatically generate a sample CSV if none exists.
  - Format dates clearly ("Today", "X days ago").
  - Sort entries to prioritize recent listings.

### Step 2: Server Logic Updates
- Modified Node.js server (`app.js`) to:
  - Correctly map new data fields (type, offer, date_posted, notes).
  - Update refresh interval to 5 minutes.
  - Implement status indicators (green for "Open", red for "Application Required").

### Step 3: Frontend Display Enhancements
- Updated `index.html` to:
  - Reflect new data structure with clear headers ("Type/Offer/Date Posted/Notes").
  - Include placeholder category icons with distinct colors.
  - Adjust sorting order to ascending (`order: 'asc'`) to align with backend sorting.

### Step 4: Visual and UX Improvements
- Enhanced readability and visual appeal:
  - Restored traditional yellow-on-black color scheme.
  - Increased row size and spacing for better readability.
  - Improved date display format to MM/DD/YY.
  - Enhanced overall contrast and definition.

### Step 5: Debugging and Fixes
- Addressed and resolved:
  - Character rendering issues.
  - Status indicator alignment.
  - Row spacing optimization.

### Step 6: Interactive and Ambient Enhancements
- Redesigned interactive elements:
  - Enlarged and enhanced "Join the Group Chat" button.
  - Added authentic airport ambiance sound with toggle functionality.
  - Improved browser compatibility and autoplay handling.

## Today's Activities and Learnings (March 7th, 2025)
- Adjusted sorting logic in `sf_resources.py` to handle future dates and prioritize recent entries.
- Modified frontend sorting order in `public/index.html` from 'desc' to 'asc' for consistency.
- Implemented debugging outputs to verify sorting behavior.
- Confirmed successful data processing and sorting through repeated server restarts.
- Documented sorting logic clearly in the README for future reference.

## Future Improvement Ideas
- Mobile responsiveness.
- Data filtering by category.
- Adjustable animation speed.
- Dark/light mode toggle.
- Multiple ambient sound options.
- Enhanced accessibility features.
- Localization support.
- User account integration for personalized tracking. 