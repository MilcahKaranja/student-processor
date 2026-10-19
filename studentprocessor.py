import csv
from abc import ABC, abstractmethod


# Task 6: Flexible method interface (method overloading equivalent)
def calculate_average(*marks):
    """Calculate an average from any number of subject marks."""
    if not marks:
        raise ValueError("At least one mark is required.")

    if any(not isinstance(mark, (int, float)) or isinstance(mark, bool)
           for mark in marks):
        raise TypeError("All marks must be numbers.")

    if any(mark < 0 or mark > 100 for mark in marks):
        raise ValueError("Marks must be between 0 and 100.")

    return sum(marks) / len(marks)


# Task 2: Abstract base class, encapsulation and abstraction
class Student(ABC):
    def __init__(self, student_id, first_name, last_name,
                 programme, marks):
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme

        if not marks:
            raise ValueError("A student must have at least one mark.")

        # Encapsulated subject marks
        self._marks = dict(marks)

        for subject, mark in self._marks.items():
            if not isinstance(mark, (int, float)) or isinstance(mark, bool):
                raise TypeError(f"{subject} mark must be numeric.")
            if not 0 <= mark <= 100:
                raise ValueError(f"{subject} mark must be between 0 and 100.")

    # Getter methods provide controlled access to student information
    @property
    def student_id(self):
        return self._student_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def programme(self):
        return self._programme

    @property
    def marks(self):
        # Return a copy so callers cannot modify the internal dictionary
        return self._marks.copy()

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    # Setter demonstrates controlled updating of marks
    def update_mark(self, subject, mark):
        if subject not in self._marks:
            raise ValueError(f"Unknown subject: {subject}")
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise TypeError("Mark must be numeric.")
        if not 0 <= mark <= 100:
            raise ValueError("Mark must be between 0 and 100.")

        self._marks[subject] = mark

    def average_score(self):
        return calculate_average(*self._marks.values())

    def get_grade(self):
        average = self.average_score()

        if average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        return "E"

    @abstractmethod
    def get_student_type(self):
        """Subclasses must provide their own student type."""
        pass


# Task 2: Inheritance and implementation of the abstract method
class AIUStudent(Student):
    def get_student_type(self):
        return "Regular AIU Student"

    # Shared method used to demonstrate polymorphism
    def performance_info(self):
        return (
            f"{self.full_name}: {self.get_student_type()}, "
            f"Average = {self.average_score():.2f}"
        )


# Task 4: Inheritance and method overriding
class ScholarshipStudent(AIUStudent):
    def __init__(self, student_id, first_name, last_name,
                 programme, marks, scholarship_amount=50000):
        super().__init__(
            student_id, first_name, last_name, programme, marks
        )

        if not isinstance(scholarship_amount, (int, float)):
            raise TypeError("Scholarship amount must be numeric.")
        if scholarship_amount < 0:
            raise ValueError("Scholarship amount cannot be negative.")

        self._scholarship_amount = scholarship_amount

    @property
    def scholarship_amount(self):
        return self._scholarship_amount

    def is_eligible(self):
        return self.average_score() >= 85

    # Override the parent method with scholarship-specific behaviour
    def performance_info(self):
        status = "Eligible" if self.is_eligible() else "Not eligible"

        return (
            f"{self.full_name}: {self.get_student_type()}, "
            f"Average = {self.average_score():.2f}, "
            f"Scholarship = KSh {self.scholarship_amount:,.2f}, "
            f"Eligibility = {status}"
        )

    # Override the inherited student type method
    def get_student_type(self):
        return "Scholarship Student"


# Task 3: Composition - analyzer works with student objects
class PerformanceAnalyzer:
    def __init__(self, students):
        self.students = list(students)

        if not self.students:
            raise ValueError("At least one student is required.")

    def highest_average(self):
        return max(self.students, key=lambda student: student.average_score())

    def lowest_average(self):
        return min(self.students, key=lambda student: student.average_score())

    def class_average(self):
        return calculate_average(
            *(student.average_score() for student in self.students)
        )


# Task 7: Report generation
def generate_report(students, analyzer):
    print("=" * 65)
    print("       STUDENT PERFORMANCE ANALYSIS REPORT")
    print("=" * 65)

    for student in students:
        print(f"\nStudent ID: {student.student_id}")
        print(f"Name: {student.full_name}")
        print(f"Programme: {student.programme}")
        print(f"Student Type: {student.get_student_type()}")

        print("Subject Marks:")
        for subject, mark in student.marks.items():
            print(f"  {subject}: {mark}")

        print(f"Average Score: {student.average_score():.2f}")
        print(f"Grade: {student.get_grade()}")

        if isinstance(student, ScholarshipStudent):
            print(
                f"Scholarship Amount: "
                f"KSh {student.scholarship_amount:,.2f}"
            )
            print(
                "Scholarship Eligibility: "
                f"{'Yes' if student.is_eligible() else 'No'}"
            )
        else:
            print("Scholarship Eligibility: Not assessed for this student type")

        print("-" * 65)

    highest = analyzer.highest_average()
    lowest = analyzer.lowest_average()

    print("\nCLASS PERFORMANCE SUMMARY")
    print("-" * 65)
    print(
        f"Highest Average: {highest.full_name} "
        f"({highest.average_score():.2f})"
    )
    print(
        f"Lowest Average: {lowest.full_name} "
        f"({lowest.average_score():.2f})"
    )
    print(f"Overall Class Average: {analyzer.class_average():.2f}")
    print(f"Total Students: {len(students)}")
    print("=" * 65)


# Read the CSV file and create student objects
def load_students(filename):
    students = []

    with open(filename, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "StudentID", "FName", "LName", "Programme",
            "Math", "English", "Science"
        }

        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV file is missing required columns.")

        for row in reader:
            marks = {
                "Math": float(row["Math"]),
                "English": float(row["English"]),
                "Science": float(row["Science"])
            }

            # Create scholarship objects for students averaging at least 85
            if calculate_average(*marks.values()) >= 85:
                student = ScholarshipStudent(
                    row["StudentID"],
                    row["FName"],
                    row["LName"],
                    row["Programme"],
                    marks,
                    scholarship_amount=50000
                )
            else:
                student = AIUStudent(
                    row["StudentID"],
                    row["FName"],
                    row["LName"],
                    row["Programme"],
                    marks
                )

            students.append(student)

    if not students:
        raise ValueError("The CSV file contains no student records.")

    return students


# Main program
if __name__ == "__main__":
    try:
        students = load_students("student.csv")

        # Task 5: Polymorphism
        print("POLYMORPHISM DEMONSTRATION")
        for student in students:
            print(student.performance_info())

        # Task 6: Demonstrate the flexible average function
        print("\nFLEXIBLE AVERAGE DEMONSTRATION")
        print("Three separate marks:", calculate_average(75, 80, 70))
        print("Variable number of marks:", calculate_average(75, 80, 70, 90))

        # Task 3 and Task 7
        analyzer = PerformanceAnalyzer(students)
        generate_report(students, analyzer)

    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
