from app import create_application, db
from app.config import *
from flask_migrate import Migrate

application = create_application(DeploymentConfig)
migrate = Migrate(application, db)

if __name__ == '__main__':
    application.run(debug=False)