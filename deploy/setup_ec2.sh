#!/bin/bash

# EC2 Setup Script for Ubuntu
# Run this script on your EC2 instance

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application directory
sudo mkdir -p /home/ubuntu/py-fla-trading
cd /home/ubuntu/py-fla-trading

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (requirements.txt should be uploaded first)
pip install -r requirements.txt

# Set up Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/flask-app
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Create systemd service for the Flask app
sudo tee /etc/systemd/system/flask-app.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/py-fla-trading
Environment="PATH=/home/ubuntu/py-fla-trading/venv/bin"
ExecStart=/home/ubuntu/py-fla-trading/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl start flask-app
sudo systemctl enable flask-app

echo "Flask app setup complete!"
echo "Your app should be accessible at http://your-ec2-public-ip"