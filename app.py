from flask import Flask, render_template, request, jsonify, send_file
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # ... (keep the existing code for handling image upload and metadata)
    if 'imageInput' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['imageInput']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    text = request.form.get('textInput', '')
    date = request.form.get('dateInput', '')

    image_metadata = {
        'text': text,
        'date': date,
        'filename': filename,
        'type': file.content_type,
        'size': os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)),
    }

    with open('data.json', 'a') as json_file:
        json.dump(image_metadata, json_file)
        json_file.write('\n')

    return jsonify({'message': 'Upload successful'}), 200

@app.route('/data')
def view_data():
    with open('data.json', 'r') as json_file:
        data = [json.loads(line) for line in json_file]

    return jsonify(data)

@app.route('/image/<filename>')
def serve_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True)
