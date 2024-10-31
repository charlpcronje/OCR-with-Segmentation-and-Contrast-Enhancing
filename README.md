# OCR with Segmentation and Contrast Enhancing

[![GitHub](https://img.shields.io/github/license/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing)](https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0.1-green)](https://flask.palletsprojects.com/)

## Overview

This project is a Python application that performs Optical Character Recognition (OCR) on images, specifically designed to handle extremely tall images by segmenting them and applying various image preprocessing effects to enhance OCR accuracy. It can be accessed via the command line, a Flask API, or a web interface.

**GitHub Repository**: [OCR-with-Segmentation-and-Contrast-Enhancing](https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing)

## Features

- **Image Segmentation**: Splits large images into smaller segments to improve OCR performance.
- **Image Preprocessing**: Applies configurable effects such as contrast enhancement, dehazing, and color inversion.
- **OCR Processing**: Extracts text from images using Tesseract OCR.
- **Logging**: Detailed logs are maintained with configurable verbosity.
- **Configuration Management**: Settings can be adjusted via `config.json`, command-line arguments, or API parameters.
- **Multi-interface Access**: Use the application from the terminal, integrate it into other applications via API, or through a user-friendly web interface.
- **Web Interface**: Drag-and-drop images onto a web page for OCR processing with real-time log display.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
  - [config.json](#configjson)
  - [.env](#env)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
    - [Basic Usage](#basic-usage)
    - [Options](#options)
  - [Flask API](#flask-api)
    - [Starting the Server](#starting-the-server)
    - [API Endpoints](#api-endpoints)
  - [Web Interface](#web-interface)
    - [Accessing the Web UI](#accessing-the-web-ui)
    - [Uploading Images](#uploading-images)
- [Image Effects](#image-effects)
- [Segments](#segments)
- [.env File](#env-file)
- [Dependencies](#dependencies)
- [Logging](#logging)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Clone the Repository

```bash
git clone https://github.com/charlpcronje/OCR-with-Segmentation-and-Contrast-Enhancing.git
cd OCR-with-Segmentation-and-Contrast-Enhancing
```

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Install Tesseract OCR

Ensure that Tesseract OCR is installed on your system:

- **Ubuntu/Debian**:

  ```bash
  sudo apt-get install tesseract-ocr
  ```

- **macOS** (using Homebrew):

  ```bash
  brew install tesseract
  ```

- **Windows**:

  Download and install from [Tesseract OCR GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki).

### Verify Tesseract Installation

Ensure that Tesseract is accessible from the command line. If not, you may need to specify the path in the code:

```python
pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'
```

## Configuration

### config.json

The `config.json` file contains the default configuration settings for the application.

```json
{
  "effects_to_try": [
    {"name": "increase_contrast", "enabled": true},
    {"name": "dehaze", "enabled": true},
    {"name": "invert_colors", "enabled": true},
    {"name": "enhance_texture", "enabled": false}
  ],
  "segment_height": 1000,
  "segment_overlap": 25,
  "word_wrap": 80,
  "iterations": 1,
  "logging": {
    "level": "INFO",
    "console": true,
    "file": true
  }
}
```

#### Configuration Parameters

- **effects_to_try**: A list of image preprocessing effects to enhance OCR accuracy.
- **segment_height**: Height of each image segment in pixels.
- **segment_overlap**: Overlap between image segments in pixels to prevent cutting through lines of text.
- **word_wrap**: Character count at which to wrap text; `0` for no wrapping.
- **iterations**: Number of times to try processing with different segmentations and effects.
- **logging**: Logging settings including level and output destinations.

### .env

The `.env` file stores environment-specific configurations.

```
FLASK_RUN_PORT=5000
LOGS_FOLDER_PATH=logs/
```

#### Environment Variables

- **FLASK_RUN_PORT**: The port on which the Flask app runs.
- **LOGS_FOLDER_PATH**: The directory where logs and segments are stored.

## Usage

### Command Line Interface

#### Basic Usage

```bash
python ocr.py input_image.png output.md
```

#### With Options

You can override any configuration setting using command-line arguments.

```bash
python ocr.py input_image.png output.md --effects_to_try increase_contrast,dehaze --segment_height 800 --logging_level DEBUG
```

#### Options

- `--effects_to_try`: Comma-separated list of effects (`increase_contrast`, `dehaze`, `invert_colors`, `enhance_texture`).
- `--segment_height`: Height of each image segment in pixels.
- `--segment_overlap`: Overlap between segments in pixels.
- `--word_wrap`: Character count at which to wrap text; `0` for no wrapping.
- `--iterations`: Number of iterations with different segmentations and effects.
- `--logging_level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- `--logging_console`: Enable console logging (`True` or `False`).
- `--logging_file`: Enable file logging (`True` or `False`).

### Flask API

#### Starting the Server

```bash
export FLASK_APP=interfaces/api_interface.py
flask run
```

#### API Endpoints

- **Upload and OCR Processing**

  - **URL**: `http://localhost:5000/upload`
  - **Method**: `POST`
  - **Form Data**:
    - `file`: The image file to process.
  - **Parameters**: Any configuration setting can be overridden via URL parameters.

  **Example Request**:

  ```bash
  curl -X POST -F 'file=@input_image.png' 'http://localhost:5000/upload?effects_to_try=increase_contrast,dehaze&segment_height=800'
  ```

- **Log Streaming**

  - **URL**: `http://localhost:5000/logs`
  - **Method**: `GET`
  - **Parameters**:
    - `task_id`: The unique task identifier returned after uploading a file.

### Web Interface

#### Accessing the Web UI

Navigate to `https://ocr.webally.co.za` in your web browser.

#### Uploading Images

- Drag and drop an image onto the black screen.
- A message "DROP FOR OCR" will appear when you drag an image over the page.
- Once you drop the image, it will automatically upload and start processing.
- Real-time logs will display in a terminal-like block.
- After processing, the terminal block will expand, and the OCR result will be displayed.

## Image Effects

The application uses various image preprocessing effects to enhance OCR accuracy. The effects are applied in the order specified in `config.json`.

### Available Effects

- **increase_contrast**: Enhances the contrast of the image using CLAHE (Contrast Limited Adaptive Histogram Equalization).
- **dehaze**: Reduces haze in the image to improve clarity. Implementation may vary; could use histogram equalization or more advanced dehazing algorithms.
- **invert_colors**: Inverts the colors of the image, which can help OCR in some cases where text and background have low contrast.
- **enhance_texture**: Placeholder for texture enhancement; currently not implemented.

### Configuring Effects

Enable or disable effects in the `config.json`, via command-line arguments, or API parameters.

```json
"effects_to_try": [
  {"name": "increase_contrast", "enabled": true},
  {"name": "dehaze", "enabled": false},
  {"name": "invert_colors", "enabled": true},
  {"name": "enhance_texture", "enabled": false}
],
```

#### Effect Descriptions

- **Increase Contrast**: Improves the contrast between text and background, making text more distinguishable.
- **Dehaze**: Removes haze or fog-like effects from images, which can obscure text.
- **Invert Colors**: Switches light pixels to dark and vice versa; useful when text is lighter than the background.
- **Enhance Texture**: Aims to highlight textural features; not currently implemented.

## Segments

To handle extremely tall images, the application segments the image into smaller pieces.

- **segment_height**: The height of each segment in pixels (default is 1000).
- **segment_overlap**: The number of pixels to overlap between segments (default is 25).
- **Purpose**: Prevents missing any text by ensuring lines are not cut off between segments.
- **Storage**: Segments are saved in the `logs/segments` directory.
- **Maintenance**: The application maintains a maximum of 500 segment files, deleting the oldest files when the limit is exceeded.

### How Segmentation Works

1. **Initial Segmentation**: The image is divided into segments of `segment_height` pixels.
2. **Overlapping Segments**: Each segment overlaps the previous one by `segment_overlap` pixels.
3. **Processing**: Each segment is processed individually through the image preprocessing and OCR pipeline.
4. **Combining Results**: The text extracted from each segment is combined to form the final output.

## .env File

The `.env` file is used to set environment-specific variables, primarily for the Flask application and logging.

### Variables

- **FLASK_RUN_PORT**: Specifies the port on which the Flask application will run.
- **LOGS_FOLDER_PATH**: Defines the directory where logs and image segments will be stored.

### Example

```
FLASK_RUN_PORT=5000
LOGS_FOLDER_PATH=logs/
```

### Usage

The application uses the `python-dotenv` package to load variables from the `.env` file. Ensure that the `.env` file is in the root directory of the project.

## Dependencies

- **Python 3.8+**
- **Required Packages**:
  - Flask
  - Flask-SSE
  - Flask-Cors
  - pytesseract
  - Pillow
  - OpenCV (`opencv-python`)
  - python-dotenv

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### Additional Requirements

- **Tesseract OCR**: The application relies on Tesseract for OCR processing. Ensure it is installed and accessible.
- **Web Server**: If deploying the web interface, you may need a web server like Nginx or Apache to serve static files and proxy requests.

## Logging

- **Log Levels**: Configurable via `config.json` and command-line arguments.
- **Outputs**:
  - **Console**: Logs are printed to the terminal if enabled.
  - **File**: Logs are saved in `logs/logs-{date}.log`.
- **Customization**: You can set the logging level and outputs in the configuration.

### Adjusting Logging Settings

In `config.json`:

```json
"logging": {
  "level": "DEBUG",
  "console": true,
  "file": true
}
```

Via Command-Line:

```bash
python ocr.py input_image.png output.md --logging_level DEBUG --logging_console True --logging_file True
```

## Project Structure

```
OCR-with-Segmentation-and-Contrast-Enhancing/
├── ocr.py
├── config.json
├── .env
├── requirements.txt
├── README.md
├── logs/
│   ├── logs-{date}.log
│   └── segments/
├── uploads/
├── interfaces/
│   ├── cli_interface.py
│   └── api_interface.py
├── modules/
│   ├── configuration.py
│   ├── image_preprocessing.py
│   ├── image_segmentation.py
│   ├── logging_module.py
│   ├── ocr_processing.py
│   └── utils.py
├── static/
│   ├── index.html
│   ├── styles.css
│   └── script.js
```

- **ocr.py**: Entry point for the CLI application.
- **config.json**: Configuration file for default settings.
- **.env**: Environment variables.
- **interfaces/**: Contains the CLI and API interfaces.
- **modules/**: Contains the core modules for image segmentation, preprocessing, OCR processing, etc.
- **static/**: Contains the web interface files.
- **logs/**: Stores log files and image segments.
- **uploads/**: Directory for uploaded images via the web interface.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**:

   Click the "Fork" button at the top right of the GitHub page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your-username/OCR-with-Segmentation-and-Contrast-Enhancing.git
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**:

   Implement your feature or bug fix.

5. **Commit Your Changes**:

   ```bash
   git commit -am 'Add some feature'
   ```

6. **Push to the Branch**:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**:

   Navigate to your fork on GitHub and click the "New Pull Request" button.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or issues, please open an issue on GitHub or contact the repository owner.

## Additional Notes

### Testing and Validation

- **Unit Tests**: Implement unit tests for each module to ensure functionality.
- **Sample Images**: Use a variety of images to test the effectiveness of different preprocessing effects.
- **Performance**: Monitor performance when processing large images or a high volume of requests.

### Security Considerations

- **File Uploads**: Validate uploaded files to ensure they are images and within acceptable size limits.
- **Error Handling**: Implement robust error handling to prevent crashes and provide meaningful feedback.
- **HTTPS**: Use HTTPS to secure communications, especially when deploying the web interface.

### Deployment

- **Web Server Configuration**: Configure your web server to serve the Flask app and static files.
- **Scaling**: Consider using a WSGI server like Gunicorn or uWSGI for production deployments.
- **Environment Variables**: Use environment variables for sensitive configurations and in production environments.

## Frequently Asked Questions (FAQ)

### 1. **I get an error saying `pytesseract.pytesseract.TesseractNotFoundError`. What should I do?**

Ensure that Tesseract OCR is installed on your system and accessible via the command line. If Tesseract is installed in a non-standard location, specify the path in your code:

```python
pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'
```

### 2. **Can I add new image preprocessing effects?**

Yes! You can implement new effects in the `ImagePreprocessingModule` within `image_preprocessing.py`. Add your effect function and update the `effects_to_try` configuration.

### 3. **How do I change the logging level to see more detailed logs?**

You can change the logging level in `config.json` or override it via the command line:

```bash
python ocr.py input_image.png output.md --logging_level DEBUG
```

### 4. **The OCR results are not accurate. What can I do?**

- Experiment with different image preprocessing effects.
- Adjust the `segment_height` and `segment_overlap` parameters.
- Ensure that the image quality is sufficient for OCR.
- Consider training Tesseract with custom data if working with specialized fonts.

---

Feel free to contribute, report issues, or suggest enhancements. Your feedback is valuable!