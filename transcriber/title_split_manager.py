import datetime

class TimeTitleList:
    def __init__(self, time, title) -> None:
        self.time = time
        self.title = title

class TitleSplitManager:
    def __init__(self) -> None:
        pass

    def get_title_time_list_from_file(self, filename: str):
        with open(filename, 'r') as file:
            title_time_list = [self._parse_line(line.strip()) for line in file]
        return title_time_list

    def _time_str_to_seconds(self, time_str):
        dt = datetime.datetime.strptime(time_str, '%H:%M:%S')
        delta = dt - datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        return delta.total_seconds()

    def _parse_line(self, line):
        time_str, _ = line.strip().split(' - ', 1)
        time_seconds = self._time_str_to_seconds(time_str)
        return TimeTitleList(time_seconds, line)


