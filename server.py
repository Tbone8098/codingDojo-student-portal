from flask_app import app
from flask_app.controllers import controller_routes, controller_cohort, controller_user, controller_student

if __name__=='__main__':
    app.run(debug=True)