import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from IPython.display import HTML, display
import pandas as pd
import re
import random
from faker import Faker
import json

nlp = spacy.load("en_core_web_lg") # Load the English language model
faker = Faker('en_IN') # Initialize Faker and set a seed for reproducibility
Faker.seed(42)

matcher = Matcher(nlp.vocab) # Create a matcher for custom patterns

#Define the 10-Level Redaction Classification System
redaction_levels = {
    1: {'GPE'},
    2: {'GPE', 'ORG'},
    3: {'GPE', 'ORG', 'JOB_TITLE'},
    4: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON'},
    5: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME'},
    6: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME', 'PHONE_NUMBER', 'EMAIL'},
    7: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME', 'PHONE_NUMBER', 'EMAIL', 'DRIVING_LICENSE', 'VOTER_ID'},
    8: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME', 'PHONE_NUMBER', 'EMAIL', 'DRIVING_LICENSE', 'VOTER_ID', 'IFSC_CODE', 'UPI_ID', 'GSTIN'},
    9: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME', 'PHONE_NUMBER', 'EMAIL', 'DRIVING_LICENSE', 'VOTER_ID', 'IFSC_CODE', 'UPI_ID', 'GSTIN', 'BANK_ACCOUNT', 'CREDIT_CARD', 'EPF_NUMBER'},
    10: {'GPE', 'ORG', 'JOB_TITLE', 'PERSON', 'TRANSACTION', 'TIME', 'PHONE_NUMBER', 'EMAIL', 'DRIVING_LICENSE', 'VOTER_ID', 'IFSC_CODE', 'UPI_ID', 'GSTIN', 'BANK_ACCOUNT', 'CREDIT_CARD', 'EPF_NUMBER', 'AADHAAR_NUMBER', 'PAN_NUMBER', 'PASSPORT_NUMBER'}
}

# Function to redact entities based on user-selected level
def selective_redact_text(sample_text, level, custom_tags):
    if level < 1 or level > 10:
        print("Invalid selection. Please choose a level between 1 and 10.") # Ensure the selected level is within the valid range (1 to 10)
        return sample_text
    
    tags_to_redact = redaction_levels[level]
    if custom_tags:
        tags_to_redact = custom_tags

    print(tags_to_redact)
    doc, custom_entities = process_text_with_matcher(nlp, sample_text)
    
    entities_to_replace = [(ent.start_char, ent.end_char, ent.label_, ent.text) for ent in doc.ents if ent.label_ in tags_to_redact]
    entities_to_replace += [(span.start_char, span.end_char, label, span.text) for span, label in custom_entities if label in tags_to_redact]
    
    anonymized_text, replacement_map = anonymize_entities(sample_text, entities_to_replace)
    
    return anonymized_text, replacement_map, entities_to_replace

# Define patterns to avoid organization classification
job_title_pattern = [{"LOWER": {"IN": ["ceo", "cto", "cfo", "coo", "president", "director", "manager", "lead", "head"]}}]
matcher.add("JOB_TITLE", [job_title_pattern])

# Custom identifiers to prevent organization classification
custom_identifier_patterns = [
    [{"LOWER": "pan"}],
    [{"LOWER": "passport"}],
    [{"LOWER": "voter"}],
    [{"LOWER": "driving"}, {"LOWER": "license"}],
    [{"LOWER": "gstin"}],
    [{"LOWER": "epf"}],
    [{"LOWER": "aadhaar"}],
    [{"LOWER": "bank"}, {"LOWER": "account"}],
    [{"LOWER": "ifsc"}, {"LOWER": "code"}],
    [{"LOWER": "credit"}, {"LOWER": "card"}],
    [{"LOWER": "upi"}, {"LOWER": "id"}]
]
matcher.add("CUSTOM_IDENTIFIER", custom_identifier_patterns)

email_pattern = [{"LIKE_EMAIL": True}]
matcher.add("EMAIL", [email_pattern])

pan_pattern = [{"TEXT": {"REGEX": r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"}}]
matcher.add("PAN_NUMBER", [pan_pattern])

passport_pattern = [{"TEXT": {"REGEX": r"^[A-Z][0-9]{7}$"}}]
matcher.add("PASSPORT_NUMBER", [passport_pattern])

voter_id_pattern = [{"TEXT": {"REGEX": r"^[A-Z]{3}[0-9]{7}$"}}]
matcher.add("VOTER_ID", [voter_id_pattern])

driving_license_pattern = [{"TEXT": {"REGEX": r"^[A-Z]{2}-\d{2}-\d{6,7}$"}}]
matcher.add("DRIVING_LICENSE", [driving_license_pattern])

gstin_pattern = [{"TEXT": {"REGEX": r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$"}}]
matcher.add("GSTIN", [gstin_pattern])

epf_pattern = [{"TEXT": {"REGEX": r"^[A-Z]{2}[0-9]{5}[A-Z]{2}[0-9]{7}$"}}]
matcher.add("EPF_NUMBER", [epf_pattern])

time_pattern = [{"TEXT": {"REGEX": r"^\d{1,2}:\d{2}(?:\s?[APap][Mm])?$"}}, {"TEXT": {"REGEX": r"^\d{1,2}(?:\s?[APap][Mm])$"}}]
matcher.add("TIME", [time_pattern])

#money_pattern = [{"TEXT": {"REGEX": r"^[₹$€£]\d+(?:,\d{3})*(?:\.\d{1,2})?$"}}]
#matcher.add("MONEY", [money_pattern])

phone_number_pattern = [{"TEXT": {"REGEX": r"^\d{10}$"}}]
matcher.add("PHONE_NUMBER", [phone_number_pattern])

# Custom patterns for financial information
bank_account_pattern = [{"TEXT": {"REGEX": r"^\d{9,18}$"}}]
matcher.add("BANK_ACCOUNT", [bank_account_pattern])

ifsc_code_pattern = [{"TEXT": {"REGEX": r"^[A-Z]{4}0[A-Z0-9]{6}$"}}]
matcher.add("IFSC_CODE", [ifsc_code_pattern])

debit_credit_card_pattern = [{"TEXT": {"REGEX": r"^\d{4}(?:\s?\d{4}){3}$"}}]
matcher.add("CREDIT_CARD", [debit_credit_card_pattern])

upi_id_pattern = [{"TEXT": {"REGEX": r"^\w+@\w+$"}}]
matcher.add("UPI_ID", [upi_id_pattern])

# Custom patterns for date (including 28/07/2000 format)
date_pattern = [
    {"TEXT": {"REGEX": r"\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2} [A-Za-z]{3,9} \d{4}|\d{1,2} [A-Za-z]{3,9} \d{2,4}|[A-Za-z]{3,9} \d{1,2}, \d{4})\b"}}
]
matcher.add("DATE", [date_pattern])


transaction_details_pattern = [
    {"TEXT": {"REGEX": r"^[₹$€£]?\d+(?:,\d{3})*(?:\.\d{1,2})?$"}},
    {"TEXT": {"REGEX": r"^(on|at|date|time|day)$"}},
]
matcher.add("TRANSACTION", [transaction_details_pattern])

aadhaar_regex = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"

date_context_mapping = {
    # Days
    r'\btomorrow\b': 'in the near future',
    r'\byesterday\b': 'in the recent past',
    r'\btoday\b': 'the current day',
    r'\bday after tomorrow\b': 'in follwing days',
    r'\bday before yesterday\b': 'few days ago',
    
    # Weeks
    r'\bnext week\b': 'the following week',
    r'\blast week\b': 'the previous week',
    r'\bthis week\b': 'the current week',
    r'\bweek after next\b': 'in following weeks',
    r'\bweek before last\b': 'few weeks ago',
    
    # Months
    r'\bnext month\b': 'the following month',
    r'\blast month\b': 'the previous month',
    r'\bthis month\b': 'the current month',
    r'\bmonth after next\b': 'in following months',
    r'\bmonth before last\b': 'few months ago',
    
    # Years
    r'\bnext year\b': 'the following year',
    r'\blast year\b': 'the previous year',
    r'\bthis year\b': 'the current year',
    r'\byear after next\b': 'in following years',
    r'\byear before last\b': 'few years ago',
    
    # General future references
    r'\bsoon\b': 'in the near future',
    r'\bshortly\b': 'in the near future',
    r'\bin the future\b': 'at a later time',
    r'\blater\b': 'at a later time',
    
   
    # General past references
    r'\brecently\b': 'in the recent past',
    r'\blately\b': 'in the recent past',
    r'\bin the past\b': 'previously',
    r'\bpreviously\b': 'at an earlier time',
    r'\ba while ago\b': 'some time ago',
    
    # General phrases for flexibility
    r'\bthis morning\b': 'earlier today',
    r'\bthis evening\b': 'later today',
    r'\blast night\b': 'the previous night',
    r'\btonight\b': 'this evening',
}

def generate_aadhaar_number():
    formats = ["#### #### ####", "####-####-####"]
    selected_format = random.choice(formats)
    return faker.bothify(text=selected_format)
    
file_path = "company_and_government.csv"
df = pd.read_csv(file_path)
company_pool = df['company_names']
government_body_pool = df['government_bodies']

# Function to classify organizations as government or private
def classify_org(org_name):
    government_keywords = ["ministry", "department", "bureau", "commission", "authority", "service", "council", "board", "agency", "office", "secretariat"]
    return any(keyword in org_name.lower() for keyword in government_keywords)

# Function to classify and get replacement for organizations
def get_org_replacement(entity_text):
    if classify_org(entity_text):  # Use the classify_org function to classify as government
        return faker.random_element(government_body_pool)
    else:
        return faker.random_element(company_pool)

def redact_text(text, level):
    # Load the NLP model
    doc = nlp(text)
    
    # Get the entities for the selected redaction level
    entities_to_redact = redaction_levels.get(level, [])

    # Replace the entities
    redacted_text = text
    for ent in doc.ents:
        if ent.label_ in entities_to_redact:
            redacted_text = redacted_text.replace(ent.text, "[REDACTED]")
    
    return redacted_text

def generalize_contextual_dates(text):
    # Replace each contextual date term with its generalized equivalent
    for pattern, replacement in date_context_mapping.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Map entity labels to Faker functions
faker_mapping = {
    "PERSON": lambda: faker.name(),
    "ORG": get_org_replacement,
    "GPE": lambda: faker.city(),
    "DATE": lambda: faker.date(),
   # "MONEY": lambda: f"₹{faker.random_int(min=100, max=1000000):,}",
    "JOB_TITLE": lambda: faker.job(),
    "EMAIL": lambda: faker.email(),
    "PAN_NUMBER": lambda: faker.bothify(text="?????#####?"),
    "PASSPORT_NUMBER": lambda: faker.bothify(text="A#######"),
    "VOTER_ID": lambda: faker.bothify(text="ABC#######"),
    "DRIVING_LICENSE": lambda: faker.bothify(text="KA-##-#######"),
    "GSTIN": lambda: faker.bothify(text="##?????####?#?Z?"),
    "EPF_NUMBER": lambda: faker.bothify(text="TN#####AB######"),
    "TIME": lambda: faker.time(),
    "PHONE_NUMBER": lambda: faker.phone_number(),
    "AADHAAR_NUMBER": generate_aadhaar_number,
    "BANK_ACCOUNT": lambda: faker.bothify(text="##########"),
    "IFSC_CODE": lambda: faker.bothify(text="ABCD0######"),
    "CREDIT_CARD": lambda: faker.credit_card_number(),
    "UPI_ID": lambda: faker.email().replace("@", "@upi"),
    "TRANSACTION": lambda: f"₹{faker.random_int(min=10, max=10000)} on {faker.date()}"
}

def process_text_with_matcher(nlp, text):
    doc = nlp(text)
    matches = matcher(doc)
    custom_entities = []

    # Debugging: print the matches
    print("Matcher matches:")
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        print(f"Match: {span.text}, Label: {label}")
        custom_entities.append((span, label))

    # Process Aadhaar numbers
    aadhaar_matches = re.finditer(aadhaar_regex, text)
    for match in aadhaar_matches:
        start, end = match.span()
        span = doc.char_span(start, end, alignment_mode="expand")
        if span:
            custom_entities.append((span, "AADHAAR_NUMBER"))

    # Custom preprocessing to remove organization tags from custom identifiers
    filtered_ents = []
    for ent in doc.ents:
        # Skip organization tags that conflict with our custom entities
        if ent.label_ == "ORG":
            is_custom_entity = any(
                (custom_ent[0].start <= ent.start < custom_ent[0].end or 
                 custom_ent[0].start < ent.end <= custom_ent[0].end)
                for custom_ent in custom_entities
            )
            if not is_custom_entity:
                filtered_ents.append(ent)
        else:
            filtered_ents.append(ent)

    # Modify the doc's entities to remove conflicting organization tags
    doc.ents = filtered_ents

    return doc, custom_entities

# Entity DataFrame
def create_entity_dataframe(doc, custom_entities):
    entity_data = []

    for ent in doc.ents:
        entity_data.append({
            "Text": ent.text,
            "Label": ent.label_,
            "Description": spacy.explain(ent.label_) if spacy.explain(ent.label_) else "Custom Entity",
            "Start": ent.start_char,
            "End": ent.end_char
        })

    for span, label in custom_entities:
        entity_data.append({
            "Text": span.text,
            "Label": label,
            "Description": "Custom Entity",
            "Start": span.start_char,
            "End": span.end_char
        })

    return pd.DataFrame(entity_data)

# Highlight entities
def highlight_entities(doc, custom_entities):
    color_mapping = {
        "PERSON": "blue",
        "ORG": "green",
        "GPE": "pink",
        "DATE": "coral",
        "MONEY": "blue",
        "JOB_TITLE": "cyan",
        "EMAIL": "gray",
        "PAN_NUMBER": "steelblue",
        "PASSPORT_NUMBER": "brown",
        "VOTER_ID": "orange",
        "DRIVING_LICENSE": "purple",
        "GSTIN": "seagreen",
        "EPF_NUMBER": "grey",
        "TIME": "palegreen",
        "PHONE_NUMBER": "thistle",
        "AADHAAR_NUMBER": "brown",
        "BANK_ACCOUNT": "powderblue",
        "IFSC_CODE": "orchid",
        "CREDIT_CARD": "sandybrown",
        "UPI_ID": "mediumaquamarine",
        "TRANSACTION": "plum"
    }

    html_tokens = []
    last_end = 0

    all_entities = [(ent.start_char, ent.end_char, ent.label_, ent.text) for ent in doc.ents]
    all_entities += [(span.start_char, span.end_char, label, span.text) for span, label in custom_entities]
    all_entities = sorted(all_entities, key=lambda x: x[0])

    for start, end, label, text in all_entities:
        html_tokens.append(doc.text[last_end:start])
        color = color_mapping.get(label, "lightyellow")
        html_tokens.append(f'<mark style="background-color: {color};" title="{label}">{text}</mark>')
        last_end = end

    html_tokens.append(doc.text[last_end:])
    return HTML(''.join(html_tokens))

def anonymize_entities(text, entities):
    replacement_map = {}
    anonymized_text = text

    for start, end, label, entity_text in entities:
        if label in faker_mapping:
            # If the entity is of type "ORG", handle it separately
            if label == "ORG":
                replacement_map[entity_text] = get_org_replacement(entity_text)  # Classify and replace
            else:
                if entity_text not in replacement_map:
                    replacement_map[entity_text] = faker_mapping[label]()
            anonymized_text = anonymized_text.replace(entity_text, replacement_map[entity_text], 1)

    return anonymized_text, replacement_map

# Highlight anonymized text
def highlight_anonymized_text(original_text, replacement_map):
    highlighted_text = original_text
    for original, replacement in replacement_map.items():
        highlighted_text = highlighted_text.replace(
            replacement,
            f'<mark style="background-color: light-green; padding: 0.2em; border-radius: 0.3em;" title="Anonymized">{replacement}</mark>'
        )
    return HTML(highlighted_text)

# Display the replacement map in a DataFrame
def display_replacement_map(replacement_map):
    df = pd.DataFrame(list(replacement_map.items()), columns=["Original Text", "Anonymized Text"])
    display(df)

def randomize_digits_in_numbers_except_dates_times_and_driving_license_and_money(text):
    # Define regex patterns for time, driving license, and money (including rupees)
    time_pattern = r'\b\d{1,2}:\d{2}(:\d{2})?( ?[APap][Mm])?\b'
    
    date_patterns = [
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]{3,9},\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]{3,9}\s+\d{4}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{4}-\d{1,2}-\d{1,2}\b',
        r'\b[A-Za-z]{3,9}\s+\d{1,2},\s+\d{4}\b',
        r'\b[A-Za-z]{3,9}\s+\d{1,2}\s+\d{4}\b',
        r'\b\d{2}-\d{2}-\d{4}\b',
    ]
    date_pattern = '|'.join(date_patterns)

    # Combine all patterns into a single regex
    combined_pattern = f'({time_pattern}|{date_pattern})'

    # Step 1: Find all protected matches in the text
    protected_matches = [match[0] for match in re.finditer(combined_pattern, text) if match[0]]

    # Step 2: Replace protected entities with placeholders to avoid altering them
    placeholder_map = {}
    protected_text = text
    for i, match in enumerate(protected_matches):
        placeholder = f"__PLACEHOLDER_{i}__"
        placeholder_map[placeholder] = match
        protected_text = protected_text.replace(match, placeholder, 1)

    # Step 3: Function to randomize digits in a number while keeping the same length
    def randomize_digits(match):
        number = match.group()
        return ''.join(random.choice('123456789') for _ in number)

    # Step 4: Randomize all numbers except the protected placeholders
    randomized_text = re.sub(r'\b\d+\b', randomize_digits, protected_text)

    # Step 5: Restore the original protected placeholders
    for placeholder, original_value in placeholder_map.items():
        randomized_text = randomized_text.replace(placeholder, original_value)

    # Step 6: Modify only the last two digits of the year part in dates
    def randomize_last_two_digits_of_year(match):
        date_text = match.group()
        # Randomize the last two digits of the year
        randomized_year = re.sub(r'(\d{2})(\d{2})$', lambda m: m.group(1) + ''.join(random.choice('0123456789') for _ in range(2)), date_text)
        return randomized_year

    randomized_text = re.sub(date_pattern, randomize_last_two_digits_of_year, randomized_text)

    return randomized_text
def redact_json(input_json = "" ):
    sample_json = json.loads(input_json)
    texts = []
    level = 4
    if sample_json.get("metadata", {}).get("gradation") != "default":
        level = int(sample_json.get("metadata", {}).get("gradation", 4))
    custom_tags = sample_json.get("metadata", {}).get("custom_tags", [])
# Redact text while preserving the position part
    for entry in sample_json["text"]:
        if 'content' in entry.keys(): 
            entry['content'] = randomize_digits_in_numbers_except_dates_times_and_driving_license_and_money(entry['content'])
            texts.append(" "+entry['content']+" ")
# Process the text and extract entities
    doc, custom_entities = process_text_with_matcher(nlp, json.dumps(texts,ensure_ascii=False))

    print("_________________________________")
    print(custom_tags)
    
    all_entities = [(ent.start_char, ent.end_char, ent.label_, ent.text) for ent in doc.ents]
    all_entities += [(span.start_char, span.end_char, label, span.text) for span, label in custom_entities]
    all_entities = sorted(all_entities, key=lambda x: x[0])
    
    print("Highlighted Text with Entities:") # Display highlighted text with entities
    display(highlight_entities(doc, custom_entities))

    print("\nEntity Table:")
    entity_df = create_entity_dataframe(doc, custom_entities)
    display(entity_df) # Display entities in a table

    sample_text = json.dumps(texts,ensure_ascii=False)  # Indent makes it readable (optional)
    sample_text = sample_text.replace('\"' , '\a')
    print(sample_text)

    anonymized_text, replacement_map, entities_replaced = selective_redact_text(sample_text, level, custom_tags) 

    print("\nHighlighted Anonymized Text:")
    display(highlight_anonymized_text(anonymized_text, replacement_map))

    print("\nReplacement Map:")
    display_replacement_map(replacement_map)
    print("\n\n")
    anonymized_text = anonymized_text.replace('\a','\"')
    print(anonymized_text)
    import ast
    anony_text_list = ast.literal_eval(anonymized_text)
    print(type(anony_text_list))
    for ind , item in enumerate(anony_text_list):
        sample_json["text"][ind]["content"] = anony_text_list[ind]

    anony = json.dumps(sample_json , indent=4,ensure_ascii=False)
    return anony
from rouge_score import rouge_scorer

def evaluate_context_preservation(original_text, anonymized_text):
    # Initialize ROUGE scorer
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(original_text, anonymized_text)

    # Convert scores to readable format
    evaluation_metrics = {
        metric: {
            "Precision": round(scores[metric].precision, 4),
            "Recall": round(scores[metric].recall, 4),
            "F1 Score": round(scores[metric].fmeasure, 4)
        }
        for metric in scores
    }

    return evaluation_metrics

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize

def calculate_bleu_score(reference_text, anonymized_text):
    """
    Calculates BLEU score between reference text and anonymized text.

    Parameters:
    - reference_text (str): The reference "gold standard" anonymized text.
    - anonymized_text (str): The text output by the anonymization script.

    Returns:
    - bleu_score (float): The BLEU score.
    """
    # Tokenize the reference and anonymized texts
    reference_tokens = word_tokenize(reference_text.lower())
    anonymized_tokens = word_tokenize(anonymized_text.lower())

    # Use a smoothing function to handle cases with few matches
    smoothing_function = SmoothingFunction().method1

    # Calculate BLEU score
    bleu_score = sentence_bleu([reference_tokens], anonymized_tokens, smoothing_function=smoothing_function)

    return bleu_score


#----------------------------------------------------------------------------------------------


from flask import Flask, request, jsonify
import json
from final_model_full_code import redact_json

app = Flask(__name__)

@app.route('/redactionprocess', methods=['POST'])
def redact():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        uploaded_file = request.files['file'] # Get the file from the request
        if uploaded_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        file_content = uploaded_file.read().decode('utf-8') # Read file content
        redacted_output = redact_json(file_content)
        return jsonify(json.loads(redacted_output))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
