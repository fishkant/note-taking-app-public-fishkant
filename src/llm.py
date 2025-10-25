# import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() # Loads environment variables from .env
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
    client = OpenAI(base_url=endpoint,api_key=token)
    response = client.chat.completions.create(messages=messages,temperature=temperature, top_p=top_p, model=model)
    return response.choices[0].message.content
# A function to translate to target language
def translate_to_language(text, target_language):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that translates text to the target language.",
        },
        {
            "role": "user",
            "content": f"Translate the following text to {target_language}: {text}",
        }
    ]
    translation = call_llm_model(model, messages)
    return translation

def generate_note_from_text(input_text):
    """Generate a note with title, content, tags, and extract date/time if present"""
    messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant that generates well-structured notes and extracts date/time information.
            When you find dates or times in the input, format them according to these rules:
            - Dates should be in YYYY-MM-DD format
            - Times should be in HH:mm 24-hour format
            - If multiple dates/times are found, use the most prominent one
            - Only extract explicit dates/times, don't assume today's date
            """
        },
        {
            "role": "user",
            "content": f"""Please create a note from this text and extract any date/time information: {input_text}
            Format your response as JSON with these fields:
            - title: The note title
            - content: The note content
            - tags: Array of 3 relevant tags
            - event_date: Date in YYYY-MM-DD format if found, or null
            - event_time: Time in HH:mm format if found, or null"""
        }
    ]
    response = call_llm_model(model, messages, temperature=0.7)
    
    # 錯誤處理：確保回應是有效的 JSON 字串並包含所有必要欄位
    import json
    try:
        note_data = json.loads(response)
        # 確保所有必要欄位都存在
        required_fields = ['title', 'content', 'tags', 'event_date', 'event_time']
        for field in required_fields:
            if field not in note_data:
                note_data[field] = None if field in ['event_date', 'event_time'] else ([] if field == 'tags' else '')
        return note_data
    except json.JSONDecodeError:
        raise ValueError("Invalid response format from LLM")
# Run the main function if this script is executed
if __name__ == "__main__":
    sample_text = "Hello, how are you?"
    target_language = "Chinese"
    translated_text = translate_to_language(sample_text, target_language)
    print(f"Original Text: {sample_text}")
    print(f"Translated Text: {translated_text}")
