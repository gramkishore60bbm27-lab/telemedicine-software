from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from models import db
from routes.consultation_routes import consultation_bp

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(consultation_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # HTML page routes
    @app.route('/')
    def index():
        """Landing page"""
        return render_template('index.html')
    
    @app.route('/consultation')
    def consultation():
        """Consultation scheduling and joining page"""
        return render_template('consultation.html')
    
    @app.route('/video-call/<room_id>')
    def video_call(room_id):
        """Video call interface page"""
        return render_template('video-call.html', room_id=room_id)
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'healthy', 'message': 'Telemedicine server is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
