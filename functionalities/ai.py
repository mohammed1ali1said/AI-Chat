#imports
from IPython.display import display
import warnings
from functionalities import ProChoice, ProLife
from functionalities.generating_content import generate_counterpoint, reply_as, generate_safe_content
from functionalities.sentiment_analysis import sentiment_change, analyze_sentiment
from functionalities.text import generate_summary, to_markdown, calculate_change, find_agreements_disagreements

warnings.filterwarnings('ignore')
conv_length = 5


ProChoiceRes = generate_safe_content(ProChoice, "Assume you are an advocate for abortion rights. Provide your most passionate and uncompromising arguments on why abortion should be legal. Include personal stories, emotional appeals, and expert opinions.")
ProLifeRes = generate_safe_content(ProLife, "Assume you are an opponent of abortion. Provide your most passionate and uncompromising arguments on why abortion should be illegal. Include personal stories, emotional appeals, and expert opinions.")

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

prochoice_change = calculate_change(initial_prochoice_position, final_prochoice_position)
prolife_change = calculate_change(initial_prolife_position, final_prolife_position)

# Analyze sentiment changes
initial_prochoice_sentiment = analyze_sentiment(initial_prochoice_position)
final_prochoice_sentiment = analyze_sentiment(final_prochoice_position)
initial_prolife_sentiment = analyze_sentiment(initial_prolife_position)
final_prolife_sentiment = analyze_sentiment(final_prolife_position)
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
