import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  

HIBP_API_KEY: Optional[str] = os.getenv("HIBP_API_KEY")
LEAKCHECK_API_KEY: Optional[str] = os.getenv("LEAKCHECK_API_KEY")
CHECKPHISH_API_KEY: Optional[str] = os.getenv("CHECKPHISH_API_KEY")
GOOGLE_SAFE_BROWSING_KEY: Optional[str] = os.getenv("GOOGLE_SAFE_BROWSING_KEY")
PHISHTANK_API_KEY: Optional[str] = os.getenv("PHISHTANK_API_KEY")

HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10.0"))

HIBP_PWNED_PASSWORDS_RANGE = "https://api.pwnedpasswords.com/range/{prefix}"
HIBP_ACCOUNT_CHECK = "https://haveibeenpwned.com/api/v3/breachedaccount/{account}"

LEAKCHECK_LOOKUP = "https://leakcheck.io/api/public"
CHECKPHISH_SCAN = "https://developers.bolster.ai/api/neo/scan"
CHECKPHISH_STATUS = "https://developers.bolster.ai/api/neo/scan/status"
GOOGLE_SAFE_BROWSING_LOOKUP = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
PHISHTANK_CHECKURL = "https://checkurl.phishtank.com/checkurl/"
CISA_KEV_JSON = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
