from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from config import Config
import os

from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.experience import experience_bp
from Backend.admin.projects import projects_bp
from Backend.admin.skills import skills_bp
from Backend.admin.upload import upload_bp
from Backend.admin.contacts import contacts_bp
from Backend.utama.utama import utama_bp


def create_app():
    app = Flask(__name__, static_folder='Frontend', template_folder='.')
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    app.register_blueprint(login_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(profiles_bp, url_prefix='/api')
    app.register_blueprint(experience_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(skills_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(contacts_bp, url_prefix='/api')
    app.register_blueprint(utama_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(app.root_path, 'index.html')

    @app.route('/index.html')
    def index_file():
        return send_from_directory(app.root_path, 'index.html')

    @app.route('/admin')
    def admin_index():
        return send_from_directory(os.path.join(app.root_path, 'Frontend', 'admin'), 'login.html')

    @app.route('/admin/<path:filename>')
    def admin_pages(filename):
        return send_from_directory(os.path.join(app.root_path, 'Frontend', 'admin'), filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Route tidak ditemukan'}), 404
        return send_from_directory(app.root_path, 'index.html')

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

    return app

# Expose a top-level Flask `app` instance for WSGI hosts (Vercel expects this)
app = create_app()


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
