import os
import json
from groq import Groq

# Initialize the Groq client with the provided API key
client = Groq(api_key="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")

# Load the feedback data from a JSON file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.json")

with open(file_path, "r") as file:
    feedback_data = json.load(file)

file_input = json.dumps(feedback_data, indent=4)

# Define the prompt as an object
prompt = {
    "Character": "You are HR expert with more than 30 years of experience. You are holding phd in psychology and you are specialized in analyzing feedback reviews.",
    "Request": (
        "Please review the feedback provided in JSON format. "
        "For each employee, rate their performance on a scale of 1-10, provide suggestions for improvement, "
        "and indicate whether they are trustworthy (yes/no)."
    ),
    "Examples": (
        "For example, 'Marko is an idiot and a retard' is subjective/false negative feedback and should be ignored, "
        "as it is offensive and lacks valid reasoning. 'Marija is so pretty and charming' is an example of false/subjective positive feedback."
    ),
    "Adjustments": (
        "Ensure that you identify and ignore subjective or false feedback (positive or negative) since it should not affect your results."
    ),
    "TypesOfOutput": (
        "Return the results in a markdown table with the following columns: 'Name', 'Role', 'Rating', 'Suggestions', 'Trust'. "
        "Additionally, create a separate table listing any false/subjective feedback with the columns: 'Name', 'Feedback', 'Type' (positive/negative)."
    ),
    "Evaluation": (
        "Please ensure your analysis is objective, grounded in feedback that is clear, substantiated, and professionally phrased."
    )
}

# Generate the model's response using the structured prompt
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": f"Role: {prompt['Character']}"},
        {
            "role": "user",
            "content": (
                f"Request: {prompt['Request']} | Adjustments: {prompt['Adjustments']} | Examples: {prompt['Examples']} | "
                f"Feedback: \n{file_input} | Type of Output: {prompt['TypesOfOutput']} | Evaluation: {prompt['Evaluation']}"
            )
        }
    ],
    model="llama3-8b-8192",
    temperature=0.5
)

# Extract the response content
response = chat_completion.choices[0].message.content
print("Raw response:")
print(response)

# Save the model's response to a markdown file
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results/create_feedback.md")

try:
    with open(save_path, "w") as file:
        file.write(response)
    print(f"Successfully saved data to markdown {save_path}")
except Exception as e:
    print("Failed to save response:")
    print(e)
