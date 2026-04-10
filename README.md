# TOC Student Attendance System v1.0

A Theory of Computation-based student attendance management system that combines formal language theory with practical attendance tracking.

## Overview

This project demonstrates how **Deterministic Finite Automaton (DFA)** from Theory of Computation can solve real-world problems. It validates student registration numbers using a formal state machine approach and provides a complete attendance management solution.

## Features

✅ **DFA-Based Validation** — Validates registration format: `24B[A-Z][A-Z][0-4]`
✅ **Student Management** — Add, delete, and manage students efficiently
✅ **Real-time Attendance** — Mark attendance with timer-based functionality (Present/Absent/Excuse)
✅ **Data Persistence** — CSV-based storage for students and attendance records
✅ **Excel Export** — Generate formatted Excel reports with styling
✅ **Modern GUI** — Tkinter-based interface with dark theme (3 tabs)

## Project Structure

```
toc/
├── toc_engine.py          # DFA validator & StudentDatabase class
├── att_gui.py             # Tkinter GUI with 3 tabs
├── QUICK_START.txt        # Quick reference guide
├── SYSTEM_README.txt      # Full system documentation
└── student_data/          # CSV storage folder
    ├── students.csv
    └── attendance.csv
```

## Registration Format

**Valid Format:** `24B[A-Z][A-Z][0-4]`

| Component | Description | Example |
|-----------|-------------|---------|
| `24` | Fixed year prefix | 24 |
| `B` | Fixed branch (Backend) | B |
| `[A-Z]` | First letter (uppercase) | A |
| `[A-Z]` | Second letter (uppercase) | A |
| `[0-4]` | Single digit (0-4 only) | 0 |

**Valid Examples:** 24BAA0, 24BCS2, 24BXY4
**Invalid Examples:** 24baa0, 24BAA5, 24AA0, 23BAA0

## Theory of Computation: DFA Implementation

### State Machine

```
Input: 24B[A-Z][A-Z][0-4]

q0 --'2'--> q1 --'4'--> q2 --'B'--> q3 --[A-Z]--> q4 --[A-Z]--> q5 --[0-4]--> q6 ✓ (Accept)
```

### Key Concepts

- **DFA (Deterministic Finite Automaton)** — Formal language recognizer with deterministic behavior
- **Regular Language** — Pattern matching using regular expressions equivalent to DFA
- **State Transitions** — Fixed transitions for each input symbol
- **Acceptance Condition** — Reaches final state q6 only if all transitions succeed

## How It Works

### Tab 1: Add Student
1. Enter registration number (DFA validates automatically)
2. Enter student name
3. Click "✅ Add Student"
4. System checks for duplicates and adds to CSV

### Tab 2: Mark Attendance
1. Set timer duration (default: 900 seconds = 15 minutes)
2. Enter student registration number
3. Click "▶️ Start" to begin countdown
4. Mark: **PRESENT** / **EXCUSE** / **ABSENT**
5. Auto-marks ABSENT when timer expires

### Tab 3: Export Data
1. Click "📥 Export to Excel"
2. Choose file location
3. Generates formatted Excel file with:
   - **Students sheet** — All registered students
   - **Attendance sheet** — All attendance records
   - **Statistics** — Today's attendance breakdown

## Installation

### Prerequisites
- Python 3.8+
- Required packages: `openpyxl` (for Excel export)

### Setup
```bash
# Clone the repository
git clone https://github.com/devarakondavenkata2024-sketch/student_Toc.git
cd student_Toc

# Install dependencies
pip install openpyxl

# Run the application
python att_gui.py
```

## Usage

### Running the Application
```bash
python att_gui.py
```

### Example Workflow

**1. Add Students:**
- Register: 24BAA0, Name: John Doe
- Register: 24BCS2, Name: Jane Smith

**2. Mark Attendance:**
- Set timer to 900 seconds
- Enter: 24BAA0
- Click: ▶️ Start
- Click: ✅ PRESENT

**3. Export Records:**
- Click: 📥 Export to Excel
- Save as: `attendance_report.xlsx`

## File Descriptions

### toc_engine.py
- **DFA Class** — Implements state machine validation
- **StudentDatabase Class** — Manages CSV operations and Excel export

### att_gui.py
- **Tkinter GUI** — 3-tab interface
- **Event handlers** — User interactions
- **Dark theme styling** — Modern appearance

## Data Storage

### students.csv
```
RegNo,Name,Date
24BAA0,John Doe,2026-04-10 10:30
24BCS2,Jane Smith,2026-04-10 10:45
```

### attendance.csv
```
Date,RegNo,Name,Status,Time
2026-04-10,24BAA0,John Doe,PRESENT,10:35:22
2026-04-10,24BCS2,Jane Smith,ABSENT,10:50:15
```

## Architecture

### Two-File Design

**Separation of Concerns:**
- `toc_engine.py` — Pure TOC logic (no GUI dependencies)
- `att_gui.py` — User interface layer

**Benefits:**
- Scalability — Easy to add web interface later
- Testability — DFA and database can be tested independently
- Maintainability — Clean code organization

## Technical Highlights

✓ **DFA Validation** — O(n) time complexity for string validation
✓ **Deterministic Behavior** — Same input always produces same output
✓ **No Ambiguity** — Formal language theory ensures correctness
✓ **CSV Persistence** — Lightweight, human-readable storage
✓ **Excel Formatting** — Professional report generation
✓ **Error Handling** — Graceful failure messages

## Future Enhancements

- [ ] Web interface (Flask/Django)
- [ ] Database backend (SQLite/MySQL)
- [ ] QR code scanning
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Multi-branch support
- [ ] Authentication system

## Educational Value

This project demonstrates:
- Practical application of Theory of Computation
- Software architecture principles (separation of concerns)
- Data persistence (CSV operations)
- GUI development (Tkinter)
- File handling and CSV management
- Excel report generation
- Clean code practices

## License

MIT License — Feel free to use for educational purposes

## Author

**Sathvik** — TOC Student Attendance System v1.0

## Contact & Contributions

For questions, suggestions, or contributions, feel free to reach out!

---

**"Applying Theory to Practice"** 🎓➕📚
