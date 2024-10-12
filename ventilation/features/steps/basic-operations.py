from behave import *

from devices.temperature_sensor import TemperatureSensor
from ventilation.source.ventilation import Ventilation
from ventilation_mode import VentilationMode
from utils.temperaturecelsius import TemperatureCelsius


class MockTemperatureSensorInterface(TemperatureSensor):
    def get_temperature(self):
        if self.current_temp is None:
            raise ValueError("Current temperature is not set.")
        return self.current_temp

    def __init__(self):
        super().__init__()
        self.current_temp = None


@given("the MVHR system is operational")
def step_impl(context):
    context.outside_temp_sensor = MockTemperatureSensorInterface()
    context.ventilation = Ventilation(context.outside_temp_sensor)


@given("the system is in {mode} mode")
def step_impl(context, mode: str):
    try:
        ventilation_mode = VentilationMode[mode.upper()]
    except KeyError:
        raise ValueError(f"Invalid ventilation mode: {mode}")
    context.ventilation.set_mode(ventilation_mode)


@given("the ventilation set-point is {setpoint:d}")
def step_impl(context, setpoint: int):
    context.ventilation.set_setpoint_temperature(TemperatureCelsius(setpoint))


@given("the outside temp is {temp:d}")
def step_impl(context, temp: int):
    context.outside_temp_sensor.current_temp = TemperatureCelsius(temp)


@when("I retrieve the temperature before and after the MVHR system")
def step_impl(context):
    context.temp_before = context.ventilation.mvhr_temp_supply_in()
    context.temp_after = context.ventilation.mvhr_temp_supply_out()


@then("the temperature before the MVHR system should be {temp:d}")
def step_impl(context, temp: int):
    expected_temp = TemperatureCelsius(temp)
    assert context.temp_before == expected_temp, \
        f"Expected temperature before MVHR to be {expected_temp.value}, but got {context.temp_before.value}"


@then("the temperature after the MVHR should be between {low_temp:d} to {high_temp:d}")
def step_impl(context, low_temp: int, high_temp: int):
    low = TemperatureCelsius(low_temp)
    high = TemperatureCelsius(high_temp)
    assert low <= context.temp_after <= high, \
        f"Expected temperature after MVHR to be between {low.value} and {high.value}, but got {context.temp_after.value}"
