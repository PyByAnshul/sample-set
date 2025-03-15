# from langchain_ollama import OllamaLLM
from globals import db
import google.generativeai as genai
from smlib.ollama.utils import api_key

def main(post_id):
    try:
        post_caption = db.post.find_one({"post_id": post_id})

        # ollama = OllamaLLM(base_url='http://localhost:11434', model='llama3.2:3b')
        # response = ollama.invoke(f"Summarize this for a Twitter post (280 chars): {post_caption.get('caption')}")
        
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(
            f"Summarize this for a Twitter post (280 chars): {post_caption.get('caption')}"
        )

        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")


