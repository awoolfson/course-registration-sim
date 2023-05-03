import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../src')

import test_stability
import match
import data
from Student import Student
from CourseSection import CourseSection
from Schedule import Schedule

def generate_y(x, sections):
    total_rogues = 0
    for i in range(2):
        match.section_dict = dict(sections)
        match.student_dict = data.generate_students_weighted(sections, x)
        for key in match.student_dict:
            match.student_dict[key].find_conflicts(sections)
        match.Gale_Shapley()
        from match import student_dict
        from match import section_dict
        num_rogues = len(test_stability.is_pairwise_stable(student_dict=student_dict, section_dict=section_dict)[1])
        total_rogues += num_rogues
    return total_rogues / 2

def main():
    y_values = []
    x_values = [100, 200, 300, 400, 500] # 600, 700, 800, 900, 1000, ] #\
    #1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]

    sections = data.section_JSON_to_dict("../scraping/classes.json")
    
    for x in x_values:
        y_values.append(generate_y(x, sections))

    plt.xlabel("Number of Students")
    plt.ylabel("Average Number of Rogue Pairs")
    plt.plot(x_values, y_values)
    plt.show()

main()
        
        