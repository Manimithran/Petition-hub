import requests
import os

def download_font():
    # Using Bamini Tamil font from a different source
    font_url = "https://www.mediafire.com/file/bamini.ttf"  # This is a placeholder URL
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'Bamini.ttf')
    
    print("Please manually download the Bamini font and place it in:", font_path)
    print("You can download the font from various Tamil font websites or use the system-installed Bamini font.")
    print("\nSteps to install:")
    print("1. Create the directory:", os.path.dirname(font_path))
    print("2. Copy your Bamini.ttf file to:", font_path)
    
    # Create the fonts directory if it doesn't exist
    os.makedirs(os.path.dirname(font_path), exist_ok=True)

if __name__ == "__main__":
    download_font() 