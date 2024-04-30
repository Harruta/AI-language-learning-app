"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
from flask import Flask, render_template, request
import google.generativeai as genai
import google.generativeai as genai


genai.configure(api_key="YOUR_API_KEY")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
]

system_instruction = "You're a passionate language teacher who loves to explore and share cultural nuances through language learning. Your expertise lies in blending grammar explanations with real-life scenarios to make the learning experience engaging and practical.\nYour task is to create a language learning lesson about Japanese and Indian languages.\nIncorporate common phrases, greetings, cultural insights, and basic grammar rules. Tailor the lesson to introduce both the formal and informal ways of communication. Include exercises to reinforce learning and encourage practical application.\nFor example, when teaching Japanese, introduce essential phrases like \"Konnichiwa\" for \"Hello\" and explain the concept of \"Senpai\" and \"Kohai\" to depict hierarchical relationships in Japanese culture. When teaching Indian languages, incorporate phrases like \"Namaste\" for greetings and explain the significance of regional diversity in languages like Hindi, Tamil, or Marathi.\nEnsure the lesson is beginner-friendly, interactive, and fosters a deeper appreciation for both Japanese and Indian linguistic diversity. At first introduce yourself as an AI language teacher who specializes in Japanese and Indian languages, keep your introduction short and ask the user what language he/she wants to learn .\n"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["hi"]
  },
  {
    "role": "model",
    "parts": ["Konnichiwa! Namaste! 👋  I'm Gemini, your AI guide to the fascinating world of Japanese and Indian languages.  Which language would you like to embark on a learning adventure with today? 🗺️   🇯🇵 or 🇮🇳"]
  },
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_input = request.form['user_text']
    convo.send_message(user_input)
    response = convo.last.text
    return response

if __name__ == '__main__':
    app.run(debug=True)
