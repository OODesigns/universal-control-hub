# Universal Control Hub

A comprehensive Python framework for industrial automation and device control, specializing in MVHR (Mechanical Ventilation with Heat Recovery) systems with robust Modbus TCP/RTU communication capabilities.

## Overview

Universal Control Hub provides a modular, extensible architecture for interfacing with industrial automation devices. The framework abstracts complex communication protocols behind clean, type-safe interfaces while maintaining the flexibility to support diverse hardware configurations and communication methods.

### Key Capabilities

- **MVHR System Control**: Complete implementation for Blauberg MVHR units with temperature monitoring, ventilation control, and system state management
- **Modbus Communication**: Full-featured Modbus TCP and RTU client implementations with connection management and error handling
- **Device Abstraction**: Protocol-agnostic device interfaces that separate business logic from communication details
- **Configuration Management**: Flexible configuration system supporting multiple device profiles and deployment scenarios
- **Sensor Integration**: Temperature sensor abstractions with multiple acquisition strategies (current-based, voltage-based)
- **Factory Pattern Architecture**: Extensible device and configuration factories for easy system expansion

## Architecture

### Core Components

```
ventilation/source/
├── devices/           # Device abstractions and factory patterns
├── modbus/           # Modbus protocol implementation (TCP/RTU)
├── py_modbus/        # PyModbus integration layer
├── state/            # System state management
├── sensor/           # Sensor abstractions and strategies
├── config/           # Configuration management system
├── utils/            # Shared utilities, validation, logging
├── registered/       # Device and protocol registration
└── blauberg/         # Blauberg MVHR specific implementation
```

### Design Patterns

- **Factory Pattern**: `DeviceFactory` for dynamic device instantiation
- **Strategy Pattern**: Multiple sensor reading strategies and temperature acquisition methods
- **Builder Pattern**: Modbus client builders for flexible connection configuration
- **Abstract Factory**: Protocol-specific client creation
- **State Management**: Centralized system state with validation

## Features

### Communication Protocols
- **Modbus TCP**: Full implementation with connection pooling and retry logic
- **Modbus RTU**: Serial communication support with configurable parameters
- **Async Support**: Non-blocking I/O operations for efficient communication
- **Connection Management**: Automatic reconnection and error recovery

### Device Support
- **Blauberg MVHR**: Complete integration with register mapping and state management
- **Temperature Sensors**: Multiple acquisition strategies (MCP3208 ADC, direct current sensing)
- **Extensible Architecture**: Easy addition of new device types through registration system

### Data Validation & Safety
- **Type-Safe Values**: Strongly typed value objects with range validation
- **Response Validation**: Comprehensive error handling and status reporting
- **Configuration Validation**: Schema-based configuration validation
- **Logging**: Structured logging with file rotation and console output

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd universal-control-hub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   python install_requirements.py
   ```
   
   This automatically detects your platform and installs appropriate dependencies:
   - **Linux**: `pymodbus`, `pyserial`, `spidev`, `behave`
   - **Windows**: `pymodbus`, `pyserial`, `behave`

## Quick Start

### Basic MVHR Control

```python
from ventilation.source.devices.device_factory import DeviceFactory
from ventilation.source.config.config_factory import ConfigFactory
from ventilation.source.utils.standard_name import ssn

# Initialize factories
config_factory = ConfigFactory()
device_factory = DeviceFactory(config_factory)

# Create MVHR device
response = device_factory.get_device(ssn("blauberg_mvhr"))
if response.status == DeviceStatus.VALID:
    mvhr = response.device
    
    # Connect and read system state
    await mvhr.open()
    state = await mvhr.read()
    
    print(f"Supply Temperature: {state.temp_supply_in}")
    print(f"Extract Temperature: {state.temp_supply_out}")
    
    mvhr.close()
```

### Direct Modbus Communication

```python
from ventilation.source.modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from ventilation.source.modbus.tcp_values import IPAddress, Port

# Build Modbus TCP client
client = (ModbusTCPClientBuilder()
    .set_ip_address(IPAddress("192.168.1.100"))
    .set_port(Port(502))
    .set_timeout(Timeout(5.0))
    .build())

# Connect and read data
await client.connect()
data = await client.read()
print(f"Holding Registers: {data.holding_register.value}")
client.disconnect()
```

## Configuration

The framework uses a flexible configuration system supporting JSON-based device profiles:

```json
{
  "mvhr-ip-address": "192.168.1.100",
  "mvhr-port": 502,
  "mvhr-timeout": 5.0,
  "mvhr-retries": 3,
  "dependencies": ["modbus_tcp"]
}
```

## Testing

### Unit Tests
```bash
cd ventilation
python -m pytest tests/unit_tests/
```

### Integration Testing
The framework includes a complete Modbus mock server for testing:

```bash
python ventilation/tests/blauberg-mvhr/mock_server.py
```

### BDD Testing
Behavior-driven tests using `behave`:

```bash
behave ventilation/tests/
```

## Extending the Framework

### Adding New Devices

1. **Create device class** inheriting from `Device`
2. **Implement required methods** (`read()`, `open()`, `close()`)
3. **Register device** in `registered/` module
4. **Add configuration** profile

```python
# devices/my_device.py
class MyDevice(Device):
    async def read(self) -> DeviceStateInterface:
        # Implementation
        pass

# registered/reg_my_device.py
from devices.device_factory import DeviceFactory
from utils.standard_name import ssn

DeviceFactory.register_device(ssn("my_device"), MyDevice)
```

### Adding Communication Protocols

1. **Implement protocol interface**
2. **Create client builder**
3. **Register in factory system**
4. **Add configuration support**

## Logging

The framework provides comprehensive logging with automatic file rotation:

```python
from utils.logger_factory import LoggerFactory

logger_response = LoggerFactory.get_logger("MyComponent")
logger = logger_response.logger

logger.info("Operation completed successfully")
logger.error("Error occurred", exc_info=True)
```

Logs are automatically saved to `logs/` directory with timestamps.

## Hardware Support

### Supported Platforms
- **Linux**: Full support including SPI devices
- **Windows**: Modbus TCP/RTU support (no SPI)
- **Raspberry Pi**: Optimized for GPIO and SPI operations

### Communication Interfaces
- **Ethernet**: Modbus TCP over standard network connections
- **Serial**: RS-485/RS-232 for Modbus RTU
- **SPI**: Direct sensor integration (Linux/Pi only)

## Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Write tests** for new functionality
4. **Ensure code quality** (follow PEP 8)
5. **Submit pull request**

### Development Guidelines
- Maintain type hints throughout codebase
- Add comprehensive docstrings
- Include unit tests for new features
- Update configuration schemas as needed
- Follow existing architectural patterns

## Support

For technical support and questions:
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Documentation**: See `designs/` directory for architectural diagrams
- **Examples**: Check `reference/` directory for usage examples

---

**Note**: This framework is designed for industrial automation applications. Ensure proper safety measures and testing in production environments.