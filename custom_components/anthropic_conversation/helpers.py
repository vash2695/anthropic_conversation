from abc import ABC, abstractmethod
from datetime import timedelta
import logging
from typing import Any

from anthropic import Anthropic, APIStatusError, APIConnectionError, APITimeoutError
import voluptuous as vol

from homeassistant.components import conversation
from homeassistant.components.homeassistant.exposed_entities import async_should_expose
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.template import Template
import homeassistant.util.dt as dt_util

from .const import DOMAIN
from .exceptions import (
    CallServiceError,
    EntityNotExposed,
    EntityNotFound,
    FunctionNotFound,
    InvalidFunction,
    CannotConnect,
    InvalidAuth,
)

_LOGGER = logging.getLogger(__name__)

async def validate_authentication(hass: HomeAssistant, api_key: str) -> None:
    """Validate the API key."""
    client = Anthropic(api_key=api_key)
    try:
        await client.models.list()
    except APIStatusError as err:
        raise InvalidAuth(f"Invalid API key: {err}") from err
    except (APIConnectionError, APITimeoutError) as err:
        raise CannotConnect(f"Unable to connect to Anthropic API: {err}") from err

def get_exposed_entities(hass: HomeAssistant):
    """Get the exposed entities."""
    states = [
        state
        for state in hass.states.async_all()
        if async_should_expose(hass, conversation.DOMAIN, state.entity_id)
    ]
    entity_registry = er.async_get(hass)
    exposed_entities = []
    for state in states:
        entity_id = state.entity_id
        entity = entity_registry.async_get(entity_id)

        aliases = []
        if entity and entity.aliases:
            aliases = entity.aliases

        exposed_entities.append(
            {
                "entity_id": entity_id,
                "name": state.name,
                "state": hass.states.get(entity_id).state,
                "aliases": aliases,
            }
        )
    return exposed_entities

class FunctionExecutor(ABC):
    def __init__(self, data_schema=vol.Schema({})) -> None:
        """Initialize function executor."""
        self.data_schema = data_schema.extend({vol.Required("type"): str})

    def to_arguments(self, arguments):
        """Convert to arguments."""
        try:
            return self.data_schema(arguments)
        except vol.error.Error as e:
            function_type = next(
                (key for key, value in FUNCTION_EXECUTORS.items() if value == self),
                None,
            )
            raise InvalidFunction(function_type) from e

    def validate_entity_ids(self, hass: HomeAssistant, entity_ids, exposed_entities):
        if any(hass.states.get(entity_id) is None for entity_id in entity_ids):
            raise EntityNotFound(entity_ids)
        exposed_entity_ids = map(lambda e: e["entity_id"], exposed_entities)
        if not set(entity_ids).issubset(exposed_entity_ids):
            raise EntityNotExposed(entity_ids)

    @abstractmethod
    async def execute(
        self,
        hass: HomeAssistant,
        function,
        arguments,
        user_input: conversation.ConversationInput,
        exposed_entities,
    ):
        """Execute function."""

class NativeFunctionExecutor(FunctionExecutor):
    def __init__(self) -> None:
        """Initialize native function."""
        super().__init__(vol.Schema({vol.Required("name"): str}))

    async def execute(
        self,
        hass: HomeAssistant,
        function,
        arguments,
        user_input: conversation.ConversationInput,
        exposed_entities,
    ):
        name = function["name"]
        if name == "execute_services":
            return await self.execute_service(
                hass, function, arguments, user_input, exposed_entities
            )
        raise FunctionNotFound(name)

    async def execute_service(
        self,
        hass: HomeAssistant,
        function,
        arguments,
        user_input: conversation.ConversationInput,
        exposed_entities,
    ):
        result = []
        for service_argument in arguments.get("list", []):
            result.append(
                await self.execute_service_single(
                    hass, function, service_argument, user_input, exposed_entities
                )
            )
        return result

    async def execute_service_single(
        self,
        hass: HomeAssistant,
        function,
        service_argument,
        user_input: conversation.ConversationInput,
        exposed_entities,
    ):
        domain = service_argument["domain"]
        service = service_argument["service"]
        service_data = service_argument.get(
            "service_data", service_argument.get("data", {})
        )
        entity_id = service_data.get("entity_id", service_argument.get("entity_id"))

        if isinstance(entity_id, str):
            entity_id = [e.strip() for e in entity_id.split(",")]
        service_data["entity_id"] = entity_id

        if entity_id is None:
            raise CallServiceError(domain, service, service_data)
        if not hass.services.has_service(domain, service):
            raise FunctionNotFound(f"Service {domain}.{service} not found")
        self.validate_entity_ids(hass, entity_id or [], exposed_entities)

        try:
            await hass.services.async_call(
                domain=domain,
                service=service,
                service_data=service_data,
            )
            return {"success": True}
        except Exception as e:
            _LOGGER.error(e)
            return {"error": str(e)}

FUNCTION_EXECUTORS: dict[str, FunctionExecutor] = {
    "native": NativeFunctionExecutor(),
}
