import csv
import json
import time
import os
import logger
import date_utils

# Get logger instance
log = logger.get_logger('sf_resources')

def load_config():
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            log.info("Configuration loaded successfully")
            return config
    except Exception as e:
        log.error(f"Error loading config file: {e}")
        # Return default values if config file cannot be loaded
        return {
            "data": {
                "csv_file_path": "sf_resources.csv",
                "output_json_path": "output.json"
            },
            "refresh": {
                "interval_seconds": 20
            },
            "logging": {
                "enable_debug": False
            }
        }

def read_csv_data(csv_path):
    """Read data from CSV file."""
    try:
        if not os.path.exists(csv_path):
            log.warning(f"CSV file not found at {csv_path}")
            # Create a sample CSV if it doesn't exist
            create_sample_csv(csv_path)
            
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            resources = list(reader)
            
        log.info(f"Read {len(resources)} entries from CSV file")
        return resources
    except Exception as e:
        log.error(f"Error reading CSV file: {e}", exc_info=True)
        return []

def create_sample_csv(csv_path):
    """Create a sample CSV file if none exists."""
    log.info("Creating sample CSV file...")
    try:
        sample_data = [
            {"type": "Housing", "offer": "2BR Apartment in Mission", "date_posted": "2023-08-15", "notes": "Pet friendly", "status": "Open"},
            {"type": "Service", "offer": "Moving assistance", "date_posted": "2023-09-01", "notes": "Available weekends", "status": "Application Required"},
            {"type": "Item", "offer": "Furniture giveaway", "date_posted": "2023-08-20", "notes": "Pick up only", "status": "Open"},
            {"type": "Job", "offer": "Software Engineer", "date_posted": "2023-08-25", "notes": "Remote friendly", "status": "Application Required"},
            {"type": "Resource", "offer": "Neighborhood guide", "date_posted": "2023-09-05", "notes": "Free digital download", "status": "Open"}
        ]
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ["type", "offer", "date_posted", "notes", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
        log.info(f"Sample CSV file created at {csv_path}")
    except Exception as e:
        log.error(f"Error creating sample CSV file: {e}", exc_info=True)

def determine_status(resource):
    """Determine item status (A for Open, B for Application Required)."""
    try:
        status = resource.get("status", "").lower()
        notes = resource.get("notes", "").lower()
        
        if "application required" in status or "application required" in notes or \
           "apply" in notes or "contact" in notes or "interview" in notes:
            return "B"  # Application Required
        else:
            return "A"  # Open
    except Exception as e:
        log.error(f"Error determining status: {e}")
        return "A"  # Default to Open

def process_and_transform_data(resources, debug=False):
    """Process and transform CSV data to the final JSON format."""
    processed_data = []
    
    try:
        for resource in resources:
            try:
                # Use date_utils module for date handling
                days_since = date_utils.calculate_days_since(resource.get("date_posted", ""), debug)
                days_formatted = date_utils.format_days_for_display(days_since)
                
                # Create a resource entry in the simplified format the frontend expects
                entry = {
                    "line": resource.get("type", "Unknown"),          # Category type
                    "terminal": resource.get("offer", "Unknown"),     # Offer description
                    "scheduled": days_formatted,                      # Days ago formatted
                    "remarks": resource.get("notes", ""),             # Notes
                    "status": determine_status(resource),             # Status indicator (A or B)
                    "stop": "San Francisco"                           # Location (constant)
                }
                
                processed_data.append(entry)
            except Exception as e:
                log.error(f"Error processing resource entry: {e}")
                # Continue processing other entries even if one fails
                continue
        
        # Sort by days (ascending - newest first)
        if debug:
            log.debug("Before sorting:")
            for item in processed_data:
                log.debug(f"  {item['terminal']}: {item['scheduled']}")
        
        processed_data = sorted(
            processed_data,
            key=lambda x: int(x["scheduled"]) if x["scheduled"].strip('-').isdigit() else 999
        )
        
        if debug:
            log.debug("\nAfter sorting:")
            for item in processed_data:
                log.debug(f"  {item['terminal']}: {item['scheduled']}")
        
        return processed_data
    except Exception as e:
        log.error(f"Error in data transformation: {e}", exc_info=True)
        return []  # Return empty list on error

def main():
    """Main function to process data and generate JSON."""
    try:
        # Load configuration
        config = load_config()
        
        # Set debug mode from config
        debug_mode = config["logging"].get("enable_debug", False)
        
        csv_path = config["data"]["csv_file_path"]
        output_path = config["data"]["output_json_path"]
        refresh_interval = config["refresh"]["interval_seconds"]
        
        log.info("Reading SF moving resources data...")
        
        # Read data from CSV
        resources = read_csv_data(csv_path)
        
        # Transform the data to match the exact format needed by frontend
        transformed_data = process_and_transform_data(resources, debug_mode)
        
        # Add metadata to the output
        current_date = date_utils.get_current_date()
        
        # Prepare final output structure
        output = {
            "data": transformed_data,
            "metadata": {
                "last_updated": current_date.isoformat(),
                "date": date_utils.format_date_for_display(current_date),
                "time": date_utils.get_time_for_display(),
                "count": len(transformed_data)
            }
        }
        
        # Write the transformed data to output.json
        with open(output_path, 'w') as file:
            json.dump(output, file, indent=2)
        
        log.info(f"Data successfully written to {output_path}")
        log.info(f"Waiting {refresh_interval} seconds before next update...")
    except Exception as e:
        log.critical(f"Fatal error in main function: {e}", exc_info=True)

if __name__ == "__main__":
    # Run in a continuous loop to keep updating the data
    log.info("Starting SF moving resources data processor")
    
    try:
        config = load_config()
        refresh_interval = config["refresh"]["interval_seconds"]
        
        while True:
            try:
                main()
                time.sleep(refresh_interval)
            except KeyboardInterrupt:
                log.info("\nExiting gracefully...")
                break
            except Exception as e:
                log.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(refresh_interval)  # Still wait before retrying
    except Exception as e:
        log.critical(f"Fatal error: {e}", exc_info=True) 