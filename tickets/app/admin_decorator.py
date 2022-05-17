from functools import wraps
from app.models import User
from flask_login import current_user
from flask import flash, redirect, url_for

def requires_access(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(username=current_user.username).first_or_404()
            if access_level == 'admin' and not user.is_admin():
                flash("The view of that page is restricted to the administrator!")
                return redirect(url_for('logout'))
            elif access_level == 'user' and user.is_admin():
                flash("The view of that page is restricted to users!")
                return redirect(url_for('logout'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator