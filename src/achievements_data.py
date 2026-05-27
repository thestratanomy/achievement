"""Curated UP/Yogi government achievements data for the Streamlit chatbot."""

CATEGORIES = [
    "Infrastructure",
    "Economy",
    "Industries",
    "Law & Order",
    "Health",
    "Education",
    "Agriculture",
]

_FACTS: dict[str, list[str]] = {
    "Infrastructure": [
        "Purvanchal Expressway (340 km) inaugurated 2021, connecting eastern UP to Lucknow.",
        "Bundelkhand Expressway (296 km) inaugurated 2022, boosting backward region connectivity.",
        "Jewar International Airport (Noida) — Asia's largest greenfield airport under construction.",
        "Metro rail extended in Lucknow, Kanpur, Agra, and Meerut under Yogi government.",
        "Ganga Expressway (594 km) — longest expressway in UP, under construction.",
    ],
    "Economy": [
        "UP GDP grew from ₹12.9 lakh crore (2017) to over ₹24 lakh crore (2024).",
        "Global Investors Summit 2023 attracted ₹33.5 lakh crore in investment proposals.",
        "One District One Product (ODOP) scheme promoted 75 unique local products globally.",
        "UP became India's 2nd largest economy by GSDP, overtaking several larger states.",
        "Ease of Doing Business rank improved from 14th (2017) to 2nd (2022) nationally.",
    ],
    "Industries": [
        "UP Defence Industrial Corridor spans Lucknow-Agra-Aligarh-Kanpur-Jhansi-Chitrakoot.",
        "Defence corridor attracted ₹50,000+ crore in investments and 200+ defence companies.",
        "Data centre capacity expanded: UP became a leading data centre hub in North India.",
        "Semiconductor and electronics manufacturing MoUs signed at GIS 2023.",
        "Gorakhpur AIIMS and fertiliser plant revived after decades, creating local employment.",
    ],
    "Law & Order": [
        "Crime rate dropped significantly: murder cases down 24%, robbery down 65% (2017-2022).",
        "Anti-mafia operations: 100+ criminal syndicates dismantled, assets worth ₹3,000+ crore seized.",
        "Anti-encroachment drive recovered thousands of acres of government land.",
        "UP became one of the safest states for women: Dial 1090 and Mission Shakti expanded.",
    ],
    "Health": [
        "Ayushman Bharat UP: 5.5 crore+ beneficiary cards issued, largest state coverage.",
        "COVID-19 management: UP's tracing, testing, treating model praised nationally.",
        "9 new medical colleges operationalised (2017-2024), adding 1,350+ MBBS seats.",
        "UP eliminated Japanese Encephalitis deaths in Gorakhpur, a decades-long problem.",
    ],
    "Education": [
        "Operation Kayakalp renovated 1.5 lakh+ government school buildings.",
        "UP Board results improved year-on-year; mass cheating completely eliminated.",
        "Atal Residential Schools provide free residential education to orphans and labourers' children.",
        "Digital classrooms and smart boards installed in thousands of government schools.",
    ],
    "Agriculture": [
        "UP became India's largest sugarcane producer; sugar mills cleared dues promptly.",
        "PM-KISAN: 2.7 crore+ farmers in UP received direct benefit transfers.",
        "Irrigation coverage expanded: Saryu Canal project completed benefiting 14 lakh hectares.",
        "MSP procurement of wheat and paddy reached record highs under Yogi government.",
    ],
}


def get_facts(categories: list[str]) -> list[str]:
    """Return curated facts for the given categories.

    Args:
        categories: List of category names. Empty list returns all facts.

    Returns:
        List of achievement facts as strings.
    """
    if not categories:
        return [fact for facts in _FACTS.values() for fact in facts]
    result = []
    for cat in categories:
        result.extend(_FACTS.get(cat, []))
    return result
