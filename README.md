# LHU Calendar Viewer

A Rich-based UI application for viewing LHU calendar schedules with Vietnamese localization.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create `.env` file with:
```env
API_URL=https://tapi.lhu.edu.vn/calen/auth/XemLich_LichSinhVien
STUDENT_ID=your_student_id
DAY_RANGE=7
```

## Usage

```bash
uv run -m src.main
```

With custom options:
```bash
uv run -m src.main -t 2025-03-02 -r 6  # -t for date, -r for range
```

## Build

For Linux, first install patchelf:
```bash
sudo apt install patchelf  # Ubuntu/Debian
```

Then build executable:
```bash
uv run build.py
```

Built executable (`calen`) will be in `dist/` folder.
