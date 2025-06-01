from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import fitz  # PyMuPDF
import spacy
import openai
import json
from datetime import datetime
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RESULTS_FILE = "results.json"

# --- Name extraction with fallback ---
def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    top_lines = lines[:10]

    # Step 1: spaCy NER
    doc = nlp("\n".join(top_lines))
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if 1 <= len(name.split()) <= 3:
                return name

    # Step 2: Fallback — 2–3 words, titlecase, no digits
    for line in top_lines:
        words = line.split()
        if not (2 <= len(words) <= 3):
            continue
        if any(char.isdigit() for char in line):
            continue
        if sum(1 for w in words if w[0].isupper() and w.isalpha()) >= 2:
            return line.strip()

    return ""

# --- Email and phone ---
def extract_contact(text):
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"\+?\d[\d\s().-]{8,}\d", text)
    return (
        email_match.group() if email_match else "",
        phone_match.group() if phone_match else ""
    )

# --- Skills from NER ---
def extract_skills(doc):
    skills = set()
    for ent in doc.ents:
        if ent.label_ in {"PRODUCT", "LANGUAGE", "ORG"}:
            text = ent.text.strip()
            if (
                1 <= len(text.split()) <= 3 and
                not any(x in text.lower() for x in ["school", "college", "academy"])
            ):
                skills.add(text)
    return list(skills)

# --- Experience filtering ---
def extract_experience(doc):
    experience = []
    for sent in doc.sents:
        s = sent.text.strip()
        if len(s.split()) < 5:
            continue
        if s.count('\n') > 1:
            continue
        if sum(1 for c in s if c.isupper()) / (len(s) + 1e-5) > 0.5:
            continue
        if not any(token.pos_ == "VERB" for token in nlp(s)):
            continue
        experience.append(s)
    return experience

# --- Use GPT to refine fields ---
def refine_with_gpt(raw_text, extracted):
    prompt = f"""
You are an AI resume parser. You will correct the following extracted fields using the full resume text.

Resume:
\"\"\"
{raw_text}
\"\"\"

Current extraction (may be incomplete or incorrect):
{json.dumps(extracted, indent=2)}

Return corrected fields in JSON:
{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["..."],
  "experience": ["..."]
}}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print("[GPT ERROR]", e)
        return extracted

# --- Main extractor ---
def extract_fields(text):
    doc = nlp(text)

    base = {
        "name": extract_name(text),
        "email": extract_contact(text)[0],
        "phone": extract_contact(text)[1],
        "skills": extract_skills(doc),
        "experience": extract_experience(doc)
    }

    return refine_with_gpt(text, base)

# --- Upload endpoint ---
@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        # Check if file is PDF
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'File must be a PDF'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        print(f"Saving file to: {filepath}")
        file.save(filepath)

        text = ""
        try:
            with fitz.open(filepath) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            return jsonify({'error': f'Error reading PDF: {str(e)}'}), 500

        if not text.strip():
            return jsonify({'error': 'No text could be extracted from PDF'}), 400

        extracted = extract_fields(text)

        # Append to results.json with timestamp
        record = extracted.copy()
        record["timestamp"] = datetime.now().isoformat()
        with open(RESULTS_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")

        return jsonify(extracted)

    except Exception as e:
        print(f"Error in upload: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# --- Get stored resume parsing history ---
@app.route('/history', methods=['GET'])
def history():
    records = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            for line in f:
                try:
                    records.append(json.loads(line.strip()))
                except:
                    continue
    return jsonify(records[::-1])  # recent first

# --- Start server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
