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
    - The program tree should look like the following:
    <pre>
    .
    ├── README.md
    ├── app
    │   ├── __init__.py
    │   ├── database
    │   │   ├── create.sh
    │   │   ├── database.db
    │   │   └── schema.sql
    │   ├── forms.py
    │   ├── routes.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── styles.css
    │   │   └── js
    │   │       └── temp.js
    │   ├── templates
    │   │   ├── base.html
    │   │   └── index.html
    │   └── tests
    │       └── test_app.py
    ├── manager.py
    ├── migrations
    │   └── versions
    └── requirements.txt
    </pre>

2. Add the secret key to the file (the below is an example secret key):
```
SECRET_KEY="this-is-a-secret-key"
```

3. Add the SQLAlchemy database to the file:
```
SQLALCHEMY_DATABASE_URI = "sqlite:////database/database.db"
```


### Starting the Application
1. Create the database using `sh database/create.sh`.
    - This will create a file named `database.db` in the `database` directory.

2. Start the flask application using `flask run`.


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
