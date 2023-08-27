# speech_converter/views.py
import os
import openai
import speech_recognition as sr
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

openai.api_key = os.environ.get("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")  # Get the API key from the environment variable

def convert_speech(request):
    converted_text = None

    if request.method == 'POST':
        audio_file = request.FILES['audio']

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            try:
                converted_text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                converted_text = "Could not understand audio"

        # Perform speech synthesis using OpenAI API
        response = openai.Completion.create(
            engine="davinci-tts",
            prompt=converted_text,
            max_tokens=100
        )
        synthesized_audio = response.choices[0].text

        with open(os.path.join(settings.MEDIA_ROOT, 'output.mp3'), 'wb') as f:
            f.write(synthesized_audio.encode("utf-8"))

    return render(request, 'convert.html', {'converted_text': converted_text})
