import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def extract_name_and_base_url(original_url):
    """
    Extracts the alphabetical name from the directory name and the base URL.

    Args:
        original_url (str): The original URL.

    Returns:
        tuple: A tuple containing the base URL and the extracted name.
    """
    import re

    match = re.search(r"/([\w\d]+)(?=/index\.html)", original_url)
    if not match:
        raise ValueError("Invalid URL format. Cannot extract the directory name.")

    directory_name = match.group(1)
    name = ''.join(filter(str.isalpha, directory_name))  # Keep only alphabets
    base_url = original_url.rsplit("/", 1)[0]  # Base URL without 'index.html'
    return base_url, name

def is_image_url(url):
    """
    Checks if the URL hosts an image by verifying the Content-Type in the response header.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL hosts an image, False otherwise.
    """
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return True
    except requests.RequestException:
        pass
    return False

def discover_image_urls(base_url, name):
    """
    Discovers all valid image URLs starting from 1, incrementing until no more valid images are found.

    Args:
        base_url (str): The base URL of the images directory.
        name (str): The name used to construct the image URLs.

    Returns:
        list: A list of discovered image URLs.
    """
    discovered_urls = []
    failures = 0
    index = 1

    with tqdm(desc="Discovering Images", unit="url", ncols=80) as pbar:
        while failures < 3:  # Stop after 3 consecutive failures
            url = f"{base_url}/images/{name}{index}.jpg"
            if is_image_url(url):
                discovered_urls.append(url)
                failures = 0  # Reset failure count on success
            else:
                failures += 1
            pbar.update(1)
            index += 1
    return discovered_urls

def download_images_concurrently(urls, download_folder):
    """
    Downloads images concurrently using ThreadPoolExecutor.

    Args:
        urls (list): List of image URLs to download.
        download_folder (str): The folder where images will be saved.
    """
    with ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=len(urls), desc="Downloading Images", unit="image", ncols=80, unit_scale=True) as pbar:
            for url in urls:
                image_name = os.path.basename(url)
                save_path = os.path.join(download_folder, image_name)
                futures.append(executor.submit(download_image, url, save_path))
            for future in as_completed(futures):
                pbar.update(1)

def download_image(url, save_path):
    """
    Downloads an image from a URL.

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
    # Input URL and custom folder name
    input_url = Prompt.ask("Enter the original URL").strip()
    download_folder = Prompt.ask("Enter the folder name for downloads", default="downloaded_images").strip()
    os.makedirs(download_folder, exist_ok=True)

    try:
        # Step 1: Extract base URL and name
        base_url, name = extract_name_and_base_url(input_url)

        # Step 2: Discover valid image URLs
        console.print("[cyan]Discovering image URLs...[/cyan]")
        discovered_urls = discover_image_urls(base_url, name)
        console.print(f"[green]Discovery complete. Found {len(discovered_urls)} valid image URLs.[/green]")

        if discovered_urls:
            # Step 3: Download discovered images
            console.print("[cyan]Downloading images...[/cyan]")
            download_images_concurrently(discovered_urls, download_folder)
            console.print(f"[green]All valid images have been downloaded to '{download_folder}' successfully![/green]")
        else:
            console.print("[yellow]No valid images found to download.[/yellow]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")

if __name__ == "__main__":
    main()