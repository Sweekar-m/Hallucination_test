import os
import sys
import subprocess
from google import genai
import json
from create_action.json_load import save_json_safely
import re
def clean_response(text):
    # Remove markdown code block markers
    text = re.sub(r"```(json)?", "", text).strip()

    # Extract first valid JSON object from the text
    match = re.search(r"\{[\s\S]*?\}", text)
    return match.group() if match else text
def media_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated media control commands*.

🎯 Instructions:
- Match only if the user_input includes clear phrases like:
  - “play music”
  - “pause the song”
  - “mute audio”
  - “open media player”
- These must map to *exact intents* under the correct cluster (media_ops).
- Do NOT infer, assume, or interpret loosely.
- If no intent clearly matches, return unknown confidently.

---

🎯 Intent List (media_ops cluster):

- play_music  
- pause_music  
- next_track  
- previous_track  
- increase_volume  
- decrease_volume  
- mute_audio  
- unmute_audio  
- open_media_player  
- play_video  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "media_ops",
  "intent": "<matched_intent_name>",
  "user_input": "<original_user_input>"
}


'''

    # Append user input to the content
    full_prompt = f"{system_prompt}\n\nuser_input: {user_msg}\nRespond with the correct JSON:"

    client = genai.Client(api_key="AIzaSyA8m0AoPKzANNjn1c6Y0l1WQr0lSzapMMk")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )


    response_text = clean_response(response.text)
    save_json_safely(response_text)