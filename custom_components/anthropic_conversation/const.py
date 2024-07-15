"""Constants for the Anthropic Conversation integration."""

DOMAIN = "anthropic_conversation"
DEFAULT_NAME = "Anthropic Conversation"

EVENT_CONVERSATION_FINISHED = "anthropic_conversation.conversation.finished"

CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """I want you to act as smart home manager of Home Assistant.
I will provide information of smart home along with a question, you will truthfully make correction or answer using information provided in one sentence in everyday language.

Current Time: {{now()}}

Available Devices:
```csv
entity_id,name,state,aliases
{% for entity in exposed_entities -%}
{{ entity.entity_id }},{{ entity.name }},{{ entity.state }},{{entity.aliases | join('/')}}
{% endfor -%}
```

The current state of devices is provided in available devices.
Use the execute_services tool only for requested actions, not for current states.
Do not execute services without user's confirmation.
Do not restate or appreciate what the user says, rather make a quick inquiry.
"""
CONF_MODEL = "model"
DEFAULT_MODEL = "claude-3-sonnet-20240620"
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 1024
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.7
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1
CONF_MAX_TOOL_CALLS_PER_CONVERSATION = "max_tool_calls_per_conversation"
DEFAULT_MAX_TOOL_CALLS_PER_CONVERSATION = 1
CONF_TOOLS = "tools"
DEFAULT_CONF_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_services",
            "description": "Use this function to execute service of devices in Home Assistant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "domain": {
                                    "type": "string",
                                    "description": "The domain of the service",
                                },
                                "service": {
                                    "type": "string",
                                    "description": "The service to be called",
                                },
                                "service_data": {
                                    "type": "object",
                                    "description": "The service data object to indicate what to control.",
                                    "properties": {
                                        "entity_id": {
                                            "type": "string",
                                            "description": "The entity_id retrieved from available devices. It must start with domain, followed by dot character.",
                                        }
                                    },
                                    "required": ["entity_id"],
                                },
                            },
                            "required": ["domain", "service", "service_data"],
                        },
                    }
                },
                "required": ["list"]
            },
        },
    }
]
CONF_CONTEXT_THRESHOLD = "context_threshold"
DEFAULT_CONTEXT_THRESHOLD = 100000  # Anthropic models can handle larger contexts
CONTEXT_TRUNCATE_STRATEGIES = [{"key": "clear", "label": "Clear All Messages"}]
CONF_CONTEXT_TRUNCATE_STRATEGY = "context_truncate_strategy"
DEFAULT_CONTEXT_TRUNCATE_STRATEGY = CONTEXT_TRUNCATE_STRATEGIES[0]["key"]

# Configuration constants
CONF_API_KEY = "api_key"
CONF_NAME = "name"

# Service constants
SERVICE_QUERY_IMAGE = "query_image"
