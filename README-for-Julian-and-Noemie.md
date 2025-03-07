# San Francisco Moving Resources Board

## What Is This Project?

This project is an animated information display board that shows resources, services, and goods for people moving to San Francisco. It's designed in the style of a split-flap (or Solari) board - the classic mechanical displays once common in train stations and airports that flip through characters to update information.

The display automatically rotates through available listings, showing:
- **Type** of offering (Housing, Service, etc.)
- **Offer** description (what's being offered)
- **Posted** date (how long ago it was posted)
- **Notes** (additional details)
- **Status** indicators (green for Open, red for Application Required)

## How It Works

1. **Data Source**: All the listings are stored in a CSV file (`sf_resources.csv`) that you can edit manually
2. **Processing**: A Python script reads this CSV and converts it to JSON format
3. **Display**: A Node.js web server displays the data as an animated split-flap board in a web browser
4. **Updates**: The board automatically refreshes to show the latest data every 5 minutes

## How to Use It

### Starting the Application

1. **Start the Server**:
   - Open a terminal window
   - Navigate to the project directory
   - Run the command: `node app.js`
   - You should see: "SF Moving Resources board started on port 8080"

2. **View the Board**:
   - Open a web browser
   - Go to: `http://localhost:8080`
   - The split-flap board should load with your SF resources information

3. **When You're Done**:
   - Return to the terminal window
   - Press `Ctrl+C` to stop the server

### Updating the Listings

You can easily add, remove, or modify the listings by editing the CSV file:

1. Open `sf_resources.csv` in any spreadsheet program (Excel, Google Sheets, etc.) or text editor
2. Edit the file following this structure:
   ```
   type,offer,date_posted,notes,status
   Housing,2BR Apartment in Mission,2023-10-15,Pet friendly,Open
   ```

3. The columns are:
   - **type**: Category of the listing (Housing, Service, Job, Resource, etc.)
   - **offer**: Brief description of what's being offered
   - **date_posted**: Date in YYYY-MM-DD format
   - **notes**: Additional details or description
   - **status**: Either "Open" or "Application Required"

4. Save the file
5. The display will automatically refresh with your new data within 5 minutes
6. If you want to see changes immediately, restart the server

### Available Categories

The current categories are set up with different colors:
- Housing (Blue)
- Service (Green)
- Item (Orange)
- Event (Deep Orange)
- Job (Purple)
- Resource (Emerald)
- Transport (Red)
- Storage (Yellow)
- Education (Light Blue)
- Financial (Teal)

You can use any of these categories in the CSV "type" column.

## Customizing the Display

### Replacing the Placeholder Icons

The current category icons are simple colored blocks with text. Here's how to replace them with custom icons:

1. **Create Your Icons**:
   - Design square icons, ideally 115px × 40px
   - Save them in a web-friendly format (PNG or SVG recommended)

2. **Option 1: Replace with Image Files**:
   - Open `public/plugins/arrivals/custom.css`
   - Find the section with comments `/* CATEGORY TYPE ICONS */`
   - For each category, replace the background color with an image:
     ```css
     .splitflap .image span.Housing {
       background-color: #4a90e2; /* Blue */
       /* Change to: */
       background: url('housing-icon.png') no-repeat center;
       background-size: contain;
     }
     ```
   - Also remove or comment out the "Add text to the icons" section if using image icons

3. **Option 2: Create a Sprite Sheet**:
   - Create a single image containing all category icons (like the original subway route bullets)
   - Replace the background positions in the CSS to point to different parts of your sprite sheet
   - The original subway implementation in this file shows how this works

### Changing Colors and Styling

1. **Board Colors**:
   - Open `public/plugins/arrivals/custom.css`
   - Find the section with comments `/* SF THEME COLORS */`
   - Modify the colors as desired

2. **Status Indicators**:
   - Find the section with comments `/* STATUS INDICATORS */`
   - Change the colors for Open (green) or Application Required (red) indicators

## Troubleshooting

- **Changes not appearing**: The board refreshes every 5 minutes. If you need to see changes immediately, restart the server.
- **Icons not displaying correctly**: Make sure your image paths are correct and the images are in the right location.
- **Server won't start**: Make sure no other process is using port 8080. You can change the port in `app.js` if needed.

## Technical Details

- The server runs on Node.js using Express
- The frontend uses jQuery, Backbone.js, and Underscore.js
- Data is stored as CSV and converted to JSON
- All animations are done using CSS

For more advanced customizations, you can modify:
- `app.js` - Server logic and data processing
- `public/index.html` - Display structure
- `public/plugins/arrivals/custom.js` - Animation and data handling
- `public/plugins/arrivals/custom.css` - Visual styling 