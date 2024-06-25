Anthropic Conversation for Home Assistant
This custom integration allows you to use Anthropic's Claude AI model as a conversation agent in Home Assistant.
Installation
HACS (Recommended)

Make sure you have HACS installed in your Home Assistant instance.
In the HACS panel, click on "Integrations".
Click the "+" button in the bottom right corner.
Search for "Anthropic Conversation" and select it.
Click "Install" and wait for the installation to complete.
Restart Home Assistant.

Manual Installation

Copy the anthropic_conversation folder from this repository to your custom_components directory in your Home Assistant config directory.
Restart Home Assistant.

Configuration

In Home Assistant, go to Configuration > Integrations.
Click the "+" button to add a new integration.
Search for "Anthropic Conversation" and select it.
Enter your Anthropic API key when prompted.
Configure additional options as desired.

Usage
Once configured, you can use the Anthropic Conversation agent in your Home Assistant conversations. You can interact with it through the conversation interface or by calling the conversation.process service with the Anthropic agent specified.
Options
You can customize the following options:

Prompt: The system prompt used to set the context for the AI.
Model: The Anthropic model to use (e.g., "claude-2").
Max Tokens: The maximum number of tokens in the AI's response.
Temperature: Controls the randomness of the AI's responses.

To modify these options, go to Configuration > Integrations, find the Anthropic Conversation integration, and click "Options".
Support
For issues, feature requests, or questions, please open an issue on GitHub.
