from pathlib import Path

from behave import given, when, then

from utils.response import Response
from utils.status import Status
from ventilation.system import System

LAST_ELEMENT = -1

CONFIG_FILE = "missing ventilation config file"

@given("the system is started without a ventilation config file")
def step_impl(context):
   context.system = System()

@when("the system attempts to read the ventilation configuration")
def step_impl(context):
    sys:System = context.system
    context.system_response =  sys.start()

@then("the system should set its state to indicate that the configuration file is missing")
def step_impl(context):
    response : Response[str] = context.system_response
    assert response.status == Status.EXCEPTION, "expecting Exception"
    assert ("%s" % CONFIG_FILE) in response.details, "Expected '%s' in response details" % CONFIG_FILE

    # Extract the log file name from response details
    log_file_path =  Path(response.details.split("Log file:")[LAST_ELEMENT].strip())  # Assuming the log file path is mentioned in response details

    # Load the log file and verify its contents
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()

    assert CONFIG_FILE in log_contents, "Expected '%s' in log file contents" % CONFIG_FILE





