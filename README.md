# python-analyze

This repository will eventually contain source code to analyze short Python programs.

## Task 1
- Create a small repository (~1000 codes) of Python programs attempting student submissions.

Datasets like these should be helpful to get you started.

https://www.itshared.org/2015/12/codeforces-submissions-dataset-for.html

- Write a script such that for every program in your repository, you replace *every* existing function call with *foo()*.
For instance, if your program reads -
```
def count_list_repeats(li):
    x = 5
    verify_results(li, x)
    ...
```
it should automatically get converted to -
```
def count_list_repeats(li):
    x = 5
    foo(li, x)
    ...
```
Are there special/edge cases to consider? What challenges can you face while attempting to solve this?

- Hint: Do not be tempted to use a regular expression/grep like strategy to make these replacements. Look up what abstract syntax trees of programs are. Modify them to achieve this functionality.

- Have at least one plot, or one table which summarizes relevant statistics from the dataset. To begin with, for the task mentioned above, ask yourself what statistics you think are even relevant and would want answered?

- Evaluation -- How will you evalute whether your algorithm/strategy covers all cases? It could well be we're unsure of this no matter what we do.

## Instructions
- Do not fork this repo. Work on a local copy. Make it a habit to push changes upstream to your repo as frequently as feasible.
- Use `Python3.7+` for this work.
- We workship the lords of reproducability of results. Use `conda` to create an environment and set up your repository. 
- Use a `.gitignore` file to ensure you are not adding junk files to the repo.
- Have a `./src/` folder containing the source.
- Have a `./env/` folder containing the Conda environment file you create for this project.
- Have a `./data/` folder containing all the data your source accesses.
- Have a `./tests/` folder to write out unit tests for key functions. Look up the `unittest` package in Python if you haven't used it before.
- Keep updating this README with instructions which will help with the reproducability of your work/results.

Setting these up can be a little painful and time consuming. Wade through it. Focus on getting the core functionality right first, though.



## Goals
- Have a working prototype
- (We will) assess how well you scope and assess the different components involved which will solve this problem
- Assess how you divide your labor into the components you identify. Remember, there's a time budget of ~2 days.
- Assess how you wiggle out of situations when you're stuck.
- Assess how well you communicate and let all stakeholders know of your progress.

## Source code data:

Python source codes have been retrieved from here: https://www.itshared.org/2015/12/codeforces-submissions-dataset-for.html
This resource provides submissions from the Codeforces website in the form of a MySQL back up file. 

Script './src/data_filer.py' processes this data by connecting to a local MySQL database server, fetching the first 1000 Python source codes, and writing them to individual files, each named after the submission id, in the './data' folder. You are welcome to use these files, or run the './src/data_filer.py' in order to generate new files, perhaps consisting of a different subset of the Python submissions. 

To run the data filter script, you will need to first set up MySQL on your system and import the './data/dump.sql' back up file in order to create your own local submissions database. Then, you will need to create a file called 'db_cred.py' inside the './src' directory that contains the following credentials to access the database:
 
 - a 'USER' global variable, as a string, which is the username to use for connecting to the MySQL server
 - a 'PASSWORD' global variable, also as a string, which is the password associated with the above user
 
This information will be imported by the data filter script in order to connect to your local database.
