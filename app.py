from flask import Flask, request, jsonify
import speech_recognition as sr
import os

app = Flask(__name__)

# Initialize the recognizer
recognizer = sr.Recognizer()


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    audio_path = "./temp_audio.wav"
    file.save(audio_path)

    # Set chunk length and initial position
    chunk_length = 20  # Length of each audio chunk in seconds
    current_position = 0
    transcribed_text = []

    # Process audio in chunks
    try:
        with sr.AudioFile(audio_path) as source:
            total_duration = source.DURATION  # Total duration of audio in seconds

            while current_position < total_duration:
                # Define the duration of the current chunk
                chunk_duration = min(chunk_length, total_duration - current_position)

                # Record a chunk of audio with offset
                audio_data = recognizer.record(source, offset=current_position, duration=chunk_duration)
                final_text = ""
                # Convert each chunk to text
                try:
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
                    final_text += text
                except sr.UnknownValueError:
                    transcribed_text.append({
                        "start": current_position,
                        "text": "Could not understand audio in this segment."
                    })
                except sr.RequestError:
                    return jsonify({'error': 'Could not connect to the speech recognition service.'}), 500

                # Move to the next chunk
                current_position += chunk_length

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(audio_path)  # Delete the temporary audio file

    return jsonify({'transcript': final_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7026)
