import pandas as pd
import smtplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# email config
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Read data from the CSV file
os.chdir('registration')
data = pd.read_csv('output_students.csv')

# Iterate through each row in the CSV file
for index, row in data.iterrows():
    sent_from = "Christine Chung (automated email)"
    to = 'cchung@conncoll.edu'#'awoolfson@conncoll.edu' #[row['name']]
    subject = 'CS Course Pre-Registration Overrides'
    initial_message = ""
    if row['enrolled_in_names'] != '[]':
        enrolled_in_names = row['enrolled_in_names'].replace('[', '').replace(']', '').replace("'", '')
        initial_message = f"You are receiving this email because you have been awarded seats in \n\n{enrolled_in_names}\n\n"
        initial_message += "Your professors will be entering overrides for you by Nov 10 so that you will be able to add the course during online pre-registration the week Nov 13. \n"
        initial_message += "Be sure to use this override no later than Nov 16.  If you add the class after Nov 16 we may have to ask you to drop it in the event it gets overenrolled."
    else:
        initial_message = """
We are sorry to inform you that you have not been allocated any seats in courses for next semester.  
There is still a chance that seats will remain unfilled after Nov 16 and in this event, you may still be assigned a course.
We will automatically add you to the wait list of the courses you ranked, but did not get into.  
If there are any other courses you are willing to take other than those you ranked, you may email the professor directly to be added to the wait list.
        """
    body = """
Dear %s:

%s

More info about how we assigned students to courses, in case you are curious:

Students who did not get any courses (or fewer than they wished for) did not get them because either:
(1) they were not declared CS majors, and/or 
(2) are first or second years with lower priority than juniors/seniors, and/or 
(3) only ranked/selected courses that were in higher demand and those courses filled up before their priority level was reached.

Thank you,
Christine
    """ % (row['name'],
           initial_message
           )
    
    email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (sent_from, "".join(to), subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print('Email sent!')
        