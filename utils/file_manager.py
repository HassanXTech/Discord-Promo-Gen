import os
import threading
from datetime import datetime
from raducord import Logger

# Thread-safe file operations
file_lock = threading.Lock()

def save_promo_link(promo_link):
    """Save promo link to promo.txt file with timestamp"""
    try:
        with file_lock:
            os.makedirs("output", exist_ok=True)
            with open("output/promo.txt", "a", encoding="utf-8") as promo_file:
                promo_file.write(f"{promo_link}\n")
            Logger.success(f'File, Promo link saved to promo.txt, Success')
            return True
    except Exception as e:
        Logger.warning(f'File, Failed to save promo link: {e}, Error')
        return False

def ensure_directories():
    """Ensure output directories exist"""
    directories = ["output"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
