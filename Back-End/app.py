from flask import Flask, request, jsonify, send_file
from services import (
    check_password_pwned,
    check_account_breaches,
    leakcheck_lookup_email,
    checkphish_scan_email,
    aggregate_url_checks,
    get_cisa_kev,
    get_random_quiz_questions,
    submit_quiz_answers,
    generate_certificate
)
import logging
# ------------ If the frontend and backend  is hosted separately on a different origin, enable CORS in Flask ------------
from flask_cors import CORS 
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ---------------- Password Checker ----------------
@app.route("/api/password/check", methods=["GET", "POST"])
def password_check():
    """
    Check if a password has been compromised in known data breaches.
    Accepts password via query param 'p', form data, or JSON body.
    """
    password = request.args.get("p") or request.form.get("p")
    if not password:
        json_data = request.get_json(silent=True)
        if json_data:
            password = json_data.get("p")
    
    if not password:
        return jsonify({"ok": False, "error": "No password provided"}), 400
    
    result = check_password_pwned(password)
    return jsonify(result)

# ---------------- Account / Email Breach ----------------
@app.route("/api/email/check", methods=["GET", "POST"])
def email_check():
    """
    Check if an email has been involved in data breaches.
    Uses both HIBP and LeakCheck APIs.
    """
    email = request.args.get("email") or request.form.get("email")
    if not email:
        json_data = request.get_json(silent=True)
        if json_data:
            email = json_data.get("email")
    
    if not email:
        return jsonify({"ok": False, "error": "No email provided"}), 400
    
    hibp_result = check_account_breaches(email)
    leak_result = leakcheck_lookup_email(email)
    
    return jsonify({
        "ok": True,
        "email": email,
        "hibp": hibp_result,
        "leakcheck": leak_result
    })

# ---------------- Phishing Email Scan ----------------
@app.route("/api/phish/check", methods=["POST"])
def phish_check():
    """
    Analyze email content for phishing attempts using CheckPhish API.
    Accepts raw email text.
    """
    raw_email = request.form.get("email")
    if not raw_email:
        json_data = request.get_json(silent=True)
        if json_data:
            raw_email = json_data.get("email")
    
    if not raw_email:
        return jsonify({"ok": False, "error": "No email content provided"}), 400
    
    result = checkphish_scan_email(raw_email)
    return jsonify(result)

# ---------------- URL Safety Check ----------------
@app.route("/api/url/check", methods=["GET", "POST"])
def url_check():
    """
    Check if a URL is malicious using multiple sources:
    - Google Safe Browsing
    - PhishTank
    """
    url_to_check = request.args.get("url") or request.form.get("url")
    if not url_to_check:
        json_data = request.get_json(silent=True)
        if json_data:
            url_to_check = json_data.get("url")
    
    if not url_to_check:
        return jsonify({"ok": False, "error": "No URL provided"}), 400
    
    result = aggregate_url_checks(url_to_check)
    return jsonify(result)

# ---------------- CISA KEV Feed ----------------
@app.route("/api/news/cisa", methods=["GET"])
def cisa_news():
    """
    Fetch the latest Known Exploited Vulnerabilities from CISA.
    Returns a comprehensive list of current cybersecurity threats.
    """
    result = get_cisa_kev()
    return jsonify(result)

# ==================== CYBERQUEST QUIZ GAME ====================

@app.route("/api/quiz/start", methods=["POST"])
def start_quiz():
    """
    Start a new quiz session.
    Returns 20 random questions from the pool.
    
    Request body (optional):
    {
        "username": "John Doe",
        "difficulty": "mixed"  // easy, medium, hard, or mixed
    }
    """
    json_data = request.get_json(silent=True) or {}
    username = json_data.get("username", "Anonymous")
    difficulty = json_data.get("difficulty", "mixed")
    
    result = get_random_quiz_questions(num_questions=20, difficulty=difficulty)
    
    if result.get("ok"):
        result["data"]["username"] = username
        logger.info(f"Quiz started for user: {username}")
    
    return jsonify(result)

@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """
    Submit quiz answers and get results.
    
    Request body:
    {
        "username": "John Doe",
        "session_id": "abc123",
        "answers": {
            "1": "A",
            "2": "B",
            ...
        }
    }
    """
    json_data = request.get_json(silent=True)
    
    if not json_data:
        return jsonify({"ok": False, "error": "No data provided"}), 400
    
    username = json_data.get("username", "Anonymous")
    session_id = json_data.get("session_id")
    answers = json_data.get("answers", {})
    
    if not session_id:
        return jsonify({"ok": False, "error": "Session ID required"}), 400
    
    if not answers:
        return jsonify({"ok": False, "error": "No answers provided"}), 400
    
    result = submit_quiz_answers(session_id, answers, username)
    
    if result.get("ok"):
        logger.info(f"Quiz submitted by {username} - Score: {result['data']['score']}/{result['data']['total']}")
    
    return jsonify(result)

@app.route("/api/quiz/certificate/<session_id>", methods=["GET"])
def download_certificate(session_id):
    """
    Generate and download a PDF certificate for a completed quiz.
    Query params:
    - username: Name to appear on certificate (optional)
    """
    username = request.args.get("username", "Anonymous")
    
    result = generate_certificate(session_id, username)
    
    if not result.get("ok"):
        return jsonify(result), 400
    
    pdf_path = result.get("pdf_path")
    
    try:
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'HawkTalos_Certificate_{username.replace(" ", "_")}.pdf'
        )
    except Exception as e:
        logger.exception("Failed to send certificate")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/quiz/questions", methods=["GET"])
def get_quiz_info():
    """
    Get information about available quiz questions (without answers).
    Useful for displaying quiz metadata.
    """
    try:
        from quiz_data import QUIZ_QUESTIONS
        
        question_count = len(QUIZ_QUESTIONS)
        categories = {}
        difficulties = {"easy": 0, "medium": 0, "hard": 0}
        
        for q in QUIZ_QUESTIONS:
            cat = q.get("category", "General")
            categories[cat] = categories.get(cat, 0) + 1
            diff = q.get("difficulty", "medium")
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        return jsonify({
            "ok": True,
            "data": {
                "total_questions": question_count,
                "questions_per_session": 20,
                "categories": categories,
                "difficulties": difficulties
            }
        })
    except Exception as e:
        logger.exception("Failed to get quiz info")
        return jsonify({"ok": False, "error": str(e)}), 500

# ---------------- Health Check ----------------
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "🦅 HawkTalos Backend is running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "password_check": "/api/password/check",
            "email_breach": "/api/email/check",
            "phishing_scan": "/api/phish/check",
            "url_safety": "/api/url/check",
            "cisa_news": "/api/news/cisa",
            "quiz_start": "/api/quiz/start",
            "quiz_submit": "/api/quiz/submit",
            "quiz_certificate": "/api/quiz/certificate/<session_id>",
            "quiz_info": "/api/quiz/questions"
        }
    })

# ---------------- Error Handlers ----------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"ok": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error")
    return jsonify({"ok": False, "error": "Internal server error"}), 500

# ---------------- Main ----------------
if __name__ == "__main__":
    logger.info("Starting HawkTalos Backend...")
    app.run(host="0.0.0.0", port=5000, debug=True)
