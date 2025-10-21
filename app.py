from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from firebase_service import firebase_service

# Load environment variables
load_dotenv()

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
    """Sample API endpoint with Firestore integration"""
    try:
        # Get data from Firestore
        trades = firebase_service.get_trades()
        
        return jsonify({
            'message': 'Hello from Flask with Firebase!',
            'trades': trades,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error fetching data from Firebase',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/trades', methods=['GET', 'POST'])
def trades():
    """API endpoint for managing trades"""
    if request.method == 'POST':
        try:
            trade_data = request.get_json()
            
            # Validate required fields
            required_fields = ['symbol', 'quantity', 'price', 'action']
            if not all(field in trade_data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Add timestamp
            trade_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Save to Firestore
            trade_id = firebase_service.add_trade(trade_data)
            
            return jsonify({
                'message': 'Trade added successfully',
                'trade_id': trade_id,
                'trade_data': trade_data
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:  # GET request
        try:
            trades = firebase_service.get_trades()
            return jsonify({
                'trades': trades,
                'count': len(trades)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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