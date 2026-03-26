import os
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
    Generates leadership-level insights from engineering signals.

    Accepts:
    - a single string
    - OR a list of signals (dicts with 'content')
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
        You are an engineering insights assistant for leadership.

        Analyze the following signals and provide:
        - Key blockers
        - Risks
        - Important trends or patterns

        Keep it concise and actionable.

        Signals:
        {combined_text}
        """

        # --- LLM call (Groq) ---
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    

    except Exception as e:
        return f"Insight generation failed: {str(e)}"