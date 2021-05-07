from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = "some_key"

    from .home import home
    # from .session import login
    # from .session import logout
    # from .session import register

    app.register_blueprint(home.home_bp)
    # app.register_blueprint(register.register_bp)
    # app.register_blueprint(login.login_bp)
    # app.register_blueprint(logout.logout_bp)

    return app
