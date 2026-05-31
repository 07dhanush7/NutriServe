from flask import Flask, send_from_directory
from sqlalchemy import event

from app.config import get_config
from app.extensions import bcrypt, cors, db, jwt, migrate
from app.middleware.errors import register_error_handlers
from app.middleware.logging import register_request_logging
from app.utils.response import success_response


def create_app(config_name=None):
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(get_config(config_name))

    register_extensions(app)
    register_routes(app)
    register_error_handlers(app)
    register_request_logging(app)

    if app.config.get("AUTO_CREATE_TABLES"):
        with app.app_context():
            from app import models  # noqa: F401

            db.create_all()
            normalize_order_statuses()

    return app


def normalize_order_statuses():
    from sqlalchemy import text

    db.session.execute(
        text(
            """
            UPDATE weekly_orders
            SET status = 'Completed'
            WHERE status IN ('Confirmed', 'Preparing', 'Delivered', 'Cancelled')
            """
        )
    )
    db.session.execute(
        text(
            """
            UPDATE weekly_orders
            SET status = 'Pending'
            WHERE status IS NULL OR status NOT IN ('Pending', 'Completed')
            """
        )
    )
    db.session.commit()


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/api/*": {"origins": "*"},
            r"/health": {"origins": "*"},
            r"/": {"origins": "*"},
        },
    )

    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        with app.app_context():
            event.listen(db.engine, "connect", set_sqlite_pragma)

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        from app.models.payment_notification import TokenBlocklist

        return TokenBlocklist.query.filter_by(jti=jwt_payload["jti"]).first() is not None

    @jwt.invalid_token_loader
    def invalid_token(message):
        from app.utils.response import error_response

        return error_response(message, 422)

    @jwt.unauthorized_loader
    def missing_token(message):
        from app.utils.response import error_response

        return error_response(message, 401)

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        from app.utils.response import error_response

        return error_response("Token has expired", 401)


def register_routes(app):
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.category import category_bp
    from app.routes.delivery import delivery_bp
    from app.routes.meal import meal_bp
    from app.routes.notification import notification_bp
    from app.routes.order import order_bp
    from app.routes.payment import payment_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(meal_bp, url_prefix="/api/meals")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(payment_bp, url_prefix="/api/payments")
    app.register_blueprint(delivery_bp, url_prefix="/api/delivery")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.get("/")
    def home():
        return success_response("Smart Canteen Backend Running Successfully")

    @app.get("/health")
    def health():
        return {"status": "healthy"}, 200

    @app.get("/favicon.ico")
    def favicon():
        return "", 204

    @app.get("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
