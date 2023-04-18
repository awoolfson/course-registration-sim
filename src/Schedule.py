class Schedule:
    
    def __init__(self, days: list, times: list):
        self.days = days
        self.times = []
        self.day_dict = {
            'M':(),
            'T':(),
            'W':(),
            'R':(),
            'F':(),
            'TBA': False
            }
        
        self.to_be_anounced = False
        
        # handle sections marked TBA
        
        for i in range(len(times)):
            if times[i] == 'TBA':
                self.times = ['TBA']
                self.to_be_anounced = True
                self.day_dict['TBA'] = True
                break
                
        if not self.to_be_anounced:
            
        # construct numeric times as (hour, minute) tuples
            
            for i in range(len(times)):
                times[i] = times[i].split(" ")
                
            numeric_times=[]
            
            for time in times:
                for i in [0, 3]:
                    parts = time[i].partition(":")
                    hour = int(parts[0])
                    minute = int(parts[2])
                    if time[i+1] == 'pm':
                        hour += 12
                    numeric_times.append((hour, minute))
                    
        # convert times to values in minutes, append to self.times
                    
            for i in range(0, len(numeric_times), 2):
                self.times.append((numeric_times[i][0] * 60 + numeric_times[i][1],
                                   numeric_times[i+1][0] * 60 + numeric_times[i+1][1]))
                
        # update dict to include meeting times for days
                
        for i, entry in enumerate(days):
            for day in entry:
                self.day_dict[day] = self.times[i]
                
        def __eq__(self, other):
            # only tests if schedules conflict, aren't fully equal
            for day in self.day_dict:
                if day != 'TBA':
                    time = self.day_dict[day]
                    other_time = other.day_dict[day]
                    if time != () and other_time != ():
                        if not (time[0] > other_time[1] or time[1] < other_time[0]):
                            return True # there is a conflict
            return False # no conflict
                    
                    
                    
    