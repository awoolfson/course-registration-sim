import pandas as pd
import smtplib
from dotenv import load_dotenv
import os
from get_semester_input import get_semester_input

def main():
    get_semester_input()

    # Load environment variables
    load_dotenv()

    # email config
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') # need to create an app password for this

    # Read data from the CSV file
    data = pd.read_csv('output/output_students.csv')

    # Iterate through each row in the CSV file
    for index, row in data.iterrows():
        print(f"Sending email to {row['name']}...")
        sent_from = "Christine Chung (automated email)"
        to = row['name']
        subject = 'CS Course Pre-Registration Overrides'
        initial_message = ""
        positive_message = ""
        if row['enrolled_in_names'] != '[]':
            enrolled_in_names = row['enrolled_in_names'].replace('[', '').replace(']', '').replace("'", '').strip()
            
            initial_message = """
    You are receiving this email because you have been awarded seats in the following CS courses for the Spring 2024 semester:

    %s

    Your professors will be entering overrides for you by Nov 10 so that you will be able to add the course during online pre-registration the week Nov 13.
    Be sure to use this override no later than Nov 16.  If you add the class after Nov 16 we may have to ask you to drop it in the event it gets overenrolled.

    We will automatically add you to the wait list of the coures you ranked, but did not get into if you got into less courses than you needed to stay on track.
            """ % (enrolled_in_names)
            
            positive_message = """
            
    The algorithm we implemented was able to successfully assign students in a “stable” way, in other words, no student wishes to have any course over one they were given, 
    unless that course they want more is filled with students that all have higher priority for getting the course.  Due to the universal nature of the priority/need function we applied, 
    it also means that there does not exist any pair of students (say, a and b) who have been assigned courses (say x and y, respectively), such that a and b would both be happier swapping their seats in x and y with each other. 

            """
            
        else:
            
            initial_message = """
    We are sorry to inform you that you have not been allocated any seats in CS courses for the Spring 2024 semester.

    There is still a chance that seats will remain unfilled after Nov 16 and in this event, you may still be assigned a seat in a course.  
    Another course that is a requirement for the major and allowed for the minor is MAT210 Discrete Math, which you can register for the usual way.

    We will automatically add you to the wait list of the courses you ranked, but did not get into.  
    If there are any courses you are willing to take other than those you have already ranked in the form, you may email the 
    professor directly to be added to their wait list.
            """
            
            positive_message = ""
            
        body = """
    Dear %s:

    %s

    Here is more info about how we assigned students to courses, in case you are curious:
    %s
    Students who did not get assigned any courses (or got fewer than they wished for) didn’t get them because they:

    (1) were not declared CS majors, and/or 
    (2) are first or second years with lower priority than juniors/seniors, and/or
    (3) only ranked/selected courses that were in higher demand, and those courses filled up before their priority level was reached, and/or
    (4) did not meet the prerequisites of the course(s) they requested (e.g., COM212 for any 300-level course, and COM219 + COM212 for COM315)"


    We appreciate your collaboration in this new process, we hope it will be a better experience for everyone. If you have any other questions please feel free to 
    reach out to me at cchung@conncoll.edu or Auden at awoolfson@conncoll.edu. The code behind the algorithm is available to view at https://github.com/awoolfson/course-registration-sim.


    Thank you,
    Christine
        """ % (row['name'],
            initial_message,
                positive_message
            )
        
        email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
        """ % (sent_from, 
            "".join(to), 
            subject, 
            body
            )

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(sent_from, to, email_text.encode("utf-8"))
        server.close()
        print(f"Email sent to {row['name']}!")
        
if __name__ == "__main__":
    main()
    