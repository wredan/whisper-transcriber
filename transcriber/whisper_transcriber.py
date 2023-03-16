import argparse
import logging
import os
import sys
import warnings
from typing import List
import whisper
import time
from halo import Halo
import coloredlogs
from transcriber.transcriber_interface import TranscriberInt
from transcriber.validators import Validator, InvalidTimeTitleFileError , InvalidInputFileError, InvalidOutputFileError, InvalidModelError
from transcriber.output_print_format import OutputPrintFormat

warnings.filterwarnings("ignore")

coloredlogs.install(level='INFO', fmt='%(message)s', level_styles={'info': {'color': 'green', 'bold': True}, 'error': {'color': 'red', 'bold': True}}, field_styles={'asctime': {'color': 'cyan'}, 'levelname': {'color': 'magenta', 'bold': True}})

logger = logging.getLogger(__name__)

class Transcriber(TranscriberInt):
        
    def __init__(self, model_name: str, output_file: str, output_format: str, timetitle_list_file: str = None):
        self.model_name = model_name
        self.output_file = output_file
        self.output_format = output_format
        self.model = None
        self.timetitle_list_file = timetitle_list_file
        self.output_formatter = OutputPrintFormat(timetitle_list_file)

    def _load_model(self):
        logger.info(f"🔄 Loading model: {self.model_name}")
        self.model = whisper.load_model(self.model_name)

    def _save_transcription_to_txt(self, result, input_file):
        try:
            self.output_formatter.print_output(result, self.output_file, input_file, self.model_name, format=self.output_format)
        except (ValueError) as e:
            logger.error(f"\n❌ {e}\n")
            sys.exit(1)

    def _transcribe(self, input_file):
        start_time = time.time()
        spinner = Halo(text=f"Transcribing {input_file} with {self.model_name} model 🗣️ -> 📝", spinner="dots")
        spinner.start()

        try:
            result = self.model.transcribe(input_file)
        except Exception as e:
            spinner.stop()
            logger.error(f"Error during transcription: {e}")
            return

        elapsed_time = time.time() - start_time
        spinner.stop()
        self._save_transcription_to_txt(result, input_file)
        logger.info(f"✅ Transcription completed for {input_file} with {self.model_name} model")
        logger.info(f"⏱️ Time elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}\n")

    def transcribe_files(self, input_files):
        try:
            Validator().validate(
                input_files, 
                self.output_file, 
                self.model_name, 
                self.timetitle_list_file, 
                self.output_format, 
                self.output_formatter)
        except (InvalidInputFileError, InvalidOutputFileError, InvalidModelError, InvalidTimeTitleFileError, ValueError) as e:
            logger.error(f"\n❌ {e}\n")
            sys.exit(1)

        with open(self.output_file, "w") as outfile:
            outfile.write("")

        self._load_model()

        for input_file in input_files:
            self._transcribe(input_file)

        logger.info("🎉 Transcription completed for all files")

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper models.")
    parser.add_argument("model", help="Choose the model to use for transcription. Available models: ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 'large-v2'].")
    parser.add_argument("input_file", nargs='+', help="List of input audio files to process.")
    parser.add_argument('-o', '--output-filename', metavar='output_file', help="Output file name. Default is 'first_file_name_transcription.txt'")
    parser.add_argument('-f', '--output-format', metavar='output_format', help="Output file format. Available format: 'timestamp', 'plain'. Default is both.", default=None)
    parser.add_argument('-t', '--timelist-filename', metavar='timelist_filename', help="Time list file name. Used for break transcription into timeblocks.", default=None)
    
    args = parser.parse_args()
    output_filename = args.output_filename or os.path.splitext(args.input_file[0])[0] + "_transcription.txt"
    transcriber = Transcriber(args.model, output_filename, args.output_format, args.timelist_filename)
    transcriber.transcribe_files(args.input_file)

if __name__ == "__main__":
    main()

