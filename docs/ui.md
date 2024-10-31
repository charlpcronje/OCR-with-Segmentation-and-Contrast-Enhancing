## Prompt
Create a very simple web interface that wil be hosted at https://ocr.webally.co.za. It must just be a black blank screen and when I drag an image onto the page huge white text must say DROP FOR OCR. Then when I drop the image it must auto upload and the server must start doing the OCR, and whatever would usuall get written to the terminal must be returned as it happens and be displayed on the screen in white text in the center of the screen in a terminal sized block with a white border. When it is done the block must animate to the size of 960px with and must be 100% of the screen height. The response text must then be displayed in that block in white text

## Response
Certainly! I'll help you create a simple web interface as per your specifications. The interface will:

- Display a black background with a message "DROP FOR OCR" when an image is dragged over it.
- Allow users to drag and drop an image onto the page.
- Upload the image to your server (`https://ocr.webally.co.za`) for OCR processing.
- Display real-time logs (what would usually be printed to the terminal) as the OCR process runs.
- After completion, animate the terminal block to a width of 960px and height of 100% of the screen.
- Display the OCR result text in the terminal block.

Below is the code for the web interface, along with explanations on how to integrate it with your existing OCR application.

---

## **1. Front-End Code**

### **1.1. HTML (`index.html`)**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OCR Web Interface</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>

  <div id="drop-zone">
    <div id="message">DROP FOR OCR</div>
  </div>

  <div id="terminal">
    <pre id="output"></pre>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

### **1.2. CSS (`styles.css`)**

```css
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #000;
  font-family: monospace;
}

#drop-zone {
  position: absolute;
  width: 100%;
  height: 100%;
  text-align: center;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

#message {
  font-size: 48px;
  opacity: 0.5;
}

#terminal {
  display: none;
  position: absolute;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 300px;
  transform: translate(-50%, -50%);
  background-color: #000;
  border: 2px solid #fff;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
  opacity: 0;
  transition: all 0.5s ease;
}

#terminal.active {
  display: block;
  opacity: 1;
}

#terminal.expanded {
  width: 960px;
  height: 100%;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
}

#output {
  color: #fff;
  white-space: pre-wrap;
  word-wrap: break-word;
}
```

### **1.3. JavaScript (`script.js`)**

```javascript
// script.js

const dropZone = document.getElementById('drop-zone');
const message = document.getElementById('message');
const terminal = document.getElementById('terminal');
const output = document.getElementById('output');

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  message.style.opacity = '1';
});

dropZone.addEventListener('dragleave', () => {
  message.style.opacity = '0.5';
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  message.style.display = 'none';
  terminal.classList.add('active');

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    uploadFile(files[0]);
  }
});

function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();

  xhr.open('POST', '/upload', true);

  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      output.innerText = `Uploading: ${Math.round(percentComplete)}%`;
    }
  };

  xhr.onload = function () {
    if (xhr.status === 200) {
      // Start receiving logs
      const response = JSON.parse(xhr.responseText);
      if (response.task_id) {
        getLogs(response.task_id);
      } else {
        output.innerText = 'Error: No task ID received.';
      }
    } else {
      output.innerText = 'Error uploading file.';
    }
  };

  xhr.send(formData);
}

function getLogs(taskId) {
  const eventSource = new EventSource(`/logs?task_id=${taskId}`);

  eventSource.onmessage = function (e) {
    output.innerText += e.data + '\n';
    output.scrollTop = output.scrollHeight;
  };

  eventSource.onerror = function () {
    eventSource.close();
    terminal.classList.add('expanded');
  };
}
```

---

## **2. Back-End Integration**

To make this work, you'll need to:

- Modify your Flask app to handle file uploads.
- Use Server-Sent Events (SSE) to stream logs to the client in real-time.
- Start OCR processing upon file upload and send logs back to the client.

### **2.1. Install Required Packages**

Add `Flask-SSE` and `Flask-Cors` to your `requirements.txt`:

```
Flask==2.0.1
Flask-SSE==0.2.1
Flask-Cors==3.0.10
pytesseract==0.3.8
Pillow==8.2.0
opencv-python==4.5.2.52
python-dotenv==0.17.1
```

Install the new packages:

```bash
pip install Flask-SSE Flask-Cors
```

### **2.2. Update `api_interface.py`**

Modify your API interface to handle file uploads and SSE.

```python
# interfaces/api_interface.py

from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
from modules.configuration import Configuration
from modules.logging_module import LoggingModule
from modules.image_segmentation import ImageSegmentationModule
from modules.image_preprocessing import ImagePreprocessingModule
from modules.ocr_processing import OCRProcessingModule
from modules.utils import Utils
import os
import threading
import queue
import uuid

app = Flask(__name__)
CORS(app)

# A dictionary to hold queues for each client
log_queues = {}

def generate_logs(task_id):
    q = log_queues.get(task_id)
    while True:
        try:
            log = q.get(timeout=30)
            yield f"data: {log}\n\n"
        except queue.Empty:
            break

def ocr_process(file_path, task_id, config):
    logger = LoggingModule(config).get_logger()
    q = log_queues[task_id]

    # Redirect logger to queue
    class QueueHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            q.put(log_entry)

    handler = QueueHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

    logger.info("Starting OCR processing via API")

    output_file = f"{os.path.splitext(file_path)[0]}.md"
    segmentation_module = ImageSegmentationModule(config, logger)
    preprocessing_module = ImagePreprocessingModule(config, logger)
    ocr_module = OCRProcessingModule(config, logger)
    utils = Utils()

    segments = segmentation_module.segment_image(file_path)
    combined_text = ''
    segment_results = []

    for idx, segment_path in enumerate(segments):
        preprocessed_images = preprocessing_module.preprocess_image(segment_path)
        for image in preprocessed_images:
            text, word_count, char_count, md5_hash = ocr_module.perform_ocr(image)
            if text.strip():
                segment_results.append({
                    'segment_number': idx + 1,
                    'word_count': word_count,
                    'char_count': char_count,
                    'md5_hash': md5_hash,
                    'text': text
                })
                combined_text += text + '\n'
                break  # Move to next segment if OCR is successful

    total_word_count = len(combined_text.split())
    total_char_count = len(combined_text)
    combined_md5 = hashlib.md5(combined_text.encode('utf-8')).hexdigest()

    utils.generate_markdown_output(
        input_file=file_path,
        output_file=output_file,
        segment_results=segment_results,
        combined_text=combined_text,
        total_word_count=total_word_count,
        total_char_count=total_char_count,
        combined_md5=combined_md5,
        config=config
    )

    logger.info("OCR processing completed via API")
    q.put("OCR processing completed.")
    q.put("RESULT_START")
    q.put(combined_text)
    q.put("RESULT_END")
    q.put(None)  # Signal the end

@app.route('/upload', methods=['POST'])
def upload_file():
    config = Configuration()
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    input_file = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(input_file)

    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    log_queues[task_id] = queue.Queue()

    # Start OCR processing in a separate thread
    threading.Thread(target=ocr_process, args=(input_file, task_id, config)).start()

    return jsonify({'task_id': task_id}), 200

@app.route('/logs')
def stream_logs():
    task_id = request.args.get('task_id')
    if task_id not in log_queues:
        return jsonify({'error': 'Invalid task ID'}), 400

    return Response(generate_logs(task_id), mimetype='text/event-stream')

if __name__ == '__main__':
    config = Configuration()
    app.run(port=int(config.env_config['FLASK_RUN_PORT']), threaded=True)
```

**Note:** Ensure you import the necessary modules at the top:

```python
import logging
from werkzeug.utils import secure_filename
```

---

## **3. Explanation and How It Works**

### **3.1. Front-End**

- **Drag and Drop Handling:**
  - The page listens for `dragover`, `dragleave`, and `drop` events.
  - When a file is dropped, it hides the message and displays the terminal block.
  - The file is uploaded via AJAX (`XMLHttpRequest`).

- **Real-Time Log Display:**
  - After the upload, the client receives a `task_id`.
  - It opens a Server-Sent Events (SSE) connection to `/logs?task_id=...`.
  - As the server sends logs, they are appended to the terminal output.

- **Animation and Final Display:**
  - When the server indicates the process is complete, the terminal block expands to 960px width and 100% height.
  - The final OCR result is displayed inside the terminal block.

### **3.2. Back-End**

- **File Upload Endpoint (`/upload`):**
  - Saves the uploaded file to a directory.
  - Generates a unique `task_id`.
  - Starts the OCR process in a separate thread, passing the `task_id`.

- **OCR Processing:**
  - Redirects logging output to a queue associated with the `task_id`.
  - As the OCR process runs, logs are put into the queue.

- **Log Streaming Endpoint (`/logs`):**
  - Uses Server-Sent Events to stream logs to the client in real-time.
  - Closes the connection when the OCR process is complete.

---

## **4. Deployment Notes**

- **Hosting the Web Interface:**
  - Place the `index.html`, `styles.css`, and `script.js` files in your web server's root directory.
  - Ensure the Flask app is running and accessible at `https://ocr.webally.co.za`.

- **CORS Configuration:**
  - The Flask app uses `Flask-Cors` to allow cross-origin requests from your web interface.

- **Static Files Serving:**
  - If you're serving the static files from Flask, ensure you set up static file serving.
  - Alternatively, serve the front-end files using a web server like Nginx or Apache.

- **Security Considerations:**
  - Use HTTPS to secure the file uploads.
  - Implement proper validation and error handling.

---

## **5. Full Project Structure**

```
ocr_app/
├── interfaces/
│   ├── api_interface.py
│   └── cli_interface.py
├── modules/
│   ├── configuration.py
│   ├── image_preprocessing.py
│   ├── image_segmentation.py
│   ├── logging_module.py
│   ├── ocr_processing.py
│   └── utils.py
├── static/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── uploads/
├── logs/
├── config.json
├── .env
├── requirements.txt
├── README.md
└── ocr.py
```

- **Note:** Place your front-end files (`index.html`, `styles.css`, `script.js`) in a `static` folder.

---

## **6. Additional Details**

### **6.1. Server-Sent Events (SSE)**

- SSE is used to push logs from the server to the client in real-time.
- The client listens to the `/logs` endpoint and appends received messages to the output.

### **6.2. Logging Redirection**

- A custom logging handler redirects log messages to the queue associated with the `task_id`.
- This allows per-client logging streams.

### **6.3. Final OCR Result**

- When the OCR process is complete, the server sends a special message (`RESULT_START`, `RESULT_END`) to indicate the beginning and end of the final OCR text.
- The client can detect this and display the final result.

---

## **7. Client-Side Adjustments**

Update the `getLogs` function in `script.js` to handle the final OCR result:

```javascript
function getLogs(taskId) {
  const eventSource = new EventSource(`/logs?task_id=${taskId}`);
  let resultMode = false;

  eventSource.onmessage = function (e) {
    if (e.data === 'RESULT_START') {
      resultMode = true;
      output.innerText = '';
      terminal.classList.add('expanded');
      return;
    }
    if (e.data === 'RESULT_END') {
      resultMode = false;
      eventSource.close();
      return;
    }
    if (resultMode) {
      output.innerText += e.data + '\n';
    } else {
      output.innerText += e.data + '\n';
      output.scrollTop = output.scrollHeight;
    }
  };

  eventSource.onerror = function () {
    eventSource.close();
  };
}
```

---

## **8. Testing the Application**

- **Upload an Image:**
  - Drag and drop an image onto the web page.
  - Observe the logs appearing in real-time.

- **Final Result:**
  - After processing, the terminal block expands.
  - The OCR result text is displayed.

---

## **9. Summary**

You've now got a simple web interface that:

- Allows users to drag and drop images for OCR processing.
- Provides real-time feedback by streaming logs from the server.
- Displays the final OCR result in an animated terminal-like block.

---

## **10. Additional Tips**

- **SSL Certificates:**
  - Ensure your server has a valid SSL certificate since you're serving content over HTTPS.

- **Error Handling:**
  - Add more robust error handling on both the client and server sides.

- **File Size Limits:**
  - Implement checks for maximum file size to prevent server overload.

- **Security:**
  - Sanitize file inputs and validate image formats to prevent security vulnerabilities.

---

## **11. Dependencies and Requirements**

- **Python Packages:**
  - `Flask`, `Flask-SSE`, `Flask-Cors`, `pytesseract`, `Pillow`, `opencv-python`, `python-dotenv`.

- **Front-End:**
  - Basic HTML, CSS, and JavaScript.

- **Server Configuration:**
  - Ensure your Flask app can handle multi-threading (use `threaded=True` in `app.run`).

- **Web Server:**
  - You may need to configure your web server (e.g., Nginx) to proxy requests to your Flask app.

---

## **12. Conclusion**

By following the steps above, you can enhance your OCR application with a user-friendly web interface that meets your requirements. Users can simply drag and drop images, watch the processing logs in real-time, and view the final OCR text—all within a sleek, minimalistic design.

Let me know if you need further assistance or have any questions!
