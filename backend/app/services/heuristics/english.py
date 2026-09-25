from .base import ScamHeuristicStrategy

# NOTE: this is a starter keyword bank. Phase 1 of the build plan is to
# expand this list using real examples pulled from cybercrime.gov.in
# advisories, RBI fraud alerts, and news coverage — don't ship the hackathon
# demo on this list alone.


class EnglishHeuristics(ScamHeuristicStrategy):
    language_code = "en"

    category_keywords = {
        "UPI Fraud": [
            "collect request", "upi pin", "approve request", "scan qr",
            "cashback", "refund pending", "payment failed", "re-verify upi",
        ],
        "Fake KYC / Bank Update": [
            "kyc", "kyc update", "account will be blocked", "pan card link",
            "aadhaar link", "bank account suspend", "re-kyc", "account frozen",
        ],
        "Courier / Customs Scam": [
            "courier", "parcel", "customs", "illegal items found", "fedex",
            "parcel is held", "delivery failed", "shipment detained",
        ],
        "Lottery / Prize Scam": [
            "lottery", "you have won", "prize money", "you are selected",
            "claim your prize", "lucky draw", "winner announcement",
        ],
        "Job Scam": [
            "work from home", "earn per day", "part time job", "no investment",
            "telegram job", "data entry job", "daily payout",
        ],
        "Digital Arrest Scam": [
            "digital arrest", "cbi", "police case", "linked to a crime",
            "video call verification", "narcotics case", "trai notice",
        ],
    }

    urgency_keywords = [
        "urgent", "immediately", "within 24 hours", "act now",
        "final notice", "account suspended", "legal action", "will be blocked",
    ]
