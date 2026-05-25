from flask import Flask, render_template, jsonify
from config import Config
import os
import warnings
warnings.filterwarnings('ignore')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize app (create directories)
    config_class.init_app(app)

    # Initialize DB
    from database.db_setup import init_db
    init_db()

    # Register blueprints
    from api.upload_api import upload_bp
    from api.analytics_api import analytics_bp
    from api.export_api import export_bp
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    @app.route('/')
    def index():
        return render_template('pages/index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('pages/dashboard.html')
        
    @app.route('/upload')
    def upload():
        return render_template('pages/upload.html')

    @app.route('/reports')
    def reports():
        return render_template('pages/reports.html')

    @app.route('/analytics')
    def analytics():
        return render_template('pages/analytics.html')

    @app.route('/insights')
    def insights():
        return render_template('pages/insights.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('pages/error.html', error="Page not found", error_code=404), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('pages/error.html', error="Internal server error", error_code=500), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
