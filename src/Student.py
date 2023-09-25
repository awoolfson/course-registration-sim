import random
from typing import Optional

class Student:
    def __init__(self, id: int, name: str, base_score: int, major: str):
        self.id = id  # 8 digit ID
        self.major = major
        self.section_limit = 4
        self.base_score = base_score + random.randrange(
            0, 100
        )  # this exists to eliminate ties
        self.name = name
        self.section_ranking = []
        self.enrolled_in = []
        self.sections_enrolled = 0
        self.section_score = None  # compare students within a section, should not be saved to a database ever
        self.next_section_index = 0

        self.conflicts_dict = (
            {}
        )  # entries take the form {section_id: [conflict_index, conflict_index, ...]}

        self.proposed_dict = {}  # entries take the form {section_id: True/False}

    def __str__(self):
        string = (
            f"{self.name}:\nid: {self.id}\nbase_score: {self.base_score}\n"
            f"section ranking: {self.section_ranking}\nschedule: {self.enrolled_in}\nsections enrolled: {self.sections_enrolled}\n"
        )
        return string

    # for sorting students by section score
    def __lt__(self, other_student):
        return self.section_score < other_student.section_score

    def __eq__(self, other_student):
        return self.section_score == other_student.section_score

    def __gt__(self, other_student):
        return self.section_score > other_student.section_score

    # sets section ranking for the student, also populates conflicts_dict and proposed_dict
    def set_section_ranking(self, ranking: list):
        for i, section_id in enumerate(ranking):
            ranking[i] = int(section_id)
        self.section_ranking = ranking
        for id in self.section_ranking:
            self.conflicts_dict[id] = []
            self.proposed_dict[id] = False

    def can_propose(self) -> bool:
        if self.get_top_section_id() == None:
            return False
        elif self.sections_enrolled >= self.section_limit:
            return False
        return True

    # join and leave section are to be used in conjunction with try_enrolling and try_enrolling_next_section
    def join_section(self, section):
        self.sections_enrolled += 1
        self.enrolled_in.append(section.id)

    def leave_section(self, section):
        if section.id in self.enrolled_in:
            self.enrolled_in.remove(section.id)
            self.sections_enrolled -= 1

    # note that this may dramatically increase the time complexity, but practially speaking, it should be fine
    def get_top_section_id(self) -> Optional[int]:
        for i in range(0, len(self.section_ranking)):
            section_id = self.section_ranking[i]
            does_conflict = False
            for c in self.conflicts_dict[section_id]:
                if c in self.enrolled_in:
                    does_conflict = True
            if self.proposed_dict[section_id] == False and not does_conflict:
                return section_id
        return None

    def add_proposal(self, section_id: int):
        self.proposed_dict[section_id] = True
    
    def has_space_to_fill(self) -> bool:
        has_space = self.sections_enrolled < self.section_limit
        return has_space

    # this method encourages students to be loaded second, after sections to find conflicts in ranking
    def find_conflicts(self, section_dict: dict):
        for id in self.section_ranking:
            cur_section = section_dict[id]
            self.conflicts_dict[id] = []
            for other_id in self.section_ranking:
                other_section = section_dict[other_id]
                if other_id != id and other_section.schedule == cur_section.schedule:
                    self.conflicts_dict[id].append(other_section.id)
