import os
from typing import List

class InvalidTimeTitleFileError(Exception):
    """Raised when an invalid input file is provided."""
    pass

class InvalidInputFileError(Exception):
    """Raised when an invalid input file is provided."""
    pass

class InvalidOutputFileError(Exception):
    """Raised when an invalid output file is provided."""
    pass

class InvalidModelError(Exception):
    """Raised when an invalid model is provided."""
    pass

class InvalidDeviceError(Exception):
    """Raised when an invalid device is provided."""
    pass

class Validator:
    def __init__(self) -> None:
        self.available_models = ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 'large-v2']
        self.available_device = ['cuda', 'mps', 'cpu']

    def validate(self, input_files, output_file, model_name, timetitle_files, output_format, device, output_formatter):
        self._validate_input_files(input_files)
        self._validate_output_file(output_file)
        self._validate_model(model_name)
        self._validate_device(device)
        if timetitle_files:
            self._validate_timetitle_file(timetitle_files)
        output_formatter.validate_format(output_format)

    def _validate_input_files(self, input_files: List[str]) -> bool:
        for file in input_files:
            if not os.path.exists(file) or not file.lower().endswith(('.mp3', '.wav', '.m4a')):
                raise InvalidInputFileError(f"Invalid input file: {file}. Please provide a valid audio file.")
        return True

    def _validate_output_file(self, output_file) -> bool:
        if not output_file.lower().endswith('.txt'):
            raise InvalidOutputFileError("Invalid output file extension. Please provide a .txt file.")
        return True

    def _validate_timetitle_file(self, timetitle_files: List[str]) -> bool:
        for file in timetitle_files:
            if not os.path.exists(file) or not file.lower().endswith('.txt'):
                raise InvalidTimeTitleFileError(f"Invalid input file: {file}. Please provide a .txt file.")
        return True
    
    def _validate_model(self, model_name) -> bool:
        if model_name not in self.available_models:
            raise InvalidModelError(f"Invalid model: {model_name}. Available models: {', '.join(self.available_models)}.")
        return True
    
    def _validate_device(self, device) -> bool:
        if device not in self.available_device:
            raise InvalidDeviceError(f"Invalid device: {device}. Available device: {', '.join(self.available_device)}.")
        return True