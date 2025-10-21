import os
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Create credentials from environment variables
                cred_dict = {
                    "type": "service_account",
                    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                    "token_uri": os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
                }
                
                # Initialize Firebase
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            
            # Get Firestore client
            self.db = firestore.client()
            print("Firebase initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            # For development, you can use the emulator
            if os.getenv('FLASK_ENV') == 'development':
                print("Using Firestore emulator for development")
                os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8080'
                self.db = firestore.client()
    
    def add_trade(self, trade_data):
        """Add a new trade to Firestore"""
        try:
            if not self.db:
                raise Exception("Firestore not initialized")
            
            # Add server timestamp
            trade_data['created_at'] = firestore.SERVER_TIMESTAMP
            trade_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Add to trades collection
            doc_ref = self.db.collection('trades').add(trade_data)
            return doc_ref[1].id  # Return the document ID
            
        except Exception as e:
            print(f"Error adding trade: {e}")
            raise e
    
    def get_trades(self, limit=50):
        """Get trades from Firestore"""
        try:
            if not self.db:
                raise Exception("Firestore not initialized")
            
            # Query trades ordered by timestamp (newest first)
            trades_ref = self.db.collection('trades')
            query = trades_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
            
            trades = []
            for doc in query.stream():
                trade_data = doc.to_dict()
                trade_data['id'] = doc.id
                
                # Convert Firestore timestamp to ISO string
                if 'created_at' in trade_data and trade_data['created_at']:
                    trade_data['timestamp'] = trade_data['created_at'].isoformat()
                
                trades.append(trade_data)
            
            return trades
            
        except Exception as e:
            print(f"Error getting trades: {e}")
            # Return empty list if there's an error
            return []
    
    def get_trade_by_id(self, trade_id):
        """Get a specific trade by ID"""
        try:
            if not self.db:
                raise Exception("Firestore not initialized")
            
            doc_ref = self.db.collection('trades').document(trade_id)
            doc = doc_ref.get()
            
            if doc.exists:
                trade_data = doc.to_dict()
                trade_data['id'] = doc.id
                return trade_data
            else:
                return None
                
        except Exception as e:
            print(f"Error getting trade by ID: {e}")
            raise e
    
    def update_trade(self, trade_id, update_data):
        """Update a trade in Firestore"""
        try:
            if not self.db:
                raise Exception("Firestore not initialized")
            
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection('trades').document(trade_id)
            doc_ref.update(update_data)
            
            return True
            
        except Exception as e:
            print(f"Error updating trade: {e}")
            raise e
    
    def delete_trade(self, trade_id):
        """Delete a trade from Firestore"""
        try:
            if not self.db:
                raise Exception("Firestore not initialized")
            
            doc_ref = self.db.collection('trades').document(trade_id)
            doc_ref.delete()
            
            return True
            
        except Exception as e:
            print(f"Error deleting trade: {e}")
            raise e
    
    def get_portfolio_summary(self):
        """Get portfolio summary statistics"""
        try:
            trades = self.get_trades(limit=1000)  # Get more trades for accurate summary
            
            if not trades:
                return {
                    'total_trades': 0,
                    'total_value': 0,
                    'unique_symbols': 0,
                    'symbols': []
                }
            
            total_value = 0
            symbols = set()
            
            for trade in trades:
                total_value += trade.get('quantity', 0) * trade.get('price', 0)
                symbols.add(trade.get('symbol', ''))
            
            return {
                'total_trades': len(trades),
                'total_value': round(total_value, 2),
                'unique_symbols': len(symbols),
                'symbols': list(symbols)
            }
            
        except Exception as e:
            print(f"Error getting portfolio summary: {e}")
            return {
                'total_trades': 0,
                'total_value': 0,
                'unique_symbols': 0,
                'symbols': []
            }

# Create a global instance
firebase_service = FirebaseService()