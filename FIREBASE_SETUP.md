# Firebase Firestore Setup Guide

## 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Enter project name (e.g., "algorithmic-trading-platform")
4. Enable Google Analytics (optional)
5. Create project

## 2. Enable Firestore Database

1. In your Firebase project, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location (choose closest to your users)
5. Click "Done"

## 3. Create Service Account

1. Go to Project Settings (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. **Keep this file secure - never commit to version control**

## 4. Configure Environment Variables

Copy the values from your service account JSON to your `.env` file:

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nyour-private-key-here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account-email@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project.iam.gserviceaccount.com
```

## 5. Firestore Security Rules

In the Firebase Console, go to Firestore → Rules and update:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write access to trades collection
    match /trades/{document} {
      allow read, write: if true; // For development - restrict in production
    }
  }
}
```

## 6. Production Security Rules (Recommended)

For production, use more restrictive rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /trades/{document} {
      allow read, write: if request.auth != null; // Requires authentication
    }
  }
}
```

## 7. Test Your Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with Firebase credentials
3. Run your Flask app: `python app.py`
4. Visit your app and try adding a trade

## 8. Deployment to EC2

When deploying to EC2:

1. Upload your `.env` file with Firebase credentials
2. Make sure the file permissions are secure: `chmod 600 .env`
3. Restart your Flask application

## 9. Firestore Collections Structure

Your app will create the following structure: