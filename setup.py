import nltk
import subprocess
import sys

def setup_nltk_data():
    """Download required NLTK data"""
    required_data = ['punkt_tab', 'punkt', 'stopwords']
    
    for data in required_data:
        try:
            nltk.download(data)
            print(f"Downloaded {data}")
        except Exception as e:
            print(f"Download failed {data}: {e}")

if __name__ == "__main__":
    print("Setting up NLTK data...")
    setup_nltk_data()
    print("Setup complete!")
