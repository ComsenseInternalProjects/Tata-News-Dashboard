import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def fetch_insights(content):
    prompt = (f"Analyze the following news content and provide insights on how it may impact Tata Motors Commercial Vehicle sector. "
              f"Additionally, suggest action steps a senior head of Tata Motors Commercial Vehicle sector should take in response to this news.\n\n"
              f"News Content: {content}\n\n"
              f"Impact and Action Steps:\n"
              f"All the impact and steps should be in bullet points")

    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Create a completion request with the combined prompt and parameters
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct-0914",
            prompt=prompt,
            temperature=0,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#", ";"]
        )
        # Extract the first choice from the response
        if hasattr(response, 'choices') and response.choices:
            output = response.choices[0].text
        else:
            output = "No choices found in the response."

        return output
    except Exception as e:
        # If there's an error, return the error message
        return str(e), False