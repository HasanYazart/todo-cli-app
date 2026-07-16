from functools import wraps

from flask import g, jsonify, redirect, request, session, url_for

from models import User, db


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("user")
        user = db.session.get(User, user_id) if user_id else None
        if user is None:
            session.clear()
            if request.path.startswith("/api/") or request.method != "GET":
                return jsonify({"status": "error", "message": "Giriş yapmalısınız."}), 401
            return redirect(url_for("auth.login"))
        g.current_user = user
        return view(*args, **kwargs)

    return wrapped_view
