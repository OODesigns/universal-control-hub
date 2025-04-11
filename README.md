# Universal Control Hub

A modular framework for interfacing with industrial devices through standardized protocols, with a focus on Modbus integration and high-level device abstractions.

## Overview

Universal Control Hub serves as a bridge between low-level communication protocols (like Modbus) and high-level device abstractions (such as MVHR - Mechanical Ventilation with Heat Recovery systems). It provides a consistent interface for controlling and monitoring various industrial devices regardless of their underlying communication methods.

## Architecture

The project is structured around these core components:

### Protocol Adapters
- **Modbus Interface**: Abstracts Modbus communications (TCP, RTU) with unified read/write operations
- **Future-ready**: Designed for extension to other protocols (BACnet, KNX, etc.)

### Device Abstraction
- High-level representations of physical devices (e.g., Blauberg MVHR)
- Device-specific state management and control logic
- Protocol-agnostic device interfaces

### Core Infrastructure
- Robust error handling and response validation
- Asynchronous I/O operations
- Type-safe value handling with validation

## Features

- **Protocol Abstraction**: Unified interface regardless of underlying protocol
- **Device Modeling**: Represents physical devices with their specific capabilities
- **Asynchronous Operations**: Non-blocking I/O for efficient communication
- **Validation Layer**: Type-safe value handling with range constraints
- **Modular Design**: Easily extend to new devices or protocols
- **Testability**: Comprehensive mock implementations for testing

## Modbus Implementation

The Modbus implementation includes:

- **ModbusInterface**: Abstract interface defining core Modbus operations
- **ModbusData**: Structured container for different Modbus register types
- **ModbusReader**: Efficient chunked reading of Modbus registers with automatic optimization
- **Value Validation**: Type-safe handling of Modbus values with range constraints

### Supported Modbus Register Types
- Coils (read/write 1-bit values)
- Discrete Inputs (read-only 1-bit values)
- Holding Registers (read/write 16-bit values)
- Input Registers (read-only 16-bit values)

## Device Implementation

### MVHR (Mechanical Ventilation with Heat Recovery)
The project includes a specific implementation for MVHR systems:

- **State representation**: Fan speeds, temperatures, modes, alarms
- **Control operations**: Start/stop, adjust ventilation levels, setpoint management
- **Monitoring**: Temperature sensing, filter status, error conditions

## Getting Started

### Prerequisites
- Python 3.9+
- Required dependencies can be installed using:
```bash
python install_requirements.py
```

### Basic Usage Example

```python
# Setting up a Modbus TCP connection to an MVHR device
from ventilation.source.modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from ventilation.source.devices.blauberg_mvhr import BlaubergMVHR

async def main():
    # Configure Modbus connection
    builder = ModbusTCPClientBuilder()
    builder.host("192.168.1.100").port(502).unit(1)
    
    # Initialize MVHR device
    mvhr = BlaubergMVHR(modbus_builder=builder)
    
    # Start communication
    response = await mvhr.start()
    if response.is_success():
        # Read device state
        state = await mvhr.read_data()
        
        # Print current temperatures
        print(f"Supply air: {state.supply_air_temperature}°C")
        print(f"Extract air: {state.extract_air_temperature}°C")
        
        # Set fan speed
        await mvhr.set_fan_speed(70)  # 70%
        
        # Stop communication
        await mvhr.stop()
```

## Project Structure

- `/ventilation`: Main project directory
    - `/source`: Source code
        - `/modbus`: Modbus implementation
        - `/devices`: Device-specific implementations
    - `/tests`: Test files
        - `/unit_tests`: Unit tests for components
        - `/blauberg-mvhr`: MVHR-specific tests and mock servers
    - `/features`: Behavior-driven tests
- `/designs`: UML diagrams and design documents
- `/reference`: Reference implementations and examples

## Development

### Running Tests
```bash
pytest ventilation/tests
```

### Adding New Devices

1. Create a new device class implementing the appropriate device interface
2. Implement device-specific protocol handling (parsing registers, commands)
3. Add unit tests for the device implementation
4. Add integration tests with mock servers if applicable

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
