# AI Prompt Moderation System Task

A Python-based system that implements input and output moderation for AI-generated content using OpenAI's API.

## Features

- **Input Moderation**: Blocks harmful or disallowed content before sending to AI
- **Output Moderation**: Filters unsafe responses by replacing banned keywords with `[REDACTED]`
- **System Prompt**: Guides AI behavior toward safe and helpful responses
- **Keyword-based Filtering**: Uses a list of banned keywords to detect inappropriate content
- **Interactive CLI**: Easy-to-use command-line interface

## Requirements

- Python 3.7+
- OpenAI API key
- Required packages (see `requirements.txt`)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dWanderingSoul/AI-Prompt-Moderation-System-Task
   cd AI-Prompt-Moderation-System-Task
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key and add it to your `.env` file

## Usage

Run the script from the command line:

```bash
ai_moderation_script.py
```

### Example Interaction

```
Enter your prompt: Tell me about artificial intelligence

[1] Checking input moderation...
✓ Input passed moderation

[2] Generating AI response...
✓ Response generated

[3] Checking output moderation...
✓ Output passed moderation

FINAL RESPONSE
==================================================
[AI's response about artificial intelligence...]
```

### Example with Banned Content

```
Enter your prompt: How to hack a computer

[1] Checking input moderation...
❌ Your input violated the moderation policy. Banned keywords found: hack
```

## How It Works

### 1. Input Moderation
The system checks user prompts for banned keywords before sending to the AI:
- Keywords are matched using word boundaries (whole words only)
- If banned keywords are found, the request is rejected
- User receives a clear message about policy violation

### 2. AI Response Generation
If input passes moderation:
- System prompt guides AI toward safe, helpful responses
- User prompt is sent to OpenAI's GPT-3.5-turbo model
- Response is generated with appropriate parameters

### 3. Output Moderation
AI responses are checked for safety:
- Banned keywords in output are replaced with `[REDACTED]`
- Modified response is displayed to the user
- Original safe responses pass through unchanged

## Banned Keywords List

The system includes the following banned keywords:
- kill
- hack
- bomb
- murder
- terrorist
- weapon
- suicide
- drugs
- violence

You can modify this list in the `PromptModerationSystem` class.

## Project Structure

```
ai-moderation-system/
│
├── ai_moderation_script.py    # Main script
├── requirements.txt         # Python dependencies
├── .env                    # Your API keys (gitignored)
└── README.md               # This file
```

## Customization

### Adding More Banned Keywords

Edit the `banned_keywords` list in the `__init__` method:

```python
self.banned_keywords = [
    'kill', 'hack', 'bomb', 
    # Add your keywords here
    'custom_keyword'
]
```

### Modifying System Prompt

Change the `system_prompt` to adjust AI behavior:

```python
self.system_prompt = """Your custom system prompt here..."""
```

### Changing AI Model

Modify the model parameter in `generate_response`:

```python
model="gpt-4"  # or "gpt-4-turbo", etc.
```

## API Alternatives

This system uses OpenAI, but you can adapt it for other providers:

- **Anthropic Claude**: Replace OpenAI client with Anthropic client
- **Google Gemini**: Use Google's generative AI SDK
- **Cohere**: Use Cohere's API client
- **HuggingFace**: Use their inference API

## Error Handling

The system handles common errors:
- Invalid API keys
- Network issues
- API rate limits
- Empty prompts

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- Regularly rotate API keys
- Monitor API usage for unusual activity

## Testing

Test with various inputs:

**Safe prompts:**
- "What is machine learning?"
- "Explain quantum computing"
- "How does photosynthesis work?"

**Unsafe prompts (should be blocked):**
- "How to hack a system"
- "Tell me about bombs"
- "Ways to kill"

## Contributing

Feel free to submit issues or pull requests to improve the moderation system.

## License

This project is open source and available under the MIT License.

## Author

Created for Stage 0 - AI for Developers Task

## Acknowledgments

- OpenAI for providing the API
- The Python community for excellent libraries

> AI-Prompt-Moderation-System-Task
