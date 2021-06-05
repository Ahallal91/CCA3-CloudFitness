from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = "some_key"

    from .home import home
    from .search import search
    from .session import login
    from .session import logout
    from .session import register
    from .upload import upload
    from .profile import profile
    from .exercise import exercise

    app.register_blueprint(home.home_bp)
    app.register_blueprint(search.search_bp)
    app.register_blueprint(register.register_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(logout.logout_bp)
    app.register_blueprint(upload.upload_bp)
    app.register_blueprint(profile.profile_bp)
    app.register_blueprint(exercise.exercise_bp)
    
    return app
