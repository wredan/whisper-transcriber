from typing import List

class InvalidInputFileError(Exception):
    """Raised when an invalid input file is provided."""
    pass

class InvalidOutputFileError(Exception):
    """Raised when an invalid output file is provided."""
    pass

class InvalidModelError(Exception):
    """Raised when an invalid model is provided."""
    pass

class TranscriberInt:
    """
    The Transcriber class handles the transcription of audio files using
    the Whisper ASR models. It validates input files, output file, and
    the chosen model, and then processes the transcription.
    """

    def __init__(self, model_name: str, output_file: str = "whisper_transcription.txt"):
        ...

    def _load_model(self) -> None:
        """Load the chosen Whisper ASR model."""
        ...

    def _validate_input_files(self, input_files: List[str]) -> bool:
        """Validate the provided input files."""
        ...

    def _validate_output_file(self) -> bool:
        """Validate the output file."""
        ...

    def _validate_model(self) -> bool:
        """Validate the chosen model."""
        ...

    def _save_transcription_to_txt(self, result, input_file) -> None:
        """Save the transcription result to the output file."""
        ...

    def _transcribe(self, input_file) -> None:
        """Transcribe the given input file using the chosen Whisper ASR model."""
        ...

    def transcribe_files(self, input_files) -> None:
        """Transcribe a list of input files using the chosen Whisper ASR model."""
        ...
