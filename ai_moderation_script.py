import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PromptModerationSystem:
    def __init__(self):
        """Initialize the moderation system with OpenAI client and banned keywords."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Define banned keywords for moderation
        self.banned_keywords = [
            'kill', 'hack', 'bomb', 'murder', 'terrorist', 
            'weapon', 'suicide', 'drugs', 'violence'
        ]
        
        # System prompt to guide AI behavior
        self.system_prompt = """You are a helpful, safe, and responsible AI assistant.
        You provide informative and constructive responses while maintaining ethical standards.
        You refuse to provide information that could be harmful, illegal, or dangerous.
        Always be respectful, professional, and focus on helping users in positive ways."""
    
    def check_banned_keywords(self, text):
        """
        Check if text contains any banned keywords.
        
        Args:
            text (str): The text to check
            
        Returns:
            tuple: (bool, list) - (contains_banned, list_of_found_keywords)
        """
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.banned_keywords:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                found_keywords.append(keyword)
        
        return len(found_keywords) > 0, found_keywords
    
    def moderate_input(self, user_prompt):
        """
        Moderate the input prompt before sending to AI.
        
        Args:
            user_prompt (str): The user's input prompt
            
        Returns:
            tuple: (bool, str) - (is_safe, message)
        """
        contains_banned, keywords = self.check_banned_keywords(user_prompt)
        
        if contains_banned:
            return False, f"Your input violated the moderation policy. Banned keywords found: {', '.join(keywords)}"
        
        return True, "Input is safe"
    
    def moderate_output(self, ai_response):
        """
        Moderate the AI's response before displaying to user.
        
        Args:
            ai_response (str): The AI's generated response
            
        Returns:
            tuple: (bool, str) - (is_safe, moderated_response)
        """
        contains_banned, keywords = self.check_banned_keywords(ai_response)
        
        if contains_banned:
            # Replace banned keywords with [REDACTED]
            moderated_text = ai_response
            for keyword in self.banned_keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                moderated_text = re.sub(pattern, '[REDACTED]', moderated_text, flags=re.IGNORECASE)
            
            return True, moderated_text
        
        return True, ai_response
    
    def generate_response(self, user_prompt):
        """
        Generate AI response using OpenAI API.
        
        Args:
            user_prompt (str): The user's prompt
            
        Returns:
            str: The AI's response
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def process_prompt(self, user_prompt):
        """
        Main function to process user prompt with moderation.
        
        Args:
            user_prompt (str): The user's input prompt
            
        Returns:
            str: The final response (moderated or error message)
        """
        print("\n" + "="*50)
        print("PROCESSING USER PROMPT")
        print("="*50)
        
        # Step 1: Moderate input
        print("\n[1] Checking input moderation...")
        input_safe, input_message = self.moderate_input(user_prompt)
        
        if not input_safe:
            print(f"❌ {input_message}")
            return input_message
        
        print("✓ Input passed moderation")
        
        # Step 2: Generate AI response
        print("\n[2] Generating AI response...")
        ai_response = self.generate_response(user_prompt)
        print("✓ Response generated")
        
        # Step 3: Moderate output
        print("\n[3] Checking output moderation...")
        output_safe, moderated_response = self.moderate_output(ai_response)
        
        if moderated_response != ai_response:
            print("⚠️  Output contained banned keywords - applied [REDACTED]")
        else:
            print("✓ Output passed moderation")
        
        print("\n" + "="*50)
        print("FINAL RESPONSE")
        print("="*50)
        
        return moderated_response


def main():
    """Main function to run the moderation system."""
    print("\n" + "="*50)
    print("AI PROMPT MODERATION SYSTEM")
    print("="*50)
    print("\nThis system moderates both input and output for safety.")
    print("Banned keywords include: kill, hack, bomb, murder, etc.\n")
    
    # Initialize the moderation system
    moderator = PromptModerationSystem()
    
    while True:
        # Get user input
        user_prompt = input("\nEnter your prompt (or 'quit' to exit): ").strip()
        
        if user_prompt.lower() == 'quit':
            print("\nThank you for using the AI Moderation System!")
            break
        
        if not user_prompt:
            print("Please enter a valid prompt.")
            continue
        
        # Process the prompt
        result = moderator.process_prompt(user_prompt)
        print(f"\n{result}\n")


if __name__ == "__main__":
    main()