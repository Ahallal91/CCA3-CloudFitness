from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.secret_key = "some_key"

    from .home import home
    from .session import login
    from .session import logout
    from .management import approved
    from .management import pending

    app.register_blueprint(home.home_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(logout.logout_bp)
    app.register_blueprint(pending.pending_bp)
    app.register_blueprint(approved.approved_bp)
    
    return app
