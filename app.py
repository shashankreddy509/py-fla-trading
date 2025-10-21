from flask import Flask, render_template, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/data')
def get_data():
    """Sample API endpoint"""
    return jsonify({
        'message': 'Hello from Flask!',
        'data': [1, 2, 3, 4, 5],
        'timestamp': datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=8000)