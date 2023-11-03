import copy
import sys

import matplotlib.pyplot as plt

sys.path.append("../src")

import data_methods
import gs
import test_stability


def generate_y(x, sections, trials):
    total_rogues = 0
    for i in range(trials):
        section_dict = copy.deepcopy(sections)
        student_dict = data_methods.generate_students_weighted(sections, x)
        for key in student_dict:
            student_dict[key].find_conflicts(sections)
        student_dict, section_dict = gs.gale_shapley_match(
            student_dict, section_dict
        )
        num_rogues = len(
            test_stability.check_stability(
                student_dict=student_dict, section_dict=section_dict
            )["rogue_count"]
        )
        total_rogues += num_rogues
    return total_rogues / trials


def main():
    y_values = []
    x_values = [
        100,
        200,
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        1600,
        1700,
        1800,
        1900,
        2000,
        2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]

    sections = data_methods.section_JSON_to_dict("../scraping/classes.json")
    # sections = data.section_csv_to_dict("../test_data/test_sections_2.csv")
    
    trials = 1

    for x in x_values:
        y_values.append(generate_y(x, sections, trials))
        if x == 3000:
            print(y_values[-1])

    plt.xlabel("Number of Students")
    plt.ylabel(f"Average Rogue Pairs Over {trials} Trials")
    plt.plot(x_values, y_values)
    plt.show()

main()
