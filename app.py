import os
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from resume_engine import generate_resume, analyze_resume, extract_text_from_upload, render_resume_pdf, clean_text

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-before-deployment')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'ResumeIQ'})

@app.post('/api/generate')
def api_generate():
    data = request.get_json(silent=True) or {}
    return jsonify({'resume': generate_resume(data), 'created_at': datetime.now().isoformat(timespec='seconds')})

@app.post('/api/analyze')
def api_analyze():
    data = request.get_json(silent=True) or {}
    resume = clean_text(data.get('resume_text', ''))
    if not resume:
        return jsonify({'error': 'Paste a resume or upload a file first.'}), 400
    return jsonify(analyze_resume(resume, clean_text(data.get('job_description', ''))))

@app.post('/api/upload')
def api_upload():
    file = request.files.get('resume_file')
    if not file or not file.filename:
        return jsonify({'error': 'Choose a file to upload.'}), 400
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Supported file types: PDF, DOCX, and TXT.'}), 400
    try:
        content = extract_text_from_upload(file, ext)
    except Exception:
        return jsonify({'error': 'Could not read this file. Try a text-based PDF, DOCX, or TXT file.'}), 400
    if not content.strip():
        return jsonify({'error': 'No readable text found. Try another file or paste the resume text.'}), 400
    return jsonify({'filename': filename, 'text': content})

@app.post('/api/export/pdf')
def api_export_pdf():
    data = request.get_json(silent=True) or {}
    text = clean_text(data.get('resume_text', ''))
    if not text:
        return jsonify({'error': 'There is no resume content to export.'}), 400
    pdf = render_resume_pdf(text, data.get('name', 'Resume'))
    return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='resume.pdf')

@app.post('/api/export/analysis')
def api_export_analysis():
    data = request.get_json(silent=True) or {}
    text = clean_text(data.get('resume_text', ''))
    if not text:
        return jsonify({'error': 'Analyze a resume before exporting results.'}), 400
    analysis = analyze_resume(text, clean_text(data.get('job_description', '')))
    from resume_engine import render_analysis_pdf
    pdf = render_analysis_pdf(analysis)
    return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='resume-analysis.pdf')

@app.errorhandler(413)
def too_large(_error):
    return jsonify({'error': 'File is too large. Maximum upload size is 8 MB.'}), 413

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='127.0.0.1', port=int(os.environ.get('PORT', 5000)))
