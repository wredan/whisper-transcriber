import time

class OutputPrintFormat:
    def __init__(self) -> None:
        pass

    def print_output(self, result, output_file, input_file, model_name, format=None):
        if format is None or format == "timestamp":
            self._print_timestamp_format(result, output_file, input_file, model_name)
        if format is None or format == "plain":
            self._print_plain_format(result, output_file, input_file, model_name)
        elif format not in ["timestamp", "plain"]:
            raise ValueError(f"Invalid format: {format}. Supported formats: 'timestamp', 'plain'.")

    def _print_timestamp_format(self, result, output_file, input_file, model_name):
        self._write_output(
            result,
            output_file,
            input_file,
            model_name,
            "format timestamp",
            lambda segment: f"[{self._format_time(segment['start'])} -> {self._format_time(segment['end'])}] {segment['text']}\n"
        )

    def _print_plain_format(self, result, output_file, input_file, model_name):
        self._write_output(
            result,
            output_file,
            input_file,
            model_name,
            "format plain text",
            lambda segment: f"{segment['text']}\n"
        )

    def _write_output(self, result, output_file, input_file, model_name, format_label, format_function):
        with open(output_file, "a") as outfile:
            outfile.write(f"File: {input_file}, {model_name} model, {format_label}\n\n")
            for segment in result["segments"]:
                outfile.write(format_function(segment))
            outfile.write("\n\n")

    def _format_time(self, timestamp):
        return time.strftime('%H:%M:%S', time.gmtime(timestamp)) + f"{timestamp % 1:.1f}"[1:]
    
    def validate_format(self, output_format) -> bool:
        if output_format and output_format not in ["timestamp", "plain"]:
            raise ValueError(f"Invalid format: {output_format}. Supported formats: 'timestamp', 'plain'.")
        return True