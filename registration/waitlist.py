import pandas as pd
import re

def main():
    google_form = pd.read_csv('google_form_students.csv')
    google_form = google_form.sort_values(by=['Email Address'])

    output_students = pd.read_csv('final_output_students.csv')
    output_students = output_students.sort_values(by=['name'])

    waitlist = pd.DataFrame(columns=[
        "Student Name (Last)",
        "(First)",
        "Status",
        "Class Year",
        "Already Taken",
        "Has Overrides For",
        "Still Wants",
        "Amount Awarded",
        "Amount Still Wanted",
        "Notes"
    ])

    for (index, form_row), (_, output_row) in zip(google_form.iterrows(), output_students.iterrows()):
        student = {}
        pattern = "[a-zA-Z]+"
        student["Student Name (Last)"] = re.findall(pattern, form_row["Email Address"][1:])[0].capitalize()
        student["(First)"] = form_row["Email Address"]
        student["Status"] = output_row["major_status"]
        student["Class Year"] = output_row["grad_semester"]
        
        pattern = "\d{3}"
        student["Already Taken"] = re.findall(pattern, str(form_row[4]))
        pattern = "\d{3}-\d"
        student["Has Overrides For"] = re.findall(pattern, str(output_row["enrolled_in_names"]))
        
        if len(student["Has Overrides For"]) >= form_row[22]:
            continue
        
        desired = set()
        for i in list(range(6, 20)) + [25]:
            num = re.findall(pattern, str(form_row[i]))
            if num:
                desired.add(num[0])
            
        student["Still Wants"] = desired - set(student["Has Overrides For"])
        
        student["Amount Awarded"] = len(student["Has Overrides For"])
        student["Amount Still Wanted"] = form_row[22] - student["Amount Awarded"]
        
        waitlist = waitlist.append(student, ignore_index=True)

    waitlist.to_csv('waitlist.csv', index=False)

if __name__ == "__main__":
    main()
    