import pandas as pd
import CourseSection

class Student: 
    def __init__(self, id: int, name: str, base_score: int):
        self.id = id # 8 digit ID
        self.credit_limit = 18
        self.base_score = base_score
        self.name = name
        self.section_ranking = []
        self.schedule = []
        self.credits_enrolled = 0
        self.section_score = None # compare students within a section, should not be saved to a database ever
        
    def __str__(self):
        return f'{self.name}:\n id: {self.id}\n base_score: {self.base_score}\n'
    
    def __lt__(self, other_student):
        return self.section_score < other_student.section_score
        
    def insert_section_preference(self, index: int, section: CourseSection):
        self.section_preferences_ordered.insert(index, section)
            
    def set_section_ranking(self, ranking: list):
        for i, section_id in enumerate(ranking):
            ranking[i] = int(section_id)
        self.section_ranking = ranking
        
    def join_section(self, section: CourseSection):
        self.credits_enrolled += section.credits
        self.schedule.append(section.id)
