# modules/utils.py
import hashlib
import os

class Utils:
    def generate_markdown_output(self, input_file, output_file, segment_results, combined_text,
                                 total_word_count, total_char_count, combined_md5, config):
        with open(output_file, 'w') as f:
            # Front Matter
            f.write('---\n')
            f.write(f'- Input: {input_file}\n')
            f.write(f'- Output: {output_file}\n')
            f.write(f'- Word count: {total_word_count}\n')
            f.write(f'- Char count: {total_char_count}\n')
            f.write('\n- Configuration\n')
            f.write('  - Effects to try\n')
            for effect in config.get('effects_to_try'):
                f.write(f'    - {effect["name"]}: {"enabled" if effect["enabled"] else "disabled"}\n')
            f.write(f'  - Word wrap on char: {config.get("word_wrap")}\n')
            f.write(f'  - Iterations: {config.get("iterations")}\n')
            f.write('---\n\n')

            # Header
            f.write(f'# {os.path.basename(input_file)}\n')
            for result in segment_results:
                f.write(f'## Segment {result["segment_number"]}\n')
                f.write(f'> Words: {result["word_count"]}, Char count: {result["char_count"]}, MD5: {result["md5_hash"]}\n')
                f.write(f'{result["text"]}\n\n')

            f.write(f'## Combined {len(segment_results)}\n')
            f.write(f'> Words: {total_word_count}, Char count: {total_char_count}, MD5: {combined_md5}\n')
            f.write(f'{combined_text}\n')
