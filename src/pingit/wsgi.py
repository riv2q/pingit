from app import app


def get_wsgi_application():
    """Return Flask application with middlewares."""
    return app


application = get_wsgi_application()
