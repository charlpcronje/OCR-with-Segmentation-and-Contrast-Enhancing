# interfaces/cli_interface.py

import argparse
import hashlib
from modules.configuration import Configuration
from modules.logging_module import LoggingModule
from modules.image_segmentation import ImageSegmentationModule
from modules.image_preprocessing import ImagePreprocessingModule
from modules.ocr_processing import OCRProcessingModule
from modules.utils import Utils
import os

class CLIInterface:
    def __init__(self):
        self.args = self.parse_arguments()
        self.config = Configuration()
        self.config.override_with_args(self.args)
        self.logger = LoggingModule(self.config).get_logger()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='OCR Application')
        parser.add_argument('input_file', help='Path to input image file')
        parser.add_argument('output_file', help='Path to output markdown file')
        parser.add_argument('--effects_to_try', help='Comma-separated list of effects to try')
        parser.add_argument('--segment_height', help='Height of image segments')
        parser.add_argument('--segment_overlap', help='Overlap between image segments')
        parser.add_argument('--word_wrap', help='Word wrap character count')
        parser.add_argument('--iterations', help='Number of iterations for processing')
        parser.add_argument('--logging_level', help='Logging level (DEBUG, INFO, WARNING, ERROR)')
        parser.add_argument('--logging_console', type=bool, help='Enable console logging')
        parser.add_argument('--logging_file', type=bool, help='Enable file logging')
        return parser.parse_args()

    def run(self):
        self.logger.info("Starting OCR processing via CLI")
        input_file = os.path.abspath(self.args.input_file)
        output_file = os.path.abspath(self.args.output_file)

        segmentation_module = ImageSegmentationModule(self.config, self.logger)
        preprocessing_module = ImagePreprocessingModule(self.config, self.logger)
        ocr_module = OCRProcessingModule(self.config, self.logger)
        utils = Utils()

        segments = segmentation_module.segment_image(input_file)
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
            input_file=input_file,
            output_file=output_file,
            segment_results=segment_results,
            combined_text=combined_text,
            total_word_count=total_word_count,
            total_char_count=total_char_count,
            combined_md5=combined_md5,
            config=self.config
        )

        self.logger.info("OCR processing completed via CLI")
