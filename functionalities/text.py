import textwrap
from difflib import SequenceMatcher

from functionalities import Summarizer
from generating_content import generate_safe_content
# Function to format text as Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ')# replace with "return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))" if working in google collab


# Function to categorize disagreements
def categorize_disagreement(prochoice_text, prolife_text):
    categories = {
        'Ethical': 'moral',
        'Legal': 'law',
        'Emotional': 'emotional',
        'Factual': 'fact'
    }
    # Simple categorization example (this could be more sophisticated)
    for category, keyword in categories.items():
        if keyword in prochoice_text.lower() and keyword in prolife_text.lower():
            return category
    return 'General'

# Function to find points of agreement and disagreement
def find_agreements_disagreements(conversation):
    agreements = []
    disagreements = []

    for i in range(1, len(conversation), 2):
        prochoice_text = conversation[i-1]["text"]
        prolife_text = conversation[i]["text"]

        # Check for similar sentences indicating agreement
        matcher = SequenceMatcher(None, prochoice_text, prolife_text)
        match = matcher.find_longest_match(0, len(prochoice_text), 0, len(prolife_text))

        if match.size > 100:  # Threshold for considering it an agreement point
            agreements.append({"ProChoice": prochoice_text, "ProLife": prolife_text})
        else:
            category = categorize_disagreement(prochoice_text, prolife_text)
            disagreements.append({"ProChoice": prochoice_text, "ProLife": prolife_text, "Category": category})

    return agreements, disagreements

# Function to get real-life examples
def get_real_life_examples():
    examples = {
        "ProChoice": [
            "In the landmark case of Roe v. Wade (1973), the U.S. Supreme Court ruled that the constitutional right to privacy extends to a woman's decision to have an abortion.",
            "Many countries, like Canada and most of Europe, have legalized abortion and provide access to safe medical procedures as part of women's health care."
        ],
        "ProLife": [
            "Countries with restrictive abortion laws, like Poland, have seen public outcry and protests due to perceived limitations on women's rights and health.",
            "In the U.S., organizations like the National Right to Life Committee advocate for restrictions on abortion and provide support to women seeking alternatives to abortion."
        ]
    }
    return examples

def calculate_change(initial_text, final_text):
    matcher = SequenceMatcher(None, initial_text, final_text)
    change = 1 - matcher.ratio()
    return change * 100

# Function to generate a summary of the debate
def generate_summary(conversation_history):
    summary_prompt = "Please summarize the following debate between ProChoice and ProLife, including key points, agreements, disagreements, and other relevant information:\n\n"
    for entry in conversation_history:
        summary_prompt += f"{entry['name']}: {entry['text']}\n\n"

    summary = generate_safe_content(Summarizer, summary_prompt)
    return summary
