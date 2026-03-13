from openai import OpenAI

client = OpenAI()


def generate_summary(signals):

    combined_text = "\n".join(
        [signal.raw_content for signal in signals]
    )

    prompt = f"""
    Analyze the following engineering signals.

    Identify:
    - major blockers
    - risks
    - key insights leadership should know

    Signals:
    {combined_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content