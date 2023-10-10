import sys
from pprint import pprint

sys.path.append("src")

import data

from gs import gale_shapley_match
from test_stability import is_weakly_stable

sys.path.append("/..")

sections = data.section_csv_to_dict("CsCoursesSpring24.csv")
students = data.generate_students_weighted(sections, 60)
gale_shapley_match(students, sections)
for section in sections.values():
    print(section)
print(is_weakly_stable(students, sections))
