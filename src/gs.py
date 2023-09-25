import random

import data
from section import CourseSection
from student import Student

seed = random.randrange(0, 1000)

def gale_shapley_match(student_dict: dict, 
                 section_dict: dict, 
                 shuffle: bool = False,
                 seed: int = seed) -> (dict, dict):

    # initialize and populate free students list
    free_students = []
    for id in student_dict:
        free_students.append(id)
        
    if shuffle:
        random.seed(seed)
        random.shuffle(free_students)

    # look at last student in free list
    while len(free_students) > 0:
        to_pop = True  # this determines if a student has been swapped out or a pop on the free student list is not needed
        cur_student = student_dict[free_students[-1]]

        # while student has more sections to propose to
        while cur_student.can_propose():

            # try enrolling student in favorite section
            proposed_section = section_dict[cur_student.get_top_section_id()]
            cur_student.add_proposal(proposed_section.id)

            if not proposed_section.is_full():
                add_student_to_section(cur_student, proposed_section)
            else:
                if (
                    proposed_section.score_student(cur_student)
                    > proposed_section.get_lowest_student().section_score
                ):
                    removed_student = proposed_section.pop_lowest_student()
                    to_pop = False
                    add_student_to_section(cur_student, proposed_section)

            # update dictionaries with returned student and section objects
            student_dict[cur_student.id] = cur_student
            section_dict[proposed_section.id] = proposed_section

            # if a student in the section has been replaced
            if to_pop == False:
                removed_student.leave_section(proposed_section)
                free_students.append(removed_student.id)
                break

        if to_pop:
            free_students.pop()

    return (student_dict, section_dict)


def add_student_to_section(
    student: Student, section: CourseSection
) -> (Student, CourseSection):
    student.join_section(section)
    section.enroll(student)


def main():
    if __name__ == "__main__":
        
        student_dict, section_dict = data.all_from_csv(
            "../test_data/test_students_2.csv", "../test_data/test_sections_2_rogue.csv"
        )

        student_dict, section_dict = gale_shapley_match(student_dict, section_dict)

main()
