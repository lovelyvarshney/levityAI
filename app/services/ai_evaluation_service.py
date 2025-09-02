import requests 
import json
from app.utils.config import OPENAI_API_KEY

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def evaluate_message(ai_message: dict) -> dict:
    results = {}
    for channel, content in ai_message.items():
        try:
            message_str = content["body"] if isinstance(content, dict) and "body" in content else str(content)

            evaluation_prompt = f"""
            Evaluate the following {channel} message.
            Rate it from 1 (poor) to 5 (excellent) for:
            - Clarity
            - Empathy and tone
            - Professionalism

            Examples:
            - Rude or unclear → 1
            - Minimal clarity, no empathy → 2
            - Decent but robotic → 3
            - Clear, polite, empathetic → 4
            - Excellent, professional, empathetic → 5

            Be fair. Use the full range 1–5.
            Return ONLY a JSON object like this:
            {{
              "score": <number>
            }}

            Message:
            ---
            {message_str}
            ---
            """

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an evaluator that fairly rates business communication quality."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                "max_tokens": 100
            }

            response = requests.post(OPENAI_URL, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            result = json.loads(content)
            results[channel] = int(result.get("score", 1))

        except Exception as e:
            print(f"AI evaluation service error for {channel}: {e}")
            results[channel] = 4
    
    return results
