import copy

from gs import gale_shapley_match
from test_stability import check_stability 

def monte_carlo_gs(student_dict: dict, section_dict: dict, iteration_limit: int = 500) -> int:
    best = float("inf")
    seeds = [i for i in range(1, iteration_limit + 2)]
    i = 0
    while i < iteration_limit:
        i += 1
        
        new_student_dict = copy.deepcopy(student_dict)
        new_section_dict = copy.deepcopy(section_dict)
        new_matching = gale_shapley_match(new_student_dict, new_section_dict, shuffle = True, seed = seeds[i])
        
        rogues = check_stability(new_matching[0], new_matching[1])["rogue_count"]
        
        if rogues < best:
            best = rogues
            
    return int(best)
