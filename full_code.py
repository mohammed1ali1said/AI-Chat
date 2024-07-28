#imports
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
from difflib import SequenceMatcher
import random
from textblob import TextBlob


conv_length = 70

# Function to format text as Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return  textwrap.indent(text, '> ')

# Configure the API key for generative AI in our case i used gemini
genai.configure(api_key='AIzaSyDhDW6ygl4n1MfKgZcIjvncn91KsbtonrQ')  # This is my personal API key, please do not give to other people

# Create generative models that represent both sides of the problem
ProChoice = genai.GenerativeModel('gemini-1.5-flash')
ProLife = genai.GenerativeModel('gemini-1.5-flash')
Summarizer = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate safe content using the model
def generate_safe_content(model, prompt):
    response = model.generate_content(prompt)
    if response.parts:
        return response.parts[0].text
    else:
        return "The response was blocked or invalid."

# Initial prompts for generating the conversation and role assignment
ProChoiceRes = generate_safe_content(ProChoice, "Assume you are an advocate for abortion rights. Provide your most passionate and uncompromising arguments on why abortion should be legal. Include personal stories, emotional appeals, and expert opinions.")
ProLifeRes = generate_safe_content(ProLife, "Assume you are an opponent of abortion. Provide your most passionate and uncompromising arguments on why abortion should be illegal. Include personal stories, emotional appeals, and expert opinions.")

# Function to generate a counterpoint from a specific point of view
def generate_counterpoint(name, input_text):
    if name == "ProChoice":
        return generate_safe_content(ProChoice, "Respond with a counterpoint to the following argument from an opponent of abortion: " + input_text)
    elif name == "ProLife":
        return generate_safe_content(ProLife, "Respond with a counterpoint to the following argument from an advocate for abortion rights: " + input_text)

# Function to simulate a reply from a specific persona with more intensity
def reply_as(name, input_text):
    if name == "ProChoice":
        return generate_safe_content(ProChoice, "Respond aggressively to the following arguments from an opponent of abortion: " + input_text + ". Challenge every point with strong counter-arguments, expert views, and emotional appeals.")
    elif name == "ProLife":
        return generate_safe_content(ProLife, "Respond aggressively to the following arguments from an advocate for abortion rights: " + input_text + ". Challenge every point with strong counter-arguments, expert views, and emotional appeals.")

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)

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

# Function to generate a summary of the debate
def generate_summary(conversation_history):
    summary_prompt = "Please summarize the following debate between ProChoice and ProLife, including key points, agreements, disagreements, and other relevant information:\n\n"
    for entry in conversation_history:
        summary_prompt += f"{entry['name']}: {entry['text']}\n\n"

    summary = generate_safe_content(Summarizer, summary_prompt)
    return summary

# Simulate the conversation for the specified number of turns
conversation = [
    {"name": "ProChoice", "text": ProChoiceRes},
    {"name": "ProLife", "text": ProLifeRes}
]
conversation_history = [{"name": "ProChoice", "text": ProChoiceRes}, {"name": "ProLife", "text": ProLifeRes}]



for turn in range(1, conv_length):
    # Alternate turns between ProChoice and ProLife
    if turn % 2 == 0:  # ProChoice's turn
        participant = conversation[0]
        other = conversation[1]
    else:  # ProLife's turn
        participant = conversation[1]
        other = conversation[0]

    other_responses = other["text"]
    reply = reply_as(participant["name"], other_responses)
    counterpoint = generate_counterpoint(participant["name"], other_responses)

    new_conversation = {"name": participant["name"], "text": reply}
    conversation[turn % 2] = new_conversation
    conversation_history.append(new_conversation)

    # Add counterpoint response
    counterpoint_conversation = {"name": participant["name"] + " Counterpoint", "text": counterpoint}
    conversation_history.append(counterpoint_conversation)

    # Check for agreement
    agreements, disagreements = find_agreements_disagreements(conversation_history)
    if len(disagreements) == 0:
        break

# Force a total agreement
if len(disagreements) > 0:
    final_agreement = "After much heated debate, we have come to a consensus that both sides agree on the following points."
    final_agreement += " We believe that a balanced approach considering both the rights of the woman and the unborn child is necessary."
    conversation_history.append({"name": "ProChoice", "text": final_agreement})
    conversation_history.append({"name": "ProLife", "text": final_agreement})



# Calculate the percentage change in positions
initial_prochoice_position = ProChoiceRes
initial_prolife_position = ProLifeRes
final_prochoice_position = conversation_history[-2]["text"]
final_prolife_position = conversation_history[-1]["text"]

def calculate_change(initial_text, final_text):
    matcher = SequenceMatcher(None, initial_text, final_text)
    change = 1 - matcher.ratio()
    return change * 100

prochoice_change = calculate_change(initial_prochoice_position, final_prochoice_position)
prolife_change = calculate_change(initial_prolife_position, final_prolife_position)

# Analyze sentiment changes
initial_prochoice_sentiment = analyze_sentiment(initial_prochoice_position)
final_prochoice_sentiment = analyze_sentiment(final_prochoice_position)
initial_prolife_sentiment = analyze_sentiment(initial_prolife_position)
final_prolife_sentiment = analyze_sentiment(final_prolife_position)

def sentiment_change(initial_sentiment, final_sentiment):
    return (final_sentiment - initial_sentiment) * 100

prochoice_sentiment_change = sentiment_change(initial_prochoice_sentiment, final_prochoice_sentiment)
prolife_sentiment_change = sentiment_change(initial_prolife_sentiment, final_prolife_sentiment)

# Display points of agreement
if agreements:
    display(to_markdown("**Points of Agreement:**"))
    for point in agreements:
        display(to_markdown(f"ProChoice: {point['ProChoice']}\n\nProLife: {point['ProLife']}"))

# Display points of disagreement
if disagreements:
    display(to_markdown("**Points of Disagreement:**"))
    for point in disagreements:
        display(to_markdown(f"ProChoice: {point['ProChoice']}\n\nProLife: {point['ProLife']}\n\nCategory: {point['Category']}"))

# Display final agreement
display(to_markdown("**Final Agreement:**"))
display(to_markdown(final_agreement))

# Generate and display summary
summary = generate_summary(conversation_history)
display(to_markdown("**Summary of the Debate:**"))
display(to_markdown(summary))

# determine the winner
if abs(prochoice_change) > abs(prolife_change):
    winner = "ProChoice"
else:
    winner = "ProLife"

# Display results
print(f"Winner of the debate: {winner}")
print(f"Percentage change in ProChoice position: {prochoice_change:.2f}%")
print(f"Percentage change in ProLife position: {prolife_change:.2f}%")
print(f"Sentiment change for ProChoice: {prochoice_sentiment_change:.2f}%")
print(f"Sentiment change for ProLife: {prolife_sentiment_change:.2f}%")
