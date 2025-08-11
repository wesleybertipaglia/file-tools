# File Tool Suite

A command-line utility for batch processing files and images with various tools such as renaming, compressing, converting, resizing, and zipping.

## Features

* **File Renaming**
  Rename files based on patterns or text styles.

* **File Compression**
  Compress single or multiple files into ZIP archives.

* **Image Compression**
  Compress images with adjustable JPEG quality.

* **Image Conversion**
  Convert images between popular formats (JPEG, PNG, BMP, TIFF, WEBP).

* **Image Resizing**
  Resize single or multiple images to specified dimensions.

## Installation

Make sure Python 3.x is installed:

### Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

### Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start the interactive tool menu:

```bash
python main.py
```

Follow the on-screen prompts to choose tool types and execute commands.

## Project Structure

* `engine/` – Core modules including command base classes, registry, and types.
* `tools/` – Implementation of individual tools (renamer, compressor, converter, etc.).
* `main.py` – Entry point to run the interactive CLI.

## Contributing

Feel free to add new tools or improve existing ones by extending the `ToolCommand` base class and registering your commands.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
