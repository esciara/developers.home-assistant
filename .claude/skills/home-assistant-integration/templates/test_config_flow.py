"""Test config flow for My Device integration."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant

from custom_components.my_device.const import DOMAIN
from tests.common import MockConfigEntry


async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == "form"
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_device_id.return_value = "device123"
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "192.168.1.100",
                CONF_API_KEY: "test-key",
            },
        )

    assert result["type"] == "create_entry"
    assert result["title"] == "192.168.1.100"
    assert result["data"] == {
        CONF_HOST: "192.168.1.100",
        CONF_API_KEY: "test-key",
    }


async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test connection error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        from my_device_lib import ConnectionError as DeviceConnectionError
        mock_api.async_test_connection.side_effect = DeviceConnectionError
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test authentication error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        from my_device_lib import AuthenticationError
        mock_api.async_test_connection.side_effect = AuthenticationError
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "bad-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_user_flow_unknown_error(hass: HomeAssistant) -> None:
    """Test unknown error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.side_effect = Exception("Unexpected")
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "unknown"}


async def test_duplicate_entry(hass: HomeAssistant) -> None:
    """Test duplicate entry is aborted."""
    # Create existing entry
    existing_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    existing_entry.add_to_hass(hass)

    # Try to add duplicate
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_device_id.return_value = "device123"  # Same unique ID
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.200", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"
