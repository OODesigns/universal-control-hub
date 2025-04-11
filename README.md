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






