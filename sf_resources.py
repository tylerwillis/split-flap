import csv
import json
import time
import os
from datetime import datetime, timedelta

# Path to the CSV file (relative to the script location)
CSV_FILE_PATH = 'sf_resources.csv'
OUTPUT_JSON_PATH = 'output.json'
REFRESH_INTERVAL = 20  # 20 seconds in seconds

def read_csv_data():
    """Read data from CSV file and convert to the required JSON format."""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            print(f"Warning: CSV file not found at {CSV_FILE_PATH}")
            # Create a sample CSV if it doesn't exist
            create_sample_csv()
            
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            resources = list(reader)
            
        return resources
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def create_sample_csv():
    """Create a sample CSV file if none exists."""
    print("Creating sample CSV file...")
    sample_data = [
        {"type": "Housing", "offer": "2BR Apartment in Mission", "date_posted": "2023-08-15", "notes": "Pet friendly", "status": "Open"},
        {"type": "Service", "offer": "Moving assistance", "date_posted": "2023-09-01", "notes": "Available weekends", "status": "Application Required"},
        {"type": "Item", "offer": "Furniture giveaway", "date_posted": "2023-08-20", "notes": "Pick up only", "status": "Open"},
        {"type": "Job", "offer": "Software Engineer", "date_posted": "2023-08-25", "notes": "Remote friendly", "status": "Application Required"},
        {"type": "Resource", "offer": "Neighborhood guide", "date_posted": "2023-09-05", "notes": "Free digital download", "status": "Open"}
    ]
    
    with open(CSV_FILE_PATH, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ["type", "offer", "date_posted", "notes", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)

def format_date_posted(date_str):
    """Convert date string to days since posting."""
    try:
        # Parse the date string (expecting YYYY-MM-DD format)
        date_posted = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now()
        
        # Debug: Print the dates we're comparing
        print(f"Debug - Comparing: today={today.strftime('%Y-%m-%d')} vs date_posted={date_posted.strftime('%Y-%m-%d')}")
        
        # Calculate days since posting
        days_since = (today - date_posted).days
        
        print(f"Debug - Days since: {days_since} for {date_str}")
        
        if days_since == 0:
            # Use '000' for today
            return "000"
        elif days_since > 0:
            # Pad with leading zeros to ensure proper string sorting
            return f"{days_since:03d}"  # Using 3 digits to handle up to 999 days
        else:
            # Handle future dates - show as negative days with leading zeros
            return f"-{abs(days_since):03d}"  # Negative days for future events
    except Exception as e:
        print(f"Error formatting date: {e}")
        return date_str  # Return original string if there's an error

def main():
    print("Reading SF moving resources data...")
    
    # Read data from CSV
    resources = read_csv_data()
    
    # Transform the data to match the expected output format
    transformed_data = []
    for resource in resources:
        # Map CSV fields to the expected JSON structure
        arrival_time = format_date_posted(resource.get("date_posted", ""))
        offer = resource.get("offer", "Unknown offer")
        
        transformed_resource = {
            "route_id": resource.get("type", "Unknown"),
            "arrival_time": arrival_time,
            "current_stop": "San Francisco",
            "last_stop_name": offer,
            "service_status": resource.get("notes", "")
        }
        
        # Add the resource to the transformed data
        transformed_data.append(transformed_resource)
    
    # Sort the data by days ago (newest first - smaller number of days = more recent)
    # For "000" entries (today), they'll naturally sort at the top with numeric sorting
    print("Before sorting:")
    for item in transformed_data:
        print(f"  {item['last_stop_name']}: {item['arrival_time']}")
    
    # Now we can simply sort by the numeric values since all entries are formatted consistently
    transformed_data = sorted(
        transformed_data,
        key=lambda x: int(x["arrival_time"]) if x["arrival_time"].strip('-').isdigit() else 999
    )
    
    print("\nAfter sorting:")
    for item in transformed_data:
        print(f"  {item['last_stop_name']}: {item['arrival_time']}")
        
    # Ensure we have exactly 3 characters for the scheduled display
    # This is important for the split-flap display to work correctly
    for item in transformed_data:
        # Format "TDY" to be properly displayed
        if item["arrival_time"] == "TDY":
            # Keep as "TDY" - this will be displayed as 3 characters
            pass
        elif item["arrival_time"].strip('-').isdigit():
            # Already formatted with leading zeros from format_date_posted
            pass
    
    # Write the transformed data to output.json
    with open(OUTPUT_JSON_PATH, 'w') as file:
        json.dump(transformed_data, file, indent=4)
    
    print(f"Data successfully written to {OUTPUT_JSON_PATH}")
    print(f"Waiting {REFRESH_INTERVAL} seconds before next update...")

if __name__ == "__main__":
    # Run in a continuous loop to keep updating the data
    while True:
        try:
            main()
            print("Data successfully written to output.json")
            print(f"Waiting {REFRESH_INTERVAL} seconds before next update...")
            time.sleep(REFRESH_INTERVAL)
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(REFRESH_INTERVAL)  # Still wait before retrying 