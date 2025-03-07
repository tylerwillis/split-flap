"""
Date utilities module for SF Moving Resources Board.
Provides standardized date handling functionality.
"""

import datetime
import logger

# Get logger instance
log = logger.get_logger('date_utils')

def get_current_date():
    """
    Get the current date.
    
    Returns:
        datetime.datetime: Current date and time
    """
    return datetime.datetime.now()

def parse_date(date_str):
    """
    Parse a date string in YYYY-MM-DD format.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
        
    Returns:
        datetime.datetime: Parsed date object or None if parsing fails
    """
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except Exception as e:
        log.error(f"Error parsing date '{date_str}': {e}")
        return None

def calculate_days_between(start_date, end_date=None):
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date (datetime.datetime): Start date
        end_date (datetime.datetime, optional): End date. Defaults to current date.
        
    Returns:
        int: Number of days between dates (positive if end_date is after start_date)
    """
    if end_date is None:
        end_date = get_current_date()
        
    if start_date is None:
        log.error("Cannot calculate days between: start_date is None")
        return 999  # Error value
        
    try:
        # Calculate the difference in days
        delta = end_date - start_date
        return delta.days
    except Exception as e:
        log.error(f"Error calculating days between dates: {e}")
        return 999  # Error value

def calculate_days_since(date_str, debug=False):
    """
    Calculate days since a specific date.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
        debug (bool, optional): Whether to log debug info. Defaults to False.
        
    Returns:
        int: Number of days since the date (positive if date is in the past)
    """
    date_obj = parse_date(date_str)
    today = get_current_date()
    
    if date_obj is None:
        return 999  # Error value
        
    days_since = calculate_days_between(date_obj, today)
    
    if debug:
        log.debug(f"Comparing: today={today.strftime('%Y-%m-%d')} vs date_posted={date_obj.strftime('%Y-%m-%d')}")
        log.debug(f"Days since: {days_since} for {date_str}")
    
    return days_since

def format_days_for_display(days):
    """
    Format days count for display in the splitflap.
    
    Args:
        days (int): Number of days
        
    Returns:
        str: Formatted string (e.g., "000" for today, "007" for 7 days ago)
    """
    try:
        if days == 0:
            return "000"  # Today
        elif days > 0:
            # Pad with leading zeros for proper sorting
            return f"{days:03d}"  # Using 3 digits (handles up to 999 days)
        else:
            # Handle future dates - show as negative days with leading zeros
            return f"-{abs(days):03d}"
    except Exception as e:
        log.error(f"Error formatting days: {e}")
        return "999"  # Error value

def format_date_for_display(date_obj=None, format_str='%b %d, %Y'):
    """
    Format a date object as a string for display.
    
    Args:
        date_obj (datetime.datetime, optional): Date to format. Defaults to current date.
        format_str (str, optional): Format string. Defaults to '%b %d, %Y'.
        
    Returns:
        str: Formatted date string
    """
    if date_obj is None:
        date_obj = get_current_date()
        
    try:
        return date_obj.strftime(format_str)
    except Exception as e:
        log.error(f"Error formatting date: {e}")
        return "Unknown date"

def get_time_for_display(format_str='%I:%M %p'):
    """
    Get the current time formatted for display.
    
    Args:
        format_str (str, optional): Format string. Defaults to '%I:%M %p'.
        
    Returns:
        str: Formatted time string
    """
    try:
        current_time = get_current_date()
        return current_time.strftime(format_str)
    except Exception as e:
        log.error(f"Error getting time for display: {e}")
        return "Unknown time" 