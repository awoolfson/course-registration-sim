def count_potential_rogues(student_dict: dict) -> int:
    counter = 0
    for student in student_dict.values():
        middles = []
        conflicts_dict = student.conflicts_dict
        for conflict_id, conflicts in conflicts_dict.items():
            if len(conflicts) >= 2:
                for conflict_id1 in conflicts:
                    for conflict_id2 in conflicts:
                        if conflict_id1 not in conflicts_dict[conflict_id2] and conflict_id1 != conflict_id2:
                            middle = False
                            outsides = [conflict_id1, conflict_id2]
                            for section_id in student.section_ranking:
                                if section_id in outsides:
                                    outsides.remove(section_id)
                                    if middle:
                                        middle = False
                                        break
                                    else:
                                        middle = True
                                elif section_id == conflict_id:
                                    if middle:
                                        if conflict_id not in middles:
                                            counter += 1
                                            middles.append(conflict_id)
                                            print(student.id, conflict_id)
                                    else:
                                        break
    return counter
