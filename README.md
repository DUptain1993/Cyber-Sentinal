# Cyber Sentinel Dashboard

A Flask-based dashboard application deployed on Vercel.

## Features

- Modern, responsive dashboard interface
- Serverless deployment on Vercel
- Health check endpoint

## Deployment on Vercel

1. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. For production deployment:
   ```bash
   vercel --prod
   ```

## Environment Variables

Set these in your Vercel dashboard:
- `SECRET_KEY`: Flask secret key for session management

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   cd flask_dashboard
   python app.py
   ```

## Project Structure

```
├── flask_dashboard/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── static/
│   │   └── style.css      # Stylesheet
│   └── templates/
│       └── index.html     # Dashboard template
├── vercel.json            # Vercel configuration
└── requirements.txt       # Root dependencies
```
