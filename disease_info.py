"""
Potato Leaf Disease Knowledge Base & Diagnostic Metadata
Contains clinical symptoms, pathogen descriptions, chemical & organic treatments,
and preventive cultural practices for Early Blight, Late Blight, and Healthy leaves.
"""

DISEASE_CLASSES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

DISEASE_DETAILS = {
    "Potato___Early_blight": {
        "display_name": "Potato Early Blight",
        "scientific_name": "Alternaria solani",
        "pathogen_type": "Fungal Ascomycete",
        "risk_level": "High",
        "risk_color": "#f59e0b",  # Amber / Warning
        "badge_color": "bg-amber-100 text-amber-800 border-amber-300",
        "summary": "Fungal infection causing target-like concentric rings on older leaves, leading to premature senescence and yield reduction.",
        "symptoms": [
            "Dark brown to black circular lesions with characteristic concentric ridges (target-board pattern)",
            "Prominent yellow chlorotic halos surrounding lesions",
            "Initial symptoms appear on the oldest (lowest) foliage first",
            "Severe lesions cause leaf curling, necrosis, and premature defoliation",
            "Sunken, dark brown lesions with raised margins on potato stems and tubers"
        ],
        "chemical_treatments": [
            {
                "name": "Chlorothalonil (Bravo / Echo)",
                "type": "Broad-spectrum protectant fungicide",
                "dosage": "1.5 - 2.0 L/ha (or 2-2.5 ml/L water)",
                "application": "Foliar spray every 7-10 days upon first sign of lesions"
            },
            {
                "name": "Mancozeb 75% WP (Dithane M-45)",
                "type": "Contact protectant fungicide (FRAC M03)",
                "dosage": "2.0 - 2.5 kg/ha (2.5 g/L water)",
                "application": "Spray thoroughly on both upper and lower leaf surfaces"
            },
            {
                "name": "Azoxystrobin + Difenoconazole (Amistar Top)",
                "type": "Systemic translaminar fungicide",
                "dosage": "0.5 - 1.0 ml/L water",
                "application": "Apply when disease pressure is moderate to high for curative action"
            }
        ],
        "organic_controls": [
            "Copper Oxychloride / Bordeaux Mixture (1% w/v) as a preventive protective barrier",
            "Foliar spray of Bacillus subtilis (Serenade ASO) bio-fungicide at 3-5 ml/L",
            "Neem seed kernel extract (NSKE 5%) or pure cold-pressed neem oil (5 ml/L with emulsifier)",
            "Trichoderma harzianum or Trichoderma viride biological spray (5 g/L)"
        ],
        "preventive_practices": [
            "Implement a minimum 3-year crop rotation avoiding Solanaceae crops (tomato, eggplant, pepper)",
            "Use certified pathogen-free certified seed tubers",
            "Employ drip or furrow irrigation to minimize canopy wetness duration; avoid evening overhead irrigation",
            "Ensure balanced fertilization: avoid nitrogen deficiency which predisposes older foliage to attack",
            "Remove and incinerate crop residues immediately after harvest to eliminate overwintering spores"
        ],
        "environmental_triggers": "Warm temperatures (24°C - 30°C / 75°F - 86°F) coupled with alternating wet periods (morning dew, light rain) and dry windy days."
    },
    "Potato___Late_blight": {
        "display_name": "Potato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "pathogen_type": "Oomycete (Water Mold)",
        "risk_level": "Critical / Emergency",
        "risk_color": "#ef4444",  # Crimson / Red
        "badge_color": "bg-red-100 text-red-800 border-red-300",
        "summary": "Highly aggressive, destructive water-mold disease capable of wiping out entire potato fields within 7-14 days under cool, humid conditions.",
        "symptoms": [
            "Rapidly expanding, irregular water-soaked dark brown to purplish-black lesions starting from leaf tips and margins",
            "Pale yellow/light green diffuse border surrounding active necrotic patches",
            "Delicate white cottony sporulation visible on the underside of leaves during morning humidity",
            "Rapid collapse, wilting, and complete necrosis of the canopy with a distinctive foul odor",
            "Reddish-brown granular dry rot extending into tuber flesh beneath the skin"
        ],
        "chemical_treatments": [
            {
                "name": "Metalaxyl-M + Mancozeb (Ridomil Gold 68 WG)",
                "type": "Systemic + Contact synergized fungicide",
                "dosage": "2.5 g/L water (2.0 - 2.5 kg/ha)",
                "application": "Apply immediately at disease onset; repeat once after 10-14 days"
            },
            {
                "name": "Cymoxanil + Mancozeb (Curzate M8)",
                "type": "Curative penetrant + protectant",
                "dosage": "2.0 - 2.5 g/L water",
                "application": "Provides 24-48 hours post-infection kickback activity"
            },
            {
                "name": "Dimethomorph or Mandipropamid (Revus)",
                "type": "Anti-oomycete translaminar specialist",
                "dosage": "1.0 ml/L water",
                "application": "Apply during peak vegetative growth under high relative humidity"
            }
        ],
        "organic_controls": [
            "Fixed Copper fungicides (Copper Hydroxide / Copper Octanoate) applied preventively prior to wet spells",
            "Potassium Phosphite (bio-rational elicitor inducing systemic acquired resistance)",
            "Bio-control with Bacillus amyloliquefaciens strain D747",
            "Immediate rogueing: physically dig out and bag infected plants to halt airborne spore showers"
        ],
        "preventive_practices": [
            "Scout fields twice weekly during cool (12°C - 20°C) and humid (>90% RH) weather spells",
            "Plant late-blight resistant potato cultivars (e.g., Sarpo Mira, Defender, Kufri Girdhari)",
            "Destroy all cull piles, volunteer potato plants, and solanaceous weeds near the field",
            "Hill soil well over developing tubers (at least 5-8 cm cover) to prevent spore wash-down",
            "Kill vines chemically or mechanically 2-3 weeks prior to harvesting to prevent tuber infection during digging"
        ],
        "environmental_triggers": "Cool to moderate temperatures (10°C - 20°C / 50°F - 68°F) paired with persistent fog, high relative humidity (>90%), and free water on leaves for >10 hours."
    },
    "Potato___healthy": {
        "display_name": "Healthy Potato Leaf",
        "scientific_name": "Solanum tuberosum",
        "pathogen_type": "None (Pathogen Free)",
        "risk_level": "None / Optimal",
        "risk_color": "#10b981",  # Emerald Green
        "badge_color": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "summary": "Vibrant, vigorously photosynthesizing leaf tissue with uniform chlorophyll distribution and no signs of bacterial, fungal, or oomycete pathology.",
        "symptoms": [
            "Uniform deep emerald green pigmentation across lamina",
            "Crisp, intact leaf margins without necrotic edges or water-soaked patches",
            "Smooth epidermal texture with healthy glandular trichomes (leaf hairs)",
            "Normal turgidity and leaf structure without curling or chlorotic mottling",
            "No mycelial growth, spore pustules, or target lesions observed"
        ],
        "chemical_treatments": [
            {
                "name": "No chemical intervention needed",
                "type": "Maintain prophylactic scouting",
                "dosage": "N/A",
                "application": "Avoid unwarranted chemical applications to preserve beneficial soil and leaf microflora"
            }
        ],
        "organic_controls": [
            "Weekly foliar application of compost tea or seaweed extract for natural plant vigor",
            "Maintain soil organic matter through cover cropping and vermicompost amendments",
            "Prophylactic bio-protective spray of Trichoderma or Bacillus to colonize phyllosphere"
        ],
        "preventive_practices": [
            "Continue calibrated drip irrigation maintaining 65-75% available soil moisture",
            "Conduct routine leaf tissue tests to balance nitrogen, phosphorus, potassium, and magnesium",
            "Monitor for insect vectors (potato aphids, psyllids, leafhoppers) using yellow sticky traps",
            "Maintain adequate plant spacing (25-30 cm in row, 75 cm between rows) for optimum air circulation",
            "Inspect field weekly during cool, moist periods for early anomaly detection"
        ],
        "environmental_triggers": "Optimal growing conditions: 18°C - 24°C daytime temperature, well-drained loamy soil, full sun (6-8 hours daily)."
    }
}
