# course-registration-sim

## Overview

This research project, "The Course Registration Problem" addresses the challenge of efficiently assigning college students to their preferred course sections while considering scheduling conflicts. The project leverages a Gale-Shapley style algorithm to create a valid course-student assignment.

## Table of Contents

- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)

## Key Features

- Utilizes a Gale-Shapley style algorithm to produce a valid matching with minimal "rogue pairs"
- Handles course preferences, capacity constraints, and scheduling conflicts.
- Applicable to real-world scenarios, such as student registration for courses.

## Getting Started

To use The Course Registration Simulator, follow these steps:

### Prerequisites

- Python (version 3.7+)

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:awoolfson/course-registration-sim.git
   ```

2. Navigate to the project directory:

   ```bash
   cd course-registration-sim
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Set Up

The first step after installition for usage is to collect and add data under the registration/semesters directory. Initialize a directory under
semesters with the name of the semester you are performing registration for.

![example file structure](https://github.com/awoolfson/course-registration-sim/tree/main/images/example_structure.png)

The next step is to initialize and input and output directory like shown above. The only files you will need to add are courses.csv and
google_form_students.csv. Be sure to give them those name or the program will not recognize them as inputs.

If you would prefer not to manually initialize these files and directories, the program will do it for you if you run register.py (from the registration directory)
and enter a semester that does not yet exist.

### Data Entry and Validation

There is a specific methodology to formatting the input data to be recognized by the program.

![example courses](https://github.com/awoolfson/course-registration-sim/tree/main/images/example_courses.png)

Above is an example of the first rows of a courses.csv file. Each field other than roster_ids is used for registration, roster_ids may or may not be
included, but will not effect the programs functionality in any way. The days and times in this example represent 11:50 - 1:05 on Tuesdays and Thursdays, and
1:00 - 1:01 on Fridays (included originally to prevent students from taking two sections of data structures). This is because the first block of days,
delimited by a space, is TR representing Tuesday Thursday. The first block of times, delimited by a + is 11:50 - 1:05. The second blocks also correspond.

![row keys](https://github.com/awoolfson/course-registration-sim/tree/main/images/row_keys.png)

The columns in google_form_students do not have to be ordered. Each of the columns must be numbered according to the dictionary shown above. This way
a google form can be used and questions can be re-worded or re-ordered but function the same in the program. For more information on student inputs,
please refer to google forms used previously, or look in the register.py file to see how they are parsed.

### Execution

To run a registration, CD into the registration directory and run register.py. Answer the prompt, and the output file will be populated with
information pertaining to the final course assignment based on the input data you entered.

### Other Functionality