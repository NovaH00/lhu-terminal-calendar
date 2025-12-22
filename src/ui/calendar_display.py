from datetime import datetime, date
from rich.console import Console
from rich.table import Table
from src.core.lhu_calen_api import CalenItem


def format_date_with_countdown(date_obj: datetime) -> str:
    """Format date as '<date> (<how long till that date>)' in Vietnamese."""
    today = datetime.now().date()
    target_date = date_obj.date()

    # Calculate the difference in days
    days_diff = (target_date - today).days

    # Format the date as DD/MM
    formatted_date = date_obj.strftime('%d/%m')

    # Vietnamese translation for days
    if days_diff == 0:
        countdown_text = "Hôm nay"
    elif days_diff == 1:
        countdown_text = "Ngày mai"
    elif days_diff == -1:
        countdown_text = "Hôm qua"
    elif days_diff > 1:
        countdown_text = f"{days_diff} ngày nữa"
    else:  # days_diff < -1
        countdown_text = f"{abs(days_diff)} ngày trước"

    return f"{formatted_date} ({countdown_text})"


class CalendarDisplay:
    def __init__(self, console: Console):
        self.console: Console = console

    def display_schedule(self, calen_items: list[CalenItem], start_date: datetime | None = None):
        """Display schedule in a horizontal table format showing only days with schedules."""
        if start_date is None:
            start_date = datetime.now()

        # Group calendar items by date
        items_by_date: dict[date, list[CalenItem]] = {}
        for item in calen_items:
            date_key = item.start_time.date()
            if date_key not in items_by_date:
                items_by_date[date_key] = []
            items_by_date[date_key].append(item)

        # Get only dates that have items
        dates_with_items = sorted([
            date 
            for date, items in items_by_date.items() 
            if items
        ])

        if not dates_with_items:
            # This message shouldn't appear since main_ui handles it with Vietnamese text
            # But if it does, we'll keep it in English as a fallback
            day_range = 7  # Default fallback, though this would be handled by main_ui
            self.console.print(f"No scheduled events in the next {day_range} days")
            return
        
        # Calculate dynamic width based on number of columns
        num_columns = len(dates_with_items)
        if num_columns > 0:
            # Calculate width: start with a base width and adjust based on number of columns
            # More columns = smaller width, fewer columns = larger width
            base_width = 100  # Maximum reasonable width when there's only 1 column
            calculated_width = max(18, min(35, base_width // num_columns))  # Keep width between 18 and 35
        else:
            calculated_width = 25  # Default if no columns

        # Create a table with one column for each day that has items
        table = Table(show_header=True, header_style="bold magenta")

        # Add headers for each date that has items
        for date_key in dates_with_items:
            date_obj = datetime.combine(date_key, datetime.min.time())

            # Mapping English day names to Vietnamese
            vietnamese_days = {
                0: "Thứ Hai",  # Monday
                1: "Thứ Ba",   # Tuesday
                2: "Thứ Tư",   # Wednesday
                3: "Thứ Năm",  # Thursday
                4: "Thứ Sáu",  # Friday
                5: "Thứ Bảy",  # Saturday
                6: "Chủ Nhật"   # Sunday
            }

            day_name = vietnamese_days[date_obj.weekday()]
            formatted_date = format_date_with_countdown(date_obj)
            table.add_column(f"{day_name}\n{formatted_date}", justify="left", width=calculated_width)
        
        # Determine the maximum number of events across all days
        max_events = max(len(items_by_date[date]) for date in dates_with_items)
        
        # Add rows for each event slot
        for i in range(max_events):
            row: list[str] = []
            for date_key in dates_with_items:
                if i < len(items_by_date[date_key]):
                    item = items_by_date[date_key][i]

                    event_info = (f"[bold green]{item.subject_name}[/bold green]\n"
                                  f"[cyan]{item.start_time.strftime('%H:%M')}-{item.end_time.strftime('%H:%M')}[/cyan]\n"
                                  f"{item.room_name} ({item.facility_name})")
                    row.append(event_info)
                else:
                    row.append(" ")  # Empty cell if no event at this position
            table.add_row(*row)
        
        self.console.print(table)
