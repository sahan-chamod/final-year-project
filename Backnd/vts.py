# import speech_recognition as sr

# def record_and_convert_sinhala_speech(output_file):
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.Microphone() as source:
#             print("Adjusting for ambient noise, please wait...")
#             recognizer.adjust_for_ambient_noise(source)
#             print("Recording... Please speak.")
            
#             audio_data = recognizer.listen(source)
#             print("Recording complete.")
        
#         try:
#             text = recognizer.recognize_google(audio_data, language="si-LK")
#             print("Transcribed Text: ", text)
            
#             # Save transcribed text to a file
#             with open(output_file, 'w', encoding='utf-8') as file:
#                 file.write(text)
#             print(f"Transcribed text saved to {output_file}")
            
#         except sr.UnknownValueError:
#             print("Sorry, I could not understand the audio.")
#         except sr.RequestError as e:
#             print(f"Could not request results from Google Speech Recognition service; {e}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage
# output_file = "transcribed_text.txt"
# record_and_convert_sinhala_speech(output_file)


from flask import Flask, jsonify, request
import speech_recognition as sr
import os

app = Flask(__name__)

TRANSCRIBED_TEXT_FILE = "transcribed_text.txt"

@app.route('/record_and_convert_sinhala_speech', methods=['POST'])
def record_and_convert_sinhala_speech():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source)
            print("Recording... Please speak.")
            
            audio_data = recognizer.listen(source)
            print("Recording complete.")
        
        try:
            text = recognizer.recognize_google(audio_data, language="si-LK")
            print("Transcribed Text: ", text)
            
            # Save transcribed text to a file
            with open(TRANSCRIBED_TEXT_FILE, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Transcribed text saved to {TRANSCRIBED_TEXT_FILE}")
            
            return jsonify({"success": True, "transcribed_text": text}), 200
            
        except sr.UnknownValueError:
            return jsonify({"success": False, "error": "Sorry, I could not understand the audio."}), 400
        except sr.RequestError as e:
            return jsonify({"success": False, "error": f"Could not request results from Google Speech Recognition service; {e}"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {e}"}), 500

@app.route('/get_transcribed_text', methods=['GET'])
def get_transcribed_text():
    if os.path.exists(TRANSCRIBED_TEXT_FILE):
        with open(TRANSCRIBED_TEXT_FILE, 'r', encoding='utf-8') as file:
            transcribed_text = file.read()
        return jsonify({"success": True, "transcribed_text": transcribed_text}), 200
    else:
        return jsonify({"success": False, "error": "Transcribed text file not found."}), 404

@app.route('/delete_transcribed_text', methods=['DELETE'])
def delete_transcribed_text():
    if os.path.exists(TRANSCRIBED_TEXT_FILE):
        os.remove(TRANSCRIBED_TEXT_FILE)
        return jsonify({"success": True, "message": "Transcribed text file deleted."}), 200
    else:
        return jsonify({"success": False, "error": "Transcribed text file not found."}), 404

@app.route('/update_transcribed_text', methods=['PUT'])
def update_transcribed_text():
    if os.path.exists(TRANSCRIBED_TEXT_FILE):
        new_text = request.json.get('new_text')
        if new_text:
            with open(TRANSCRIBED_TEXT_FILE, 'w', encoding='utf-8') as file:
                file.write(new_text)
            return jsonify({"success": True, "message": "Transcribed text updated.", "new_text": new_text}), 200
        else:
            return jsonify({"success": False, "error": "No new text provided."}), 400
    else:
        return jsonify({"success": False, "error": "Transcribed text file not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
