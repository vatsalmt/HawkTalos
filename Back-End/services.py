import hashlib
import logging
import requests
import csv
import io
import time
import uuid
import random
from datetime import datetime
from typing import Dict, Any, List
from config import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
HTTP_TIMEOUT = 10  

quiz_sessions = {}

# ------------- HIBP -------------
def check_password_pwned(password: str) -> Dict[str, Any]:
   
    try:
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        url = HIBP_PWNED_PASSWORDS_RANGE.format(prefix=prefix)
        res = requests.get(url, timeout=HTTP_TIMEOUT)
        
        if res.status_code != 200:
            return {"ok": False, "error": f"HIBP returned {res.status_code}"}
        
        for line in res.text.splitlines():
            parts = line.split(":")
            if parts[0] == suffix:
                count = int(parts[1])
                return {
                    "ok": True,
                    "data": {
                        "pwned": True,
                        "count": count,
                        "message": f"⚠️ This password has been seen {count:,} times in data breaches!"
                    }
                }
        
        return {
            "ok": True,
            "data": {
                "pwned": False,
                "count": 0,
                "message": "✓ This password has not been found in known data breaches."
            }
        }
    except Exception as e:
        logger.exception("Error checking pwned password")
        return {"ok": False, "error": str(e)}

def check_account_breaches(account: str) -> Dict[str, Any]:
 
    if not HIBP_API_KEY:
        return {
            "ok": False,
            "error": "HIBP API key not provided; account breach check unavailable."
        }
    
    try:
        headers = {"hibp-api-key": HIBP_API_KEY, "User-Agent": "HawkTalos"}
        url = HIBP_ACCOUNT_CHECK.format(account=account)
        res = requests.get(
            url,
            headers=headers,
            timeout=HTTP_TIMEOUT,
            params={"truncateResponse": "false"}
        )
        
        if res.status_code == 200:
            breaches = res.json()
            return {
                "ok": True,
                "data": {
                    "breached": True,
                    "breach_count": len(breaches),
                    "breaches": breaches
                }
            }
        elif res.status_code == 404:
            return {
                "ok": True,
                "data": {
                    "breached": False,
                    "breach_count": 0,
                    "message": "No breaches found for this account."
                }
            }
        else:
            return {"ok": False, "error": f"HIBP returned {res.status_code}"}
    except Exception as e:
        logger.exception("HIBP account check failed")
        return {"ok": False, "error": str(e)}

# ------------- LeakCheck -------------
def leakcheck_lookup_email(email: str) -> Dict[str, Any]:
    
    try:
      
        params = {
            "key": LEAKCHECK_API_KEY,
            "check": email,
            "type": "email" 
        }
        
        res = requests.get(
            LEAKCHECK_LOOKUP,
            params=params,
            timeout=HTTP_TIMEOUT
        )
        
        if res.status_code == 200:
            data = res.json()
          
            if data.get("success") == True:
                return {"ok": True, "data": data}
            elif data.get("success") == False and data.get("found") == False:
             
                return {
                    "ok": True,
                    "data": {
                        "found": False,
                        "message": "No leaks found for this email."
                    }
                }
            else:
                return {"ok": False, "error": data.get("error", "Unknown error")}
        elif res.status_code == 404:
            return {
                "ok": True,
                "data": {
                    "found": False,
                    "message": "No leaks found for this email."
                }
            }
        else:
            return {"ok": False, "error": f"LeakCheck returned {res.status_code}: {res.text}"}
    except Exception as e:
        logger.exception("LeakCheck lookup failed")
        return {"ok": False, "error": str(e)}

# ------------- CheckPhish -------------
def checkphish_submit_scan(payload: dict) -> Dict[str, Any]:

    try:
        res = requests.post(CHECKPHISH_SCAN, json=payload, timeout=HTTP_TIMEOUT)
        if res.status_code in (200, 201):
            try:
                return {"ok": True, "data": res.json()}
            except ValueError:
                return {"ok": True, "data": res.text}
        else:
            return {"ok": False, "error": f"CheckPhish submit returned {res.status_code}: {res.text}"}
    except Exception as e:
        logger.exception("CheckPhish submit failed")
        return {"ok": False, "error": str(e)}

def checkphish_get_status(payload: dict) -> Dict[str, Any]:

    try:
        res = requests.post(CHECKPHISH_STATUS, json=payload, timeout=HTTP_TIMEOUT)
        if res.status_code in (200, 201):
            try:
                return {"ok": True, "data": res.json()}
            except ValueError:
                return {"ok": True, "data": res.text}
        else:
            return {"ok": False, "error": f"CheckPhish status returned {res.status_code}: {res.text}"}
    except Exception as e:
        logger.exception("CheckPhish status failed")
        return {"ok": False, "error": str(e)}

def checkphish_scan_email(raw_email_text: str,
                          wait_for_result: bool = True,
                          poll_interval: float = 2.0,
                          timeout: float = 30.0) -> Dict[str, Any]:

    if not CHECKPHISH_API_KEY:
        return {"ok": False, "error": "No CheckPhish API key configured (CHECKPHISH_API_KEY)"}

    payload = {
        "apiKey": CHECKPHISH_API_KEY,
        "type": "email",
        "content": raw_email_text
    }

    submit = checkphish_submit_scan(payload)
    if not submit.get("ok"):
        return submit

    data = submit.get("data") or {}
    job_id = data.get("jobID") or data.get("jobId")

    if not job_id:
        return {"ok": True, "data": data}

    if not wait_for_result:
        return {"ok": True, "data": {"jobID": job_id, "raw": data}}

    start = time.time()
    while True:
        status_payload = {"apiKey": CHECKPHISH_API_KEY, "jobID": job_id}
        status_res = checkphish_get_status(status_payload)
        if not status_res.get("ok"):
            return status_res

        status_data = status_res.get("data") or {}
        job_status = (status_data.get("status") or status_data.get("jobStatus") or "").upper()

        if job_status in ("DONE", "COMPLETED", "FINISHED"):
            return {"ok": True, "data": status_data}

        if isinstance(status_data, dict) and any(k in status_data for k in ("verdict", "disposition", "insights")):
            return {"ok": True, "data": status_data}

        if (time.time() - start) > timeout:
            return {"ok": False, "error": "CheckPhish status polling timed out", "jobID": job_id}

        time.sleep(poll_interval)

def checkphish_scan_url(url_to_scan: str, wait_for_result=True, poll_interval=2.0, timeout=30.0) -> Dict[str, Any]:

    if not CHECKPHISH_API_KEY:
        return {"ok": False, "error": "No CheckPhish API key configured (CHECKPHISH_API_KEY)"}
    
    payload = {
        "apiKey": CHECKPHISH_API_KEY,
        "urlInfo": {"url": url_to_scan},
        "scanType": "quick"
    }
    
    submit = checkphish_submit_scan(payload)
    if not submit.get("ok"):
        return submit

    data = submit.get("data") or {}
    job_id = data.get("jobID") or data.get("jobId")
    if not job_id:
        return {"ok": True, "data": data}

    if not wait_for_result:
        return {"ok": True, "data": {"jobID": job_id}}

    start = time.time()
    while True:
        status_payload = {"apiKey": CHECKPHISH_API_KEY, "jobID": job_id}
        status_res = checkphish_get_status(status_payload)
        if not status_res.get("ok"):
            return status_res

        status_data = status_res.get("data") or {}
        job_status = (status_data.get("status") or status_data.get("jobStatus") or "").upper()

        if job_status in ("DONE", "COMPLETED", "FINISHED"):
            return {"ok": True, "data": status_data}

        if isinstance(status_data, dict) and any(k in status_data for k in ("verdict", "disposition", "insights")):
            return {"ok": True, "data": status_data}

        if (time.time() - start) > timeout:
            return {"ok": False, "error": "CheckPhish URL polling timed out", "jobID": job_id}

        time.sleep(poll_interval)

# ------------- Google Safe Browsing -------------
def google_safe_browsing_check(url_to_check: str) -> Dict[str, Any]:

    try:
        if not GOOGLE_SAFE_BROWSING_KEY:
            return {"ok": False, "error": "No Google Safe Browsing API key configured"}
        
        payload = {
            "client": {"clientId": "hawktalos", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url_to_check}],
            },
        }
        
        res = requests.post(
            f"{GOOGLE_SAFE_BROWSING_LOOKUP}?key={GOOGLE_SAFE_BROWSING_KEY}",
            json=payload,
            timeout=HTTP_TIMEOUT
        )
        
        if res.status_code == 200:
            return {"ok": True, "data": res.json()}
        else:
            return {"ok": False, "error": res.text}
    except Exception as e:
        logger.exception("Google Safe Browsing failure")
        return {"ok": False, "error": str(e)}

# ------------- PhishTank (with fallback) -------------
def phishtank_check_url(url_to_check: str) -> Dict[str, Any]:
    """Check if a URL is in PhishTank database."""
    if PHISHTANK_API_KEY:
        try:
            payload = {"url": url_to_check, "format": "json", "app_key": PHISHTANK_API_KEY}
            res = requests.post(PHISHTANK_CHECKURL, data=payload, timeout=HTTP_TIMEOUT)
            
            if res.status_code == 200:
                return {"ok": True, "data": res.json()}
            else:
                return {"ok": False, "error": f"PhishTank returned {res.status_code}: {res.text}"}
        except Exception as e:
            logger.exception("PhishTank API call failed")

    csv_url = "https://data.phishtank.com/data/online-valid.csv"
    try:
        res = requests.get(csv_url, timeout=HTTP_TIMEOUT)
        if res.status_code == 200 and res.text:
            stream = io.StringIO(res.text)
            reader = csv.DictReader(stream)
            for row in reader:
                row_url = row.get("url") or row.get("URL") or row.get("phish_url") or row.get("phish-url")
                if row_url and row_url.strip().lower() == url_to_check.strip().lower():
                    return {"ok": True, "data": {"found": True, "row": row}}
            return {"ok": True, "data": {"found": False}}
    except Exception as e:
        logger.exception("Unable to fetch PhishTank CSV fallback")

    return {"ok": False, "error": "PhishTank unavailable (no API key and CSV fallback failed or blocked)"}

# ------------- Aggregate URL check -------------
def aggregate_url_checks(url_to_check: str) -> Dict[str, Any]:
   
    results = {
        "google_safe_browsing": google_safe_browsing_check(url_to_check),
        "phishtank": phishtank_check_url(url_to_check),
    }

    verdict = "safe"
    threat_types = []

    
    g = results.get("google_safe_browsing", {})
    if g.get("ok") and g.get("data", {}).get("matches"):
        verdict = "malicious"
        for match in g["data"]["matches"]:
            threat_types.append(match.get("threatType", "Unknown"))
    
    p = results.get("phishtank", {})
    if p.get("ok") and p.get("data", {}).get("found") is True:
        verdict = "malicious"
        threat_types.append("PHISHING")
    
    if verdict == "safe":
        if g.get("ok") or p.get("ok"):
            verdict = "safe"
        else:
            verdict = "unknown"

    results["verdict"] = verdict
    results["threat_types"] = list(set(threat_types))
    results["url"] = url_to_check
    
    return {"ok": True, "data": results}

# ------------- CISA KEV feed -------------
def get_cisa_kev() -> Dict[str, Any]:
   
    try:
        res = requests.get(CISA_KEV_JSON, timeout=HTTP_TIMEOUT)
        if res.status_code == 200:
            return {"ok": True, "data": res.json()}
        else:
            return {"ok": False, "error": res.text}
    except Exception as e:
        logger.exception("CISA KEV fetch failed")
        return {"ok": False, "error": str(e)}

# ==================== QUIZ GAME FUNCTIONS ====================

def get_random_quiz_questions(num_questions: int = 20, difficulty: str = "mixed") -> Dict[str, Any]:
  
    try:
        from quiz_data import QUIZ_QUESTIONS
        
        if difficulty != "mixed":
            filtered_questions = [q for q in QUIZ_QUESTIONS if q.get("difficulty") == difficulty]
        else:
            filtered_questions = QUIZ_QUESTIONS
        
        if len(filtered_questions) < num_questions:
            logger.warning(f"Not enough questions for difficulty {difficulty}. Using all available.")
            selected_questions = filtered_questions
        else:
            selected_questions = random.sample(filtered_questions, num_questions)
        
        session_id = str(uuid.uuid4())
        
        questions_for_client = []
        for q in selected_questions:
            questions_for_client.append({
                "id": q["id"],
                "question": q["question"],
                "options": q["options"],
                "category": q.get("category", "General"),
                "difficulty": q.get("difficulty", "medium")
            })
        
        quiz_sessions[session_id] = {
            "questions": selected_questions,
            "started_at": datetime.now().isoformat(),
            "completed": False
        }
        
        return {
            "ok": True,
            "data": {
                "session_id": session_id,
                "questions": questions_for_client,
                "total_questions": len(questions_for_client)
            }
        }
    
    except ImportError:
        return {"ok": False, "error": "Quiz questions not available. quiz_data.py not found."}
    except Exception as e:
        logger.exception("Failed to get quiz questions")
        return {"ok": False, "error": str(e)}

def submit_quiz_answers(session_id: str, answers: Dict[str, str], username: str = "Anonymous") -> Dict[str, Any]:

    try:

        if session_id not in quiz_sessions:
            return {"ok": False, "error": "Invalid session ID"}
        
        session = quiz_sessions[session_id]
        
        if session.get("completed"):
            return {"ok": False, "error": "This quiz has already been submitted"}
        
        questions = session["questions"]
        
        correct_count = 0
        total_count = len(questions)
        detailed_results = []
        
        for question in questions:
            q_id = str(question["id"])
            user_answer = answers.get(q_id, "").strip().upper()
            correct_answer = question["correct_answer"].strip().upper()
            
            is_correct = user_answer == correct_answer
            if is_correct:
                correct_count += 1
            
            detailed_results.append({
                "question_id": q_id,
                "question": question["question"],
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "")
            })
        
        
        score_percentage = (correct_count / total_count * 100) if total_count > 0 else 0
        
        
        if score_percentage < 45:
            performance_tier = "Failed"
            motivational_quote = "Failure is simply the opportunity to begin again, this time more intelligently."
            passed = False
            certificate_available = False
        elif score_percentage < 80:
            performance_tier = "Average"
            motivational_quote = "Good effort! Every click toward awareness counts."
            passed = False
            certificate_available = False
        else:  
            performance_tier = "Passed"
            motivational_quote = "Well done! You've mastered the basics of cybersecurity awareness."
            passed = True
            certificate_available = True
        
        
        session["completed"] = True
        session["completed_at"] = datetime.now().isoformat()
        session["score"] = correct_count
        session["total"] = total_count
        session["percentage"] = score_percentage
        session["passed"] = passed
        session["performance_tier"] = performance_tier
        session["username"] = username
        
        return {
            "ok": True,
            "data": {
                "session_id": session_id,
                "score": correct_count,
                "total": total_count,
                "percentage": round(score_percentage, 2),
                "passed": passed,
                "performance_tier": performance_tier,
                "grade": _calculate_grade(score_percentage),
                "motivational_quote": motivational_quote,
                "results": detailed_results,
                "certificate_available": certificate_available
            }
        }
    
    except Exception as e:
        logger.exception("Failed to submit quiz")
        return {"ok": False, "error": str(e)}

def _calculate_grade(percentage: float) -> str:
    
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"

def generate_certificate(session_id: str, username: str = "Anonymous") -> Dict[str, Any]:

    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        
        if session_id not in quiz_sessions:
            return {"ok": False, "error": "Invalid session ID"}
        
        session = quiz_sessions[session_id]
        
        if not session.get("completed"):
            return {"ok": False, "error": "Quiz not completed yet"}
        
        percentage = session.get("percentage", 0)
        if percentage < 80:
            performance_tier = session.get("performance_tier", "Failed")
            return {
                "ok": False, 
                "error": f"Certificate only available for Passed tier (80%+). Your performance: {performance_tier} ({percentage:.1f}%)"
            }
        
        import tempfile
        
        pdf_filename = f"certificate_{session_id}.pdf"
        
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        c = canvas.Canvas(pdf_path, pagesize=landscape(letter))
        width, height = landscape(letter)
        
        primary_color = HexColor("#1a73e8")
        secondary_color = HexColor("#34a853")
        text_color = HexColor("#202124")
        
        c.setStrokeColor(primary_color)
        c.setLineWidth(3)
        c.rect(0.5*inch, 0.5*inch, width-inch, height-inch)
        
        c.setStrokeColor(secondary_color)
        c.setLineWidth(1)
        c.rect(0.6*inch, 0.6*inch, width-1.2*inch, height-1.2*inch)
        
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(primary_color)
        c.drawCentredString(width/2, height-1.5*inch, "CERTIFICATE OF COMPLETION")
        
        c.setFont("Helvetica", 18)
        c.setFillColor(text_color)
        c.drawCentredString(width/2, height-2*inch, "CyberQuest Security Awareness Training")
        
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-2.8*inch, "This certificate is proudly awarded to")
        
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(secondary_color)
        c.drawCentredString(width/2, height-3.5*inch, username)
        
        c.setFont("Helvetica", 14)
        c.setFillColor(text_color)
        score = session.get("score", 0)
        total = session.get("total", 0)
        percentage = session.get("percentage", 0)
        performance_tier = session.get("performance_tier", "Passed")
        
        c.drawCentredString(
            width/2, height-4.3*inch,
            f"For successfully completing the HawkTalos CyberQuest Challenge"
        )
        c.drawCentredString(
            width/2, height-4.7*inch,
            f"Score: {score}/{total} ({percentage:.1f}%) - Performance: {performance_tier} - Grade: {_calculate_grade(percentage)}"
        )
        
        completed_at = session.get("completed_at", datetime.now().isoformat())
        date_str = datetime.fromisoformat(completed_at).strftime("%B %d, %Y")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height-5.5*inch, f"Date: {date_str}")
        
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(HexColor("#5f6368"))
        c.drawCentredString(width/2, 1*inch, "🦅 HawkTalos - Protecting You Through Awareness")
        c.drawCentredString(width/2, 0.7*inch, f"Session ID: {session_id}")
        
        c.save()
        
        logger.info(f"Certificate generated for {username} (session: {session_id})")
        
        return {
            "ok": True,
            "pdf_path": pdf_path,
            "session_id": session_id,
            "username": username
        }
    
    except ImportError:
        return {
            "ok": False,
            "error": "reportlab library not installed. Install with: pip install reportlab"
        }
    except Exception as e:
        logger.exception("Failed to generate certificate")
        return {"ok": False, "error": str(e)}