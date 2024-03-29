import argparse
import logging
import os
import sys
import warnings
from transcriber.title_split_manager import InvalidLineFormatError, TitleSplitManager
import whisper
import time
import coloredlogs
import torch
from transcriber.validators import InvalidDeviceError, Validator, InvalidTimeTitleFileError , InvalidInputFileError, InvalidModelError
from transcriber.output_print_format import OutputPrintFormat

warnings.filterwarnings("ignore")

coloredlogs.install(level='INFO', fmt='%(message)s', level_styles={'info': {'color': 'green', 'bold': True}, 'error': {'color': 'red', 'bold': True}}, field_styles={'asctime': {'color': 'cyan'}, 'levelname': {'color': 'magenta', 'bold': True}})

logger = logging.getLogger(__name__)

class Transcriber():
        
    def __init__(self, model_name: str, output_format: str):
        self.model_name = model_name
        self.output_format = output_format
        self.model = None
        self.output_formatter = OutputPrintFormat()

    def _load_model(self, device):
        logger.info(f"🔄 - Loading model: {self.model_name}\n")
        self.model = whisper.load_model(self.model_name, device=device)

    def _save_transcription_to_txt(self, result, input_file, timetitle_list):        
        try:
            output_filename = os.path.splitext(input_file)[0] + "_transcription.txt"
            self.output_formatter.print_output(result, output_filename, input_file, self.model_name, timetitle_list, format=self.output_format)
        except (ValueError) as e:
            logger.error(f"\n❌ - {e}\n")
            sys.exit(1)

    def _transcribe(self, input_file, timetitle_list, language=None):
        logger.info(f"🗣️  -> 📝 - Transcribing {input_file} with {self.model_name} model...")

        try:
            decode_options = {"language": (language or None)}
            result = self.model.transcribe(input_file, verbose=False, **decode_options)
        except Exception as e:
            logger.error(f"\n❌ - Error during transcription: {e}\n")
            sys.exit(1)
        except KeyboardInterrupt:
            logger.info(f"\n\nInterrupted by user. Stopping...")
            sys.exit(0)

        self._save_transcription_to_txt(result, input_file, timetitle_list)
        logger.info(f"✅ - Transcription completed for {input_file} with {self.model_name} model\n")

    def transcribe_files(self, input_files, timelist_files, device, language=None):
        self._validate(input_files, timelist_files, device)
 
        try:
            self._load_model(device)

            for index, input_file in enumerate(input_files):
                timelist_file = timelist_files[index] if timelist_files and index < len(timelist_files) else None
                timetitle_list = TitleSplitManager().get_title_time_list_from_file(timelist_file) if timelist_file else None
                self._transcribe(input_file, timetitle_list, language)
        except (Exception, InvalidLineFormatError) as e:
            logger.error(f"\n❌ - {e}\n")
            sys.exit(1)

        logger.info("🎉 - Transcription completed for all files")

    def _validate(self, input_files, timelist_files, device):
        try:
            Validator().validate(
                input_files, 
                self.model_name, 
                timelist_files, 
                self.output_format,
                device,
                self.output_formatter)
        except (InvalidInputFileError, InvalidModelError, InvalidTimeTitleFileError, InvalidDeviceError, ValueError) as e:
            logger.error(f"\n❌ - {e}\n")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="whisper-transcriber by Danilo Santitto. Transcribe audio files using Whisper models.")
    parser.add_argument("model", help="Choose the model to use for transcription. Available models: ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 'large-v3'].")
    parser.add_argument("input_file", nargs='+', help="List of input audio files to process.")
    parser.add_argument('-f', '--output-format', metavar='output_format', help="Output file format. Available format: 'timestamp', 'plain'. Default is both.", default=None)
    parser.add_argument('-t', '--timelist-files', nargs='+', metavar='timelist_files', help="Time list files name. Used to break transcription into time blocks. Use '.txt' file with format: line HH:MM:SS - Title for each column.", default=None)
    parser.add_argument('-l', '--language', metavar='language', help="Language code for transcription. Use ISO 639-1 codes (e.g., 'en' for English, 'it' for Italian).", default=None)
    parser.add_argument('-d', "--device", metavar='device', default="cuda" if torch.cuda.is_available() else "cpu", help="Device to use for PyTorch inference: cuda, mps, cpu")
    args = parser.parse_args()
    
    transcriber = Transcriber(args.model, args.output_format)
    transcriber.transcribe_files(args.input_file, args.timelist_files, args.device, args.language)

if __name__ == "__main__":
    main()

