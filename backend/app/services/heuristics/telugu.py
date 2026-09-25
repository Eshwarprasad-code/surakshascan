from .base import ScamHeuristicStrategy

# NOTE: starter keyword bank. Expand with real samples in Phase 1.


class TeluguHeuristics(ScamHeuristicStrategy):
    language_code = "te"

    category_keywords = {
        "UPI Fraud": [
            "యూపీఐ పిన్", "కలెక్ట్ రిక్వెస్ట్", "క్యూఆర్ కోడ్ స్కాన్", "క్యాష్‌బ్యాక్",
        ],
        "Fake KYC / Bank Update": [
            "కేవైసీ", "కేవైసీ అప్‌డేట్", "ఖాతా బ్లాక్ అవుతుంది", "ఆధార్ లింక్ చేయండి",
            "పాన్ కార్డ్ లింక్",
        ],
        "Courier / Customs Scam": [
            "పార్శిల్", "కస్టమ్స్", "కొరియర్ నిలిచిపోయింది", "డెలివరీ విఫలమైంది",
        ],
        "Lottery / Prize Scam": [
            "లాటరీ", "మీరు గెలిచారు", "బహుమతి డబ్బు", "మీరు ఎంపికయ్యారు",
        ],
        "Job Scam": [
            "ఇంటి నుండి సంపాదన", "పార్ట్ టైమ్ జాబ్", "రోజువారీ సంపాదన", "పెట్టుబడి లేకుండా",
        ],
        "Digital Arrest Scam": [
            "డిజిటల్ అరెస్ట్", "పోలీస్ కేసు", "సీబీఐ", "నేరం లింక్ అయింది", "వీడియో కాల్ వెరిఫికేషన్",
        ],
    }

    urgency_keywords = [
        "వెంటనే", "ఇప్పుడే చేయండి", "24 గంటల్లో", "ఖాతా బ్లాక్ అవుతుంది",
        "చట్టపరమైన చర్య", "చివరి హెచ్చరిక",
    ]
