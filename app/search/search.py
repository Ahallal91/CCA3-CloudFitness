from flask import Blueprint, render_template

search_bp = Blueprint(
    'search_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("search.html")
