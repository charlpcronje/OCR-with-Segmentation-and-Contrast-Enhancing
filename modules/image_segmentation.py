# modules/image_segmentation.py

from PIL import Image
import os

class ImageSegmentationModule:
    def __init__(self, config, logger):
        self.segment_height = config.get('segment_height')
        self.segment_overlap = config.get('segment_overlap')
        self.logger = logger
        self.segments_folder = os.path.join(config.env_config['LOGS_FOLDER_PATH'], 'segments')
        os.makedirs(self.segments_folder, exist_ok=True)

    def segment_image(self, image_path):
        self.logger.info(f"Segmenting image: {image_path}")
        image = Image.open(image_path)
        width, height = image.size
        segments = []
        y = 0

        while y < height:
            box = (0, y, width, min(y + self.segment_height, height))
            segment = image.crop(box)
            segment_path = os.path.join(self.segments_folder, f"segment_{y}.png")
            segment.save(segment_path)
            segments.append(segment_path)
            y += self.segment_height - self.segment_overlap

        self._manage_segments_folder()
        return segments

    def _manage_segments_folder(self):
        # Maintain a maximum of 500 files
        files = sorted(os.listdir(self.segments_folder), key=lambda x: os.path.getctime(os.path.join(self.segments_folder, x)))
        if len(files) > 500:
            files_to_delete = files[:len(files) - 500]
            for file in files_to_delete:
                os.remove(os.path.join(self.segments_folder, file))
                self.logger.debug(f"Deleted old segment file: {file}")
