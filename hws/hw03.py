import sys

from share import check_path


def parse_log_line(line: str) -> dict | None:
    """
    parse a log line if it has the structure below, otherwise print an error
    :param line: <date> <time> <log_level> <log>
    :return: dict {'level': <level>, 'date': <date>, 'time': <time>, 'log': <rest of line>} or None
    """
    try:
        date, time, level, *log = line.split()
        return {
            'level': level,
            'date': date,
            'time': time,
            'log': ' '.join(log)
        }
    except Exception:
        print(f'Error: Log must have structure "<date> <time> <log_level> <log>: ({line})')
        return None


def load_logs(file_path: str) -> list:
    """
    load logs from a file and parse them line by line with parse_log_line, skipping invalid lines
    :param file_path: path/to/file
    :return: list(dict) from parse_log_line
    """
    res = list()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if parsed_line := parse_log_line(line):
                res.append(parsed_line)
    return res


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    find only logs of the given level
    :param logs: list(dict(log))
    :param level: log level, e.g. 'ERROR'
    :return: list of logs with this level
    """
    return list(filter(lambda x: x.get('level') == level, logs))


def count_logs_by_level(logs: list) -> dict:
    """
    count logs by level from list(dict(log))
    :param logs: list(dict(log))
    :return: dict(<level>: <count>)
    """
    res = dict()
    for log in logs:
        res[log['level']] = res.get(log['level'], 0) + 1
    return res


def display_log_counts(counts: dict) -> None:
    """
    display a table of log levels and their counts
    :param counts: dict(<level>: <count>)
    """
    print(f'{"Рівень логування":<17}| {"Кількість":<6}')
    print('-' * 17 + '|-' + '-' * 6)

    for level, num in counts.items():
        print(f'{level:<17}| {num:<6}')


def display_logs(levels: list, logs: dict) -> None:
    """
    show logs for each requested level, or a message if the level is not in logs
    :param levels: requested log levels (any case)
    :param logs: dict(<level>: list(dict(log)))
    """
    for level in levels:
        level_name = level.upper()
        if d_logs := logs.get(level_name):
            print(f'\n{level_name}:')
            print('\n'.join([f'{log["date"]} {log["time"]} - {log["log"]}' for log in d_logs]))
        else:
            print(f'\n{level_name}: Not in logs')


def main():
    """
    entry point: read the log path and optional levels from sys.argv
    """
    if len(sys.argv) < 2:
        raise Exception("path must be provided as argument")
    path, *args = sys.argv[1:]
    check_path(path)
    logs = load_logs(path)
    filtered_logs = dict()
    for level in set(log['level'] for log in logs):
        filtered_logs[level] = filter_logs_by_level(logs, level)

    log_counts = count_logs_by_level(logs)
    display_log_counts(log_counts)

    if args:
        display_logs(args, filtered_logs)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
