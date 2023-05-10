import matplotlib.pyplot as plt
import sys
import copy

sys.path.append('../src')

import test_stability
import data
import GaleShapley

def generate_y(x, sections, trials):
    total_rogues = 0
    for i in range(trials):
        section_dict = copy.deepcopy(sections)
        student_dict = data.generate_students_weighted(sections, x)
        for key in student_dict:
            student_dict[key].find_conflicts(sections)
        student_dict, section_dict = GaleShapley.Gale_Shapley(student_dict, section_dict)
        num_rogues = len(test_stability.is_pairwise_stable(student_dict=student_dict, section_dict=section_dict)[1])
        total_rogues += num_rogues
    return total_rogues / trials

def main():
    y_values = []
    x_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, \
    1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
    #2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]

    sections = data.section_JSON_to_dict("../scraping/classes.json")
    # sections = data.section_csv_to_dict("../test_data/test_sections_2.csv")
    
    for x in x_values:
        y_values.append(generate_y(x, sections, 3))

    plt.xlabel("Number of Students")
    plt.ylabel("Average Rogue Pairs / Student Over 20 Trials")
    plt.plot(x_values, y_values)
    plt.show()

main()
        
        