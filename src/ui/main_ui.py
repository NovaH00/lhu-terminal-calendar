from datetime import datetime
from rich.console import Console
from src.core.lhu_calen_api import LHUCalenAPI, FailedToFetch
from src.ui.calendar_display import CalendarDisplay
from src.utils.env import get_env


class MainUI:
    def __init__(self):
        self.console: Console = Console()
        self.api: LHUCalenAPI = self.initialize_api()
        self.calendar_display: CalendarDisplay = CalendarDisplay(self.console)

    def initialize_api(self):
        """Initialize the LHU Calendar API with environment variables."""
        try:
            api_url = get_env("API_URL")
            student_id = get_env("STUDENT_ID")
            return LHUCalenAPI(api_url, student_id)
        except Exception as e:
            self.console.print(f"[red]Failed to initialize API: {str(e)}[/red]")
            raise

    def run(self, query_time: datetime | None = None, day_range: int | None = None):
        """Main UI function."""
        try:
            # Use provided day_range or fall back to environment variable
            if day_range is None:
                day_range = get_env("DAY_RANGE", int)

            # Use provided query_time or fall back to current time
            if query_time is None:
                query_time = datetime.now()

            calen_items = self.api.get_data(query_time, day_range=day_range)
            # calen_items = self.api.get_data(datetime(2026, 3, 6), day_range)
            if not calen_items:
                self.console.print(f"Không có lịch học trong {day_range} ngày tới")
            else:
                # Display the schedule in a horizontal format
                self.calendar_display.display_schedule(calen_items, start_date=query_time)

        except FailedToFetch as e:
            self.console.print(f"[red]Lấy dữ liệu lịch học thất bại: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Lỗi khi lấy hoặc hiển thị lịch: {str(e)}[/red]")
