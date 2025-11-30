# 🦅 HawkTalos - Cybersecurity Awareness Platform

HawkTalos is a comprehensive cybersecurity awareness and education platform that helps users check their security posture, learn about threats, and improve their cyber hygiene through interactive tools and quizzes.

## 🎯 Features

### Security Tools
- **🔐 Password Checker** - Check if your password has been compromised in known data breaches (using k-anonymity)
- **📧 Email Breach Scanner** - Verify if your email appears in breach databases
- **🔗 URL Safety Scanner** - Analyze URLs for phishing and malware threats
- **🚨 CISA KEV Feed** - View latest Known Exploited Vulnerabilities from CISA

### Educational Content
- **🎮 CyberQuest Quiz** - Interactive 20-question quiz on cybersecurity topics
- **🎓 Certification System** - Earn certificates for scoring 80%+ on quizzes

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **Python 3.8+** - Core programming language
- **Requests** - HTTP library for API calls
- **ReportLab** - PDF generation for certificates
- **python-dotenv** - Environment variable management
- **Flask-CORS** - Cross-Origin Resource Sharing support

### Frontend
- **HTML5/CSS3** - Modern semantic markup and styling
- **Vanilla JavaScript** - No framework dependencies
- **Responsive Design** - Mobile-friendly interface
- **Dark Theme** - Eye-friendly dark mode by default

### APIs Integrated
- **Have I Been Pwned (HIBP)** - Password and email breach checking
- **LeakCheck** - Additional breach database
- **Google Safe Browsing** - URL malware/phishing detection
- **PhishTank** - Phishing URL database
- **CheckPhish (Bolster.ai)** - Email phishing analysis
- **CISA KEV** - Known Exploited Vulnerabilities feed

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API calls

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hawktalos.git
cd hawktalos
```

### 2. Create Virtual Environment
```bash

python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:
```env
# API Keys (get these from respective services)
HIBP_API_KEY=your_hibp_api_key_here
LEAKCHECK_API_KEY=your_leakcheck_api_key_here
CHECKPHISH_API_KEY=your_checkphish_api_key_here
GOOGLE_SAFE_BROWSING_KEY=your_google_safe_browsing_key_here
PHISHTANK_API_KEY=your_phishtank_api_key_here

# Optional Configuration
HTTP_TIMEOUT=10.0
```

## 🔑 Getting API Keys

| **HIBP** | 
| **LeakCheck** | 
| **Google Safe Browsing** | 
| **PhishTank** | 
| **CheckPhish** |

> **Note:** The app works with partial API keys. For example, if you only have LeakCheck, email breach checking will still function.

## 📁 Project Structure
```
HawkTalos/
│
├── app.py                 # Main Flask application
├── services.py            # API service integrations
├── config.py              # Configuration management
├── quiz_data.py           # Quiz questions database
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
│
├── GUI/                   # Frontend files
│   ├── index.html        # Main HTML file
│   ├── styles.css        # CSS styling
│   ├── app.js           # JavaScript functionality
│   └── images/          # Image assets
│
└── tests/                # Test files
    └── test_leakcheck.py # API testing script
```

## 🖥️ Usage

### Starting the Application

1. **Start the Backend Server:**
```bash
python app.py
```

The server will start on `http://localhost:5000`

2. **Open the Frontend:**

Open `GUI/index.html` in your web browser, or serve it with a local server:
```bash

python -m http.server 3000

### Using the Features

#### Password Checker
1. Navigate to the Password section
2. Enter a password to check
3. Click "Check Password"
4. View breach status and count

#### Email Breach Scanner
1. Go to Email section
2. Enter an email address
3. Click "Check Breaches"
4. View list of breaches (if any)

#### URL Safety Scanner
1. Navigate to URL section
2. Enter a suspicious URL
3. Click "Scan URL"
4. View safety verdict from multiple sources

#### CyberQuest Quiz
1. Go to Learn section
2. Click "Start Quiz"
3. Answer 20 questions
4. Score 80%+ to unlock certificate
5. Download your personalized certificate


## 🐛 Troubleshooting

### Common Issues

**CORS Errors in Browser**
- Make sure Flask-CORS is installed
- Check that `CORS(app)` is enabled in `app.py`

**API Key Errors**
- Verify `.env` file exists and contains valid keys
- Check API key format (no extra spaces or quotes)
- Ensure API services haven't hit rate limits

**Frontend Not Connecting to Backend**
- Verify Flask server is running on port 5000
- Check `API_BASE` in `app.js` matches your backend URL
- Look for firewall blocking localhost connections

**Certificate Generation Fails**
- Install ReportLab: `pip install reportlab`
- Check write permissions in temp directory

## 📊 API Rate Limits

| Service | Rate Limit | Notes |
|---------|------------|-------|
| HIBP | 10 requests/minute | Per API key |
| LeakCheck | 100/day (free) | Upgradeable |
| Google Safe Browsing | 10,000/day | Per API key |
| PhishTank | 5,000/day | Per API key |
| CISA KEV | Unlimited | Public feed |

## 🔒 Security & Privacy

- **No Password Storage**: Passwords are never stored or logged
- **K-Anonymity**: Password checking uses partial hash matching
- **Local Processing**: Quiz and certificates generated locally
- **HTTPS Ready**: Can be deployed with SSL/TLS
- **No Tracking**: No analytics or user tracking implemented



<p align="center">Built with ❤️ for cybersecurity awareness</p>
<p align="center">🦅 Stay vigilant, stay secure 🦅</p>


