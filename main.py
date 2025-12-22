import argparse
from datetime import datetime
from rich_argparse import RichHelpFormatter
from src.ui.main_ui import MainUI

def main():
    parser = argparse.ArgumentParser(
        description='LHU Calendar Viewer',
        formatter_class=RichHelpFormatter
    )
    parser.add_argument('student_id', type=str, help='Student ID')
    parser.add_argument('-r', '--range', type=int, default=4, help='Day range to query (default: 4)')
    parser.add_argument('-t', '--time', type=str, help='Query time in YYYY-MM-DD format (default: today)')

    args = parser.parse_args()

    # Parse the time argument if provided
    query_time = None
    if args.time:
        try:
            query_time = datetime.strptime(args.time, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    ui = MainUI()
    ui.run(student_id=args.student_id, query_time=query_time, day_range=args.range)

if __name__ == "__main__":
    main()
