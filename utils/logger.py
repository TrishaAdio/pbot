import logging
import sys
from datetime import datetime
from config import Config

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    FORMATS = {
        logging.DEBUG: Colors.BLUE + "[DEBUG] %(message)s" + Colors.END,
        logging.INFO: Colors.GREEN + "[INFO] %(message)s" + Colors.END,
        logging.WARNING: Colors.YELLOW + "[WARNING] %(message)s" + Colors.END,
        logging.ERROR: Colors.RED + "[ERROR] %(message)s" + Colors.END,
        logging.CRITICAL: Colors.RED + Colors.BOLD + "[CRITICAL] %(message)s" + Colors.END,
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger():
    """Setup colored logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    return logger

def log_user_action(user_id, username, first_name, action, details=""):
    """Format user action log with colors"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_display = f"{first_name} (@{username})" if username else f"{first_name}"
    
    log_msg = (
        f"{Colors.CYAN}[{timestamp}]{Colors.END} "
        f"{Colors.YELLOW}[USER ACTION]{Colors.END} "
        f"{Colors.GREEN}{user_display}{Colors.END} "
        f"{Colors.BOLD}[ID: {user_id}]{Colors.END} "
        f"{Colors.BLUE}{action}{Colors.END} "
        f"{Colors.CYAN}{details}{Colors.END}"
    )
    
    print(log_msg)
    return log_msg
