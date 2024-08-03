# Created by Michael Lindre at 03/08/2024
Feature: Basic operations
  # Is it possible to turn the ventilation off and on

  Scenario: Turn power on
    Given the ventilation is off
    When I turn the power on
    Then the power status should be "ON"

  Scenario: Turn power off
    Given the ventilation is running
    When I turn the power off
    Then the power status should be "OFF"