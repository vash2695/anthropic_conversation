"""Exceptions for the Anthropic Conversation integration."""

from homeassistant.exceptions import HomeAssistantError


class AnthropicError(HomeAssistantError):
    """Base class for Anthropic integration errors."""


class InvalidAuth(AnthropicError):
    """Error to indicate there is invalid auth."""


class CannotConnect(AnthropicError):
    """Error to indicate we cannot connect."""


class InvalidAPIKey(AnthropicError):
    """Error to indicate there is an invalid API key."""


class APIRateLimitExceeded(AnthropicError):
    """Error to indicate that the API rate limit has been exceeded."""


class ServiceError(AnthropicError):
    """Error to indicate a problem with a service call."""
