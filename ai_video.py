import os
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI"))  
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

def generate_video(topic: str):
    print(f"[INFO] Generating video for topic: {topic}")

    prompt = f"Generate an engaging, plain-text voiceover script about '{topic}' for an educational video—no visuals, no narrator cues, just spoken content."
    response = model.generate_content(prompt)
    script = response.text.strip()

    # Text-to-Speech
    tts = gTTS(text=script, lang='en')
    tts.save("voice.mp3")

    avatar_path = os.path.join("static", "avatar.mp4")
    if not os.path.exists(avatar_path):
        raise FileNotFoundError(f"Missing required file: {avatar_path}")

    video = VideoFileClip(avatar_path)
    audio = AudioFileClip("voice.mp3").set_duration(video.duration)

    final_video = video.set_audio(audio)
    output_path = "static/output.mp4"
    final_video.write_videofile(output_path, fps=video.fps)

    return output_path

def generate_quiz(topic: str):
    prompt = f"""
    Based on the topic '{topic}', generate a short quiz with 3 multiple-choice questions.
    Format like this:

    Q1. What is...?
    a) Option A
    b) Option B
    c) Option C
    d) Option D
    Answer: b
    """
    response = model.generate_content(prompt)
    return response.text.strip()
