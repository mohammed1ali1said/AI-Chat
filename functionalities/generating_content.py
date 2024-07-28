from __init__ import ProLife,ProChoice
# Function to generate safe content using the model

def generate_safe_content(model, prompt):
    response = model.generate_content(prompt)
    if response.parts:
        return response.parts[0].text
    else:
        return "The response was blocked or invalid."

# Initial prompts for generating the conversation and role assignment

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
