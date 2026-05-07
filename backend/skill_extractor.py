import re

COMMON_SKILLS = [
    # Tech
    "python", "java", "sql", "machine learning", "data analysis", "linux",
    "tensorflow", "pytorch", "html", "css", "javascript",

    # Marketing
    "marketing", "seo", "content marketing", "social media", "campaign",
    "branding", "google analytics", "consumer insights","retail", "sales", "supervisor", "excel", "data entry",
    "computer", "typing", "operations", "field work",

    # Tools
    "excel", "power bi", "tableau", "mailchimp", "analytics",
    "instagram", "instagram insights", "dash hudson",

    # Business / Soft
    "sales", "negotiation", "crm", "lead generation",
    "communication", "leadership", "management", "collaboration",

    # 🧠 NEW: Education / Healthcare / Social
    "childcare", "early childhood development", "education",
    "teaching", "classroom management", "special needs",
    "patient care", "client care", "counseling",
    "case management", "record management",
    "coordination", "supervision", "volunteer management",
    "behavioral support", "family support"
]


def extract_skills(text):
    text = text.lower()
    found = set()

    # Step 1: match known skills
    for skill in COMMON_SKILLS:
        if skill in text:
            found.add(skill)

    # Step 2: extract capitalized tools (like "Google Analytics", "TikTok")
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)

    for term in capitalized:
        if len(term) > 3:
            found.add(term.lower())

    return list(found)