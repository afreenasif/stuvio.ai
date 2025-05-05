from flask import Flask, render_template, request
from ai_video import generate_video, generate_quiz

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['prompt']
    video_path = generate_video(topic)
    quiz_text = generate_quiz(topic)
    return render_template('index.html', video_url='/' + video_path, quiz=quiz_text)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")
