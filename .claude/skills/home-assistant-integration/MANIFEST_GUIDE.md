# Manifest.json Complete Reference

The `manifest.json` file contains all metadata about your Home Assistant integration.

## Required Fields

### domain

```json
"domain": "my_device"
```

**Requirements**:
- Lowercase only
- Underscores allowed (NOT hyphens)
- Must be unique across all Home Assistant integrations
- Cannot be changed after publication
- Should be descriptive but concise

**Examples**:
- ✅ `"philips_hue"`, `"mqtt"`, `"google_assistant"`
- ❌ `"My-Device"` (uppercase, hyphens)
- ❌ `"light"` (conflicts with core platform)

### name

```json
"name": "My Device"
```

Human-readable name shown in the UI.

**Requirements**:
- Proper capitalization
- No "integration" suffix
- Brand name as users know it

**Examples**:
- ✅ `"Philips Hue"`, `"MQTT"`, `"Google Assistant"`
- ❌ `"philips hue integration"`, `"The Philips Hue Integration"`

### codeowners

```json
"codeowners": ["@github_username"]
```

List of GitHub usernames responsible for maintaining the integration.

**Requirements**:
- Must include `@` prefix
- At least one codeowner required
- Add yourself for new integrations
- Max 3 codeowners (best practice)

**Example**:
```json
"codeowners": ["@balloob", "@emontnemery"]
```

### documentation

```json
"documentation": "https://www.home-assistant.io/integrations/my_device"
```

URL to integration documentation on home-assistant.io.

**Requirements**:
- Must be `https://www.home-assistant.io/integrations/{domain}`
- Replace `{domain}` with your domain name
- Documentation created in separate home-assistant.io repo

### requirements

```json
"requirements": ["my-device-lib==1.2.3"]
```

Python packages required by the integration.

**Requirements** (CRITICAL):
- ✅ MUST pin exact versions: `"package==1.2.3"`
- ✅ MUST be published to PyPI (NOT GitHub)
- ✅ MUST contain ALL API-specific code (integration just orchestrates)
- ❌ NEVER use unpinned: `"package"` or `"package>=1.0"`
- ❌ NEVER use GitHub URLs

**Examples**:
```json
// ✅ GOOD
"requirements": ["aiohue==4.6.2", "aiohttp==3.8.4"]

// ❌ BAD
"requirements": ["aiohue"]  // Not pinned
"requirements": ["git+https://..."]  // Not on PyPI
```

**Why pinned?**
- Ensures reproducible installs
- Prevents breaking changes from upstream
- Required for Home Assistant stability

### dependencies

```json
"dependencies": ["mqtt", "http"]
```

List of other Home Assistant integrations required.

**Common dependencies**:
- `"mqtt"` - If using MQTT
- `"http"` - If registering HTTP views
- `"zeroconf"` - If using mDNS discovery
- `"bluetooth"` - If using Bluetooth

**Examples**:
```json
// Most integrations
"dependencies": []

// MQTT sensor
"dependencies": ["mqtt"]

// Zigbee hub using MQTT and Zeroconf
"dependencies": ["mqtt", "zeroconf"]
```

### integration_type

```json
"integration_type": "hub"
```

Describes the integration architecture.

**Types**:

1. **device** - Single device
   - Smart bulb, thermostat, switch
   - One config entry = one device
   - Example: WLED, Shelly

2. **hub** - Gateway to multiple devices
   - Connects to hub that manages devices
   - One config entry = many devices
   - Example: Philips Hue, Zigbee2MQTT, UniFi

3. **service** - Single service
   - One config entry = one service instance
   - Not a physical device
   - Example: DuckDNS, IFTTT, Twilio

4. **helper** - Virtual entity
   - Creates entities for automations
   - Not connected to external systems
   - Example: input_boolean, template, group

5. **entity** - Basic entity platform (rarely used)
   - Simple entity without config entry
   - Legacy pattern, prefer `device` or `hub`

6. **hardware** - Hardware integration (rarely used)
   - System hardware integration
   - Example: USB devices, GPIO

7. **system** - System integration (core only)
   - Reserved for core system integrations
   - Example: homeassistant, person

8. **virtual** - Points to another integration
   - Deprecated, points users to replacement
   - Example: legacy integrations

**Choose wisely**: Cannot be changed after publication.

### iot_class

```json
"iot_class": "cloud_polling"
```

Describes how the integration communicates with devices.

**Classes**:

1. **local_polling** - Direct device, delayed updates
   - Polls device on local network
   - State updates delayed by polling interval
   - No cloud dependency
   - Example: Polling HTTP API on device

2. **local_push** - Direct device, immediate updates
   - Device pushes updates to HA
   - Real-time state changes
   - No cloud dependency
   - Example: Webhooks, MQTT from device

3. **cloud_polling** - Cloud API, delayed updates
   - Polls cloud API
   - State updates delayed by polling interval
   - Requires internet
   - Example: Polling REST API

4. **cloud_push** - Cloud API, immediate updates
   - Cloud pushes updates via webhooks
   - Real-time state changes
   - Requires internet
   - Example: Webhooks from cloud service

5. **assumed_state** - Cannot read state
   - Sends commands but cannot verify state
   - Assumes state based on last command
   - No status feedback
   - Example: IR blaster, 433MHz transmitter

6. **calculated** - Calculated from other data
   - No device communication
   - Computes result from other entities
   - Example: template sensor, statistics

**Choosing iot_class**:
```
Do you communicate with a device?
├─ No → calculated
└─ Yes
   ├─ Can you read state?
   │  ├─ No → assumed_state
   │  └─ Yes
   │     ├─ Local network?
   │     │  ├─ Device pushes updates? → local_push
   │     │  └─ You poll device? → local_polling
   │     └─ Cloud API?
   │        ├─ Cloud pushes updates? → cloud_push
   │        └─ You poll cloud? → cloud_polling
```

### quality_scale

```json
"quality_scale": "bronze"
```

Integration quality tier.

**Tiers** (lowest to highest):
- `"bronze"` - Minimum for core integrations
- `"silver"` - Enhanced quality
- `"gold"` - High quality
- `"platinum"` - Highest quality
- `"legacy"` - No config flow (deprecated)

**Start with `"bronze"`** and upgrade as you improve.

See [QUALITY_SCALE.md](QUALITY_SCALE.md) for detailed requirements.

## Optional Fields

### config_flow

```json
"config_flow": true
```

Whether integration supports UI configuration.

**Requirements**:
- MUST be `true` for Bronze tier and above
- If `false`, integration is Legacy tier (deprecated)
- Nearly all new integrations should use config flows

### version

```json
"version": "1.2.0"
```

Integration version using semantic versioning.

**When to use**:
- Multi-file integrations with dependencies between files
- Breaking changes tracking
- Usually omitted for simple integrations

### after_dependencies

```json
"after_dependencies": ["mqtt"]
```

Load integration after these dependencies (soft dependency).

**Difference from `dependencies`**:
- `dependencies` - REQUIRED, setup fails if missing
- `after_dependencies` - Optional, just affects load order

### bluetooth

```json
"bluetooth": [
  {
    "local_name": "My Device*",
    "service_uuid": "0000abcd-0000-1000-8000-00805f9b34fb",
    "manufacturer_id": 1234
  }
]
```

Bluetooth discovery matchers.

**When to use**:
- Integration discovers Bluetooth devices
- Triggers automatic config flow

**Fields**:
- `local_name` - Device name (supports wildcards `*`)
- `service_uuid` - BLE service UUID
- `manufacturer_id` - Manufacturer ID from advertisement
- `manufacturer_data_start` - Manufacturer data prefix (hex)
- `service_data_uuid` - Service data UUID

**Example**:
```json
"bluetooth": [
  {
    "local_name": "MyBrand *",
    "manufacturer_id": 12345,
    "connectable": true
  }
]
```

### dhcp

```json
"dhcp": [
  {
    "hostname": "mydevice-*",
    "macaddress": "AABBCC*"
  }
]
```

DHCP discovery matchers.

**Fields**:
- `hostname` - Device hostname (supports wildcards)
- `macaddress` - MAC address prefix (supports wildcards)
- `registered_devices` - Only match known devices (boolean)

### zeroconf

```json
"zeroconf": [
  {
    "type": "_mydevice._tcp.local.",
    "name": "mydevice*"
  }
]
```

Zeroconf/mDNS discovery matchers.

**Fields**:
- `type` - Service type (e.g., `"_http._tcp.local."`)
- `name` - Service name (supports wildcards)
- `properties` - Required properties dict

**Example**:
```json
"zeroconf": [
  {
    "type": "_hap._tcp.local.",
    "properties": {
      "md": "MyDevice*"
    }
  }
]
```

### ssdp

```json
"ssdp": [
  {
    "st": "urn:schemas-upnp-org:device:MyDevice:1",
    "manufacturer": "MyBrand"
  }
]
```

SSDP/UPnP discovery matchers.

**Fields**:
- `st` - Service type URN
- `manufacturer` - Manufacturer name
- `deviceType` - Device type
- `modelName` - Model name

### usb

```json
"usb": [
  {
    "vid": "10C4",
    "pid": "EA60"
  }
]
```

USB device discovery matchers.

**Fields**:
- `vid` - Vendor ID (hex)
- `pid` - Product ID (hex)
- `serial_number` - Serial number prefix
- `manufacturer` - Manufacturer string
- `description` - Description string

### homekit

```json
"homekit": {
  "models": ["MyDevice1", "MyDevice2"]
}
```

HomeKit discovery matchers.

**Fields**:
- `models` - List of model names from HomeKit advertisement

### mqtt

```json
"mqtt": [
  "mydevice/status",
  "mydevice/+/state"
]
```

MQTT discovery topics.

**Format**:
- List of MQTT topic patterns
- Supports wildcards (`+` single level, `#` multi-level)

### loggers

```json
"loggers": ["my_device_lib", "aiohttp"]
```

Python loggers used by the integration.

**When to use**:
- External library uses specific logger names
- Helps users configure logging for troubleshooting

**Example**:
```json
"loggers": ["aiohue", "aiohttp"]
```

### single_config_entry

```json
"single_config_entry": true
```

Whether integration allows only one config entry.

**When to use**:
- Integration controls singleton resource (e.g., system settings)
- Multiple entries would conflict
- Most integrations should allow multiple entries

### disabled

```json
"disabled": "Integration has been replaced by new_integration"
```

Disables integration with explanation message.

**When to use**:
- Integration deprecated
- Replaced by different integration
- Prevents new setups, existing entries continue working

## Complete Example

Bronze tier integration with multiple features:

```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@myusername"],
  "config_flow": true,
  "dependencies": ["zeroconf"],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "hub",
  "iot_class": "local_push",
  "loggers": ["my_device_lib"],
  "quality_scale": "bronze",
  "requirements": ["my-device-lib==2.1.0"],
  "zeroconf": [
    {
      "type": "_mydevice._tcp.local.",
      "name": "MyDevice*"
    }
  ]
}
```

## Validation

After creating/modifying `manifest.json`, always run:

```bash
python3 -m script.hassfest
```

This validates:
- All required fields present
- Field values are correct format
- Requirements are pinned
- Codeowners exist
- Documentation URL is correct format

## Common Mistakes

1. **Unpinned requirements**:
   ```json
   // ❌ BAD
   "requirements": ["aiohue"]

   // ✅ GOOD
   "requirements": ["aiohue==4.6.2"]
   ```

2. **Wrong domain format**:
   ```json
   // ❌ BAD
   "domain": "My-Device"

   // ✅ GOOD
   "domain": "my_device"
   ```

3. **Missing config_flow**:
   ```json
   // ❌ BAD - Legacy tier
   {
     "domain": "my_device",
     ...
   }

   // ✅ GOOD - Bronze tier
   {
     "domain": "my_device",
     "config_flow": true,
     ...
   }
   ```

4. **Wrong integration_type**:
   ```json
   // ❌ BAD - Philips Hue is a hub
   "integration_type": "device"

   // ✅ GOOD
   "integration_type": "hub"
   ```

5. **Wrong iot_class**:
   ```json
   // ❌ BAD - Polling cloud API is not "push"
   "iot_class": "cloud_push"

   // ✅ GOOD
   "iot_class": "cloud_polling"
   ```

## Discovery Setup Example

Integration with automatic Bluetooth and Zeroconf discovery:

```json
{
  "domain": "my_smart_bulb",
  "name": "My Smart Bulb",
  "codeowners": ["@myusername"],
  "config_flow": true,
  "dependencies": ["bluetooth", "zeroconf"],
  "documentation": "https://www.home-assistant.io/integrations/my_smart_bulb",
  "integration_type": "device",
  "iot_class": "local_push",
  "quality_scale": "bronze",
  "requirements": ["my-bulb-lib==1.0.0"],
  "bluetooth": [
    {
      "local_name": "MyBulb*",
      "manufacturer_id": 12345,
      "connectable": true
    }
  ],
  "zeroconf": [
    {
      "type": "_mydevice._tcp.local.",
      "properties": {
        "model": "SmartBulb*"
      }
    }
  ]
}
```

## Quality Tier Progression

As your integration improves, update `quality_scale`:

**Bronze** (initial):
```json
"quality_scale": "bronze"
```

**Silver** (80%+ coverage, diagnostics):
```json
"quality_scale": "silver"
```

**Gold** (90%+ coverage, strict typing):
```json
"quality_scale": "gold"
```

**Platinum** (95%+ coverage, perfect):
```json
"quality_scale": "platinum"
```

See [QUALITY_SCALE.md](QUALITY_SCALE.md) for detailed tier requirements.
