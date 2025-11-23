# quiz_data.py

"""
CyberQuest Quiz Questions Database
50 questions covering various cybersecurity topics
"""

QUIZ_QUESTIONS = [
    # ==================== PHISHING AWARENESS ====================
    {
        "id": 1,
        "category": "Phishing",
        "difficulty": "easy",
        "question": "You receive an email from 'support@amaz0n.com' asking you to verify your account. What should you do?",
        "options": {
            "A": "Click the link and verify immediately",
            "B": "Delete the email - it's likely a phishing attempt",
            "C": "Reply with your account information",
            "D": "Forward it to all your contacts"
        },
        "correct_answer": "B",
        "explanation": "This is a classic phishing attempt. Notice the '0' instead of 'o' in amazon. Always verify sender addresses and never click suspicious links."
    },
    {
        "id": 2,
        "category": "Phishing",
        "difficulty": "medium",
        "question": "Which of the following is NOT a common sign of a phishing email?",
        "options": {
            "A": "Poor grammar and spelling",
            "B": "Urgent or threatening language",
            "C": "Personalized greeting with your name",
            "D": "Suspicious sender email address"
        },
        "correct_answer": "C",
        "explanation": "While phishing emails can sometimes use your name, legitimate personalization is NOT a sign of phishing. Phishers often use generic greetings like 'Dear Customer'."
    },
    {
        "id": 3,
        "category": "Phishing",
        "difficulty": "hard",
        "question": "What is 'spear phishing'?",
        "options": {
            "A": "Phishing attacks targeting fish",
            "B": "Targeted phishing attacks aimed at specific individuals or organizations",
            "C": "Phishing emails with spear images",
            "D": "A type of antivirus software"
        },
        "correct_answer": "B",
        "explanation": "Spear phishing is a highly targeted attack directed at specific individuals or organizations, often using personal information to appear legitimate."
    },
    {
        "id": 4,
        "category": "Phishing",
        "difficulty": "medium",
        "question": "An email claims you've won a prize but need to pay a small fee to claim it. What is this?",
        "options": {
            "A": "A legitimate lottery",
            "B": "An advance-fee scam",
            "C": "A promotional offer",
            "D": "A tax refund"
        },
        "correct_answer": "B",
        "explanation": "This is an advance-fee scam. Legitimate prizes never require payment to claim. These scams trick victims into paying fees for something they'll never receive."
    },
    {
        "id": 5,
        "category": "Phishing",
        "difficulty": "easy",
        "question": "What should you check before clicking a link in an email?",
        "options": {
            "A": "The color of the link",
            "B": "The actual URL by hovering over it",
            "C": "The font size",
            "D": "The number of words in the email"
        },
        "correct_answer": "B",
        "explanation": "Always hover over links to see the actual destination URL before clicking. Scammers often disguise malicious links with legitimate-looking text."
    },

    # ==================== PASSWORD SECURITY ====================
    {
        "id": 6,
        "category": "Password Security",
        "difficulty": "easy",
        "question": "What makes a password strong?",
        "options": {
            "A": "It's your birthday",
            "B": "It's easy to remember like 'password123'",
            "C": "It's long, complex, and unique",
            "D": "It's the same as your username"
        },
        "correct_answer": "C",
        "explanation": "Strong passwords are long (12+ characters), include uppercase, lowercase, numbers, and symbols, and are unique for each account."
    },
    {
        "id": 7,
        "category": "Password Security",
        "difficulty": "medium",
        "question": "What is Two-Factor Authentication (2FA)?",
        "options": {
            "A": "Using two passwords",
            "B": "An additional security layer requiring a second verification method",
            "C": "Logging in from two devices",
            "D": "Having two email accounts"
        },
        "correct_answer": "B",
        "explanation": "2FA adds an extra layer of security by requiring a second form of verification (like a code sent to your phone) in addition to your password."
    },
    {
        "id": 8,
        "category": "Password Security",
        "difficulty": "easy",
        "question": "Should you use the same password for multiple accounts?",
        "options": {
            "A": "Yes, it makes it easier to remember",
            "B": "No, if one account is compromised, all are at risk",
            "C": "Yes, but only for important accounts",
            "D": "It doesn't matter"
        },
        "correct_answer": "B",
        "explanation": "Never reuse passwords. If one account is breached, attackers will try the same credentials on other services (credential stuffing)."
    },
    {
        "id": 9,
        "category": "Password Security",
        "difficulty": "medium",
        "question": "What is a password manager?",
        "options": {
            "A": "A person who remembers your passwords",
            "B": "Software that securely stores and generates passwords",
            "C": "A physical notebook",
            "D": "A type of lock"
        },
        "correct_answer": "B",
        "explanation": "A password manager is a secure tool that stores all your passwords in an encrypted vault and can generate strong, unique passwords for each account."
    },
    {
        "id": 10,
        "category": "Password Security",
        "difficulty": "hard",
        "question": "How often should you change your passwords?",
        "options": {
            "A": "Every week",
            "B": "Every 30 days",
            "C": "Only when you suspect a breach or the service recommends it",
            "D": "Never"
        },
        "correct_answer": "C",
        "explanation": "Modern security guidance recommends changing passwords only when necessary (breach, compromise) rather than on a schedule, as frequent changes can lead to weaker passwords."
    },

    # ==================== MALWARE & RANSOMWARE ====================
    {
        "id": 11,
        "category": "Malware",
        "difficulty": "easy",
        "question": "What is malware?",
        "options": {
            "A": "Software designed to harm or exploit devices",
            "B": "A type of hardware",
            "C": "A good antivirus program",
            "D": "A computer game"
        },
        "correct_answer": "A",
        "explanation": "Malware (malicious software) is any software intentionally designed to cause damage to a computer, server, or network."
    },
    {
        "id": 12,
        "category": "Malware",
        "difficulty": "medium",
        "question": "What is ransomware?",
        "options": {
            "A": "Software that makes your computer faster",
            "B": "Malware that encrypts your files and demands payment",
            "C": "A type of firewall",
            "D": "Free antivirus software"
        },
        "correct_answer": "B",
        "explanation": "Ransomware encrypts your files and demands payment (usually in cryptocurrency) to decrypt them. Never pay the ransom as there's no guarantee of file recovery."
    },
    {
        "id": 13,
        "category": "Malware",
        "difficulty": "easy",
        "question": "What should you do if you suspect malware on your device?",
        "options": {
            "A": "Ignore it",
            "B": "Disconnect from the internet and run antivirus software",
            "C": "Turn off your device permanently",
            "D": "Share files with others"
        },
        "correct_answer": "B",
        "explanation": "Disconnect from the internet to prevent malware from spreading or communicating with attackers, then run a full antivirus scan."
    },
    {
        "id": 14,
        "category": "Malware",
        "difficulty": "hard",
        "question": "What is a 'zero-day' vulnerability?",
        "options": {
            "A": "A bug that was fixed yesterday",
            "B": "A security flaw unknown to software creators that's being exploited",
            "C": "A type of calendar virus",
            "D": "A scheduled maintenance window"
        },
        "correct_answer": "B",
        "explanation": "A zero-day vulnerability is a software flaw that's unknown to the vendor and has no patch available, making it particularly dangerous if exploited."
    },
    {
        "id": 15,
        "category": "Malware",
        "difficulty": "medium",
        "question": "What is a Trojan horse in cybersecurity?",
        "options": {
            "A": "A physical security device",
            "B": "Malware disguised as legitimate software",
            "C": "A type of firewall",
            "D": "An ancient Greek weapon"
        },
        "correct_answer": "B",
        "explanation": "A Trojan horse is malware that appears to be legitimate software but contains malicious code that can harm your system or steal data."
    },

    # ==================== SOCIAL ENGINEERING ====================
    {
        "id": 16,
        "category": "Social Engineering",
        "difficulty": "medium",
        "question": "What is social engineering?",
        "options": {
            "A": "Building social media platforms",
            "B": "Manipulating people to divulge confidential information",
            "C": "A type of software development",
            "D": "Creating social networks"
        },
        "correct_answer": "B",
        "explanation": "Social engineering is the psychological manipulation of people into performing actions or divulging confidential information."
    },
    {
        "id": 17,
        "category": "Social Engineering",
        "difficulty": "easy",
        "question": "A caller claims to be from IT support and asks for your password. What should you do?",
        "options": {
            "A": "Give them your password",
            "B": "Hang up and verify through official channels",
            "C": "Give them half your password",
            "D": "Ask them to wait while you find it"
        },
        "correct_answer": "B",
        "explanation": "Legitimate IT support will never ask for your password. This is a social engineering attack. Always verify through official channels."
    },
    {
        "id": 18,
        "category": "Social Engineering",
        "difficulty": "hard",
        "question": "What is 'pretexting' in cybersecurity?",
        "options": {
            "A": "Writing code before testing",
            "B": "Creating a fabricated scenario to steal information",
            "C": "Sending test emails",
            "D": "Previewing text messages"
        },
        "correct_answer": "B",
        "explanation": "Pretexting is when an attacker creates a fabricated scenario (pretext) to engage a targeted victim and steal their information or access."
    },
    {
        "id": 19,
        "category": "Social Engineering",
        "difficulty": "medium",
        "question": "What is 'tailgating' in physical security?",
        "options": {
            "A": "Following too closely when driving",
            "B": "Following someone through a secure door without authorization",
            "C": "A type of network attack",
            "D": "Monitoring someone's online activity"
        },
        "correct_answer": "B",
        "explanation": "Tailgating is when an unauthorized person follows an authorized person into a restricted area without proper authentication."
    },
    {
        "id": 20,
        "category": "Social Engineering",
        "difficulty": "easy",
        "question": "Why is it dangerous to overshare personal information on social media?",
        "options": {
            "A": "It's not dangerous",
            "B": "Attackers can use it for targeted attacks and identity theft",
            "C": "It uses too much data",
            "D": "It makes your profile too long"
        },
        "correct_answer": "B",
        "explanation": "Personal information shared on social media can be used by attackers to craft convincing phishing attacks, guess security questions, or commit identity theft."
    },

    # ==================== NETWORK SECURITY ====================
    {
        "id": 21,
        "category": "Network Security",
        "difficulty": "easy",
        "question": "Is it safe to use public Wi-Fi for online banking?",
        "options": {
            "A": "Yes, always",
            "B": "No, public Wi-Fi is not secure for sensitive transactions",
            "C": "Only on weekends",
            "D": "Yes, if the network name looks official"
        },
        "correct_answer": "B",
        "explanation": "Public Wi-Fi is often unsecured and can allow attackers to intercept your data. Avoid sensitive transactions on public networks or use a VPN."
    },
    {
        "id": 22,
        "category": "Network Security",
        "difficulty": "medium",
        "question": "What does VPN stand for?",
        "options": {
            "A": "Very Private Network",
            "B": "Virtual Private Network",
            "C": "Verified Public Network",
            "D": "Visual Programming Node"
        },
        "correct_answer": "B",
        "explanation": "VPN stands for Virtual Private Network. It creates an encrypted connection over the internet, protecting your data from eavesdropping."
    },
    {
        "id": 23,
        "category": "Network Security",
        "difficulty": "hard",
        "question": "What is a Man-in-the-Middle (MitM) attack?",
        "options": {
            "A": "When someone stands between two people",
            "B": "When an attacker intercepts communication between two parties",
            "C": "A type of password attack",
            "D": "A physical security breach"
        },
        "correct_answer": "B",
        "explanation": "A Man-in-the-Middle attack occurs when an attacker secretly intercepts and potentially alters communication between two parties who believe they're directly communicating."
    },
    {
        "id": 24,
        "category": "Network Security",
        "difficulty": "medium",
        "question": "What is a firewall?",
        "options": {
            "A": "A physical wall that prevents fires",
            "B": "A security system that monitors and controls network traffic",
            "C": "A type of antivirus",
            "D": "A browser extension"
        },
        "correct_answer": "B",
        "explanation": "A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules."
    },
    {
        "id": 25,
        "category": "Network Security",
        "difficulty": "easy",
        "question": "Should you change the default password on your home router?",
        "options": {
            "A": "No, the default is secure",
            "B": "Yes, default passwords are widely known and insecure",
            "C": "Only if you remember it",
            "D": "It doesn't matter"
        },
        "correct_answer": "B",
        "explanation": "Default router passwords are publicly available and should always be changed immediately. Attackers often target devices with default credentials."
    },

    # ==================== DATA PROTECTION ====================
    {
        "id": 26,
        "category": "Data Protection",
        "difficulty": "easy",
        "question": "What does encryption do?",
        "options": {
            "A": "Makes files smaller",
            "B": "Converts data into a coded format to prevent unauthorized access",
            "C": "Deletes files permanently",
            "D": "Speeds up your computer"
        },
        "correct_answer": "B",
        "explanation": "Encryption converts readable data into an unreadable format that can only be decoded with the correct key, protecting it from unauthorized access."
    },
    {
        "id": 27,
        "category": "Data Protection",
        "difficulty": "medium",
        "question": "What is data backup important for?",
        "options": {
            "A": "Making files load faster",
            "B": "Recovering data after loss, corruption, or ransomware attack",
            "C": "Organizing files",
            "D": "Sharing files with others"
        },
        "correct_answer": "B",
        "explanation": "Regular backups are crucial for recovering your data after hardware failure, accidental deletion, ransomware attacks, or other disasters."
    },
    {
        "id": 28,
        "category": "Data Protection",
        "difficulty": "hard",
        "question": "What is the '3-2-1 backup rule'?",
        "options": {
            "A": "3 computers, 2 monitors, 1 keyboard",
            "B": "3 copies of data, 2 different media types, 1 offsite",
            "C": "Backup every 3 days, 2 times, 1 location",
            "D": "3 passwords, 2 emails, 1 phone"
        },
        "correct_answer": "B",
        "explanation": "The 3-2-1 rule: Keep 3 copies of your data, on 2 different media types, with 1 copy stored offsite. This ensures data resilience."
    },
    {
        "id": 29,
        "category": "Data Protection",
        "difficulty": "easy",
        "question": "What should you do before disposing of an old computer?",
        "options": {
            "A": "Nothing, just throw it away",
            "B": "Securely wipe or destroy the hard drive",
            "C": "Leave all your files on it",
            "D": "Remove the keyboard"
        },
        "correct_answer": "B",
        "explanation": "Always securely wipe or physically destroy storage devices before disposal to prevent data recovery by unauthorized parties."
    },
    {
        "id": 30,
        "category": "Data Protection",
        "difficulty": "medium",
        "question": "What is PII (Personally Identifiable Information)?",
        "options": {
            "A": "Public Internet Interface",
            "B": "Information that can identify an individual",
            "C": "A type of virus",
            "D": "Password Integration Interface"
        },
        "correct_answer": "B",
        "explanation": "PII is any data that could potentially identify a specific individual, such as name, SSN, email, address, or biometric data. It requires special protection."
    },

    # ==================== WEB SECURITY ====================
    {
        "id": 31,
        "category": "Web Security",
        "difficulty": "easy",
        "question": "What does 'HTTPS' indicate?",
        "options": {
            "A": "The website is very fast",
            "B": "The connection between your browser and website is encrypted",
            "C": "The website has high-quality content",
            "D": "The website is popular"
        },
        "correct_answer": "B",
        "explanation": "HTTPS (HTTP Secure) indicates that the connection is encrypted using SSL/TLS, protecting data transmitted between your browser and the website."
    },
    {
        "id": 32,
        "category": "Web Security",
        "difficulty": "medium",
        "question": "What are browser cookies?",
        "options": {
            "A": "Snacks for your computer",
            "B": "Small files stored by websites to remember information about you",
            "C": "Types of viruses",
            "D": "Search engine tools"
        },
        "correct_answer": "B",
        "explanation": "Cookies are small text files stored by websites on your device to remember login status, preferences, and other information. Some can track your activity."
    },
    {
        "id": 33,
        "category": "Web Security",
        "difficulty": "hard",
        "question": "What is Cross-Site Scripting (XSS)?",
        "options": {
            "A": "Copying website content",
            "B": "Injecting malicious scripts into trusted websites",
            "C": "Sharing links between sites",
            "D": "A web design technique"
        },
        "correct_answer": "B",
        "explanation": "XSS is a security vulnerability where attackers inject malicious scripts into web pages viewed by other users, potentially stealing data or hijacking sessions."
    },
    {
        "id": 34,
        "category": "Web Security",
        "difficulty": "easy",
        "question": "Should you download software from unofficial sources?",
        "options": {
            "A": "Yes, it's usually free",
            "B": "No, it may contain malware",
            "C": "Yes, if it looks safe",
            "D": "Only on weekends"
        },
        "correct_answer": "B",
        "explanation": "Only download software from official sources. Unofficial downloads often contain malware, trojans, or other malicious code."
    },
    {
        "id": 35,
        "category": "Web Security",
        "difficulty": "medium",
        "question": "What is 'clickjacking'?",
        "options": {
            "A": "Clicking too many times",
            "B": "Tricking users into clicking something different from what they perceive",
            "C": "A type of mouse",
            "D": "A legitimate advertising technique"
        },
        "correct_answer": "B",
        "explanation": "Clickjacking is an attack where users are tricked into clicking on something different from what they think they're clicking, potentially revealing information or changing settings."
    },

    # ==================== MOBILE SECURITY ====================
    {
        "id": 36,
        "category": "Mobile Security",
        "difficulty": "easy",
        "question": "Should you install apps from unknown sources on your smartphone?",
        "options": {
            "A": "Yes, always",
            "B": "No, only install from official app stores",
            "C": "Only if they're free",
            "D": "Yes, if recommended by strangers"
        },
        "correct_answer": "B",
        "explanation": "Only install apps from official app stores (Google Play, Apple App Store) as they have security vetting processes. Third-party sources often distribute malware."
    },
    {
        "id": 37,
        "category": "Mobile Security",
        "difficulty": "medium",
        "question": "Why should you review app permissions before installing?",
        "options": {
            "A": "It's not necessary",
            "B": "To ensure the app isn't requesting unnecessary access to your data",
            "C": "To make installation faster",
            "D": "It's required by law"
        },
        "correct_answer": "B",
        "explanation": "App permissions should align with functionality. A flashlight app requesting access to contacts is suspicious. Review and limit permissions to protect your data."
    },
    {
        "id": 38,
        "category": "Mobile Security",
        "difficulty": "easy",
        "question": "What should you do if your phone is stolen?",
        "options": {
            "A": "Nothing",
            "B": "Remotely wipe it and report it to your carrier and police",
            "C": "Wait a week to see if it's returned",
            "D": "Buy a new one immediately"
        },
        "correct_answer": "B",
        "explanation": "Immediately use remote wipe features (Find My iPhone, Find My Device), change passwords, notify your carrier, and file a police report."
    },
    {
        "id": 39,
        "category": "Mobile Security",
        "difficulty": "hard",
        "question": "What is 'jailbreaking' or 'rooting' a mobile device?",
        "options": {
            "A": "Charging your phone in prison",
            "B": "Removing manufacturer restrictions to gain full control",
            "C": "A legal requirement",
            "D": "A battery optimization technique"
        },
        "correct_answer": "B",
        "explanation": "Jailbreaking (iOS) or rooting (Android) removes built-in security restrictions, potentially exposing the device to malware and voiding warranties."
    },
    {
        "id": 40,
        "category": "Mobile Security",
        "difficulty": "medium",
        "question": "Why is it important to keep your mobile OS updated?",
        "options": {
            "A": "To get new emojis",
            "B": "Updates patch security vulnerabilities",
            "C": "To make the phone prettier",
            "D": "It's not important"
        },
        "correct_answer": "B",
        "explanation": "OS updates include critical security patches that fix vulnerabilities. Delaying updates leaves your device exposed to known exploits."
    },

    # ==================== GENERAL CYBERSECURITY ====================
    {
        "id": 41,
        "category": "General",
        "difficulty": "medium",
        "question": "What does CIA stand for in cybersecurity?",
        "options": {
            "A": "Central Intelligence Agency",
            "B": "Confidentiality, Integrity, Availability",
            "C": "Computer Internet Access",
            "D": "Cybersecurity Investigation Authority"
        },
        "correct_answer": "B",
        "explanation": "The CIA triad represents the three core principles of information security: Confidentiality, Integrity, and Availability."
    },
    {
        "id": 42,
        "category": "General",
        "difficulty": "easy",
        "question": "What is the first step when you suspect a security breach?",
        "options": {
            "A": "Post about it on social media",
            "B": "Disconnect the device and report it to IT/security team",
            "C": "Ignore it",
            "D": "Try to fix it yourself secretly"
        },
        "correct_answer": "B",
        "explanation": "Immediately disconnect the affected device to prevent spread, then report to your IT or security team. Fast response is crucial in breach situations."
    },
    {
        "id": 43,
        "category": "General",
        "difficulty": "hard",
        "question": "What is a DDoS attack?",
        "options": {
            "A": "A type of password crack",
            "B": "Overwhelming a service with traffic to make it unavailable",
            "C": "A data deletion technique",
            "D": "A network speed optimization"
        },
        "correct_answer": "B",
        "explanation": "Distributed Denial of Service (DDoS) attacks flood a target with traffic from multiple sources, overwhelming it and making it unavailable to legitimate users."
    },
    {
        "id": 44,
        "category": "General",
        "difficulty": "medium",
        "question": "What is security awareness training?",
        "options": {
            "A": "Learning to be aware of your surroundings",
            "B": "Education about recognizing and responding to security threats",
            "C": "Physical fitness training",
            "D": "A type of software"
        },
        "correct_answer": "B",
        "explanation": "Security awareness training educates people about cyber threats and best practices, making them the first line of defense against attacks."
    },
    {
        "id": 45,
        "category": "General",
        "difficulty": "easy",
        "question": "Why is it important to log out of accounts on shared computers?",
        "options": {
            "A": "It's not important",
            "B": "To prevent unauthorized access to your accounts",
            "C": "To save electricity",
            "D": "To make the computer faster"
        },
        "correct_answer": "B",
        "explanation": "Always log out of accounts on shared or public computers to prevent the next user from accessing your personal information or accounts."
    },

    # ==================== EMAIL SECURITY ====================
    {
        "id": 46,
        "category": "Email Security",
        "difficulty": "medium",
        "question": "What is email spoofing?",
        "options": {
            "A": "Sending emails quickly",
            "B": "Forging email headers to make it appear from a trusted source",
            "C": "Archiving old emails",
            "D": "Encrypting emails"
        },
        "correct_answer": "B",
        "explanation": "Email spoofing is forging the sender's address to make an email appear to come from someone else, often used in phishing attacks."
    },
    {
        "id": 47,
        "category": "Email Security",
        "difficulty": "easy",
        "question": "Should you open email attachments from unknown senders?",
        "options": {
            "A": "Yes, always",
            "B": "No, they may contain malware",
            "C": "Only .txt files",
            "D": "Only on Fridays"
        },
        "correct_answer": "B",
        "explanation": "Never open attachments from unknown senders. They often contain malware. Even familiar senders could be compromised, so verify unexpected attachments."
    },
    {
        "id": 48,
        "category": "Email Security",
        "difficulty": "hard",
        "question": "What is BEC (Business Email Compromise)?",
        "options": {
            "A": "Breaking email continuously",
            "B": "A scam targeting businesses via email impersonation",
            "C": "Business email certification",
            "D": "A type of email encryption"
        },
        "correct_answer": "B",
        "explanation": "BEC is a sophisticated scam where attackers impersonate executives or vendors via email to trick employees into transferring money or revealing sensitive information."
    },
    {
        "id": 49,
        "category": "Email Security",
        "difficulty": "medium",
        "question": "What is the purpose of the spam folder?",
        "options": {
            "A": "To store old emails",
            "B": "To automatically filter potentially unwanted or malicious emails",
            "C": "To organize work emails",
            "D": "To save storage space"
        },
        "correct_answer": "B",
        "explanation": "Spam folders automatically filter emails identified as unwanted, suspicious, or potentially malicious based on various criteria and machine learning."
    },
    {
        "id": 50,
        "category": "Email Security",
        "difficulty": "easy",
        "question": "You receive an email with urgent language like 'Act now or your account will be closed!' What should you think?",
        "options": {
            "A": "It's definitely legitimate",
            "B": "It could be a phishing attempt using urgency to bypass critical thinking",
            "C": "Panic and click immediately",
            "D": "Forward it to everyone"
        },
        "correct_answer": "B",
        "explanation": "Urgent or threatening language is a common phishing tactic designed to make you act without thinking. Always verify through official channels."
    }
]

# Helper function to get questions by category
def get_questions_by_category(category: str):
    """Return all questions for a specific category"""
    return [q for q in QUIZ_QUESTIONS if q.get("category") == category]

# Helper function to get questions by difficulty
def get_questions_by_difficulty(difficulty: str):
    """Return all questions for a specific difficulty level"""
    return [q for q in QUIZ_QUESTIONS if q.get("difficulty") == difficulty]

# Statistics
def get_quiz_stats():
    """Return statistics about the quiz question pool"""
    categories = {}
    difficulties = {"easy": 0, "medium": 0, "hard": 0}
    
    for q in QUIZ_QUESTIONS:
        cat = q.get("category", "General")
        categories[cat] = categories.get(cat, 0) + 1
        diff = q.get("difficulty", "medium")
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    return {
        "total_questions": len(QUIZ_QUESTIONS),
        "categories": categories,
        "difficulties": difficulties
    }

if __name__ == "__main__":
    # Print quiz statistics when run directly
    stats = get_quiz_stats()
    print(f"Total Questions: {stats['total_questions']}")
    print(f"\nQuestions by Category:")
    for cat, count in stats['categories'].items():
        print(f"  {cat}: {count}")
    print(f"\nQuestions by Difficulty:")
    for diff, count in stats['difficulties'].items():
        print(f"  {diff.capitalize()}: {count}")
