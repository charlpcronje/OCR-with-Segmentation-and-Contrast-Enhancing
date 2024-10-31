# modules/configuration.py

import json
import argparse
import os
from dotenv import load_dotenv

class Configuration:
    def __init__(self):
        # Load default config
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        # Load environment variables
        load_dotenv()
        self.env_config = {
            'FLASK_RUN_PORT': os.getenv('FLASK_RUN_PORT', 5000),
            'LOGS_FOLDER_PATH': os.getenv('LOGS_FOLDER_PATH', 'logs/')
        }

    def override_with_args(self, args):
        # Override config with command-line arguments
        if args.effects_to_try:
            effects = []
            for effect in args.effects_to_try.split(','):
                effects.append({"name": effect.strip(), "enabled": True})
            self.config['effects_to_try'] = effects
        if args.segment_height:
            self.config['segment_height'] = int(args.segment_height)
        if args.segment_overlap:
            self.config['segment_overlap'] = int(args.segment_overlap)
        if args.word_wrap:
            self.config['word_wrap'] = int(args.word_wrap)
        if args.iterations:
            self.config['iterations'] = int(args.iterations)
        if args.logging_level:
            self.config['logging']['level'] = args.logging_level.upper()
        if args.logging_console is not None:
            self.config['logging']['console'] = args.logging_console
        if args.logging_file is not None:
            self.config['logging']['file'] = args.logging_file

    def override_with_params(self, params):
        # Override config with API parameters
        for key, value in params.items():
            if key in self.config:
                self.config[key] = value
            elif key in self.config['logging']:
                self.config['logging'][key] = value

    def get(self, key, default=None):
        return self.config.get(key, default)
