# LHU Calendar Viewer

A Rich-based UI application for viewing LHU calendar schedules with Vietnamese localization.

## Setup

1. Install dependencies:
```bash
uv sync
```

## Usage

```bash
uv run -m src.main STUDENT_ID
```

With custom options:
```bash
uv run -m src.main 123456789 -t 2025-03-02 -r 6  # STUDENT_ID is required, -t for date, -r for range (default: 4)
```

Available options:
- `STUDENT_ID` (required): Your student ID
- `-r, --range`: Day range to query (default: 4)
- `-t, --time`: Query time in YYYY-MM-DD format (default: today)

## Build

For Linux, first install patchelf:
```bash
sudo apt install patchelf  # Ubuntu/Debian
```

Then build executable:
```bash
uv run build.py
```

Built single executable file (`calen`) will be in `dist/` folder.

## Using the Executable

Run the executable with your student ID:

```bash
# Basic usage
./dist/calen 123456789

# With custom options
./dist/calen 123456789 -t 2025-03-02 -r 6  # -t for date, -r for range (default: 4)
```

Available options:
- `STUDENT_ID` (required): Your student ID
- `-r, --range`: Day range to query (default: 4)
- `-t, --time`: Query time in YYYY-MM-DD format (default: today)
