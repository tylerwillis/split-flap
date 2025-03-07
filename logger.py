"""
Logger module for SF Moving Resources Board.
Provides consistent logging functionality across the application.
"""

import logging
import os
import json
from datetime import datetime
import glob
import shutil

# Define log levels
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def load_config():
    """
    Load configuration from config.json file
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config
    except Exception:
        # Return default values if config file cannot be loaded
        return {
            "logging": {
                "enable_debug": False,
                "log_to_file": True,
                "log_directory": "logs",
                "max_log_files": 7,
                "log_level": "INFO"
            }
        }

def get_log_config():
    """
    Get logging configuration from config.json
    
    Returns:
        tuple: (log_level, log_to_file, log_directory, max_log_files)
    """
    config = load_config()
    logging_config = config.get('logging', {})
    
    # Get log level
    if logging_config.get('enable_debug', False):
        log_level = 'DEBUG'
    else:
        log_level = logging_config.get('log_level', 'INFO').upper()
    
    # Get other logging settings
    log_to_file = logging_config.get('log_to_file', True)
    log_directory = logging_config.get('log_directory', 'logs')
    max_log_files = logging_config.get('max_log_files', 7)
    
    return log_level, log_to_file, log_directory, max_log_files

def cleanup_old_logs(log_directory, max_files):
    """
    Remove old log files to keep only the specified number of most recent files
    
    Args:
        log_directory (str): Directory containing log files
        max_files (int): Maximum number of log files to keep
    """
    try:
        if not os.path.exists(log_directory):
            return
            
        # Get list of log files sorted by modification time (oldest first)
        log_files = glob.glob(os.path.join(log_directory, '*.log'))
        log_files.sort(key=os.path.getmtime)
        
        # Remove oldest files if we have more than the max
        if len(log_files) > max_files:
            for old_file in log_files[:-max_files]:
                try:
                    os.remove(old_file)
                except Exception:
                    pass  # Ignore errors when removing old files
    except Exception:
        pass  # Don't let cleanup failure affect logging

def setup_logger(name='sf_resources', level=None, log_to_file=None, log_directory=None):
    """
    Configure and return a logger instance.
    
    Args:
        name (str): Logger name
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_directory (str): Directory to store log files
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get config settings if not provided
    if level is None or log_to_file is None or log_directory is None:
        config_level, config_log_to_file, config_log_directory, max_log_files = get_log_config()
        level = level or config_level
        log_to_file = log_to_file if log_to_file is not None else config_log_to_file
        log_directory = log_directory or config_log_directory
    else:
        # Use default max_log_files if not getting from config
        max_log_files = 7
    
    # Ensure log level is valid
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers = []
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
            
        # Clean up old log files
        cleanup_old_logs(log_directory, max_log_files)
            
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_directory, f'{name}_{timestamp}.log')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name='sf_resources'):
    """
    Get a configured logger instance with settings from config file
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return setup_logger(name) 