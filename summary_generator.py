from typing import Optional
import openai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_summary(text: str, custom_prompt: Optional[str] = None) -> str:
    """
    Generate a summary of the given text using Perplexity API.
    """
    try:
        client = openai.OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"), 
            base_url="https://api.perplexity.ai"
        )
        
        default_prompt = "You are a helpful assistant that summarizes corporate announcements. Provide concise, factual summaries focusing on key information and business impact.REMEMBER TO USE LAKHS OR CRORES wherever needed. DONT INCLUDE ANY CITATIONS OR REFERENCES"
        system_prompt = custom_prompt or default_prompt
        
        full_prompt = f"{system_prompt}\n\nPlease provide a brief summary of this corporate announcement in 2-3 sentences AT THE MAX: {text[:4000]}"
        
        response = client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{
                "role": "user",
                "content": full_prompt
            }]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary with Perplexity: {e}")
        return "" 