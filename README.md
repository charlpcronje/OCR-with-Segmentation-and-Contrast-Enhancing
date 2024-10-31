# OCR with Segmentation and Contrast Enhancing

[![GitHub](https://img.shields.io/github/license/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing)](https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-green)](https://flask.palletsprojects.com/)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
  - [API Usage](#api-usage)
  - [Web UI](#web-ui)
- [Configuration](#configuration)
  - [config.json](#configjson)
  - [.env File](#env-file)
- [Image Effects](#image-effects)
- [Segmentation](#segmentation)
- [Logging](#logging)
- [Cache Management](#cache-management)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

**OCR with Segmentation and Contrast Enhancing** is a Python-based Optical Character Recognition (OCR) application designed to process large images efficiently. It segments images into manageable chunks, applies configurable image enhancements to improve text recognition, and provides access through both a Command-Line Interface (CLI) and a Flask API.

**GitHub Repository**: [https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing](https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing)

---

## Features

- **Image Segmentation**: Efficiently process large images by segmenting them into smaller, manageable chunks with overlapping regions to prevent text loss.
- **Image Enhancements**: Apply configurable image effects such as contrast enhancement, color inversion, dehazing, and sharpening to improve OCR accuracy.
- **OCR Processing**: Extract text from images using Tesseract OCR via the `pytesseract` library.
- **Command-Line Interface**: User-friendly CLI with options to customize logging and word wrapping.
- **Flask API**: RESTful API endpoint to upload images and receive extracted text in JSON format.
- **Configuration Files**: Customize application behavior using `config.json` and `.env` files.
- **Logging System**: Detailed logging with options to output to terminal or log files.
- **Cache Management**: Efficient cache handling with automatic deletion of old files based on a FIFO strategy.
- **Markdown Report Generation**: Generates a comprehensive markdown report with statistics and OCR results.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing.git
   cd OCR-with-Segmentation-and-Contrast-Enhancing
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**

   - **Windows**: Download and install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
   - **macOS**: Install via Homebrew:

     ```bash
     brew install tesseract
     ```

   - **Linux**: Install via package manager:

     ```bash
     sudo apt-get install tesseract-ocr
     ```

5. **Set Up Configuration Files**

   - **config.json**: Copy the provided `config.example.json` to `config.json` and customize as needed.
   - **.env**: Create a `.env` file and define the necessary environment variables.

---

## Usage

### Command-Line Interface (CLI)

The CLI allows you to process images directly from the terminal.

#### Syntax

```bash
ocr <input_file> <output_file> [options]
```

#### Options

- `--logs [verbose|error|file|terminal]`: Set the log output and level.
- `--word-wrap [true|false]`: Override the `word_wrap` setting from `config.json`.

#### Example

```bash
ocr input_image.png output_text.md --word-wrap false --logs verbose
```

This command processes `input_image.png`, writes the OCR result to `output_text.md`, disables word wrapping, and sets the logging level to verbose.

### API Usage

The Flask API provides an endpoint to upload images and receive extracted text in JSON format.

#### Starting the API Server

```bash
python api_server.py
```

The server will start on the port specified in the `.env` file.

#### API Endpoint

- **URL**: `http://localhost:{API_PORT}/api/ocr`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Form Data**: `image` (The image file to be processed)

#### Example Using `curl`

```bash
curl -X POST -F "image=@input_image.png" http://localhost:{API_PORT}/api/ocr
```

#### Response

```json
{
  "text": "Extracted text content...",
  "word_count": 100,
  "char_count": 500,
  "md5_hash": "d41d8cd98f00b204e9800998ecf8427e"
}
```

### Web UI

*Note: If a web UI is implemented, include instructions here. Otherwise, remove this section.*

---

## Configuration

### config.json

The `config.json` file allows you to customize various aspects of the application.

#### Example

```json
{
  "segment_height": 1000,
  "overlap_pixels": 25,
  "effects": {
    "increase_contrast": true,
    "invert_colors": true,
    "dehaze": true,
    "sharpen": false
  },
  "word_wrap": 80,
  "log_level": "verbose"
}
```

#### Configuration Options

- **segment_height**: (Integer) Height of each image segment in pixels.
- **overlap_pixels**: (Integer) Number of pixels by which segments overlap to prevent text loss.
- **effects**: (Object) Configurable image effects.
  - **increase_contrast**: (Boolean) Enhance image contrast.
  - **invert_colors**: (Boolean) Invert image colors.
  - **dehaze**: (Boolean) Apply a dehazing effect.
  - **sharpen**: (Boolean) Sharpen the image.
- **word_wrap**: (Integer) Maximum line width for word wrapping. Set to 0 for no wrapping.
- **log_level**: (String) Default logging level (`verbose`, `error`, etc.).

### .env File

The `.env` file stores environment variables for the application.

#### Example

```bash
API_PORT=5000
LOG_FOLDER_PATH=./logs
```

#### Environment Variables

- **API_PORT**: Port number on which the Flask API server runs.
- **LOG_FOLDER_PATH**: Directory path where log files are stored.

---

## Image Effects

Image effects are applied sequentially to enhance OCR accuracy. They can be enabled or disabled in `config.json`.

### Available Effects

1. **Increase Contrast**
   - Enhances the contrast of the image.
   - Makes text stand out against the background.

2. **Invert Colors**
   - Inverts the colors of the image.
   - Useful for images with light text on dark backgrounds.

3. **Dehaze**
   - Reduces haze and noise.
   - Improves clarity and sharpness.

4. **Sharpen**
   - Enhances edges in the image.
   - Makes text edges more distinct.

### Configuration Example

```json
"effects": {
  "increase_contrast": true,
  "invert_colors": false,
  "dehaze": true,
  "sharpen": true
}
```

### Effect Application Order

Effects are applied in the order they appear in `config.json`. Adjust the order if necessary to achieve the best results.

---

## Segmentation

Large images are segmented to improve OCR processing efficiency and accuracy.

### How Segmentation Works

- **Primary Segments**: Image is divided into chunks of `segment_height` pixels starting from the top.
- **Secondary Segments**: Additional segments are created, starting `overlap_pixels` pixels below each primary segment.
- **Overlapping**: Segments overlap by `overlap_pixels` to ensure that text split between segments is captured.

### Purpose

- **Manageability**: Prevents issues with processing very large images.
- **Text Integrity**: Ensures that lines of text are not cut off between segments.

### Configuration

- **segment_height**: Defines the height of each segment.
- **overlap_pixels**: Specifies the overlap between segments.

### Example

If `segment_height` is 1000 pixels and `overlap_pixels` is 25 pixels:

- **Primary Segments Start At**: 0, 1000, 2000, ...
- **Secondary Segments Start At**: 25, 1025, 2025, ...

---

## Logging

The application includes a robust logging system configurable via `config.json` or CLI options.

### Log Outputs

- **Terminal**: Logs are displayed in the console.
- **Log Files**: Logs are written to `logs/logs-{date}.log`.

### Log Levels

- **verbose**: Detailed information for debugging.
- **error**: Only error messages.

### Configuration

- **config.json**: Set the default `log_level`.
- **CLI Option**: Override using `--logs [level]`.

### Example

```bash
ocr input_image.png output_text.md --logs error
```

This command sets the logging level to error, overriding the `config.json` setting.

---

## Cache Management

To manage disk space and improve performance, the application implements cache management.

### Features

- **Storage Location**: All segments and cache files are stored in `logs/segments/`.
- **File Limit**: Keeps only the latest 500 files.
- **FIFO Strategy**: Automatically deletes the oldest files when the limit is exceeded.

### Configuration

- The file limit is currently hardcoded to 500 but can be modified in the source code if needed.

---

## Dependencies

The application relies on several Python libraries and external tools.

### Python Libraries

- **Pillow**: Image processing.
- **OpenCV**: Advanced image operations.
- **pytesseract**: OCR processing.
- **Flask**: API development.
- **python-dotenv**: Environment variable management.
- **argparse**: Command-line argument parsing.
- **logging**: Logging functionality.

### External Tools

- **Tesseract OCR**: The OCR engine used for text extraction.

### Installation

All Python dependencies are listed in `requirements.txt` and can be installed using:

```bash
pip install -r requirements.txt
```

Ensure that Tesseract OCR is installed on your system and accessible in your system's PATH.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### Steps to Contribute

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you have any questions or need further assistance, please open an issue on GitHub or contact the maintainer.

Happy OCR processing!