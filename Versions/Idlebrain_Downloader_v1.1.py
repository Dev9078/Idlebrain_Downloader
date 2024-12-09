import os
import requests
from tqdm import tqdm
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt

console = Console()

def extract_name_and_generate_urls(original_url, end):
    """
    Extracts the alphabetical name from the directory name and generates image URLs.

    Args:
        original_url (str): The original URL.
        end (int): The ending value for the incrementing number.

    Returns:
        list: A list of generated image URLs.
    """
    import re

    # Extract the directory name from the URL
    match = re.search(r"/([\w\d]+)(?=/index\.html)", original_url)
    if not match:
        raise ValueError("Invalid URL format. Cannot extract the directory name.")

    directory_name = match.group(1)
    name = ''.join(filter(str.isalpha, directory_name))  # Keep only alphabets

    base_url = original_url.rsplit("/", 1)[0]  # Base URL without 'index.html'

    # Generate URLs with progress tracking
    urls = [
        f"{base_url}/images/{name}{i}.jpg"
        for i in track(range(1, end + 1), description="Generating URLs...")
    ]
    return urls

def validate_url(url):
    """
    Validates if a URL is reachable.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        response = requests.head(url, timeout=5)  # Send HEAD request to check availability
        return response.status_code == 200
    except requests.RequestException:
        return False

def download_image(url, save_path):
    """
    Downloads an image from a URL and saves it to the specified path.

    Args:
        url (str): The URL of the image.
        save_path (str): The path to save the image.
    """
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        console.log(f"[red]Failed to download {url}: {e}[/red]")

def main():
    # Input URL and ending number
    input_url = Prompt.ask("Enter the original URL").strip()
    end_num = int(Prompt.ask("Enter the ending number", default="5"))

    # Create the download directory
    download_folder = "downloaded_images"
    os.makedirs(download_folder, exist_ok=True)

    try:
        # Step 1: Generate URLs
        urls = extract_name_and_generate_urls(input_url, end_num)

        # Step 2: Validate URLs
        console.print("[cyan]Validating URLs...[/cyan]")
        valid_urls = [
            url for url in tqdm(urls, desc="Validating URLs", unit="url")
            if validate_url(url)
        ]
        console.print(f"[green]Validation complete. Found {len(valid_urls)} valid URLs.[/green]")

        # Step 3: Download Images
        console.print("[cyan]Downloading images...[/cyan]")
        for url in track(valid_urls, description="Downloading Images", total=len(valid_urls)):
            image_name = os.path.basename(url)  # Extract filename from URL
            image_path = os.path.join(download_folder, image_name)
            download_image(url, image_path)

        console.print("[green]All valid images have been downloaded successfully![/green]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")

if __name__ == "__main__":
    main()