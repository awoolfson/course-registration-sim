import pandas as pd
import Student 
from queue import PriorityQueue as pq
import heapq
class CourseSection:
    
    def __init__(self, id: int, course_name: str, capacity: int, credits: int):
        self.id = id # 6 digit CRN
        self.capacity = capacity
        self.credits = credits
        self.course_name = course_name
        self.roster_pq = [] # sorted by section score
        self.number_enrolled = 0
        self.swapped_out = (False, 0) # this lets the algorithm know if a student was swapped out and which student
        self.student_section_scores = {}
        
    def __str__(self):
        roster = []
        for s in self.roster_pq:
            roster.append(s.id)
        return f'{self.course_name}:\n id: {self.id}\n capacity: {self.capacity}\n credits: {self.credits}\n' + f'roster: {roster}'
    
    def score_student(self, student: Student):
        id = student.id
        if id in self.student_section_scores:
            return self.student_section_scores[id]
        else:
            # subject to change once scoring function is done
            self.student_section_scores[id] = student.base_score
            return student.base_score
    
    def pop_lowest_student(self):
        popped_student = heapq.heappop(self.roster_pq)
        return popped_student
    
    def return_lowest_student(self):
        lowest_student = heapq.heappop(self.roster_pq)
        heapq.heappush(self.roster_pq, lowest_student)
        return lowest_student
    
    def is_full(self):
        return len(self.roster_pq) >= self.capacity
    
    def enroll(self, student: Student):
        student.section_score = self.score_student(student)
        heapq.heappush(self.roster_pq, student)