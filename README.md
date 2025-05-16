# Tournament Manager (Group 17)
Our new Tournament Manager helps you create, manage, and track competitive tournaments with ease. Whether you're organising local gaming events, online challenges, or just 
tracking friendly rivalries, our platform has you covered for all of your needs. This application has the following supported features:
- Accounts, allowing users to register, add tournament data to their accounts, and manage their profiles.
- Tournament creation, permitting users to add tournament data to their accounts and share it with the world.
- Explore public tournaments created by others.
- Connections with friends to follow their activity.
- A privacy option for users (set by default) which allows users to hide their data and only show it to people they follow.

## Launching the Application
The following steps should be taken in order to setup and start running the application. \
*NOTE: This application was tested on Unix systems, and is not guaranteed to work on Windows.*
### Creating the Virtual Environment
1. Clone the repository from GitHub.
```
git clone https://github.com/saacutter/CITS3403-Project
```

2. Install the [Python interpreter](https://www.python.org/downloads/) for your operating system.
    - This was developed using Python 3.12.3, the latest version of Python available on Ubuntu 24.04.

3. Create and activate a virtual environment.
    - A virtual environment can be created using `python -m venv /path/to/venv`.
    - The virtual environment is activated depending on the operating system:
        - Linux and MacOS: `source path/to/venv/bin/activate`
        - Windows Command Prompt: `path\to\venv\Scripts\activate`
        - Windows Powershell: `path\to\venv\Scripts\Activate.ps1`
    - The virtual environment can be stopped at any time using the `deactivate` command (operating system agnostic).

5. Install the dependencies for the project backend.
```bash
pip install -r requirements.txt
```

### Setting Environment Variables
1. Create a new file in the root directory with the filename `.env`.
    - The directory tree should look like the following (excluding the virtual environment, which should be created as above):
        <pre>
        .
        ├── .env
        ├── .flaskenv
        ├── README.md
        ├── app
        │   ├── __init__.py
        │   ├── blueprints.py
        │   ├── config.py
        │   ├── forms.py
        │   ├── models.py
        │   ├── routes.py
        │   ├── static
        │   │   ├── css
        │   │   │   └── styles.css
        │   │   ├── html
        │   │   │   ├── home.html
        │   │   │   └── login-signup.html
        │   │   ├── img
        │   │   │   ├── chess.png
        │   │   │   ├── default.png
        │   │   │   ├── profilepic1.png
        │   │   │   ├── profilepic2.png
        │   │   │   ├── rocketleague.png
        │   │   │   └── user-profile-background.webp
        │   │   ├── js
        │   │   │   ├── chart.js
        │   │   │   ├── delete_tournaments.js
        │   │   │   ├── details.js
        │   │   │   ├── profile_friend_requests.js
        │   │   │   ├── remove_friend.js
        │   │   │   ├── render_image.js
        │   │   │   └── search_users.js
        │   │   ├── previews
        │   │   └── profilepictures
        │   └── templates
        │       ├── 404.html
        │       ├── 500.html
        │       ├── _tournament.html
        │       ├── _tournament_profile.html
        │       ├── add-tournament.html
        │       ├── base.html
        │       ├── edit-profile.html
        │       ├── edit-tournament.html
        │       ├── home.html
        │       ├── login.html
        │       ├── privacy-policy.html
        │       ├── register.html
        │       ├── search.html
        │       ├── tournaments.html
        │       └── user.html
        ├── logs
        ├── manager.py
        ├── migrations
        │   ├── README
        │   ├── alembic.ini
        │   ├── env.py
        │   ├── script.py.mako
        │   └── versions
        │       ├── 1a185a813ada_adjusted_tournaments_table_to_have_a_.py
        │       ├── 518c88c18d5f_updated_users.py
        │       ├── 56f705820311_recreated_database_to_fix_broken_.py
        │       ├── 5d3f9f639ef5_users_table.py
        │       ├── 7406e470d526_added_detail_attribute_to_tournaments_.py
        │       ├── 880d94870c32_added_image_attribute_to_tournaments_.py
        │       ├── 8ce13cf5e121_merged_the_tournaments_and_matches_.py
        │       ├── a823f3370236_added_friends_table.py
        │       ├── ac1c030fc5b9_added_profile_picture_section_to_users_.py
        │       └── b41b7621e32c_added_email_and_creation_date_field_to_.py
        ├── requirements.txt
        └── tests
            ├── __init__.py
            ├── test_selenium.py
            └── test_unit.py
        </pre>

2. Add the secret key to the file, e.g. `SECRET_KEY="this-is-a-secret-key"`
    - As this is just setting an environment variable, the following can also be done:
        - Linux and MacOS: `export SECRET_KEY="this-is-a-secret-key"`
        - Windows: `set SECRET_KEY="this-is-a-secret-key"`

3. (Optional) Add the SQLAlchemy database URL to the file, e.g. `DATABASE_URL="sqlite:///app.db"`
    - This is another environment variable, and can be set in the same way as above.

4. (Optional) Add a path for the logs to be saved to, e.g. `LOG_PATH='logs'`


### Starting the Application
1. Initialise the database using `flask db upgrade`
    - If the database isn't initialising properly, using `flask db init` and then applying the migrations may work

2. Start the flask application using `flask run`.
    - Note that the `.flaskenv` file sets the `FLASK_APP` environment variable. If this does not work, the following should be done:
        - Linux and MacOS: `export FLASK_APP=manager.py`
        - Windows: `set FLASK_APP=manager.py`


## Running the Unit Tests
To run the unit tests, the instructions above should be followed and the following steps should be taken.
1. Run the unit tests
```bash
python3 -m unittest tests.unit_tests
```

2. Run the Selenium tests
```bash
python3 -m unittest tests.selenium_tests
```


## Authors
<div style="text-align: center; justify-self: center;">

|     Name      | Student ID |                GitHub Username                |     
|---------------|------------|-----------------------------------------------|
| Jordan Joseph | 23332309   | [Jordan-672](https://github.com/Jordan-672)   |
| Arnav Kaul    | 23857081   | [arnavkaul77](https://github.com/arnavkaul77) |
| Jay Owens     | 23459289   | [JayJay7704](https://github.com/JayJay7704)   |
| Isaac Rutter  | 24273992   | [saacutter](https://github.com/saacutter)     |

</div>


## References
[1] M, Grinberg, "The Flask Mega-Tutorial," Miguel Grinberg Blog. [Online]. Available: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

[2] “Jsonify a SQLAlchemy result set in Flask,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask

[3] “Creating a new DOM element from an HTML string using built-in DOM methods or properties,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro

[4] “How can I assign a multiline string literal to a variable,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/805107/how-can-i-assign-a-multiline-string-literal-to-a-variable

[5] M. Grinberg, “Handling File Uploads with Flask,” Miguel Grinberg Blog. [Online]. Available: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

[6] “How to set image source as input file using JavaScript,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/69595046/how-to-set-image-source-as-input-file-using-javascript

[7] “Fancy Cushion Pattern,” Toptal Subtle Patterns. [Online]. Available: https://www.toptal.com/designers/subtlepatterns/fancy-cushion-pattern/

[8] “Joystick for Game Console – Vector Art,” Vecteezy. [Online]. Available: https://www.vecteezy.com/vector-art/17287469-joystick-for-game-console-computer-ps-line-icon-joypad-game-controller-for-videogame-pictogram-computer-gamepad-play-equipment-outline-symbol-editable-stroke-isolated-vector-illustration

[9] “No Photo Available,” Wikipedia. [Online]. Available: https://en.m.wikipedia.org/wiki/File:No_photo_available.svg

[10] Crash Course - WTForms Documentation. [Online]. Available: https://wtforms.readthedocs.io/en/3.0.x/crash_course/#displaying-errors

[11] Doughnut and Pie Charts, Chart.js. [Online]. Available: https://www.chartjs.org/docs/latest/charts/doughnut.html