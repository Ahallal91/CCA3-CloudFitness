from flask import Blueprint, redirect, url_for, session, flash

logout_bp = Blueprint(
    'logout_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@logout_bp.route('/logout')
def logout():
    pass
