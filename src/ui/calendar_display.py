from datetime import datetime, date, timedelta
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

    def display_schedule(self, calen_items: list[CalenItem], start_date: datetime | None = None, day_range: int = 4):
        """Display schedule in a horizontal table format with morning/afternoon separation."""
        if start_date is None:
            start_date = datetime.now()

        # Generate all dates in the range (not just ones with items)
        all_dates: list[date] = []
        for i in range(day_range):
            all_dates.append((start_date + timedelta(days=i)).date())

        # Group calendar items by date
        items_by_date: dict[date, list[CalenItem]] = {}
        for item in calen_items:
            date_key = item.start_time.date()
            if date_key not in items_by_date:
                items_by_date[date_key] = []
            items_by_date[date_key].append(item)

        # Calculate dynamic width based on number of columns
        num_columns = len(all_dates)
        if num_columns > 0:
            base_width = 100
            calculated_width = max(18, min(35, base_width // num_columns))
        else:
            calculated_width = 25

        # Create table
        table = Table(show_header=True, header_style="bold magenta")

        # Add headers for all dates
        for date_key in all_dates:
            date_obj = datetime.combine(date_key, datetime.min.time())

            vietnamese_days = {
                0: "Thứ Hai",
                1: "Thứ Ba",
                2: "Thứ Tư",
                3: "Thứ Năm",
                4: "Thứ Sáu",
                5: "Thứ Bảy",
                6: "Chủ Nhật"
            }

            day_name = vietnamese_days[date_obj.weekday()]
            formatted_date = format_date_with_countdown(date_obj)
            table.add_column(f"{day_name}\n{formatted_date}", justify="left", width=calculated_width)

        # Split items into morning (before 12:00) and afternoon (12:00 and after)
        def split_by_session(items: list[CalenItem]) -> tuple[list[CalenItem], list[CalenItem]]:
            morning = []
            afternoon = []
            for item in items:
                if item.start_time.hour < 12:
                    morning.append(item)
                else:
                    afternoon.append(item)
            return morning, afternoon

        # Build morning and afternoon data for each date
        morning_by_date: dict[date, list[CalenItem]] = {}
        afternoon_by_date: dict[date, list[CalenItem]] = {}
        for date_key in all_dates:
            items = items_by_date.get(date_key, [])
            morning, afternoon = split_by_session(items)
            morning_by_date[date_key] = morning
            afternoon_by_date[date_key] = afternoon

        # Calculate max rows for morning and afternoon separately
        max_morning = max(len(morning_by_date.get(d, [])) for d in all_dates) if all_dates else 0
        max_afternoon = max(len(afternoon_by_date.get(d, [])) for d in all_dates) if all_dates else 0

        def format_item(item: CalenItem) -> str:
            if item.is_cancelled:
                return (f"[dim strikethrough bold green]{item.subject_name}[/dim strikethrough bold green]\n"
                        f"[dim cyan]{item.start_time.strftime('%H:%M')}-{item.end_time.strftime('%H:%M')}[/dim cyan]\n"
                        f"[dim]{item.room_name} ({item.facility_name})[/dim]\n"
                        f"[red bold][HUỶ][/red bold]")
            else:
                return (f"[bold green]{item.subject_name}[/bold green]\n"
                        f"[cyan]{item.start_time.strftime('%H:%M')}-{item.end_time.strftime('%H:%M')}[/cyan]\n"
                        f"{item.room_name} ({item.facility_name})")

        # Morning rows
        for i in range(max_morning):
            row: list[str] = []
            for date_key in all_dates:
                if i < len(morning_by_date.get(date_key, [])):
                    row.append(format_item(morning_by_date[date_key][i]))
                else:
                    row.append(" ")
            table.add_row(*row)

        # Separator row between morning and afternoon
        if max_morning > 0 and max_afternoon > 0:
            separator = "─" * calculated_width
            table.add_row(*[separator] * num_columns)

        # Afternoon rows
        for i in range(max_afternoon):
            row: list[str] = []
            for date_key in all_dates:
                if i < len(afternoon_by_date.get(date_key, [])):
                    row.append(format_item(afternoon_by_date[date_key][i]))
                else:
                    row.append(" ")
            table.add_row(*row)

        self.console.print(table)
