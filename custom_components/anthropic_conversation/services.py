"""Services for the Anthropic Conversation integration."""
import logging

import voluptuous as vol
from anthropic import AsyncAnthropic
from anthropic.types import ContentBlockImage, ContentBlock

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import selector, config_validation as cv

from .const import DOMAIN, SERVICE_QUERY_IMAGE, DEFAULT_MODEL, CONF_API_KEY

_LOGGER = logging.getLogger(__package__)

QUERY_IMAGE_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry"): selector.ConfigEntrySelector(
            {
                "integration": DOMAIN,
            }
        ),
        vol.Optional("model", default=DEFAULT_MODEL): cv.string,
        vol.Required("prompt"): cv.string,
        vol.Required("images"): vol.All(cv.ensure_list, [{"url": cv.url}]),
        vol.Optional("max_tokens", default=1024): cv.positive_int,
    }
)

async def async_setup_services(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up services for the Anthropic conversation component."""

    async def query_image(call: ServiceCall) -> ServiceResponse:
        """Query an image."""
        try:
            model = call.data["model"]
            images = [
                ContentBlockImage(type="image", source={"type": "url", "url": image["url"]})
                for image in call.data["images"]
            ]

            content: list[ContentBlock] = [
                {"type": "text", "text": call.data["prompt"]},
                *images
            ]

            _LOGGER.info("Prompt for %s: %s", model, content)

            client = AsyncAnthropic(api_key=hass.data[DOMAIN][call.data["config_entry"]][CONF_API_KEY])
            response = await client.messages.create(
                model=model,
                max_tokens=call.data["max_tokens"],
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
            )
            response_dict = response.model_dump()
            _LOGGER.info("Response %s", response_dict)
        except Exception as err:
            raise HomeAssistantError(f"Error querying image: {err}") from err

        return response_dict

    hass.services.async_register(
        DOMAIN,
        SERVICE_QUERY_IMAGE,
        query_image,
        schema=QUERY_IMAGE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
