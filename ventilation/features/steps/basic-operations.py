from bisect import insort

from behave import *

from ventilation.temperature_sensor import AbstractTemperatureSensor
from ventilation.ventilation import Ventilation, VentilationMode


class MockTemperatureSensor(AbstractTemperatureSensor):
    def get_temperature(self):
        return self.current_temp

    def __init__(self):
        self.current_temp = None

@given("the MVHR system is operational")
def step_impl(context):
    context.outside_temp_sensor = MockTemperatureSensor()
    context.ventilation = Ventilation(context.outside_temp_sensor)

@given("the system is in {mode} mode")
def step_impl(context, mode):
    context.ventilation.set_mode(VentilationMode[mode.upper()])

@given("the ventilation set-point is {setpoint:d}")
def step_impl(context, setpoint):
    context.ventilation.set_setpoint_temperature(setpoint)

@given("the outside temp is {temp:d}")
def step_impl(context, temp):
    context.outside_temp_sensor.temp = temp

@when("I retrieve the temperature before and after the MVHR system")
def step_impl(context):
    context.temp_before = context.ventilation.get_mvhr_temp_before()
    context.temp_after = context.ventilation.get_mvhr_temp_after()

@then("the temperature before the MVHR system should be {temp:d}")
def step_impl(context, temp):
    assert context.temp_before == temp,f'{temp} is not {context.temp_before}'


@then("the temperature after the MVHR should be between {low_temp:d} to {high_temp:d}")
def step_impl(context, low_temp, high_temp):
    assert context.temp_after in range(low_temp, high_temp), \
        f'{context.temp_after} is not in range {low_temp} to {high_temp}'
