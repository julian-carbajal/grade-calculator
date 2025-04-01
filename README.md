# Grade Calculator

A Streamlit-based web application for calculating and tracking academic grades with support for extra credit and attendance.

## Features

- Calculate weighted grades across multiple categories:
  - Homeworks (15%)
  - Quizzes (15%)
  - Projects (20%)
  - Exams (50%)
  - Extra Credit Assignments (7%)
  - Attendance (-5% max penalty)

- Support for extra credit:
  - Homework and project assignments can earn up to 130% through bonus questions
  - Separate extra credit assignments worth 7% of total grade

- Real-time grade updates and detailed breakdowns
- Track completion status for all assignments
- Visual grade presentation with color-coded final grade

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/grade-calculator.git
cd grade-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser. You can then:
1. Enter grades for completed assignments
2. View your current grade and detailed breakdown
3. Track your progress in each category

## File Structure

- `streamlit_app.py`: Main Streamlit web application
- `grade_calculator.py`: Core grade calculation logic
- `requirements.txt`: Python dependencies
