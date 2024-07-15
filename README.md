# Anthropic Conversation for Home Assistant

This custom integration allows you to use Anthropic's advanced language models, particularly Claude, within your Home Assistant setup. It enables natural language interactions with your smart home devices and provides powerful AI-assisted functionalities.

## Features

- **Natural Language Control**: Interact with your Home Assistant devices using natural language commands processed by Anthropic's Claude model.
- **Context-Aware Conversations**: The integration maintains conversation context, allowing for more natural and coherent interactions.
- **Customizable Prompts**: Tailor the system prompt to fit your specific needs and use cases.
- **Function Calling**: Utilize Claude's function calling capabilities to execute Home Assistant services.
- **Image Analysis**: Query images using Claude's vision capabilities (requires Claude 3 models with vision support).

## Requirements

- A Home Assistant installation
- An Anthropic API key
- Python 3.9 or higher

## Configuration

The integration can be configured through the Home Assistant UI. You'll need to provide your Anthropic API key and can customize various options such as:

- Model selection (e.g., claude-3-sonnet-20240620)
- Maximum tokens for responses
- Temperature and top_p settings for response generation
- Custom system prompts
- Tool definitions for function calling

## Usage

Once configured, you can interact with the Anthropic Conversation integration through:

1. The conversation integration in Home Assistant
2. Service calls for specific functionalities like image analysis

Example conversation:
```
User: "Turn on the living room lights and set them to 50% brightness"
Claude: "Certainly! I'll turn on the living room lights and set their brightness to 50%. Is there anything else you'd like me to do?"
```

## Contributing

Contributions to this integration are welcome! Please read our contributing guidelines (link to be added) before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a community project and is not officially supported by Anthropic or Home Assistant. Use at your own risk.

## Support

If you encounter any issues or have questions, please file an issue on our GitHub repository.

---

Note: This integration is in active development. Features and configurations may change. Always refer to the latest documentation for the most up-to-date information.
