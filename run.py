import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Permission, Role, Student, Department, Course

#Create application instance
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


#Make shell context processor
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Student=Student,
                Department=Department, Course=Course)

@app.cli.command()
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
