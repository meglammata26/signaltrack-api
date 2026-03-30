import os
import json
from openai import OpenAI

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def generate_insight(input_data):
    """
    Generates structured leadership insights from engineering signals.
    Returns JSON with blockers, risks, and trends.
    """

    try:
        # --- Normalize input ---
        if isinstance(input_data, str):
            combined_text = input_data
        elif isinstance(input_data, list):
            combined_text = "\n".join([
                s.get("content", "") if isinstance(s, dict) else str(s)
                for s in input_data
            ])
        else:
            combined_text = str(input_data)

        # --- Prompt ---
        prompt = f"""
You are a senior engineering insights assistant.

Analyze the following signals and extract:
- blockers (things actively preventing progress)
- risks (potential future issues)
- trends (patterns across signals)

Return ONLY valid JSON in this format:
{{
  "blockers": ["..."],
  "risks": ["..."],
  "trends": ["..."]
}}

Signals:
{combined_text}
"""

        # --- LLM call ---
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        output = response.choices[0].message.content.strip()

        # --- Parse JSON safely ---
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {
                "blockers": [],
                "risks": [],
                "trends": [],
                "raw": output  # fallback for debugging
            }

    except Exception as e:
        return {
            "error": f"Insight generation failed: {str(e)}"
        }