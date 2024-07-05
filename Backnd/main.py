from flask import Flask, request, send_file, jsonify, send_from_directory
from gtts import gTTS
import os
from werkzeug.utils import secure_filename  # For secure file handling

app = Flask(__name__)

# Define allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert text to speech
def text_to_speech(text, output_folder, filename):
    try:
        tts = gTTS(text=text, lang='si')  # 'si' is the language code for Sinhala
        output_file = os.path.join(output_folder, filename + '.mp3')  # Append .mp3 extension
        tts.save(output_file)
        return output_file  # Return the path to the generated MP3 file
    except Exception as e:
        return None  # Return None if an error occurs

# Route to handle file upload and text-to-speech conversion
@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    try:
        # Check if a file was uploaded in the request
        if 'file' not in request.files:
            return "Error: No file part", 400
        
        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return "Error: No selected file", 400
        
        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            # Save uploaded file to a folder
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(app.root_path, 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Handle different file types
            if filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            elif filename.endswith('.pdf'):
                # Code to extract text from PDF (example using PyMuPDF)
                import fitz
                pdf_text = []
                with fitz.open(file_path) as pdf:
                    for page in pdf:
                        pdf_text.append(page.get_text())
                input_text = '\n'.join(pdf_text)
            elif filename.endswith('.docx'):
                # Code to extract text from DOCX (example using python-docx)
                from docx import Document
                doc = Document(file_path)
                input_text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            else:
                return "Error: Unsupported file format", 400
            
            # Save output MP3 file with the same name as the uploaded file
            output_folder = os.path.join(app.root_path, 'voice_messages')
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Use filename without extension as the base name for the output MP3
            base_filename = os.path.splitext(filename)[0]
            output_file_path = text_to_speech(input_text, output_folder, base_filename)
            
            if output_file_path:
                # Send the generated MP3 file as an attachment
                return send_file(output_file_path, as_attachment=True)
            else:
                return "Error: Failed to generate MP3", 500  # Return error if MP3 generation failed
        
        return "Error: File format not allowed", 400
    except Exception as e:
        return str(e), 500  # Return generic server error if an unexpected exception occurs

# Route to retrieve a list of all generated voice messages (MP3 files)
@app.route('/voices', methods=['GET'])
def get_generated_voices():
    try:
        output_folder = os.path.join(app.root_path, 'voice_messages')
        
        # Check if voice_messages folder exists
        if not os.path.exists(output_folder):
            return jsonify({'error': 'No voice messages found'}), 404
        
        # List all files in the voice_messages folder
        voice_files = os.listdir(output_folder)
        
        # Filter out non-MP3 files if any
        voice_files = [f for f in voice_files if f.endswith('.mp3')]
        
        # Return the list of voice files
        return jsonify({'voices': voice_files})
    except Exception as e:
        return str(e), 500  # Return generic server error if an unexpected exception occurs

# Route to serve voice messages (MP3 files)
@app.route('/voice/<filename>', methods=['GET'])
def serve_voice(filename):
    try:
        voice_folder = os.path.join(app.root_path, 'voice_messages')
        return send_from_directory(voice_folder, filename)
    except Exception as e:
        return str(e), 500  # Return generic server error if an unexpected exception occurs

if __name__ == "__main__":
    app.run(debug=True)
