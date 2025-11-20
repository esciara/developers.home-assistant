# Config Flow Complete Guide

Config flows provide UI-based configuration for Home Assistant integrations. This guide covers everything from basic user flows to advanced reauth, reconfigure, and discovery patterns.

## Config Flow Basics

### What is a Config Flow?

A config flow is a multi-step UI wizard for setting up integrations. Users never edit YAML.

**Benefits**:
- User-friendly UI
- Input validation
- Duplicate detection
- Discovery support
- Required for Bronze tier

### Config Entry Lifecycle

```
User adds integration → Config flow starts
                       ↓
         User provides input (credentials, host, etc.)
                       ↓
         Flow validates and creates config entry
                       ↓
         Entry state: not_loaded → setup_in_progress → loaded
```

**States**:
- `not_loaded` - Entry exists but not set up
- `setup_in_progress` - Running `async_setup_entry()`
- `loaded` - Successfully loaded
- `setup_error` - Temporary failure, will retry
- `setup_retry` - Retry in progress
- `migration_error` - Migration failed
- `failed_unload` - Unload failed

## Phase 1: Basic User Flow

### Minimum Config Flow

```python
"""Config flow for My Device."""
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
import voluptuous as vol

from .const import DOMAIN

class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Device."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate by attempting connection
                api = MyDeviceAPI(
                    user_input[CONF_HOST],
                    user_input[CONF_API_KEY]
                )
                await api.async_test_connection()

                # Get unique ID to prevent duplicates
                device_id = await api.async_get_device_id()
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                # Create config entry
                return self.async_create_entry(
                    title=user_input[CONF_HOST],  # Shown in UI
                    data=user_input  # Stored immutably
                )

            except ConnectionError:
                errors["base"] = "cannot_connect"
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"

        # Show form (first time or on error)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        )
```

### Key Methods

**`async_step_user(user_input=None)`**:
- Called for manual user setup
- `user_input=None` on first call (show form)
- `user_input` contains form data on subsequent calls

**`async_show_form()`**:
- Displays form to user
- Parameters:
  - `step_id` - Current step name
  - `data_schema` - Voluptuous schema for form fields
  - `errors` - Dict of field errors
  - `description_placeholders` - Template variables

**`async_create_entry()`**:
- Creates config entry
- Parameters:
  - `title` - Display name in UI
  - `data` - Immutable data (credentials, host)
  - `options` - Mutable settings (update_interval, etc.)

**`async_set_unique_id()`**:
- Sets unique ID for entry
- Prevents duplicate entries
- Must be called before `async_create_entry()`

**`_abort_if_unique_id_configured()`**:
- Aborts if unique ID already exists
- Prevents duplicates
- Called after `async_set_unique_id()`

### Form Schema with Voluptuous

```python
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Simple schema
vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_API_KEY): str,
})

# With defaults and optional fields
vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=80): cv.port,
    vol.Optional(CONF_SCAN_INTERVAL, default=30): cv.positive_int,
})

# With validation
vol.Schema({
    vol.Required(CONF_HOST): cv.string,  # Non-empty string
    vol.Required(CONF_EMAIL): cv.email,  # Valid email
    vol.Required(CONF_URL): cv.url,  # Valid URL
})

# With selection
vol.Schema({
    vol.Required("mode"): vol.In(["auto", "manual", "advanced"]),
})

# With boolean
vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional("ssl", default=True): cv.boolean,
})
```

**Common validators** (`homeassistant.helpers.config_validation`):
- `cv.string` - Non-empty string
- `cv.port` - Valid port (1-65535)
- `cv.positive_int` - Positive integer
- `cv.email` - Valid email address
- `cv.url` - Valid URL
- `cv.boolean` - Boolean value
- `cv.latitude` - Valid latitude
- `cv.longitude` - Valid longitude

### Error Handling

**Error dict format**:
```python
errors = {
    "base": "cannot_connect",  # General error
    "host": "invalid_host",    # Field-specific error
}
```

**Common error keys**:
- `"base"` - General error shown at top of form
- Field name - Error shown under specific field

**String translations** (in `strings.json`):
```json
{
  "config": {
    "error": {
      "cannot_connect": "Failed to connect",
      "invalid_auth": "Invalid authentication",
      "invalid_host": "Invalid hostname or IP address",
      "unknown": "Unexpected error occurred"
    }
  }
}
```

### Unique ID Requirements

**Acceptable unique ID sources**:
- ✅ Serial number
- ✅ MAC address
- ✅ Device ID from API
- ✅ Account ID (for cloud services)
- ✅ Hardware identifier
- ❌ IP address (can change)
- ❌ Hostname (can change)
- ❌ Device name (user-changeable)
- ❌ Combination of changeable values

**Examples**:
```python
# ✅ GOOD - Stable serial number
await self.async_set_unique_id(device.serial_number)

# ✅ GOOD - MAC address
await self.async_set_unique_id(device.mac_address)

# ✅ GOOD - Account ID for cloud service
await self.async_set_unique_id(f"account_{account.id}")

# ❌ BAD - IP address can change
await self.async_set_unique_id(user_input[CONF_HOST])

# ❌ BAD - User-provided name
await self.async_set_unique_id(user_input[CONF_NAME])
```

**Last resort**: Use config entry ID (if truly no unique identifier)
```python
# Only if absolutely no other option
# This allows duplicates but at least works
return self.async_create_entry(
    title=user_input[CONF_HOST],
    data=user_input
)
# (no unique_id set)
```

### Multi-Step Flows

For complex setup, split into multiple steps:

```python
class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Multi-step config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._host = None
        self._discovered_devices = None

    async def async_step_user(self, user_input=None):
        """Step 1: Get host."""
        if user_input is not None:
            self._host = user_input[CONF_HOST]
            # Move to next step
            return await self.async_step_auth()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
            }),
        )

    async def async_step_auth(self, user_input=None):
        """Step 2: Authenticate."""
        if user_input is not None:
            # Combine data from both steps
            data = {
                CONF_HOST: self._host,
                CONF_API_KEY: user_input[CONF_API_KEY],
            }

            # Validate and create entry
            api = MyDeviceAPI(data[CONF_HOST], data[CONF_API_KEY])
            await api.async_test_connection()

            device_id = await api.async_get_device_id()
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self._host,
                data=data
            )

        return self.async_show_form(
            step_id="auth",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
            }),
            description_placeholders={"host": self._host},
        )
```

## Phase 2: Advanced Flows

### Reauth Flow

Triggered when credentials expire or become invalid.

**When to use**:
- API returns 401/403 auth error
- Refresh token expired
- User changed password
- Session timeout

**Triggering reauth** (from coordinator or __init__.py):
```python
from homeassistant.exceptions import ConfigEntryAuthFailed

async def _async_update_data(self):
    """Fetch data from API."""
    try:
        return await self.api.async_get_data()
    except ApiAuthError as err:
        # This automatically triggers reauth flow
        raise ConfigEntryAuthFailed("Credentials expired") from err
```

**Implementing reauth step**:
```python
async def async_step_reauth(self, entry_data):
    """Handle reauth when credentials expire."""
    # Store entry for later
    self._reauth_entry = self.hass.config_entries.async_get_entry(
        self.context["entry_id"]
    )
    # Show reauth form
    return await self.async_step_reauth_confirm()

async def async_step_reauth_confirm(self, user_input=None):
    """Handle reauth confirmation."""
    errors = {}

    if user_input is not None:
        # Validate new credentials
        try:
            api = MyDeviceAPI(
                self._reauth_entry.data[CONF_HOST],
                user_input[CONF_API_KEY]
            )
            await api.async_test_connection()

            # Update existing entry with new credentials
            self.hass.config_entries.async_update_entry(
                self._reauth_entry,
                data={
                    **self._reauth_entry.data,
                    CONF_API_KEY: user_input[CONF_API_KEY],
                }
            )

            # Reload entry to use new credentials
            await self.hass.config_entries.async_reload(
                self._reauth_entry.entry_id
            )

            return self.async_abort(reason="reauth_successful")

        except AuthenticationError:
            errors["base"] = "invalid_auth"

    # Show form with just API key field
    return self.async_show_form(
        step_id="reauth_confirm",
        data_schema=vol.Schema({
            vol.Required(CONF_API_KEY): str,
        }),
        description_placeholders={
            "host": self._reauth_entry.data[CONF_HOST],
        },
        errors=errors,
    )
```

### Reconfigure Flow

Allows updating immutable config entry data (host, credentials, etc.) without deleting and re-adding.

**When to use**:
- User wants to change host/IP
- Update credentials
- Change connection settings
- Modify any `data` field

**Triggering reconfigure** (from UI):
- User clicks "Configure" on integration
- If `async_step_reconfigure` exists, "Reconfigure" button appears

**Implementing reconfigure**:
```python
async def async_step_reconfigure(self, user_input=None):
    """Handle reconfiguration."""
    errors = {}
    entry = self.hass.config_entries.async_get_entry(
        self.context["entry_id"]
    )

    if user_input is not None:
        # Validate new settings
        try:
            api = MyDeviceAPI(
                user_input[CONF_HOST],
                user_input[CONF_API_KEY]
            )
            await api.async_test_connection()

            # Update entry
            self.hass.config_entries.async_update_entry(
                entry,
                data=user_input
            )

            # Reload to apply changes
            await self.hass.config_entries.async_reload(entry.entry_id)

            return self.async_abort(reason="reconfigure_successful")

        except ConnectionError:
            errors["base"] = "cannot_connect"
        except AuthenticationError:
            errors["base"] = "invalid_auth"

    # Pre-fill form with current values
    return self.async_show_form(
        step_id="reconfigure",
        data_schema=vol.Schema({
            vol.Required(CONF_HOST, default=entry.data[CONF_HOST]): str,
            vol.Required(CONF_API_KEY, default=entry.data[CONF_API_KEY]): str,
        }),
        errors=errors,
    )
```

### Options Flow

For mutable settings that users can change without reloading (scan interval, enabled features, etc.).

**Difference from reconfigure**:
- **Reconfigure**: Changes immutable `data` (credentials, host), requires reload
- **Options**: Changes mutable `options` (settings), no reload needed

**Implementing options flow**:
```python
@staticmethod
@callback
def async_get_options_flow(config_entry):
    """Get options flow handler."""
    return MyDeviceOptionsFlow(config_entry)

class MyDeviceOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            # Save options (no reload needed)
            return self.async_create_entry(
                title="",
                data=user_input
            )

        # Show form with current options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", 30)
                ): cv.positive_int,
                vol.Optional(
                    "enable_feature_x",
                    default=self.config_entry.options.get("enable_feature_x", True)
                ): cv.boolean,
            }),
        )
```

**Using options in integration**:
```python
async def async_setup_entry(hass, entry):
    """Set up from config entry."""
    # Read options (with defaults)
    scan_interval = entry.options.get("scan_interval", 30)
    enable_feature_x = entry.options.get("enable_feature_x", True)

    # Use in coordinator
    coordinator = MyCoordinator(
        hass,
        entry,
        api,
        update_interval=timedelta(seconds=scan_interval)
    )

    return True
```

**Listen for options updates**:
```python
async def async_setup_entry(hass, entry):
    """Set up from config entry."""
    coordinator = MyCoordinator(...)

    # Listen for options updates
    entry.async_on_unload(
        entry.add_update_listener(async_update_options)
    )

    return True

async def async_update_options(hass, entry):
    """Handle options update."""
    # Reload entry to apply new options
    await hass.config_entries.async_reload(entry.entry_id)
```

### Discovery Flows

Automatically discover devices on the network and create config entries.

**Supported discovery methods**:
- `bluetooth` - Bluetooth LE discovery
- `dhcp` - DHCP discovery
- `zeroconf` - mDNS/Zeroconf discovery
- `ssdp` - SSDP/UPnP discovery
- `usb` - USB device discovery
- `homekit` - HomeKit accessory discovery

**Zeroconf discovery example**:

1. Add to `manifest.json`:
```json
{
  "zeroconf": [
    {
      "type": "_mydevice._tcp.local.",
      "name": "MyDevice*"
    }
  ]
}
```

2. Implement discovery step:
```python
async def async_step_zeroconf(self, discovery_info):
    """Handle zeroconf discovery."""
    # Extract info from discovery
    host = discovery_info["host"]
    port = discovery_info["port"]
    properties = discovery_info["properties"]

    # Try to get unique ID from discovery
    unique_id = properties.get("id")
    if unique_id:
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

    # Store discovery info for later steps
    self.context["title_placeholders"] = {"name": properties.get("name", host)}
    self._discovered_host = host
    self._discovered_port = port

    # Show confirmation form
    return await self.async_step_discovery_confirm()

async def async_step_discovery_confirm(self, user_input=None):
    """Confirm discovery."""
    if user_input is not None:
        # User confirmed, move to auth
        return await self.async_step_auth()

    # Show confirmation
    return self.async_show_form(
        step_id="discovery_confirm",
        description_placeholders={
            "name": self.context["title_placeholders"]["name"]
        },
    )
```

## Reserved Step Names

**Discovery methods** (automatically called):
- `async_step_bluetooth`
- `async_step_dhcp`
- `async_step_zeroconf`
- `async_step_ssdp`
- `async_step_usb`
- `async_step_homekit`
- `async_step_mqtt`

**User flows**:
- `async_step_user` - Manual setup by user
- `async_step_import` - Import from YAML (legacy)

**Management flows**:
- `async_step_reauth` - Re-authentication
- `async_step_reconfigure` - Reconfiguration

**Custom steps**:
- Can have any name
- Called via `return await self.async_step_custom_name()`

## Testing Config Flows

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for complete testing patterns.

**Minimum tests required** (100% coverage):
- User flow success
- User flow connection error
- User flow auth error
- Duplicate entry abort
- Reauth flow (if implemented)
- Reconfigure flow (if implemented)
- Discovery flow (if implemented)

## Common Patterns

### Storing Temporary Data Between Steps

```python
def __init__(self):
    """Initialize."""
    self._host = None
    self._name = None
    self._discovered_devices = []

async def async_step_user(self, user_input=None):
    """First step."""
    if user_input:
        self._host = user_input[CONF_HOST]  # Store for later
        return await self.async_step_auth()
    ...
```

### Abort Reasons

```python
# Duplicate entry
return self.async_abort(reason="already_configured")

# Successful reauth
return self.async_abort(reason="reauth_successful")

# Successful reconfigure
return self.async_abort(reason="reconfigure_successful")

# No devices found
return self.async_abort(reason="no_devices_found")

# Custom reason (add to strings.json)
return self.async_abort(reason="custom_reason")
```

### Update Existing Entry

```python
self.hass.config_entries.async_update_entry(
    entry,
    data={**entry.data, CONF_API_KEY: new_key},  # Update data
    options={**entry.options, "setting": new_value},  # Update options
    title="New Title",  # Update title
)
```

## Best Practices

1. **Always validate input**: Test connection before creating entry
2. **Set unique ID**: Prevents duplicates
3. **Handle errors gracefully**: Show clear error messages
4. **Use constants**: Import from `homeassistant.const` when possible
5. **Add translations**: All strings in `strings.json`
6. **Test all paths**: 100% config flow test coverage required
7. **Store immutable data in `data`**: Credentials, host, device ID
8. **Store mutable settings in `options`**: Scan interval, features
9. **Implement reauth**: Handle expired credentials
10. **Consider discovery**: Auto-discover when possible

## Next Steps

- See [ENTITY_GUIDE.md](ENTITY_GUIDE.md) for entity development
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for config flow testing
- See [QUALITY_SCALE.md](QUALITY_SCALE.md) for Silver+ tier requirements
