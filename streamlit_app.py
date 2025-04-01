import streamlit as st
import numpy as np

class GradeCalculator:
    def __init__(self):
        self.weights = {
            'homeworks': 0.15,
            'quizzes': 0.15,
            'projects': 0.20,
            'exams': 0.50,
            'extra_credit': 0.07,
            'attendance': -0.05
        }
        self.assignment_counts = {
            'homeworks': 5,
            'quizzes': 4,
            'projects': 4,
            'exams': 2
        }
    
    def calculate_grade(self, grades):
        """Calculate the final grade based on provided category grades"""
        final_grade = 0
        breakdown = {}
        
        for category, grades_list in grades.items():
            if category == 'attendance':
                absences = grades_list
                penalty_per_absence = self.weights[category] / 5
                impact = absences * penalty_per_absence
                final_grade += impact
                breakdown[category] = {
                    'absences': absences,
                    'impact': impact
                }
            else:
                if grades_list and any(g is not None for g in grades_list):
                    valid_grades = [g for g in grades_list if g is not None]
                    if valid_grades:
                        avg = sum(valid_grades) / len(valid_grades)
                        weighted = avg * self.weights[category]
                        final_grade += weighted
                        breakdown[category] = {
                            'grades': grades_list,
                            'average': avg,
                            'weighted': weighted
                        }
        
        return final_grade, breakdown

def main():
    st.set_page_config(page_title="Grade Calculator", layout="wide")
    st.title("Grade Calculator")
    
    calc = GradeCalculator()
    
    # Initialize session state for grades
    if 'grades' not in st.session_state:
        st.session_state.grades = {
            'homeworks': [89.0, 83.0, 62.0, None, None],
            'quizzes': [40.0, 62.0, None, None],
            'projects': [120.0, 127.0, None, None],
            'exams': [None, None],
            'extra_credit': [0],
            'attendance': 0
        }
    
    # Create columns for different categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Grades")
        
        # Homeworks (0-130)
        st.write("### Homeworks (15%)")
        st.info("""
        💡 Base score is out of 100 points
        * Extra credit questions can boost score up to 130%
        * Example: Score of 115 means 100 regular + 15 extra credit points
        """)
        for i in range(calc.assignment_counts['homeworks']):
            grade = st.number_input(
                f"Homework {i+1}",
                min_value=0.0,
                max_value=130.0,
                value=st.session_state.grades['homeworks'][i] or 0.0,
                step=1.0,
                key=f'hw_{i}'
            )
            st.session_state.grades['homeworks'][i] = grade if grade > 0 else None
        
        # Quizzes (0-100)
        st.write("### Quizzes (15%)")
        st.write("Regular scoring: 0-100 points")
        for i in range(calc.assignment_counts['quizzes']):
            grade = st.number_input(
                f"Quiz {i+1}",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.grades['quizzes'][i] or 0.0,
                step=1.0,
                key=f'quiz_{i}'
            )
            st.session_state.grades['quizzes'][i] = grade if grade > 0 else None
    
    with col2:
        # Projects (0-130)
        st.write("### Projects (20%)")
        st.info("""
        💡 Base score is out of 100 points
        * Extra credit questions can boost score up to 130%
        * Example: Score of 120 means 100 regular + 20 extra credit points
        """)
        for i in range(calc.assignment_counts['projects']):
            grade = st.number_input(
                f"Project {i+1}",
                min_value=0.0,
                max_value=130.0,
                value=st.session_state.grades['projects'][i] or 0.0,
                step=1.0,
                key=f'proj_{i}'
            )
            st.session_state.grades['projects'][i] = grade if grade > 0 else None
        
        # Exams (0-100)
        st.write("### Exams (50%)")
        st.write("Regular scoring: 0-100 points")
        exam_names = ["Midterm", "Final"]
        for i in range(calc.assignment_counts['exams']):
            grade = st.number_input(
                f"{exam_names[i]} Exam",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.grades['exams'][i] or 0.0,
                step=1.0,
                key=f'exam_{i}'
            )
            st.session_state.grades['exams'][i] = grade if grade > 0 else None
        
        # Extra Credit Assignments (separate from homework/project bonus points)
        st.write("### Extra Credit Assignments (7%)")
        st.info("""
        💡 These are separate extra credit assignments
        * Different from bonus points in homework/projects
        * Worth 7% of your total grade
        * Enter your total score for all extra credit assignments
        """)
        ec = st.number_input(
            "Extra Credit Score",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.grades['extra_credit'][0]),
            step=1.0,
            key='ec'
        )
        st.session_state.grades['extra_credit'] = [float(ec)]
        
        # Attendance (0-5 absences)
        st.write("### Attendance (-5% max penalty)")
        absences = st.number_input(
            "Number of Absences",
            min_value=0,
            max_value=5,
            value=st.session_state.grades['attendance'],
            step=1,
            key='attendance'
        )
        st.session_state.grades['attendance'] = absences
    
    # Calculate and display results
    final_grade, breakdown = calc.calculate_grade(st.session_state.grades)
    
    # Display results in an expander
    with st.expander("View Grade Breakdown", expanded=True):
        st.write("## Grade Breakdown")
        
        # Create columns for the breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Display category breakdowns
            for category in ['homeworks', 'quizzes', 'projects']:
                if category in breakdown:
                    st.write(f"### {category.title()} ({calc.weights[category]*100}%)")
                    b = breakdown[category]
                    grades = b['grades']
                    
                    # Create a more detailed grade display
                    if category in ['homeworks', 'projects']:
                        for i, g in enumerate(grades):
                            if g is not None:
                                base_score = min(100, g)
                                extra_credit = max(0, g - 100)
                                st.write(f"{category[:-1].title()} {i+1}:")
                                st.write(f"* Regular: {base_score:.1f}/100")
                                if extra_credit > 0:
                                    st.write(f"* Extra Credit: +{extra_credit:.1f}")
                                st.write(f"* Total: {g:.1f}%")
                            else:
                                st.write(f"{category[:-1].title()} {i+1}: Not entered")
                    else:
                        st.write(f"Grades: {[f'{g:.1f}' if g is not None else 'Not entered' for g in grades]}")
                    
                    st.write(f"Average: {b['average']:.2f}%")
                    st.write(f"Weighted: {b['weighted']:.2f}%")
                    st.write(f"Completed: {sum(1 for g in grades if g is not None)}/{calc.assignment_counts[category]}")
                    st.write("---")
        
        with col2:
            # Display exam grades
            if 'exams' in breakdown:
                st.write(f"### Exams ({calc.weights['exams']*100}%)")
                b = breakdown['exams']
                st.write(f"Grades: {[f'{g:.1f}' if g is not None else 'Not entered' for g in b['grades']]}")
                st.write(f"Average: {b['average']:.2f}%")
                st.write(f"Weighted: {b['weighted']:.2f}%")
                st.write(f"Completed: {sum(1 for g in b['grades'] if g is not None)}/{calc.assignment_counts['exams']}")
                st.write("---")
            
            # Display extra credit
            if 'extra_credit' in breakdown:
                st.write(f"### Extra Credit Assignments (7%)")
                b = breakdown['extra_credit']
                st.write(f"Total Score: {b['grades'][0]:.1f}%")
                st.write(f"Contribution to Final Grade: {b['weighted']:.2f}%")
                st.write("(Separate from homework/project bonus points)")
                st.write("---")
            
            # Display attendance
            if 'attendance' in breakdown:
                st.write("### Attendance")
                b = breakdown['attendance']
                st.write(f"Absences: {b['absences']}/5")
                st.write(f"Impact: {b['impact']:.2f}%")
                st.write("---")
    
    # Display final grade with color
    st.markdown("---")
    st.markdown("## Final Grade")
    grade_color = 'red' if final_grade < 60 else 'orange' if final_grade < 70 else 'yellow' if final_grade < 80 else 'green'
    st.markdown(f"<h1 style='color: {grade_color}'>{final_grade:.2f}%</h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
