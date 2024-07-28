# AI-Chat
# AI-Driven Debate Simulation

This project is an AI-driven simulation of a debate between two AI agents, each representing a different view on a controversial topic. The aim is to simulate a constructive discussion and find common ground, reducing sensitivity and fostering understanding between opposing viewpoints.

## Project Structure

The project is organized into the following files and directories:

- `ai.py`: Main script that initializes the debate, handles interactions between AI agents, and generates the debate summary.
- `functionalities/`
  - `__init__.py`: Initialization file for the functionalities module.
  - `generating_content.py`: Contains functions for generating content using the AI models.
  - `sentiment_analysis.py`: Contains functions for performing sentiment analysis on the generated content.
  - `text.py`: Utility functions for text manipulation and formatting.

## Requirements

To run this project, you need to have the following installed:

- Python 3.7 or later
- `textblob` library for sentiment analysis
- `google-generativeai` library for interacting with Google's generative AI models

You can install the required libraries using pip:

```sh
pip install textblob google-generativeai
