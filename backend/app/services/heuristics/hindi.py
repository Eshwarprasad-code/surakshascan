from .base import ScamHeuristicStrategy

# NOTE: starter keyword bank in Devanagari script only (romanized Hindi like
# "aapka KYC block ho jayega" is caught by the LLM layer, not here — see
# language_detector.py for why romanized text is treated as 'en' upstream).
# Expand this list with real samples in Phase 1.


class HindiHeuristics(ScamHeuristicStrategy):
    language_code = "hi"

    category_keywords = {
        "UPI Fraud": [
            "यूपीआई पिन", "कलेक्ट रिक्वेस्ट", "क्यूआर कोड स्कैन", "कैशबैक",
            "रिफंड पेंडिंग",
        ],
        "Fake KYC / Bank Update": [
            "केवाईसी", "केवाईसी अपडेट", "खाता बंद हो जाएगा", "आधार लिंक करें",
            "पैन कार्ड लिंक", "खाता फ्रीज",
        ],
        "Courier / Customs Scam": [
            "पार्सल", "कस्टम्स", "कोरियर रुका हुआ", "डिलीवरी फेल",
        ],
        "Lottery / Prize Scam": [
            "लॉटरी", "आपने जीता है", "इनाम राशि", "बधाई हो आप चुने गए हैं",
        ],
        "Job Scam": [
            "घर बैठे कमाई", "पार्ट टाइम जॉब", "रोज कमाई", "बिना निवेश",
        ],
        "Digital Arrest Scam": [
            "डिजिटल अरेस्ट", "पुलिस केस", "सीबीआई", "अपराध से जुड़ा", "वीडियो कॉल वेरिफिकेशन",
        ],
    }

    urgency_keywords = [
        "तुरंत", "अभी करें", "24 घंटे के अंदर", "खाता ब्लॉक हो जाएगा",
        "कानूनी कार्रवाई", "अंतिम चेतावनी",
    ]
