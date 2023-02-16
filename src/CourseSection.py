import pandas as pd
import Student 
from queue import PriorityQueue as pq

class CourseSection:
    #condider this: using only the priority queue of students to track the roster
    #and instead of searching a student to force remove use a hash table to track previously removed students
    #and cross check it in an indefinite loop when a student is popped from the table, this won't impact
    #time complexity. Entry set can be used maybe for printing and stuff
    
    #actually just let this be, force remove can be worried about later this is totally fine
    
    def __init__(self, id: int, course_name: str, capacity: int, credits: int):
        self.id = id # 6 digit CRN
        self.capacity = capacity
        self.credits = credits
        self.course_name = course_name
        self.roster_pq = pq() # sorted by section score
        self.number_enrolled = 0
        removed_students_ids = {}
        
    def __str__(self):
        return f'{self.course_name}:\n id: {self.id}\n capacity: {self.capacity}\n credits: {self.credits}\n'
    
    def score_student(self, student: Student):
        return student.base_score
    
    def pop_lowest_student(self):
        # nessecary so hash table can be used for validation of students
        popped_student = self.roster_pq.pop()
        self.removed_students[popped_student.id] = popped_student
        while self.roster_pq[0].id in self.removed_students:
            self.roster_pq.get()
        return popped_student
    
    def is_full(self):
        if self.roster_pq.qsize() >= self.capacity:
            return True
        else:
            return False
    
    def enroll(self, student: Student):
        student.section_score = self.score_student(student)
        self.roster_pq.put(student)
        