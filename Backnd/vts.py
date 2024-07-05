import speech_recognition as sr

def record_and_convert_sinhala_speech(output_file):
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
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Transcribed text saved to {output_file}")
            
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
output_file = "transcribed_text.txt"
record_and_convert_sinhala_speech(output_file)
