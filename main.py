import ast
import os
import google.generativeai as genai

# Optional: load a .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # dotenv is optional

# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit(
        "❌ Error: No API key found. Please set the GEMINI_API_KEY environment variable.\n"
        "Example (bash): export GEMINI_API_KEY='your_api_key_here'\n"
        "Example (PowerShell): setx GEMINI_API_KEY 'your_api_key_here'"
    )

# Configure the gemini client
genai.configure(api_key=api_key)

# Create the model
model = genai.GenerativeModel("gemini-2.5-flash")
# Get code from user
print("=== Code Explainer ===")
print("Paste your code below (press Enter twice when done):\n")

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

user_code = "\n".join(lines)

# Check Python syntax locally
try:
    ast.parse(user_code)
except SyntaxError as e:
    print(f"\n❌ Syntax Error detected locally: {e}")
    exit(1)  # Stop execution if code is invalid

# Create prompt with instructions for Gemini
prompt = f"""
You are a helpful Python assistant.

Instructions:
1. First, check if the code below is valid Python.
2. If the code has syntax errors or is invalid, respond ONLY with:
   "Error: The code contains a syntax error."
3. If the code is valid, explain it step by step in simple terms, as if to a beginner.
4. Keep explanations clear and concise. Do not execute the code.

Code to check and explain:

{user_code}
"""

# Call Gemini with error handling
print("\nGenerating explanation...")
try:
    response = model.generate_content(prompt)
    print("\n=== Explanation ===")
    print(response.text)
except Exception as e:
    print(f"\nError while calling Gemini API: {e}")
