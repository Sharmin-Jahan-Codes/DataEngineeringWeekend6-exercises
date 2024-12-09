import requests
import os
import zipfile
from pathlib import Path

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def create_downloads_dir():
    """Create the downloads directory if it doesn't exist."""
    downloads_path = Path("downloads")
    downloads_path.mkdir(exist_ok=True)
    return downloads_path

def download_file(url, output_path):
    """Download a file from the given URL and save it to the specified path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {output_path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

def extract_zip_file(zip_path, extract_to):
    """Extract a zip file and remove the original zip."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted: {zip_path}")
        os.remove(zip_path)
    except zipfile.BadZipFile:
        print(f"Invalid zip file: {zip_path}")

def main():
    downloads_dir = create_downloads_dir()
    
    for url in download_uris:
        filename = url.split("/")[-1]  # Extract filename from URL
        zip_path = downloads_dir / filename
        
        # Download the file
        download_file(url, zip_path)
        # Extract the zip if downloaded successfully
        if zip_path.exists():
            extract_zip_file(zip_path, downloads_dir)

if __name__ == "__main__":
    main()
