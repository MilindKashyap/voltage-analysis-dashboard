# Voltage Data Analysis Dashboard

A professional Flask-based web application for analyzing voltage time series data with interactive visualizations.

## Features

- **Interactive Charts**: Built with Plotly.js for responsive data visualization
- **Multiple Analysis Views**: 
  - Voltage vs Timestamp with trendline analysis
  - Moving averages (5, 1000, and 5000 point)
  - Peak and trough detection
  - Voltage threshold monitoring (below 20V)
  - Downward slope acceleration detection
- **Modern UI**: Dark theme with Bootstrap 5 and custom CSS
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Plotly.js
- **Styling**: Bootstrap 5, Custom CSS
- **Data Processing**: Pandas, NumPy, SciPy

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Open http://localhost:5000 in your browser

## Deployment

This app is configured for deployment on:
- Render (recommended)
- Heroku
- Railway
- Any WSGI-compatible hosting service

## Live Demo

Visit: [Your deployed URL will be here]

## Deployment to Render

### Method 1: Using render.yaml (Recommended)
1. Push your code to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and configure the deployment
6. Click "Create Web Service"

### Method 2: Manual Configuration
1. Push your code to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: voltage-analysis-dashboard
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. Click "Create Web Service"

Your app will be deployed and available at: `https://your-app-name.onrender.com`

## License

MIT License 