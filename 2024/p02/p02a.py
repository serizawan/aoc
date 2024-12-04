def is_safe(report):
    if sorted(report) != report and sorted(report, reverse=True) != report:
        return False

    for i in range(len(report) - 1):
        if not(0 < abs(report[i] - report[i + 1]) <= 3):
            return False
    return True

if __name__ == "__main__":
    reports = open(0).read().splitlines()
    reports = [[int(level) for level in report.split(" ")] for report in reports]

    safe_reports_count = 0
    for report in reports:
        safe_reports_count += 1 if is_safe(report) else 0

    print(safe_reports_count)