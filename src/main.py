import argparse
import re
from datetime import datetime
from rich_argparse import RichHelpFormatter
from src.ui.main_ui import MainUI
from src.core.lhu_calen_api import LHUCalenAPI
from src.core.cache import CacheManager
from src.core.configurations import APIConfigs, CacheConfigs


def validate_student_id(value: str) -> str:
    """Validate that the student ID follows the format: 1<year><count> (e.g., 124000095)"""
    if not re.match(r'^1\d{8}$', value):
        raise argparse.ArgumentTypeError(
            f"Invalid student ID."
        )
    return value

def main():
    parser = argparse.ArgumentParser(description='LHU Calendar Viewer', formatter_class=RichHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', required=True)

    # --- Subcommand 1: View (The main calendar functionality) ---
    view_parser = subparsers.add_parser('view', help='View calendar', formatter_class=RichHelpFormatter)
    view_parser.add_argument('student_id', type=validate_student_id, help='Student ID')
    view_parser.add_argument('-r', '--range', type=int, default=APIConfigs.DEFAULT_DAY_RANGE)
    view_parser.add_argument('-t', '--time', type=str)

    # --- Subcommand 2: Cache ---
    cache_parser = subparsers.add_parser('cache', help='Cache management', formatter_class=RichHelpFormatter)
    cache_parser.add_argument('action', choices=['dir', 'clean'])

    args = parser.parse_args()
    
    cache_manager = CacheManager(
        app_name=CacheConfigs.APP_NAME,
        ttl_hours=CacheConfigs.TTL_HOURS
    )

    if args.command == 'cache':
        if args.action == "dir":
            print(cache_manager.cache_dir)     
        else:
            print("TODO: Implement cache clean")
        return 
    # Parse the time argument if provided
    day_range = args.range
    query_time = None
    if args.time:
        try:
            query_time = datetime.strptime(args.time, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    api = LHUCalenAPI(
        api_url=APIConfigs.LHU_API_URL,
        student_id=args.student_id,
        cache_manager=cache_manager
    )
    ui = MainUI()
    ui.run(api, query_time=query_time, day_range=day_range)

if __name__ == "__main__":
    main()
