TOC STUDENT ATTENDANCE SYSTEM v1.0

================================================================================
TWO FILE ARCHITECTURE
================================================================================

1. toc_engine.py
   - Pure Theory of Computation implementation
   - DFA: Deterministic Finite Automaton for registration validation
   - Format: 24B[A-Z][A-Z][0-4]
   - States: q0 → q1 → q2 → q3 → q4 → q5 → q6 (accept)
   - StudentDatabase: Handles CSV storage and Excel export
   - No GUI dependencies

2. att_gui.py
   - Tkinter GUI with 3 tabs
   - Modern dark theme styling
   - Imports DFA and StudentDatabase from toc_engine


================================================================================
REGISTRATION FORMAT (DFA VALIDATION)
================================================================================

Format: 23B[A-Z][A-Z][0-4]
Example: 23BAA0, 23BCS2, 23BZZ4, 23BXY1

Components:
- "23"     : Fixed year prefix
- "B"      : Fixed branch (Backend only)
- [A-Z]    : First letter (uppercase A-Z)
- [A-Z]    : Second letter (uppercase A-Z)
- [0-4]    : Single digit (0, 1, 2, 3, or 4)

Total: 6 characters

INVALID Formats:
- 24BAA0   (year must be 23)
- 23BAA5   (last digit must be 0-4)
- 23baa0   (letters must be uppercase)
- 23MA100  (branch must be B, not M)


================================================================================
FEATURES & WORKFLOW
================================================================================

TAB 1: ➕ ADD STUDENT
  • Enter registration number (DFA validates format automatically)
  • Enter student name
  • Click "✅ Add Student"
  • Duplicate check prevents re-registration
  • Real-time student list display

TAB 2: ⏱️ MARK ATTENDANCE
  • Set timer duration (default 900 seconds = 15 minutes)
  • Enter student registration number
  • Click "▶️ Start" to begin countdown
  • Two options:
    - "✅ PRESENT" : Mark student present (within timer)
    - "🆓 EXCUSE"  : Mark student excused
    - "❌ ABSENT"  : Mark student absent
  • When timer completes:
    - Auto-marks as ABSENT if not marked yet
    - Shows notification
    - Clears timer
  • "⏹️ Stop" to pause timer
  • Real-time attendance records show today's entries

TAB 3: 📊 EXPORT DATA
  • Click "📥 Export to Excel" to save all data
  • Creates formatted Excel file with:
    - Students sheet (all registered students)
    - Attendance sheet (all attendance records)
  • Statistics tab shows:
    - Total students count
    - Total attendance records
    - Today's breakdown (Present/Absent/Excuse)


================================================================================
DFA STATE TRANSITIONS
================================================================================

Input: 23B[A-Z][A-Z][0-4]

q0 --'2'--> q1 --'3'--> q2 --'B'--> q3 --[A-Z]--> q4 --[A-Z]--> q5 --[0-4]--> q6 (Accept)

If any character doesn't match expected symbol → Return False


================================================================================
DATA STORAGE
================================================================================

Folder: student_data/

Files:
  students.csv
    - Headers: RegNo, Name, Date
    - Stores all registered students

  attendance.csv
    - Headers: Date, RegNo, Name, Status, Time
    - Stores all attendance records
    - Status values: PRESENT, ABSENT, EXCUSE


================================================================================
RUNNING THE APPLICATION
================================================================================

python att_gui.py


================================================================================
TESTED VALID REGISTRATIONS
================================================================================

24BAA0  ✅  (A, A, 0)
24BCS2  ✅  (C, S, 2)
24BZZ4  ✅  (Z, Z, 4)
24BXY1  ✅  (X, Y, 1)


================================================================================
INVALID REGISTRATIONS (Will be rejected)
================================================================================

22BAA0  ❌  (Year not 24)
24baa0  ❌  (Lowercase letters)
24BA00  ❌  (Two zeros at end)
24BAA5  ❌  (Last digit > 4)
24B1234 ❌  (No letters)
24BAA   ❌  (Missing last digit)


================================================================================
KEY FEATURES
================================================================================

✓ DFA-based format validation
✓ Timer-based attendance marking
✓ Auto-absent on timer expiry
✓ CSV data persistence
✓ Excel export with formatting
✓ Modern dark UI with emojis
✓ Real-time data display
✓ No comments in code (clean)
✓ Two-file architecture (TOC + GUI)
✓ Student duplicate prevention
