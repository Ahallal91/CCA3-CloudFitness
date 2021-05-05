from flask import Blueprint

register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@register_bp.route('/register', methods=["GET", "POST"])
def register():
    pass
