import argparse
from datetime import datetime
from src.ui.main_ui import MainUI
from dotenv import load_dotenv
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='LHU Calendar Viewer')
    parser.add_argument('-t', '--time', type=str, help='Query time in YYYY-MM-DD format (default: today)')
    parser.add_argument('-r', '--range', type=int, help='Day range to query (default: from environment variable)')

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
    ui.run(query_time=query_time, day_range=args.range)

if __name__ == "__main__":
    main()
