import os
import json
import cv2
import PyPDF2
import docx
import pytesseract
import nltk
import uuid
import shutil
from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertForSequenceClassification
from langdetect import detect
from db_connection import check_user_credentials, register_user, initialize_database, save_document_history, get_user_documents, get_document_by_id, get_user_id
from email_service import send_emails_for_analysis
from pdf_generator import generate_pdf
import tempfile
import re

# Download necessary NLTK resources
nltk.download("punkt")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Initialize the database
initialize_database()

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the 'documents' directory exists for permanent storage
DOCUMENTS_FOLDER = os.path.join("static", "documents")
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)
app.config["DOCUMENTS_FOLDER"] = DOCUMENTS_FOLDER

# Load IPC Sections JSON File
try:
    with open("ipc_sections.json", "r", encoding="utf-8") as file:
        ipc_data = json.load(file)
except FileNotFoundError:
    ipc_data = []

# Load Pretrained Multilingual BERT Model
tokenizer = BertTokenizer.from_pretrained("google/muril-base-cased")  # BERT for Tamil & English
model = BertForSequenceClassification.from_pretrained("google/muril-base-cased")

# TF-IDF Vectorizer for Machine Learning Analysis
tfidf_vectorizer = TfidfVectorizer()

# Extract text for training, with error handling
ipc_texts = []
for section in ipc_data:
    try:
        # Ensure the section has 'desc_eng' and 'desc_tam' fields
        desc_eng = section.get("desc_eng", "")  # Default to empty string if 'desc_eng' is missing
        desc_tam = section.get("desc_tam", "")  # Default to empty string if 'desc_tam' is missing
        ipc_texts.append(desc_eng + " " + desc_tam)
    except Exception as e:
        print(f"Error processing section: {e}")

# Fit the TF-IDF Vectorizer
if ipc_texts:
    tfidf_vectorizer.fit(ipc_texts)
else:
    print("Warning: No valid IPC texts found for TF-IDF vectorization.")

# Function to Extract Text from Files
def extract_text(file_path, file_ext):
    text = ""
    try:
        if file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif file_ext == ".pdf":
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        elif file_ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs)
        elif file_ext in [".jpg", ".jpeg", ".png"]:
            text = perform_ocr(file_path)  # Use file_path for OCR
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text.strip()

# Function to Perform OCR on Images
def perform_ocr(file_path):
    try:
        image = cv2.imread(file_path)  # Read the image using file_path
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng+tam")  # English & Tamil OCR
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def analyze_petition(petition_text):
    """Analyze the petition text and identify relevant IPC sections"""
    # Detect the language of the petition text
    try:
        language = detect(petition_text)
    except:
        language = "en"  # Default to English if language detection fails

    # Preprocess the text
    petition_text = petition_text.lower()
    
    # Vectorize the petition text
    petition_vector = tfidf_vectorizer.transform([petition_text])
    
    # Calculate similarity with each IPC section
    relevant_sections = []
    for section in ipc_data:
        # Check if any keywords (English or Tamil) are present in the petition
        english_keywords = section.get("keywords", {}).get("en", [])
        tamil_keywords = section.get("keywords", {}).get("ta", [])
        
        # Check for matches in both English and Tamil keywords
        keyword_match = (
            any(keyword.lower() in petition_text for keyword in english_keywords) or
            any(keyword.lower() in petition_text for keyword in tamil_keywords)
        )
        
        # If keywords match, add to relevant sections
        if keyword_match:
            section["display_language"] = language
            relevant_sections.append(section)
    
    # Sort by priority
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    relevant_sections.sort(key=lambda x: priority_order.get(x["priority"], 4))
    
    return relevant_sections

# Route to Upload and Analyze Petition
@app.route("/upload", methods=["POST"])
def upload():
    # Check if user is logged in
    if "username" not in session:
        flash("Please log in to upload documents", "error")
        return redirect(url_for("login"))
    
    # Check if file was uploaded
    if "document" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("home"))
    
    file = request.files["document"]
    
    # Check if file is empty
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("home"))
    
    # Generate a unique filename
    original_filename = file.filename
    file_ext = os.path.splitext(original_filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Save the file temporarily
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(temp_path)
    
    # Extract text from the document
    extracted_text = extract_text(temp_path, file_ext)
    
    if not extracted_text:
        flash("Could not extract text from the document", "error")
        os.remove(temp_path)  # Clean up
        return redirect(url_for("home"))
    
    # Analyze the petition
    analysis_results = analyze_petition(extracted_text)
    
    # Save the document permanently
    permanent_path = os.path.join(app.config["DOCUMENTS_FOLDER"], unique_filename)
    shutil.copy2(temp_path, permanent_path)
    
    # Save to database - convert analysis_results to JSON string
    username = session["username"]
    doc_id = save_document_history(username, original_filename, permanent_path, json.dumps(analysis_results))
    
    # Store the document ID and analysis results in the session for acknowledgment
    session["pending_doc_id"] = doc_id
    session["analysis_results"] = analysis_results
    
    # Clean up temporary file
    os.remove(temp_path)

    # Redirect to the home page with analysis results
    flash("Document analyzed successfully. Please acknowledge to notify departments.", "info")
    return redirect(url_for("home"))

# app.py (No major changes, just ensure the function call is correct)
@app.route("/acknowledge", methods=["POST"])
def acknowledge():
    # Check if user is logged in
    if "username" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    # Get the document ID and analysis results from the session
    doc_id = session.get("pending_doc_id")
    analysis_results = session.get("analysis_results")
    
    if not doc_id or not analysis_results:
        return jsonify({"success": False, "message": "No document to acknowledge"}), 400
    
    # Get user_id from session
    user_id = session.get("user_id")
    if not user_id:
        user_id = get_user_id(session["username"])
        if user_id:
            session["user_id"] = user_id
    
    if user_id:
        # Get document details from the database
        document = get_document_by_id(doc_id)
        if not document:
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        # Extract required fields
        document_name = document["original_filename"]
        file_path = document["file_path"]
        
        # Send emails to relevant departments
        success, sent_departments = send_emails_for_analysis(
            user_id,
            document_name,
            file_path,
            analysis_results
        )
        
        if success:
            # Clear the pending document from the session
            session.pop("pending_doc_id", None)
            session.pop("analysis_results", None)
            return jsonify({"success": True, "message": "Emails sent successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to send emails"}), 500
    else:
        return jsonify({"success": False, "message": "Could not determine user_id for email sending"}), 400
    

# Route to Show Email Notification
@app.route("/email_notification")
def email_notification():
    """Show email notification dialog"""
    # Check if user is logged in
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Get the document ID and analysis results from the session
    doc_id = session.get("pending_doc_id")
    analysis_results = session.get("analysis_results")
    
    if not doc_id or not analysis_results:
        flash("No document to acknowledge", "error")
        return redirect(url_for("home"))
    
    # Get unique departments from analysis results
    departments = set(section.get("department") for section in analysis_results if section.get("department"))
    
    # URL to redirect to after clicking OK
    redirect_url = url_for("view_analysis", doc_id=doc_id)
    
    return render_template("email_notification.html", departments=departments, redirect_url=redirect_url, document_id=doc_id)

# Route to Home Page
@app.route('/')
def home():
    if 'username' in session:
        # Check if there is a pending document to acknowledge
        pending_doc_id = session.get("pending_doc_id")
        analysis_results = session.get("analysis_results")
        
        return render_template('home.html', 
                              username=session['username'], 
                              pending_doc_id=pending_doc_id,
                              analysis_results=analysis_results)
    return redirect(url_for('login'))

# Route to View Document History
@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get user's document history
    documents = get_user_documents(session['username'])
    return render_template('history.html', username=session['username'], documents=documents)

# Route to Download Document
@app.route('/download/<doc_id>')
def download_document(doc_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get document details
    document = get_document_by_id(doc_id)
    if not document:
        flash('Document not found.')
        return redirect(url_for('history'))
    
    # Check if the file exists
    file_path = document['file_path']
    if not os.path.exists(file_path):
        flash('Document file not found.')
        return redirect(url_for('history'))
    
    # Return the file for download
    return send_file(file_path, as_attachment=True, download_name=document['original_filename'])

# Route to View Analysis Results
@app.route('/view_analysis/<doc_id>')
def view_analysis(doc_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get document details
    document = get_document_by_id(doc_id)
    if not document:
        flash('Document not found.')
        return redirect(url_for('history'))
    
    # Extract text from the document
    file_path = document['file_path']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if not os.path.exists(file_path):
        flash('Document file not found.')
        return redirect(url_for('history'))
    
    try:
        petition_text = extract_text(file_path, file_ext)
        
        # Parse the JSON analysis results
        analysis_results_json = document['analysis_results']
        try:
            analysis_results = json.loads(analysis_results_json)
        except json.JSONDecodeError:
            analysis_results = analysis_results_json  # Use as is if not valid JSON
        
        return render_template('home.html', username=session['username'], 
                              petition_text=petition_text, 
                              analysis_results=analysis_results,
                              from_history=True)
    except Exception as e:
        flash(f'Error viewing document: {str(e)}')
        return redirect(url_for('history'))

# Route to Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        full_name = request.form['full_name']
        
        # Validate passwords match
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")
        
        # Register the user
        success, message = register_user(username, password, email, full_name)
        
        if success:
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error=message)
            
    return render_template('signup.html')

# Route to Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = check_user_credentials(username, password)
        if user:
            session['username'] = username
            session['user_id'] = user[0]  # Store user_id in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Route to Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_report():
    try:
        # Get the analysis results and petition text from the form data
        analysis_results = json.loads(request.form.get('analysis_results', '[]'))
        petition_text = request.form.get('petition_text', '')
        
        # Clean the petition text
        # Remove all special characters and emojis
        petition_text = re.sub(r'[^\w\s\u0B80-\u0BFF.,!?;:()\n]', '', petition_text)
        # Remove multiple spaces
        petition_text = re.sub(r'\s+', ' ', petition_text)
        # Remove multiple newlines
        petition_text = re.sub(r'\n+', '\n', petition_text)
        # Strip whitespace
        petition_text = petition_text.strip()
        
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            output_path = temp_file.name

        # Generate the PDF
        generate_pdf(analysis_results, petition_text, output_path)

        # Send the file for download
        return send_file(
            output_path,
            as_attachment=True,
            download_name='petition_analysis_report.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
