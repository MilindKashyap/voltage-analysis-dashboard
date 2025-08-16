from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
import json
from scipy.signal import find_peaks
import os

app = Flask(__name__)

# Global variable to store processed data
df = None

def load_and_process_data():
    """Load and process the dataset"""
    global df
    
    # Check if data file exists, if not create sample data
    if not os.path.exists('static/data/Sample_Data.csv'):
        # Create sample data similar to the original assignment
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=10000, freq='1min')
        voltage = 50 + 20 * np.sin(np.linspace(0, 20*np.pi, 10000)) + np.random.normal(0, 5, 10000)
        
        df = pd.DataFrame({
            'Timestamp': dates,
            'Voltage': voltage
        })
        
        # Save sample data
        os.makedirs('static/data', exist_ok=True)
        df.to_csv('static/data/Sample_Data.csv', index=False)
    else:
        df = pd.read_csv('static/data/Sample_Data.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Process data for analysis
    df['MA_5'] = df['Voltage'].rolling(5).mean()
    df['MA_1000'] = df['Voltage'].rolling(1000).mean()
    df['MA_5000'] = df['Voltage'].rolling(5000).mean()
    
    # Find peaks and troughs
    peaks, _ = find_peaks(df['Voltage'])
    troughs, _ = find_peaks(-df['Voltage'])
    
    # Calculate derivatives for acceleration
    df['d1'] = np.gradient(df['Voltage'])
    df['d2'] = np.gradient(df['d1'])
    
    return df, peaks, troughs

@app.route('/')
def home():
    """Homepage with project description and navigation"""
    return render_template('home.html')

@app.route('/voltage_trend')
def voltage_trend():
    """Voltage vs Timestamp with trendline"""
    try:
        df, _, _ = load_and_process_data()
        print(f"Data loaded successfully. DataFrame shape: {df.shape}")
        
        # Create trendline
        z = np.polyfit(range(len(df)), df['Voltage'], 1)
        p = np.poly1d(z)
        trendline = p(range(len(df)))
        
        # Create minimal Plotly figure
        fig = go.Figure()
        
        # Main voltage line - minimal styling
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['Voltage'],
            mode='lines',
            name='Voltage Signal',
            line=dict(color='#00d4ff', width=2)
        ))
        
        # Trendline - minimal styling
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=trendline,
            mode='lines',
            name='Trendline',
            line=dict(color='#ff6b6b', width=3, dash='dash')
        ))
        
        # Minimal layout
        fig.update_layout(
            title='Voltage vs Timestamp with Trendline Analysis',
            xaxis_title='Timestamp',
            yaxis_title='Voltage (V)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        # Convert to JSON with minimal settings
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print(f"Chart JSON length: {len(graph_json)}")
        
        # Get basic statistics
        stats = {
            'total_points': len(df),
            'mean_voltage': round(df['Voltage'].mean(), 2),
            'min_voltage': round(df['Voltage'].min(), 2),
            'max_voltage': round(df['Voltage'].max(), 2),
            'trend_slope': round(z[0], 4)
        }
        
        return render_template('voltage_trend.html', graph_json=graph_json, stats=stats)
        
    except Exception as e:
        print(f"Error in voltage_trend route: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500

@app.route('/moving_averages')
def moving_averages():
    """Line chart with multiple moving averages"""
    try:
        df, _, _ = load_and_process_data()
        
        fig = go.Figure()
        
        # Original voltage signal
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['Voltage'],
            mode='lines',
            name='Original Voltage',
            line=dict(color='#00d4ff', width=1.5)
        ))
        
        # 5-point moving average
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['MA_5'],
            mode='lines',
            name='5-Point Moving Average',
            line=dict(color='#ff6b6b', width=3)
        ))
        
        # 1000-point moving average
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['MA_1000'],
            mode='lines',
            name='1000-Point Moving Average',
            line=dict(color='#4ecdc4', width=3)
        ))
        
        # 5000-point moving average
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['MA_5000'],
            mode='lines',
            name='5000-Point Moving Average',
            line=dict(color='#ffe66d', width=3)
        ))
        
        # Minimal layout
        fig.update_layout(
            title='Voltage Signal with Multiple Moving Averages',
            xaxis_title='Timestamp',
            yaxis_title='Voltage (V)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('moving_averages.html', graph_json=graph_json)
        
    except Exception as e:
        print(f"Error in moving_averages route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/peaks_troughs')
def peaks_troughs():
    """Peaks and troughs plot with table"""
    try:
        df, peaks, troughs = load_and_process_data()
        
        fig = go.Figure()
        
        # Main voltage line
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['Voltage'],
            mode='lines',
            name='Voltage Signal',
            line=dict(color='#00d4ff', width=2)
        ))
        
        # Peaks (local maxima)
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].iloc[peaks].astype(str),
            y=df['Voltage'].iloc[peaks],
            mode='markers',
            name='Peaks (Local Maxima)',
            marker=dict(color='#ff6b6b', size=10, symbol='diamond')
        ))
        
        # Troughs (local minima)
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].iloc[troughs].astype(str),
            y=df['Voltage'].iloc[troughs],
            mode='markers',
            name='Troughs (Local Minima)',
            marker=dict(color='#4ecdc4', size=10, symbol='diamond')
        ))
        
        # Minimal layout
        fig.update_layout(
            title='Peaks and Troughs Detection in Voltage Signal',
            xaxis_title='Timestamp',
            yaxis_title='Voltage (V)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Prepare data for tables
        peaks_data = df.iloc[peaks][['Timestamp', 'Voltage']].head(20)
        troughs_data = df.iloc[troughs][['Timestamp', 'Voltage']].head(20)
        
        return render_template('peaks_troughs.html', 
                             graph_json=graph_json, 
                             peaks_data=peaks_data, 
                             troughs_data=troughs_data)
                             
    except Exception as e:
        print(f"Error in peaks_troughs route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/voltage_below_20')
def voltage_below_20():
    """Instances where Voltage < 20"""
    try:
        df, _, _ = load_and_process_data()
        
        below_20 = df[df['Voltage'] < 20][['Timestamp', 'Voltage']]
        
        fig = go.Figure()
        
        # Main voltage line
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['Voltage'],
            mode='lines',
            name='Voltage Signal',
            line=dict(color='#00d4ff', width=2)
        ))
        
        # Critical voltage points below 20V
        fig.add_trace(go.Scatter(
            x=below_20['Timestamp'].astype(str),
            y=below_20['Voltage'],
            mode='markers',
            name='Voltage < 20V (Critical)',
            marker=dict(color='#ff6b6b', size=12, symbol='x')
        ))
        
        # Add threshold line
        fig.add_hline(y=20, line_dash="dash", line_color="#ff6b6b", line_width=3)
        
        # Minimal layout
        fig.update_layout(
            title='Voltage Threshold Monitoring (Below 20V)',
            xaxis_title='Timestamp',
            yaxis_title='Voltage (V)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('voltage_below_20.html', 
                             graph_json=graph_json, 
                             below_20_data=below_20.head(50))
                             
    except Exception as e:
        print(f"Error in voltage_below_20 route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/downward_acceleration')
def downward_acceleration():
    """Downward slope acceleration cycles"""
    try:
        df, _, _ = load_and_process_data()
        
        accel_down = df[(df['d1'] < 0) & (df['d2'] < 0)][['Timestamp', 'Voltage', 'd1', 'd2']]
        
        fig = go.Figure()
        
        # Main voltage line
        fig.add_trace(go.Scatter(
            x=df['Timestamp'].astype(str),
            y=df['Voltage'],
            mode='lines',
            name='Voltage Signal',
            line=dict(color='#00d4ff', width=2)
        ))
        
        # Accelerating downward points
        fig.add_trace(go.Scatter(
            x=accel_down['Timestamp'].astype(str),
            y=accel_down['Voltage'],
            mode='markers',
            name='Accelerating Downward',
            marker=dict(color='#ff6b6b', size=8, symbol='circle')
        ))
        
        # Minimal layout
        fig.update_layout(
            title='Downward Slope Acceleration Detection',
            xaxis_title='Timestamp',
            yaxis_title='Voltage (V)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('downward_acceleration.html', 
                             graph_json=graph_json, 
                             accel_data=accel_down.head(50))
                             
    except Exception as e:
        print(f"Error in downward_acceleration route: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True) 