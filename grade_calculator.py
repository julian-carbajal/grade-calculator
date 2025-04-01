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
                if grades_list:
                    avg = sum(grades_list) / len(grades_list)
                    weighted = avg * self.weights[category]
                    final_grade += weighted
                    breakdown[category] = {
                        'grades': grades_list,
                        'average': avg,
                        'weighted': weighted
                    }
        
        return final_grade, breakdown

    def calculate_needed_grades(self, current_grades, target_grade):
        """Calculate needed grades for remaining assignments to reach target"""
        current_grade, breakdown = self.calculate_grade(current_grades)
        
        # Calculate remaining weight percentages
        remaining_weights = {
            'homeworks': 0,
            'quizzes': 0,
            'projects': 0,
            'exams': 0
        }
        
        # Count remaining assignments
        for category in remaining_weights:
            if category in self.assignment_counts:
                remaining = self.assignment_counts[category] - len(current_grades[category])
                if remaining > 0:
                    remaining_weights[category] = self.weights[category] * remaining / self.assignment_counts[category]
        
        total_remaining_weight = sum(remaining_weights.values())
        if total_remaining_weight == 0:
            return None
        
        # Calculate needed average on remaining assignments
        points_needed = target_grade - current_grade
        needed_average = points_needed / total_remaining_weight * 100
        
        return {
            'current_grade': current_grade,
            'points_needed': points_needed,
            'needed_average': needed_average,
            'remaining_weights': remaining_weights
        }

def main():
    calc = GradeCalculator()
    
    # Your actual grades
    grades = {
        'homeworks': [89, 83, 62],  
        'quizzes': [40, 62],        
        'projects': [120, 127],      
        'exams': [],                
        'extra_credit': [100],      
        'attendance': 0             
    }
    
    while True:
        print("\n=== Grade Calculator Menu ===")
        print("1. Show current grade breakdown")
        print("2. Calculate needed grades for targets")
        print("3. Try hypothetical grades")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            final_grade, breakdown = calc.calculate_grade(grades)
            print("\nCurrent Grade Breakdown:")
            print("-" * 50)
            
            print("Homeworks (15%):")
            if 'homeworks' in breakdown:
                hw = breakdown['homeworks']
                print(f"  Grades: {hw['grades']}")
                print(f"  Average: {hw['average']:.2f}%")
                print(f"  Weighted: {hw['weighted']:.2f}%")
                print(f"  Completed: {len(hw['grades'])}/{calc.assignment_counts['homeworks']}")
            
            print("\nQuizzes (15%):")
            if 'quizzes' in breakdown:
                q = breakdown['quizzes']
                print(f"  Grades: {q['grades']}")
                print(f"  Average: {q['average']:.2f}%")
                print(f"  Weighted: {q['weighted']:.2f}%")
                print(f"  Completed: {len(q['grades'])}/{calc.assignment_counts['quizzes']}")
            
            print("\nProjects (20%):")
            if 'projects' in breakdown:
                p = breakdown['projects']
                print(f"  Grades: {p['grades']}")
                print(f"  Average: {p['average']:.2f}%")
                print(f"  Weighted: {p['weighted']:.2f}%")
                print(f"  Completed: {len(p['grades'])}/{calc.assignment_counts['projects']}")
            
            print("\nExams (50%):")
            if 'exams' in breakdown:
                e = breakdown['exams']
                print(f"  Grades: {e['grades']}")
                print(f"  Average: {e['average']:.2f}%")
                print(f"  Weighted: {e['weighted']:.2f}%")
                print(f"  Completed: {len(e['grades'])}/{calc.assignment_counts['exams']}")
            
            print("\nExtra Credit (7%):")
            if 'extra_credit' in breakdown:
                ec = breakdown['extra_credit']
                print(f"  Score: {ec['grades'][0]}%")
                print(f"  Weighted: {ec['weighted']:.2f}%")
            
            print("\nAttendance (-5%):")
            if 'attendance' in breakdown:
                att = breakdown['attendance']
                print(f"  Absences: {att['absences']}/5")
                print(f"  Impact: {att['impact']:.2f}% (0 = no penalty, -5 = max penalty)")
            
            print("\n" + "-" * 50)
            print(f"Current Grade: {final_grade:.2f}%")
            
        elif choice == '2':
            print("\nCalculating needed grades for different targets...")
            for target in [70, 80, 90]:
                needed = calc.calculate_needed_grades(grades, target)
                print(f"\nTo get a {target}%:")
                print(f"  Points needed: {needed['points_needed']:.2f}%")
                print(f"  Average needed on remaining work: {needed['needed_average']:.2f}%")
                print("\nRemaining work weight distribution:")
                for category, weight in needed['remaining_weights'].items():
                    if weight > 0:
                        remaining = calc.assignment_counts[category] - len(grades[category])
                        print(f"  {category.title()}: {weight*100:.1f}% ({remaining} remaining)")
                        
        elif choice == '3':
            print("\nEnter hypothetical grades (press Enter to skip):")
            print("Note: Homeworks and Projects can score up to 130%")
            
            # Create a copy of current grades
            new_grades = grades.copy()
            new_grades = {k: list(v) if isinstance(v, list) else v for k, v in grades.items()}
            
            # Remaining Homeworks (0-130)
            remaining_hw = calc.assignment_counts['homeworks'] - len(new_grades['homeworks'])
            for hw_num in range(len(new_grades['homeworks']) + 1, calc.assignment_counts['homeworks'] + 1):
                while True:
                    hw = input(f"Homework {hw_num} grade (0-130): ")
                    if not hw.strip():
                        break
                    try:
                        grade = float(hw)
                        if 0 <= grade <= 130:
                            new_grades['homeworks'].append(grade)
                            break
                        else:
                            print("Please enter a grade between 0 and 130")
                    except ValueError:
                        print("Please enter a valid number")
            
            # Quiz 3 & 4 (0-100)
            for quiz_num in range(len(new_grades['quizzes']) + 1, calc.assignment_counts['quizzes'] + 1):
                while True:
                    quiz = input(f"Quiz {quiz_num} grade (0-100): ")
                    if not quiz.strip():
                        break
                    try:
                        grade = float(quiz)
                        if 0 <= grade <= 100:
                            new_grades['quizzes'].append(grade)
                            break
                        else:
                            print("Please enter a grade between 0 and 100")
                    except ValueError:
                        print("Please enter a valid number")
            
            # Project 3 & 4 (0-130)
            for proj_num in range(len(new_grades['projects']) + 1, calc.assignment_counts['projects'] + 1):
                while True:
                    proj = input(f"Project {proj_num} grade (0-130): ")
                    if not proj.strip():
                        break
                    try:
                        grade = float(proj)
                        if 0 <= grade <= 130:
                            new_grades['projects'].append(grade)
                            break
                        else:
                            print("Please enter a grade between 0 and 130")
                    except ValueError:
                        print("Please enter a valid number")
            
            # Midterm & Final (0-100)
            exam_names = ["Midterm", "Final"]
            for exam_num in range(len(new_grades['exams']), calc.assignment_counts['exams']):
                while True:
                    exam = input(f"{exam_names[exam_num]} exam grade (0-100): ")
                    if not exam.strip():
                        break
                    try:
                        grade = float(exam)
                        if 0 <= grade <= 100:
                            new_grades['exams'].append(grade)
                            break
                        else:
                            print("Please enter a grade between 0 and 100")
                    except ValueError:
                        print("Please enter a valid number")
            
            # Extra Credit (0-100%)
            print("\nExtra Credit (7% of total grade):")
            while True:
                ec = input("Extra Credit score (0-100): ")
                if not ec.strip():
                    break
                try:
                    grade = float(ec)
                    if 0 <= grade <= 100:
                        new_grades['extra_credit'] = [grade]  
                        break
                    else:
                        print("Please enter a grade between 0 and 100")
                except ValueError:
                    print("Please enter a valid number")
            
            # Calculate new grade
            new_final_grade, new_breakdown = calc.calculate_grade(new_grades)
            print("\nHypothetical Grade Breakdown:")
            print("-" * 50)
            
            # Show detailed breakdown
            print("Homeworks (15%):")
            if 'homeworks' in new_breakdown:
                hw = new_breakdown['homeworks']
                print(f"  Grades: {hw['grades']}")
                print(f"  Average: {hw['average']:.2f}%")
                print(f"  Weighted: {hw['weighted']:.2f}%")
                print(f"  Completed: {len(hw['grades'])}/{calc.assignment_counts['homeworks']}")
            
            print("\nQuizzes (15%):")
            if 'quizzes' in new_breakdown:
                q = new_breakdown['quizzes']
                print(f"  Grades: {q['grades']}")
                print(f"  Average: {q['average']:.2f}%")
                print(f"  Weighted: {q['weighted']:.2f}%")
                print(f"  Completed: {len(q['grades'])}/{calc.assignment_counts['quizzes']}")
            
            print("\nProjects (20%):")
            if 'projects' in new_breakdown:
                p = new_breakdown['projects']
                print(f"  Grades: {p['grades']}")
                print(f"  Average: {p['average']:.2f}%")
                print(f"  Weighted: {p['weighted']:.2f}%")
                print(f"  Completed: {len(p['grades'])}/{calc.assignment_counts['projects']}")
            
            print("\nExams (50%):")
            if 'exams' in new_breakdown:
                e = new_breakdown['exams']
                print(f"  Grades: {e['grades']}")
                print(f"  Average: {e['average']:.2f}%")
                print(f"  Weighted: {e['weighted']:.2f}%")
                print(f"  Completed: {len(e['grades'])}/{calc.assignment_counts['exams']}")
            
            print("\nExtra Credit (7%):")
            if 'extra_credit' in new_breakdown:
                ec = new_breakdown['extra_credit']
                print(f"  Score: {ec['grades'][0]}%")
                print(f"  Weighted: {ec['weighted']:.2f}%")
            
            print("\nAttendance (-5%):")
            if 'attendance' in new_breakdown:
                att = new_breakdown['attendance']
                print(f"  Absences: {att['absences']}/5")
                print(f"  Impact: {att['impact']:.2f}% (0 = no penalty, -5 = max penalty)")
            
            print("\n" + "-" * 50)
            print(f"Current grade: {calc.calculate_grade(grades)[0]:.2f}%")
            print(f"Hypothetical grade: {new_final_grade:.2f}%")
            print(f"Difference: {new_final_grade - calc.calculate_grade(grades)[0]:+.2f}%")
            
        elif choice == '4':
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
