# Cyber Sentinel - Inventory Management System

A Flask-based inventory management system with file upload capabilities and Telegram bot integration.

## Features

- CSV file upload for inventory management
- Modern, responsive web interface
- Telegram bot for product sales
- File storage and management
- Health check endpoint

## Hosting Options (Support File Uploads)

### 1. **Render** (Recommended - Free Tier)
```bash
# Deploy using Render dashboard or CLI
# 1. Connect your GitHub repo to Render
# 2. Create new Web Service
# 3. Set build command: cd flask_dashboard && pip install -r requirements.txt
# 4. Set start command: cd flask_dashboard && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 2. **Railway** (Free Tier Available)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. **Heroku** (Paid - $5/month)
```bash
# Install Heroku CLI
# Create app and deploy
heroku create your-app-name
git push heroku main
```

### 4. **Google Cloud Run** (Pay-per-use)
```bash
# Deploy to Google Cloud Run
gcloud run deploy --source .
```

### 5. **DigitalOcean App Platform** (Paid - $5/month)
- Use the DigitalOcean dashboard
- Connect your GitHub repository
- Set build and run commands

## Environment Variables

Set these in your hosting platform's dashboard:

### For Flask Dashboard:
- `SECRET_KEY`: Flask secret key for session management
- `GOOGLE_EMAIL`: Gmail address for sending emails
- `GOOGLE_PASSWORD`: Gmail app password

### For Telegram Bot:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `CHAT_ID`: Your Telegram chat ID
- `GOOGLE_EMAIL`: Gmail address for sending emails
- `GOOGLE_PASSWORD`: Gmail app password

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your environment variables

3. Run the Flask dashboard:
   ```bash
   cd flask_dashboard
   python app.py
   ```

4. Run the Telegram bot:
   ```bash
   cd telegram_bot
   python bot.py
   ```

## File Upload Functionality

The system supports CSV file uploads for inventory management:
- Upload CSV files through the web interface
- Files are stored in the `uploads/` directory
- The Telegram bot reads from `uploads/inventory.csv`

## Project Structure

```
├── flask_dashboard/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── static/
│   │   └── style.css      # Stylesheet
│   └── templates/
│       └── index.html     # Upload interface
├── telegram_bot/
│   ├── bot.py             # Telegram bot
│   └── requirements.txt   # Bot dependencies
├── uploads/               # File storage (created automatically)
├── render.yaml           # Render configuration
├── Procfile             # Heroku configuration
├── railway.json         # Railway configuration
├── app.yaml            # Google Cloud configuration
└── requirements.txt    # Root dependencies
```

## CSV Format

Your inventory CSV should have the following format:
```csv
product_key,quantity
atm_exploit,10
info_stealer,25
daily_fullz_x10,100
daily_fullz_bulk,50
credit_cards_x5,75
credit_cards_x50,30
```

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Use strong, unique secret keys
- Enable 2FA on your Gmail account and use app passwords
- Regularly update dependencies for security patches
