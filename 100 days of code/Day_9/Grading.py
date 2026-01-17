def grade_convert(diction: dict) -> dict:
    new_dic = diction.copy()  # create a copy so we don't modify the original
    
    for key, value in new_dic.items():
        if 91 <= value <= 100:
            new_dic[key] = "Outstanding"
        elif 81 <= value <= 90:
            new_dic[key] = "Exceeds Expectations"
        elif 71 <= value <= 80:
            new_dic[key] = "Acceptable"
        else:  # value <= 70
            new_dic[key] = "Fail"
    
    return new_dic


# Test
student_scores = {
    'Harry': 88,
    'Ron': 78,
    'Hermione': 95,
    'Draco': 75,
    'Neville': 60
}

student_grades = grade_convert(student_scores)
print(student_grades)