# modules/ocr_processing.py

import pytesseract
import hashlib
from textwrap import wrap

class OCRProcessingModule:
    def __init__(self, config, logger):
        self.word_wrap = config.get('word_wrap')
        self.logger = logger

    def perform_ocr(self, image):
        self.logger.info("Performing OCR")
        text = pytesseract.image_to_string(image)
        if self.word_wrap > 0:
            text = '\n'.join(wrap(text, self.word_wrap))
        word_count = len(text.split())
        char_count = len(text)
        md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        return text, word_count, char_count, md5_hash
