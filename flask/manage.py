import unittest
import coverage
from flask_script import Manager

from nrf import create_app, logger, db

# The logger should always be used instead of a print(). You need to import it from
# the project package. If you want to understand how to use it properly and why you
# should use it, check: http://bit.ly/2nqkupO
logger.info('Server has started.')

# Defines which parts of the code to include and omit when calculating code coverage.
COV = coverage.coverage(
    branch=True,
    include='nrf/*',
    omit=[
        'nrf/website/*'
    ]
)
COV.start()

# app = create_app()

# Creates the Flask application object that we use to initialize things in the app.
app = create_app()

# Creates all the models specified in project/models
import nrf.models
db.create_all(app=app)

# Initializes the Manager object, which allows us to run terminal commands on the
# Flask application while it's running (using Flask-Script).
manager = Manager(app)


@manager.command
def cov():
    """
    Runs the unit tests and generates a coverage report on success.
    While the application is running, you can run the following command in a new terminal:
    'docker-compose run --rm flask python manage.py cov' to run all the tests in the
    'tests' directory. If all the tests pass, it will generate a coverage report.
    :return int: 0 if all tests pass, 1 if not
    """

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    else:
        return 1


if __name__ == '__main__':
    manager.run()

