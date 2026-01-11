from difflib import get_close_matches

SYMPTOM_DB = {

    
   "yellowing leaves": {
    "diseases": ["Nitrogen Deficiency", "Overwatering", "Early Fungal Infection"],
    "cause": (
        "Yellowing leaves commonly occur due to nitrogen deficiency, "
        "overwatering, poor drainage, root damage, or early signs of fungal infection."
    ),
    "treatment": (
        "Apply nitrogen-rich fertilizer, improve soil drainage, reduce excess watering, "
        "loosen the soil around roots, and check for pests under the leaves."
    ),
    "prevention": (
        "Use balanced fertilizers, avoid waterlogging, improve soil aeration, "
        "and keep a regular watering schedule."
    )
    },

    "leaf spots": {
    "diseases": ["Early Blight", "Bacterial Spot", "Septoria Spot"],
    "cause": (
        "Leaf spots usually appear due to fungal infections like early blight, "
        "bacterial spot, high humidity, or water droplets sitting on leaves."
    ),
    "treatment": (
        "Remove affected leaves immediately, spray copper fungicide, avoid overhead watering, "
        "and increase airflow around the plant."
    ),
    "prevention": (
        "Water at the base, maintain proper spacing, prune lower leaves, and avoid wet foliage."
    )
    },

    "brown spots": {
    "diseases": ["Early Blight", "Septoria Leaf Spot", "Sunburn Damage"],
    "cause": (
        "Brown spots often indicate fungal diseases such as early blight or septoria leaf spot. "
        "It can also be caused by nutrient deficiency or sunburn on tender leaves."
    ),
    "treatment": (
        "Use copper-based fungicide, remove infected leaves, maintain proper spacing, "
        "mulch soil to prevent splash infections, and avoid watering the leaves."
    ),
    "prevention": (
        "Mulch soil, water at the base, rotate crops yearly, and avoid exposing tender leaves to harsh sunlight."
    )
    },

    "black spots": {
    "diseases": ["Bacterial Spot", "Severe Fungal Infection"],
    "cause": (
        "Black spots appear due to bacterial spot or advanced fungal infection. "
        "Often spread by rain, tools, or contact between plants."
    ),
    "treatment": (
        "Remove infected leaves, disinfect tools, spray bactericide/fungicide, "
        "and avoid touching wet leaves."
    ),
    "prevention": (
        "Sanitize tools regularly, avoid overhead watering, increase spacing, and improve airflow."
    )
    },

    "curling leaves": {
    "diseases": ["Leaf Curl Virus", "Whitefly Infestation", "Heat Stress"],
    "cause": (
        "Leaves curl due to viral infection (leaf curl virus), pest attacks (aphids/whiteflies), "
        "heat stress, or nutrient imbalance."
    ),
    "treatment": (
        "Spray neem oil every 3 days, remove heavily infected leaves, keep plant hydrated, "
        "and use organic insecticides to control pests."
    ),
    "prevention": (
        "Use yellow sticky traps, check for insects weekly, protect plants from intense heat, "
        "and maintain balanced fertilization."
    )
   },

   "wilted plant": {
    "diseases": ["Fusarium Wilt", "Root Rot", "Underwatering"],
    "cause": (
        "Wilting is caused by underwatering, root rot, fungal wilt disease, or hot temperatures. "
        "If only one side wilts, it is likely fungal wilt."
    ),
    "treatment": (
        "Water deeply, improve drainage, treat soil with fungicide drench, "
        "and remove plants severely infected by fungal wilt."
    ),
    "prevention": (
        "Avoid waterlogging, rotate crops yearly, sterilize pots/soil, and maintain proper watering."
    )
    },

    "drooping leaves": {
    "diseases": ["Underwatering", "Heat Stress", "Early Wilt"],
    "cause": (
        "Drooping happens due to underwatering, heat stress, root restriction, or sudden shock."
    ),
    "treatment": (
        "Water the plant thoroughly, keep it in shade temporarily, and check roots for decay."
    ),
    "prevention": (
        "Maintain consistent watering, protect the plant from extreme heat, and repot if roots are crowded."
    )
   },


   "holes in leaves": {
    "disease": "Insect/Pest Infestation",
    "cause": (
        "Holes are caused by caterpillars, beetles, leaf-eating worms, snails, "
        "or grasshoppers feeding on the leaves."
    ),
    "treatment": (
        "Spray neem oil, Bacillus thuringiensis (BT) spray, handpick visible pests, "
        "and keep the soil clean."
    ),
    "prevention": (
        "Use neem spray weekly, install yellow sticky traps, maintain clean soil, "
        "and use protective netting to stop insects."
    )
    },

    "white powder on leaves": {
    "disease": "Powdery Mildew",
    "cause": (
        "A white powdery coating caused by fungal infection in humid weather."
    ),
    "treatment": (
        "Spray sulfur fungicide, prune infected leaves, avoid overhead watering, "
        "and improve airflow."
    ),
    "prevention": (
        "Provide proper spacing, water at the base, avoid crowding, and monitor humidity levels."
    )
   },

    "brown edges": {
    "disease": "Leaf Tip Burn",
    "cause": (
        "Browning leaf edges caused by potassium deficiency, excessive heat, "
        "salt buildup in soil, or underwatering."
    ),
    "treatment": (
        "Apply potash fertilizer, ensure consistent watering, flush soil with fresh water, "
        "and offer partial shade."
    ),
    "prevention": (
        "Maintain proper nutrient balance, avoid over-fertilization, water consistently, "
        "and protect plants from harsh sunlight."
    )
    },

# ------------------ TOMATO ------------------

    "tomato leaf curl": {
    "disease": "Tomato Yellow Leaf Curl Virus (TYLCV)",
    "cause": (
        "Viral infection spread by whiteflies causing upward curling and yellowing."
    ),
    "treatment": (
        "Spray neem oil or soap spray, use sticky traps, remove infected plants, "
        "and control whiteflies."
    ),
    "prevention": (
        "Use insect netting, apply neem weekly, grow resistant varieties, "
        "and avoid planting tomatoes repeatedly in same area."
    )
   },

    "tomato early blight": {
    "disease": "Alternaria Early Blight",
    "cause": (
        "Fungal disease causing brown concentric ring spots on older leaves."
    ),
    "treatment": (
        "Spray copper/chlorothalonil fungicide, prune lower leaves, and mulch the soil."
    ),
    "prevention": (
        "Avoid overhead watering, rotate crops yearly, maintain spacing, and use mulch."
    )
    },

    "tomato late blight": {
    "disease": "Phytophthora Late Blight",
    "cause": (
        "A fast-spreading fungal disease causing dark patches and fruit rot."
    ),
    "treatment": (
        "Remove infected leaves immediately, apply strong systemic fungicide, "
        "and destroy infected plants."
    ),
    "prevention": (
        "Avoid wet leaves, use resistant varieties, ensure airflow, and remove debris regularly."
    )
   },

   "tomato mosaic virus": {
    "disease": "Tomato Mosaic Virus (ToMV)",
    "cause": (
        "Highly contagious virus spread through hands, tools, and infected plants."
    ),
    "treatment": (
        "No cure. Remove infected plants and disinfect tools frequently."
    ),
    "prevention": (
        "Sanitize tools, avoid touching plants after smoking, and use resistant tomato varieties."
    )
    },

    "blossom end rot": {
    "disease": "Calcium Deficiency Disorder",
    "cause": (
        "Caused by inconsistent watering and lack of calcium in soil."
    ),
    "treatment": (
        "Spray calcium nitrate and maintain consistent watering schedule."
    ),
    "prevention": (
        "Mulch soil, water regularly, avoid overuse of nitrogen fertilizers."
    )
   },

# ------------------ POTATO ------------------

    "potato early blight": {
    "disease": "Alternaria Early Blight",
    "cause": (
        "Fungal disease causing brown circular rings on older leaves."
    ),
    "treatment": (
        "Spray copper fungicide, prune infected leaves, and rotate crops."
    ),
    "prevention": (
        "Avoid overhead watering, keep foliage dry, fertilize properly, and use mulch."
    )
    },

    "potato late blight": {
    "disease": "Phytophthora Late Blight",
    "cause": (
        "Rapid fungal disease causing leaf collapse and tuber rot."
    ),
    "treatment": (
        "Remove infected leaves, apply systemic fungicide, destroy infected debris."
    ),
    "prevention": (
        "Improve airflow, avoid excess moisture, use resistant varieties, and rotate crops."
    )
    },

    "potato scab": {
    "disease": "Bacterial Potato Scab",
    "cause": (
        "Caused by Streptomyces bacteria in alkaline or dry soil."
    ),
    "treatment": (
        "Maintain soil moisture, acidify soil using sulfur, avoid fresh manure."
    ),
    "prevention": (
        "Keep soil slightly acidic, irrigate properly, plant scab-resistant potato varieties."
    )
    },

    "potato leaf roll": {
    "disease": "Potato Leaf Roll Virus (PLRV)",
    "cause": (
        "Virus spread mainly by aphids; causes upward rolling and yellowing."
    ),
    "treatment": (
        "Control aphids with neem or insecticides; remove infected plants."
    ),
    "prevention": (
        "Use disease-free seeds, control aphids early, and avoid reusing infected tubers."
    )
    },

    "potato wilt": {
    "disease": "Fusarium/Bacterial Wilt",
    "cause": (
        "Fungal or bacterial infection causing wilting and stem browning."
    ),
    "treatment": (
        "Remove infected plants, improve drainage, avoid overwatering, and use clean seeds."
    ),
    "prevention": (
        "Rotate crops, avoid waterlogging, sterilize tools, and check seed quality."
    )
    },

    
    "Pepper__bell___Bacterial_spot": {
        "name": "Pepper Bacterial Spot",
        "symptoms": (
            "Small water-soaked dark spots on leaves, which later turn black or brown. "
            "Leaves may become yellow and drop."
        ),
        "cause": (
            "A bacterial infection caused by Xanthomonas. Spread through rain splash, contaminated tools, "
            "infected seeds, and warm/humid conditions."
        ),
        "treatment": (
            "Remove infected leaves immediately. Apply copper fungicide weekly. "
            "Avoid overhead irrigation and disinfect tools."
        ),
        "prevention": (
            "Use disease-free seeds, space plants properly, keep leaves dry, and rotate crops yearly."
        )
    },

    "Pepper__bell___healthy": {
        "name": "Healthy Bell Pepper Leaf",
        "symptoms": "Green, shiny, smooth leaf surface with no discoloration or lesions.",
        "cause": "Normal, disease-free leaf.",
        "treatment": "No treatment needed. Continue regular watering and fertilization.",
        "prevention": "Maintain good spacing and check for pests weekly."
    },

    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "symptoms": (
            "Brown circular spots with concentric ring patterns (‘bullseye rings’) on older leaves."
        ),
        "cause": (
            "Fungal disease caused by Alternaria solani. "
            "Spreads in warm temperatures, old foliage, and poor nutrition."
        ),
        "treatment": (
            "Remove infected leaves. Spray copper or chlorothalonil fungicide. "
            "Avoid wetting leaves and improve airflow."
        ),
        "prevention": (
            "Use mulch, water at the base, rotate crops yearly, and avoid planting potatoes too densely."
        )
    },

    "Potato___healthy": {
        "name": "Healthy Potato Leaf",
        "symptoms": "Bright green leaf with smooth texture and no spots or wilting.",
        "cause": "No disease present.",
        "treatment": "No action required.",
        "prevention": (
            "Maintain proper soil moisture and fertilize lightly with nitrogen and potassium."
        )
    },

    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "symptoms": (
            "Dark brown irregular patches on leaves. White fuzzy mold appears under leaves in humidity. "
            "Leaves collapse quickly."
        ),
        "cause": (
            "Caused by Phytophthora infestans, the same fungus that caused the Irish Potato Famine. "
            "Thrives in cool, wet weather."
        ),
        "treatment": (
            "Remove severely infected plants. Apply strong systemic fungicides. "
            "Improve ventilation and avoid overhead watering."
        ),
        "prevention": (
            "Grow resistant varieties, space plants properly, and remove diseased debris immediately."
        )
    },

    "Tomato__Target_Spot": {
        "name": "Tomato Target Spot",
        "symptoms": (
            "Brown spots on leaves with concentric ring patterns like a ‘target’. "
            "Severe infection causes yellowing and premature leaf drop."
        ),
        "cause": (
            "Caused by the fungus Corynespora cassiicola. "
            "Favors humid, warm environments and spreads through water splash."
        ),
        "treatment": (
            "Remove infected leaves, apply copper/chlorothalonil fungicides, "
            "and increase airflow around the plant."
        ),
        "prevention": (
            "Avoid overhead watering, prune lower leaves, and use mulch to minimize splash infection."
        )
    },

    "Tomato__Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus (ToMV)",
        "symptoms": (
            "Mosaic yellow-green patterns on leaves, leaf distortion, stunting, "
            "and reduced fruit size."
        ),
        "cause": (
            "A highly contagious virus spread by hands, tools, insects, and infected plants."
        ),
        "treatment": (
            "There is NO cure. Remove infected plants immediately and disinfect tools with bleach."
        ),
        "prevention": (
            "Avoid touching plants after handling tobacco, sanitize tools, and plant resistant varieties."
        )
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "symptoms": (
            "Leaves curl upward, turn yellow, and plant growth becomes stunted."
        ),
        "cause": "Virus spread mainly by whiteflies.",
        "treatment": (
            "Use neem oil or insecticidal soap to control whiteflies. Remove highly infected plants."
        ),
        "prevention": (
            "Use yellow sticky traps, grow resistant varieties, and use insect netting."
        )
    },

    "Tomato_Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "symptoms": (
            "Small water-soaked spots that turn brown. Leaves may yellow and drop early."
        ),
        "cause": "Caused by Xanthomonas bacteria.",
        "treatment": (
            "Spray copper fungicide. Avoid touching wet leaves. Remove and destroy infected material."
        ),
        "prevention": (
            "Use certified seeds, rotate crops yearly, avoid overhead irrigation."
        )
    },

    "Tomato_Early_blight": {
        "name": "Tomato Early Blight",
        "symptoms": (
            "Brown circular leaf spots with concentric rings on older leaves."
        ),
        "cause": "Fungal disease caused by Alternaria solani.",
        "treatment": (
            "Spray copper or chlorothalonil fungicides, prune lower leaves, and water only at the base."
        ),
        "prevention": (
            "Use mulch, maintain spacing, rotate crops, and avoid overcrowding."
        )
    },

    "Tomato_healthy": {
        "name": "Healthy Tomato Leaf",
        "symptoms": "Vibrant green leaf with no fungal spots or yellowing.",
        "cause": "Healthy plant with no disease.",
        "treatment": "No treatment required.",
        "prevention": (
            "Regular pruning, balanced fertilization, and pest monitoring."
        )
    },

    "Tomato_Late_blight": {
        "name": "Tomato Late Blight",
        "symptoms": (
            "Dark, oily-looking patches on leaves. White fuzzy mold under leaves. "
            "Rapid leaf collapse."
        ),
        "cause": "Caused by Phytophthora infestans fungus.",
        "treatment": (
            "Remove infected leaves, apply strong systemic fungicides, and keep foliage dry."
        ),
        "prevention": (
            "Improve ventilation, avoid overhead watering, and remove debris after harvest."
        )
    },

    "Tomato_Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "symptoms": (
            "Yellow spots on leaf tops, olive green or gray fuzzy mold underneath."
        ),
        "cause": "Caused by Passalora fulva fungus in humid conditions.",
        "treatment": (
            "Increase ventilation, remove affected leaves, and apply fungicides."
        ),
        "prevention": (
            "Avoid overcrowding, use drip irrigation, and keep greenhouse humidity low."
        )
    },

    "Tomato_Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "symptoms": (
            "Tiny circular spots with dark borders and light centers. "
            "Usually starts on lower leaves."
        ),
        "cause": "Caused by Septoria lycopersici fungus.",
        "treatment": (
            "Remove infected leaves, apply copper fungicide, and avoid wet foliage."
        ),
        "prevention": (
            "Mulch soil, water at base, rotate crops, and prune regularly."
        )
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "name": "Spider Mite Infestation",
        "symptoms": (
            "Tiny yellow or white speckles on leaves. Fine webbing under the leaves. "
            "Leaves may dry and fall."
        ),
        "cause": "Caused by two-spotted spider mites sucking plant sap.",
        "treatment": (
            "Spray neem oil every 3 days, wash leaves with water spray, and increase humidity."
        ),
        "prevention": (
            "Keep plants well-watered, avoid dusty environments, and use predatory mites."
        )
    },



}
SYMPTOM_SYNONYMS = {

   
    "yellowing leaves": [
        "yellow leaves", "leaves turning yellow", "pale leaves", "yellow colour leaves",
        "light yellow leaves", "yellowing", "yellow spots on leaves",
        "my leaves are yellow", "leaf turning pale", "yellow patches",
        "yellowish leaves", "faded leaves", "chlorosis"
    ],

    "leaf spots": [
        "spots on leaves", "black spots", "brown patches", "spotting on leaves",
        "dark spots", "small spots", "tiny dots on leaves", "patches on leaves",
        "brown dots", "black dots", "round spots", "lots of spots on leaves",
        "leaf spot", "spotted leaves", "my plant has spots"
    ],

    "brown spots": [
        "brown patches", "brown dots", "brownish marks", "dark brown spots",
        "brown circles", "brown lesions", "brown marks", "brown stain",
        "dry brown patches", "potato brown spot", "tomato brown spots",
        "brown patches on leaves"
    ],

    "black spots": [
        "black dots", "black marks", "black patches", "small black spots",
        "dark black circles", "black stains", "my leaves becoming black"
    ],

    "curling leaves": [
        "leaf curl", "leaves are curling", "curled leaves", "rolled leaves",
        "twisted leaves", "shriveled leaves", "leaf rolling", "leaf folding",
        "my leaves are folding", "wrinkled leaves"
    ],

    "wilted plant": [
        "wilt", "wilting", "completely drooping", "my plant is dying",
        "weak plant", "shrinked plant", "collapsed plant", "leaves hanging down",
        "plant bending", "not standing straight"
    ],

    "drooping leaves": [
        "droopy leaves", "leaves hanging down", "soft leaves", "weak leaves",
        "falling leaves", "hanging leaves", "leaves downwards"
    ],

    "holes in leaves": [
        "eaten leaves", "insects eating leaves", "holes", "chewed leaves",
        "destroyed leaves", "bite marks", "leaf damaged by insects",
        "worms eating leaves", "caterpillar damage"
    ],

    "white powder on leaves": [
        "white dust", "white powder", "powdery coating", "white layer",
        "ash-like powder", "white fungus", "white spots on leaves",
        "powder on leaves", "chalky appearance"
    ],

    "brown edges": [
        "leaf edges turning brown", "dry edges", "burnt edges", "edges dried",
        "brown border", "leaf tips brown", "crispy edges", "dry leaf tips"
    ],

    # TOMATO SYMPTOMS 
    "tomato leaf curl": [
        "tomato leaves curled", "tomato leaf bending", "leaf upward curl",
        "curl virus", "tomato curled leaves", "tomato leaf folding",
        "tomato leaf rolled", "whitefly problem on tomato"
    ],

    "tomato early blight": [
        "tomato brown rings", "target spot tomato", "brown circular spots tomato",
        "tomato blight early", "alternaria tomato", "old tomato leaves spots",
        "ring pattern tomato leaves"
    ],

    "tomato late blight": [
        "tomato black patches", "wet brown patches tomato", "tomato leaves collapsing",
        "fast spreading tomato disease", "late blight tomato", "phytophthora tomato",
        "dark tomato leaf patches"
    ],

    "tomato mosaic virus": [
        "tomato mosaic", "mosaic pattern leaves", "light and dark patches",
        "twisted tomato leaves", "virus tomato", "TMV", "tomato leaf distortion",
        "mosaic tomato leaves"
    ],

    "blossom end rot": [
        "tomato bottom black", "black spot on tomato bottom", "end rot tomato",
        "tomato turning black", "tomato fruit base rot", "bottom rot"
    ],

   
    "potato early blight": [
        "potato brown rings", "potato leaf spots", "alternaria potato",
        "brown circular marks potato", "potato blight early"
    ],

    "potato late blight": [
        "potato leaf collapse", "black patches potato", "wet black spots potato",
        "fast disease potato", "late blight potato", "phytophthora potato"
    ],

    "potato scab": [
        "rough potato skin", "potato surface dry", "potato skin disease",
        "patchy potato surface", "corky spots on potato"
    ],

    "potato leaf roll": [
        "potato leaves rolled", "potato leaf curling upward", "leaf roll virus potato",
        "rolled leaves potato", "potato upward curl"
    ],

    "potato wilt": [
        "potato plant drooping", "potato stem turning brown", "potato drying",
        "wilt potato", "potato leaves yellow then dry", "potato suddenly died"
    ]
}




def check_symptom(user_text):
    """
    Improved symptom detection:
    - Detects color + spot patterns (brown spots, dark spots, yellow patches)
    - Detects single-word variations (spot, spots, spotting)
    - Detects plant + symptom combinations
    - Still safe: does NOT guess diseases when unclear
    """
    user_text = user_text.strip().lower()
    matched = []

   
    synonyms = {
        "leaf spots": ["leaf spot", "spots", "spotting", "brown spots", "dark spots", "circular spots"],
        "yellowing leaves": ["yellow leaves", "yellowing", "pale leaves", "leaves turned yellow", "leaf yellowing", "yellowing"],
        "wilting": ["wilt", "wilting leaves", "drooping"],
        "dry leaves": ["dry", "dryness", "crispy leaves"],
        "holes in leaves": ["holes", "chewed leaves", "eaten leaves"],
    }

    
    keyword_map = {}
    for main_symptom, syns in synonyms.items():
        for s in syns:
            keyword_map[s] = main_symptom
    
    for key in SYMPTOM_DB.keys():
        keyword_map[key] = key

    
    keyword_list = sorted(keyword_map.keys(), key=len, reverse=True)

    
    for key in keyword_list:
        if key in user_text:
            true_symptom = keyword_map[key]
            matched.append({true_symptom: SYMPTOM_DB[true_symptom]})
            return matched

    
    from difflib import get_close_matches
    close = get_close_matches(user_text, SYMPTOM_DB.keys(), n=1, cutoff=0.70)
    if close:
        s = close[0]
        matched.append({s: SYMPTOM_DB[s]})
        return matched

    
    return []  