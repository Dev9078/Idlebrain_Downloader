import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TextColumn

console = Console()

ROOT_FOLDER = os.path.join(os.getcwd(), "Idlebrain Downloads")


def setup_root_folder():
    """
    Ensures the root folder for downloads exists.
    """
    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)
        console.print(f"[bold green]Created root folder:[/bold green] {ROOT_FOLDER}")


def extract_base_url_and_name(url):
    """
    Extract the base URL and name from the given URL.

    Args:
        url (str): Original URL.

    Returns:
        tuple: Base URL and extracted name.
    """
    match = re.search(r"/([\w\d]+)/index\.html", url)
    if not match:
        raise ValueError("Invalid URL format. Ensure the URL contains '/index.html'.")
    base_url = url.rsplit('/', 1)[0]
    name = ''.join(filter(str.isalpha, match.group(1)))
    return base_url, name


def generate_image_urls(base_url, name, max_attempts=100):
    """
    Generate image URLs without validation.

    Args:
        base_url (str): Base URL for constructing image URLs.
        name (str): Identifier used in image filenames.
        max_attempts (int): Maximum attempts to generate URLs.

    Returns:
        list: All generated image URLs.
    """
    return [f"{base_url}/images/{name}{i}.jpg" for i in range(1, max_attempts + 1)]


def download_image(session, url, folder):
    """
    Downloads a single image.

    Args:
        session (requests.Session): HTTP session.
        url (str): URL of the image to download.
        folder (str): Folder where the image will be saved.

    Returns:
        bool: True if download succeeded, False otherwise.
    """
    try:
        response = session.get(url, stream=True, timeout=15)
        response.raise_for_status()
        filename = os.path.basename(url)
        file_path = os.path.join(folder, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except requests.RequestException:
        return False


def download_images(urls, folder):
    """
    Downloads all images with a single progress bar.

    Args:
        urls (list): List of image URLs.
        folder (str): Folder where images will be saved.

    Returns:
        tuple: Number of successful and failed downloads.
    """
    os.makedirs(folder, exist_ok=True)
    session = requests.Session()
    success_count = 0
    fail_count = 0

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        BarColumn(), TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("[cyan]Downloading images...", total=len(urls))
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(download_image, session, url, folder): url for url in urls}
            for future in as_completed(futures):
                if future.result():
                    success_count += 1
                else:
                    fail_count += 1
                progress.update(task, advance=1)

    return success_count, fail_count


def main():
    setup_root_folder()

    console.print("[bold yellow]Enter the original URL:[/bold yellow]")
    original_url = input("> ").strip()

    console.print("[bold yellow]Enter folder name for downloads (e.g., 'Event1'):[/bold yellow]")
    folder_name = input("> ").strip() or "default"
    download_folder = os.path.join(ROOT_FOLDER, folder_name)

    console.print("[bold yellow]Enter the maximum number of images to download:[/bold yellow]")
    try:
        max_attempts = int(input("> ").strip())
    except ValueError:
        console.print("[bold red]Invalid number. Using default of 100.[/bold red]")
        max_attempts = 100

    try:
        base_url, name = extract_base_url_and_name(original_url)
        console.print(f"[cyan]Base URL: {base_url}, Name: {name}[/cyan]")

        console.print("[bold cyan]Generating image URLs...[/bold cyan]")
        all_urls = generate_image_urls(base_url, name, max_attempts)

        console.print("[bold cyan]Downloading images...[/bold cyan]")
        success_count, fail_count = download_images(all_urls, download_folder)
        console.print(
            f"[bold green]Download completed! Total: {len(all_urls)}, "
            f"Downloaded: {success_count}, Failed: {fail_count}[/bold green]"
        )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()