# interfaces/api_interface.py

import logging
from werkzeug.utils import secure_filename
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
