from flask import Blueprint, redirect, url_for, session, flash

logout_bp = Blueprint(
    'logout_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def remove_session_id():
    session['user'] = None

@logout_bp.route('/logout')
def logout():
    remove_session_id()
    return redirect(url_for('home_bp.home'))
