import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from IPython.display import HTML, display
import pandas as pd
import re
import random
from faker import Faker
import json

# Load the English language model
nlp = spacy.load("en_core_web_lg")

# Initialize Faker and set a seed for reproducibility
faker = Faker('en_IN')
Faker.seed(42)

# Create a matcher for custom patterns
matcher = Matcher(nlp.vocab)

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
def selective_redact_text(sample_text, level):
    # Ensure the selected level is within the valid range (1 to 10)
    if level < 1 or level > 10:
        print("Invalid selection. Please choose a level between 1 and 10.")
        return sample_text
    
    # Get the set of tags to be redacted at the selected level
    tags_to_redact = redaction_levels[level]
    
    # Process the text to extract entities
    doc, custom_entities = process_text_with_matcher(nlp, sample_text)
    
    # Create a list of entities to be replaced
    entities_to_replace = [(ent.start_char, ent.end_char, ent.label_, ent.text) 
                           for ent in doc.ents if ent.label_ in tags_to_redact]
    entities_to_replace += [(span.start_char, span.end_char, label, span.text) 
                            for span, label in custom_entities if label in tags_to_redact]
    
    # Generate synthetic replacements only for the selected entities
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
    
file_path = "company_and_government.csv"  # Ensure the file is in the same directory as the script

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

pd.set_option("display.max_rows", None)
df.head(165)

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

