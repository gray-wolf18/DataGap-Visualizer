from flask import Flask, render_template, request, redirect, url_for, flash
import os
import plotly
import plotly.graph_objs as go
import pandas as pd
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "secret_key"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_div = ''
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'data' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['data']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            df = pd.read_csv(filename)
            missing_data = df.isnull().sum()
            traces = [go.Bar(x=missing_data.index, y=missing_data.values)]
            plot_div = plotly.offline.plot(traces, output_type='div')
    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
