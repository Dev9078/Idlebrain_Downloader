
# Idlebrain Downloader 2024

A Python-based tool to asynchronously download a sequence of images from a base URL using dynamic URL generation. The program ensures integrity checks for downloaded images and provides detailed progress updates using the `rich` library.

---

## Features 🚀

- **Asynchronous Downloads**: Speeds up downloads using `aiohttp` and asyncio.
- **Dynamic URL Generation**: Automatically constructs image URLs based on a base URL and an identifier.
- **Image Validation**: Ensures that downloaded files are valid images.
- **Retry Logic**: Retries downloads on failure (configurable).
- **Customizable Settings**:
  - Base URL and identifier extraction.
  - Folder naming and storage location.
  - Maximum number of images to attempt.
- **Progress Feedback**: Real-time feedback on download progress, including successes, failures, and missing files.

---

## Prerequisites 

Ensure the following are installed on your system:

1. **Python**: Version 3.7 or higher.
2. Required Python packages:
    - `aiohttp`
    - `Pillow`
    - `rich`

Install dependencies with the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Usage 📖

1. Clone the repository or download the script.
2. Navigate to the folder containing the script.
3. Run the script:
    ```bash
    python Idlebrain_Downloader.py
    ```
4. Follow the prompts:
    - Enter the base URL (ending with `/index.html`).
    - Specify a folder name for storing downloaded images.
    - Provide the maximum number of images to attempt downloading.

---

## Example Input and Output 📥📤

### Example Input:
- Original URL:  
  ```
  https://www.idlebrain.com/movie/photogallery/rakulpreetsingh40/index.html
  ```
- Folder Name:  
  ```
  Rakul-40
  ```
- Max Images to Download:  
  ```
  50
  ```

### Example Output:
```plaintext
Base URL: https://www.idlebrain.com/movie/photogallery/rakulpreetsingh40/index.html, 
Name: Rakul-40
Downloading images...
  Download completed! Total: 50, Downloaded: 42, Not Found: 8, Failed: 0
Images saved in: ./Idlebrain Downloads/Rakul-40
```

---

## File Structure 📂

```plaintext
Idlebrain Downloader/
│
├── Idlebrain Downloads/
│   ├── Rakul-40/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── ...
├── idlebrain_downloader.py
├── README.md
└── requirements.txt
```

---

## Features to Add 📝

- **Multiple Format Support**: Allow the user to specify desired image formats (e.g., `.png`, `.jpeg`).
- **Parallel URL Sets**: Handle multiple base URLs in one run.
- **Resume Support**: Skip already downloaded images.
- **Advanced Validation**: Check image dimensions and metadata.
- **Command-Line Arguments**: Replace interactive prompts with CLI options.

---

## License 📜

This project is licensed under the MIT License.

---

## Contact 📧

For suggestions, questions, or feedback, contact:

- **Name**: Devendra Sonawane
- **Email**: [Mail me](mailto:dpsonawane789@gmail.com)
- **GitHub**: [Devson](https://github.com/DevSon1024)

---
