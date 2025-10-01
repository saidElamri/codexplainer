from flask import Flask, render_template, request
import google.generativeai as genai
import markdown
import ast
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in environment. Add it to your .env file.")

# Configure Gemini
genai.configure(api_key=API_KEY)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain():
    user_code = request.form['code']
    level = request.form['level']

    # ✅ Local syntax check before calling Gemini
    try:
        ast.parse(user_code)
    except SyntaxError as e:
        explanation_html = f"<p style='color:red;'>❌ Syntax Error detected: {e}</p>"
        return render_template(
            'index.html', 
            code=user_code, 
            explanation=explanation_html, 
            level=level
        )

    # Build prompt depending on level
    if level == "beginner":
        prompt = f"Explain this Python code step by step in simple beginner-friendly terms:\n\n{user_code}"
    else:
        prompt = f"Explain this Python code concisely for someone with programming experience:\n\n{user_code}"

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        explanation_html = markdown.markdown(
            getattr(response, "text", "⚠️ No explanation generated."),
            extensions=['fenced_code', 'codehilite', 'tables']
        )
    except Exception as e:
        explanation_html = f"<p style='color:red;'>Error: {str(e)}</p>"

    return render_template(
        'index.html', 
        code=user_code, 
        explanation=explanation_html, 
        level=level
    )

if __name__ == '__main__':
    app.run(debug=True)
