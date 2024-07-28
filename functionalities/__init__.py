import google.generativeai as genai

# Configure the API key for generative AI in our case i used gemini
genai.configure(api_key='AIzaSyDhDW6ygl4n1MfKgZcIjvncn91KsbtonrQ')  # This is my personal API key, please do not give to other people

# Create generative models that represent both sides of the problem
ProChoice = genai.GenerativeModel('gemini-1.5-flash')
ProLife = genai.GenerativeModel('gemini-1.5-flash')
Summarizer = genai.GenerativeModel('gemini-1.5-flash')
