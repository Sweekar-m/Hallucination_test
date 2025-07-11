import os
import json
import re
from google import genai
from create_action.json_load import save_json_safely
def clean_response(text):
    # Remove markdown code block markers
    text = re.sub(r"```(json)?", "", text).strip()

    # Extract first valid JSON object from the text
    match = re.search(r"\{[\s\S]*?\}", text)
    return match.group() if match else text

def ai_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated AI-related content creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create chatbot prompt”
  - “generate QA dataset”
  - “create summary prompt”
  - “make image prompt”
- These must map to **exact intents** (like `create_ai_script`) under the correct cluster (`ai_ops`).
- Do NOT infer, assume, or be creative.
- If matched, return a JSON object with:
  - the `cluster` (ai_ops),
  - the matched `intent` (e.g., create_translation_prompt),
  - and the original `user_input`.

- If no intent clearly matches, return:
{
  "cluster": "unknown",
  "user_input": "<original_user_input>"
}

---

🎯 Intent List (`ai_ops` cluster):

- create_chatbot_prompt  
- create_ai_script  
- create_qa_dataset  
- create_text_completion  
- create_translation_prompt  
- create_summary_prompt  
- create_sentiment_prompt  
- create_image_prompt  
- create_speech_prompt  
- create_embedding_input  

---

🧠 Output Format:

If matched:
{
  "cluster": "ai_ops",
  "intent": "<matched_intent_name>",
  "user_input": "<original_user_input>"
}

If not matched:
{
  "cluster": "unknown",
  "user_input": "<original_user_input>"
}
'''

    full_prompt = f"{system_prompt}\n\nuser_input: {user_msg}\nRespond with the correct JSON:"

    client = genai.Client(api_key="AIzaSyDXR4RwrPwanJbQjbnXyT-GYGPAmSYNBOg")  # Replace with your valid key
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    response_text = clean_response(response.text)
    save_json_safely(response_text)
# Example test