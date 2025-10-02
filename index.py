from flask import Flask, render_template, request
import google.generativeai as genai
import markdown
import os

app = Flask(__name__)

# Configure Gemini - Use environment variable for security
API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBoRSlgKuQ-mBQiEQWiK0mmpXG9pn17Afc')
genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/explain', methods=['POST'])
def explain():
    user_code = request.form['code']
    level = request.form['level']
    
    if level == "beginner":
        prompt = f"Explain this code step by step in very simple terms for a beginner:\n\n{user_code}"
    else:
        prompt = f"Explain this code concisely for someone with programming experience:\n\n{user_code}"
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Convert Markdown to HTML
        explanation_html = markdown.markdown(
            response.text,
            extensions=['fenced_code', 'codehilite', 'tables']
        )
    except Exception as e:
        explanation_html = f"<p>Error: {str(e)}</p>"
    
    return render_template(
        'index.html', 
        code=user_code, 
        explanation=explanation_html, 
        level=level
    )

# Vercel needs this
handler = app