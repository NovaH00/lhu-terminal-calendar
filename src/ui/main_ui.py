from datetime import datetime
from rich.console import Console
from src.core.lhu_calen_api import LHUCalenAPI
from src.core import lhu_calen_api
from src.ui.calendar_display import CalendarDisplay

class MainUI:
    def __init__(self):
        self._console: Console = Console()
        self._calendar_display: CalendarDisplay = CalendarDisplay(self._console)
     
    def run(self, api: LHUCalenAPI, query_time: datetime, day_range: int):
        """Main UI function."""
        try:
            calen_items = api.get_data(day_range, query_time)
            
            if not calen_items:
                self._console.print(f"Không có lịch học trong {day_range} ngày tới", style="italic")
            else:
                # Display the schedule in a horizontal format
                self._calendar_display.display_schedule(calen_items, start_date=query_time)

        except lhu_calen_api.ConnectionError:
            self._console.print(f"[red]Không thể kết nối, hãy kiểm tra lại mạng[/red]")
        except lhu_calen_api.TimeoutError:
            self._console.print(f"[red]Kết nối hết thời gian chờ, hãy kiểm tra lại đường truyền mạng[/red]")
        except Exception as e:
            self._console.print(f"[red]Lỗi khi lấy hoặc hiển thị lịch: {str(e)}[/red]")
