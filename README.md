Hello! 

I created this app as part of my journey to learn Python and for an assignment in my class at IU Academy in March 2023. Fortunately, with the existence of modern AI, I was able to use ChatGPT to help me learn coding concepts and create a functional prototype more quickly.

The app is not complete, and some features like GUI and the implementation of bonus points are still lacking. Nonetheless, it was a fun exercise.


+-------------------------+
|REQUIREMENTS:            |
+-------------------------+

- Python 3.6 or higher (coded with 3.11)
- pip package manager (to install the required packages - see 'requirements.txt')


+-------------------------+
|TO SETUP THE APP:  	  |
+-------------------------+


1) Clone or download the project's repository from GitHub.

2) Open a command prompt or terminal window.

3) Navigate to the project's directory using the 'cd' command.

4) Run the following command to install the required packages: 

pip install -r requirements.txt

This command will install the required packages listed in the 'requirements.txt' file.


+-------------------------+
| USER GUIDE:             |
+-------------------------+

Run the app by running one of the following commands:

python app_CLI.py (recommended) or app_GUI.py (not recommended) since incomplete.

This will launch the app and display a menu of options. Here's a brief description of each option:

1) Add a habit: Allows you to add a new habit to your tracker. You'll be prompted to enter the name of the habit and how often you want to do it (daily or weekly). 

2) Delete a habit: Allows you to delete a habit from your tracker. You'll be shown a list of your current habits and asked to select one to delete.

3) Modify a habit: Allows you to modify the name or frequency of a habit. You'll be shown a list of your current habits and asked to select one to modify.

4) Check off a habit: Allows you to mark a habit as completed for the day or week. You'll be shown a list of your current habits and asked to select one to check off. Displays a motivational quote each time a habit is checked off.

5) List all habits: Displays a list of all your habits, including their names, frequency, streak, and points.

6) Quit: Exits the app.



+-------------------------+
| STRUCTURE OF THE APP:   |
+-------------------------+

                                       +----------------------------+
                                       | app_CLI.py (or app_GUI.py) |
                                       +----------------------------+
                                                   |
            +------------------------+-------------------------------+--------------------------+
            |                        |                               |                          |
     +------------------+    +------------------------+    +-----------------------+    +-----------------------+
     | habit_tracker.py |    | database.py            |    | motivational_quotes.py|    | habits.py             |
     |                  |    |                        |    |                       |    |                       |
     | add_habit()      |    | create_table()         |    | get_quote()           |    | check()               |    
     | delete_habit()   |    | insert_habit()         |    |                       |    |                       |
     | modify_habit()   |    | delete_habit()         |    |                       |    |                       |
     | check_habit()    |    | update_habit()         |    |                       |    |                       |
     |                  |    | get_all_habits()       |    |                       |    |                       |
     |                  |    | update_habit_stats()   |    |                       |    |                       |
     +------------------+    +------------------------+    +-----------------------+    +-----------------------+


The app_CLI.py (or app_GUI.py) script is the main entry point for the app. It interacts with the HabitTracker, Database, MotivationalQuotes, and Habits classes, which are located in separate Python modules. 

The Habits class defines the Habit object, which represents a single habit and has methods for checking it off and updating its stats. 

The HabitTracker class provides methods for adding, deleting, modifying, and checking off habits. 

The Database class handles all interactions with the SQLite database file that stores the user's habits in a database.db file that is located in the same directory as the rest of the .py files. 

The MotivationalQuotes class provides a method for generating a random motivational quotes as soon as the user checks off a habit with option 4) when running 'app_CLI.py'.


+-------------------------+
| LEGAL NOTICE:           |
+-------------------------+

Please note that the habit tracking app is provided as-is and without warranty of any kind, express or implied. It is intended for personal, non-commercial use only, and I am not responsible for any loss or damage caused by the use of the app.
