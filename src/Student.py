import pandas as pd
import CourseSection

class Student: 
    def __init__(self, id: int, name: str, base_score: int):
        self.id = id # 8 digit ID
        self.credit_limit = 16
        self.base_score = base_score
        self.name = name
        self.section_ranking = []
        self.schedule = []
        self.credits_enrolled = 0
        self.section_score = None # compare students within a section, should not be saved to a database ever
        self.next_section_index = 0
        
    def __str__(self):
        return f'{self.name}:\n id: {self.id}\n base_score: {self.base_score}\n section ranking: {self.section_ranking}\n schedule: {self.schedule}\n credits enrolled: {self.credits_enrolled }'
    
    def __lt__(self, other_student):
        return self.section_score < other_student.section_score
     
    def __eq__(self, other_student):
        return self.section_score == other_student.section_score
    
    def __gt__(self, other_student):
        return self.section_score > other_student.section_score
        
    def insert_section_preference(self, index: int, section: CourseSection):
        self.section_ranking.insert(index, section)
            
    def set_section_ranking(self, ranking: list):
        for i, section_id in enumerate(ranking):
            ranking[i] = int(section_id)
        self.section_ranking = ranking
        
    def join_section(self, section: CourseSection):
        self.credits_enrolled += section.credits
        self.schedule.append(section.id)
        
    def leave_section(self, section: CourseSection):
        # this can be optimized to dictionary later, just too lazy right now
        if section.id in self.schedule:
            self.schedule.remove(section.id)
            self.credits_enrolled -= section.credits
        
    def get_top_section_id(self):
        return self.section_ranking[self.next_section_index]
    
    def increment_next_section(self):
        self.next_section_index += 1
        
    def has_credits_to_fill(self, credits: int):
        has_credits = self.credit_limit - self.credits_enrolled >= credits
        return has_credits

    def is_finished_proposing(self):
        return self.next_section_index >= len(self.section_ranking)
        
        
