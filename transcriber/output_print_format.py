import time
class OutputPrintFormat:
    def __init__(self) -> None:
        pass

    def print_output(self, result, output_file, input_file, model_name, timetitle_list = None, format=None):
        self.create_file(output_file)
        if format is None or format == "timestamp":
            self._print_timestamp_format(result, output_file, input_file, model_name, timetitle_list)
        if format is None or format == "plain":
            self._print_plain_format(result, output_file, input_file, model_name, timetitle_list)
        elif format not in ["timestamp", "plain"]:
            raise ValueError(f"Invalid format: {format}. Supported formats: 'timestamp', 'plain'.")
        
    def create_file(self, output_file):
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write("")

    def _print_timestamp_format(self, result, output_file, input_file, model_name, timetitle_list):
        self._write_output(
            result,
            output_file,
            input_file,
            model_name,
            timetitle_list,
            "format timestamp",
            lambda segment: f"[{self._format_time(segment['start'])} -> {self._format_time(segment['end'])}] {segment['text']}\n"
        )

    def _print_plain_format(self, result, output_file, input_file, model_name, timetitle_list):
        self._write_output(
            result,
            output_file,
            input_file,
            model_name,
            timetitle_list,
            "format plain text",
            lambda segment: f"{segment['text']}\n"
        )

    def _write_output(self, result, output_file, input_file, model_name, timetitle_list, format_label, format_function):
        with open(output_file, "a", encoding="utf-8") as outfile:
            self._write_header(outfile, input_file, model_name, format_label)

            if timetitle_list:
                self._write_segments_with_titles(outfile, result, iter(timetitle_list), format_function)
            else:
                self._write_segments(outfile, result, format_function)

            outfile.write("\n\n")

    def _write_header(self, outfile, input_file, model_name, format_label):
        outfile.write(f"File: {input_file}, {model_name} model, {format_label}\n\n")

    def _write_segments_with_titles(self, outfile, result, timetitle_iter, format_function):
        timetitle = next(timetitle_iter, None)
        for segment in result["segments"]:
            timetitle = self._write_titles(outfile, segment, timetitle_iter, timetitle)
            outfile.write(format_function(segment))

    def _write_titles(self, outfile, segment, timetitle_iter, timetitle):
        while timetitle and segment['start'] >= timetitle.time:
            outfile.write(f"\n{timetitle.title}\n\n")
            timetitle = next(timetitle_iter, None)
        return timetitle

    def _write_segments(self, outfile, result, format_function):
        for segment in result["segments"]:
            outfile.write(format_function(segment))

    def _format_time(self, timestamp):
        return time.strftime('%H:%M:%S', time.gmtime(timestamp)) + f"{timestamp % 1:.1f}"[1:]
    
    def validate_format(self, output_format) -> bool:
        if output_format and output_format not in ["timestamp", "plain"]:
            raise ValueError(f"Invalid format: {output_format}. Supported formats: 'timestamp', 'plain'.")
        return True