from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_bp
from models import PricingPlan

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)

    return app

app = create_app()

# ---- Application context block moved here ----
with app.app_context():
    db.create_all()

    # Only insert pricing plans if they don't exist
    if not PricingPlan.query.first():
        plans = [
            PricingPlan(name='Free', price=0, features='Basic listing'),
            PricingPlan(name='Standard', price=49.99, features='Multiple listings'),
            PricingPlan(name='Premium', price=99.99, features='Unlimited listings + analytics')
        ]
        db.session.add_all(plans)
        db.session.commit()
# ---------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
