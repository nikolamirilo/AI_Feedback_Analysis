import os
from groq import Groq
import json

client = Groq(api_key="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")

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.json")

with open(file_path, "r") as file:
    feedback_data = json.load(file)

file_input = json.dumps(feedback_data, indent=4)

prompt = {
    "role": "You are HR expert with more than 30 years of experience. You are holding phd in psychology and you are specialized in analyzing feedback reviews.",
    "task": "Read feedback I sent in JSON and rate (1-10) each employee, write suggestions for improvement (be careful, try to notice some subjective/false feedback and don't take it into consideration). Also, I want to know if I should trust them or not (yes/no).",
    "format": "Return data in md table (single table). Columns: 'Name', 'Role', 'Rating', 'Suggestions', 'Trust'. In separate table write feedback which is false/subjective positive or false/subjective negative. Second table columns: 'Name', 'Feedback', 'Type'. In column 'Type' possible values are Subjective Positive/Subjective Negative"
}

chat_completion = client.chat.completions.create(messages=[
    {
        "role": "system",
        "content": f"Role: {prompt["role"]}"
    },
    {
        "role": "user",
        "content": f"Task: {prompt["task"]} Here is the feedback: \n{file_input} | Format: {prompt["format"]}"
    }
],
   model="llama3-8b-8192",
   temperature=0.1
)

response = chat_completion.choices[0].message.content
print("Raw response:")
print(response)

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./results/rtf_feedback.md")

try:
    with open(save_path, "w") as file:
        file.write(response)
    print(f"Successfully saved data to markdown {save_path}")
except Exception as e:
    print("Failed to save response:")
    print(e)