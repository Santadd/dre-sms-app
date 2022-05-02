import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import Users

#Create application instance
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


#Make shell context processor
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Users=Users)
