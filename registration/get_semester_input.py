import os
import sys

def get_semester_input():
    dir = input("Enter the directory name (semester) of registration\n")
    
    if os.path.isdir(f"../registration/semesters/{dir}"):
        os.chdir(f"../registration/semesters/{dir}/")
    else:
        os.chdir("../registration/semesters/")
        ans = input(f"Directorty not found, would you like to initialize a new directory with name {dir}? (y/n)")
        if ans == "y":
            os.mkdir(f"{dir}")
            os.chdir(f"{dir}/")
            os.mkdir("input")
            os.mkdir("output")
            
            os.chdir("input/")
            open(f"courses.csv", "w")
            open(f"google_form_students.csv", "w")
            
            os.chdir("../output/")
            os.mkdir("individual_sections")
            os.chdir("../../")
            print("Directory initialized...\nExiting...")
            sys.exit()
        else:
            print("Exiting...")
            sys.exit()
        