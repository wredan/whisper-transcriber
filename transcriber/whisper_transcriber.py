import argparse
import datetime
import logging
import os
import sys
import threading
import warnings
from typing import List
import whisper
import time
from halo import Halo
import coloredlogs
import torch
from transcriber.transcriber_interface import TranscriberInt
from transcriber.validators import InvalidDeviceError, Validator, InvalidTimeTitleFileError , InvalidInputFileError, InvalidOutputFileError, InvalidModelError
from transcriber.output_print_format import OutputPrintFormat

warnings.filterwarnings("ignore")

coloredlogs.install(level='INFO', fmt='%(message)s', level_styles={'info': {'color': 'green', 'bold': True}, 'error': {'color': 'red', 'bold': True}}, field_styles={'asctime': {'color': 'cyan'}, 'levelname': {'color': 'magenta', 'bold': True}})

logger = logging.getLogger(__name__)

class Transcriber(TranscriberInt):
        
    def __init__(self, model_name: str, output_format: str):
        self.model_name = model_name
        self.output_format = output_format
        self.model = None
        self.output_formatter = OutputPrintFormat()

    def _load_model(self, device):
        logger.info(f"🔄 Loading model: {self.model_name}")
        self.model = whisper.load_model(self.model_name, device=device)

    def _save_transcription_to_txt(self, result, input_file, timetitle_file):        
        try:
            output_filename = os.path.splitext(input_file)[0] + "_transcription.txt"
            self.output_formatter.print_output(result, output_filename, input_file, self.model_name, timetitle_file, format=self.output_format)
        except (ValueError) as e:
            logger.error(f"\n❌ {e}\n")
            sys.exit(1)
    
    def _update_spinner_text(self, spinner, input_file, start_time):
        while not self.spinner_stop:
            elapsed_time = datetime.timedelta(seconds=int(time.time() - start_time))
            spinner.text = f"({elapsed_time}) - Transcribing {input_file} with {self.model_name} model 🗣️ -> 📝"
            time.sleep(1)
    
    def _start_spinner_thread(self, spinner, input_file, start_time):
        self.spinner_stop = False
        spinner_thread = threading.Thread(target=self._update_spinner_text, args=(spinner, input_file, start_time))
        spinner_thread.start()
        return spinner_thread

    def _stop_spinner_thread(self, spinner, spinner_thread):
        self.spinner_stop = True
        spinner_thread.join()
        spinner.stop()

    def _transcribe(self, input_file, timetitle_file):
        start_time = time.time()
        spinner = Halo(text='', spinner="dots", interval=80)
        spinner.start()

        spinner_thread = self._start_spinner_thread(spinner, input_file, start_time)

        try:
            result = self.model.transcribe(input_file)
        except Exception as e:
            self._stop_spinner_thread(spinner, spinner_thread)
            logger.error(f"Error during transcription: {e}")
            sys.exit(0)
        except KeyboardInterrupt:
            logger.info(f"\n\nInterrupted by user. Stopping...")
            self._stop_spinner_thread(spinner, spinner_thread)
            sys.exit(0)

        self._stop_spinner_thread(spinner, spinner_thread)
        self._save_transcription_to_txt(result, input_file, timetitle_file)
        logger.info(f"✅ Transcription completed for {input_file} with {self.model_name} model")
        elapsed_time = time.time() - start_time
        logger.info(f"⏱️ Time elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}\n")

    def transcribe_files(self, input_files, timelist_files, device):
        try:
            Validator().validate(
                input_files, 
                self.model_name, 
                timelist_files, 
                self.output_format,
                device,
                self.output_formatter)
        except (InvalidInputFileError, InvalidOutputFileError, InvalidModelError, InvalidTimeTitleFileError, InvalidDeviceError, ValueError) as e:
            logger.error(f"\n❌ {e}\n")
            sys.exit(1)
        
        try:
            self._load_model(device)
        except (Exception) as e:
            logger.error(f"\n❌ {e}\n")
            sys.exit(1)

        for index, input_file in enumerate(input_files):
            timetitle_file = timelist_files[index] if timelist_files and index < len(timelist_files) else None
            self._transcribe(input_file, timetitle_file)

        logger.info("🎉 Transcription completed for all files")

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper models.")
    parser.add_argument("model", help="Choose the model to use for transcription. Available models: ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 'large-v2'].")
    parser.add_argument("input_file", nargs='+', help="List of input audio files to process.")
    parser.add_argument('-f', '--output-format', metavar='output_format', help="Output file format. Available format: 'timestamp', 'plain'. Default is both.", default=None)
    parser.add_argument('-t', '--timelist-files', nargs='+', metavar='timelist_files', help="Time list files name. Used for break transcription into timeblocks. Use .txt file with format: line HH:MM:SS - Title for each column.", default=None)
    parser.add_argument('-d', "--device", metavar='device', default="cuda" if torch.cuda.is_available() else "cpu", help="Device to use for PyTorch inference: cuda, mps, cpu")
    args = parser.parse_args()
    
    transcriber = Transcriber(args.model, args.output_format)
    transcriber.transcribe_files(args.input_file, args.timelist_files, args.device)

if __name__ == "__main__":
    main()

