# Tournament Manager
[DESCRIPTION]

## Launching the Application
### Creating the Virtual Environment
1. Clone the repository from GitHub.
```
git clone https://github.com/saacutter/CITS3403-Project
```

2. Install the [Python interpreter](https://www.python.org/downloads/) for your operating system.
    - This was developed using Python 3.12.3, the latest version of Python available on Ubuntu 24.04 (and the aptitude package manager).

3. Create and activate a virtual environment.
    - A virtual environment can be created using `python -m venv /path/to/venv`.
    - The virtual environment is activated depending on the operating system:
        - UNIX-based (Linux and MacOS): `source path/to/venv/bin/activate`
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
        │   │   │   └── user-profile-background.webp
        │   │   ├── js
        │   │   │   ├── login.js
        │   │   │   ├── profile_friend_requests.js
        │   │   │   ├── profile_image.js
        │   │   │   ├── remove_friend.js
        │   │   │   ├── search_users.js
        │   │   │   └── upload.js
        │   │   └── profilepictures
        │   └── templates
        │       ├── 404.html
        │       ├── add-match.html
        │       ├── add-tournament.html
        │       ├── base.html
        │       ├── edit-profile.html
        │       ├── home.html
        │       ├── login.html
        │       ├── privacy-policy.html
        │       ├── search.html
        │       └── user.html
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
        │       ├── 880d94870c32_added_image_attribute_to_tournaments_.py
        │       ├── a823f3370236_added_friends_table.py
        │       ├── ac1c030fc5b9_added_profile_picture_section_to_users_.py
        │       └── b41b7621e32c_added_email_and_creation_date_field_to_.py
        └── requirements.txt
        </pre>

2. Add the secret key to the file (the below is an example secret key):
```
SECRET_KEY="this-is-a-secret-key"
```

3. Add the SQLAlchemy database to the file:
```
DATABASE_URL = "sqlite:///app.db"
```


### Starting the Application
1. Initialise the database (if it hasn't already been) with the `flask db init` command.
    - The database can then be updated using the `flask db upgrade`.

2. Start the flask application using `flask run`.
    - Note that the `.flaskenv` file sets the `FLASK_APP` environment variable. If this does not work, the following should be done:
        - UNIX-based (Linux and MacOS): `export FLASK_APP=manager.py`
        - Windows: `set FLASK_APP=manager.py`


## Running the Unit Tests
TEMPORARY


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
