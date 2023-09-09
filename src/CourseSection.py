import heapq

import pandas as pd

import Student
from Schedule import Schedule


class CourseSection:
    def __init__(self, id: int, code: str, capacity: int, credits: int, dept: str, name: str, times: list, days: list):
        self.id = id  # 6 digit CRN
        self.capacity = capacity
        self.credits = credits
        self.dept = dept
        self.course_code = code
        self.course_name = name
        self.roster_pq = []  # sorted by section score
        self.number_enrolled = 0
        self.swapped_out = (False, 0)  # this lets the algorithm know if a student was swapped out and which student
        self.student_section_scores = {}
        self.schedule = Schedule(times=times, days=days)

    def __str__(self):
        roster = []
        for s in self.roster_pq:
            roster.append(s.id)
        log = (
            f"{self.dept}{self.course_code}: {self.course_name}\nid: {self.id}\ncapacity: {self.capacity}\n"
            f"credits: {self.credits}\nroster: {roster}\nschedule: {self.schedule}\n"
        )
        return log

    def score_student(self, student: Student):
        id = student.id
        if id in self.student_section_scores:
            return self.student_section_scores[id]
        else:
            mod = 0
            if student.major == self.dept:
                mod = 50
            score = student.base_score + mod
            self.student_section_scores[id] = score
            return score

    def pop_lowest_student(self):
        popped_student = heapq.heappop(self.roster_pq)
        return popped_student

    def get_lowest_student(self):
        lowest_student = heapq.heappop(self.roster_pq)
        heapq.heappush(self.roster_pq, lowest_student)
        return lowest_student

    def is_full(self):
        return len(self.roster_pq) >= self.capacity

    def is_empty(self):
        return len(self.roster_pq) == 0

    def enroll(self, student: Student):
        student.section_score = self.score_student(student)
        heapq.heappush(self.roster_pq, student)
