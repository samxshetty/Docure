from flask import Flask, render_template, request, redirect, url_for
import os
from signature import match

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'
THRESHOLD = 85

# Ensure upload and temp directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['TEMP_FOLDER']):
    os.makedirs(app.config['TEMP_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return redirect(request.url)

    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return redirect(request.url)

    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
    
    file1.save(file1_path)
    file2.save(file2_path)

    try:
        similarity = match(file1_path, file2_path)
    except Exception as e:
        return f"An error occurred: {e}"

    result_message = (
        f"Signatures are {similarity:.2f}% similar. This signature may be forged."
        if similarity <= THRESHOLD
        else f"Signatures are {similarity:.2f}% similar. This signature appears genuine."
    )

    return render_template('result.html', message=result_message)

if __name__ == '__main__':
    try:
        app.run(debug=True,port=5007)
    except Exception as e:
        print(f"Error starting Flask server: {e}")
