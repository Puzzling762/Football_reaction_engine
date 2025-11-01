import json
import time
from groq import Groq
from reaction_engine.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS, TEMPERATURE, TOP_P

class LLMClient:
    """Handles all LLM interactions with Groq"""
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
        self.request_count = 0
        self.total_tokens = 0
        
    def generate_reaction(self, prompt, temperature=None):
        """
        Generate a single reaction using Groq LLM
        
        Args:
            prompt (str): The formatted prompt
            temperature (float): Override default temperature
            
        Returns:
            str: Generated reaction text
        """
        try:
            temp = temperature if temperature is not None else TEMPERATURE
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert football journalist and commentator. Generate authentic, varied, and emotionally resonant match reactions. Never repeat phrases. Be creative and natural."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temp,
                max_tokens=MAX_TOKENS,
                top_p=TOP_P
            )
            
            self.request_count += 1
            self.total_tokens += response.usage.total_tokens
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return self._fallback_reaction()
    
    def generate_multi_tone_reactions(self, base_prompt, player_name):
        """
        Generate reactions in 3 different tones for the same match
        
        Returns:
            dict: {commentator, journalist, fan_tweet}
        """
        reactions = {}
        
        # 1. Commentator Style (High energy, 0.9 temp)
        commentator_prompt = f"{base_prompt}\n\nGenerate a COMMENTATOR-STYLE reaction: High energy, broadcast tone, emotional, like you're calling the match live. 2-3 sentences max."
        reactions['commentator'] = self.generate_reaction(commentator_prompt, temperature=0.9)
        time.sleep(0.3)  # Rate limit friendly
        
        # 2. Journalist Style (Formal, 0.7 temp)
        journalist_prompt = f"{base_prompt}\n\nGenerate a JOURNALIST-STYLE match report: Professional, analytical, balanced tone. Include a headline and 3-4 sentences."
        reactions['journalist'] = self.generate_reaction(journalist_prompt, temperature=0.7)
        time.sleep(0.3)
        
        # 3. Fan Tweet Style (Emotional, 0.95 temp)
        fan_prompt = f"{base_prompt}\n\nGenerate a FAN TWEET reaction: Emotional, short (under 280 chars), uses caps for emphasis, maybe an emoji. Raw fan emotion!"
        reactions['fan_tweet'] = self.generate_reaction(fan_prompt, temperature=0.95)
        
        return reactions
    
    def _fallback_reaction(self):
        """Fallback if LLM fails"""
        return "[Error generating reaction - check API key and connection]"
    
    def get_stats(self):
        """Return usage statistics"""
        return {
            'requests': self.request_count,
            'total_tokens': self.total_tokens,
            'avg_tokens_per_request': self.total_tokens / max(self.request_count, 1)
        }