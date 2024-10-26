# Created by Michael Lindre at 03/08/2024
Feature: MVHR System basic information
  As a user of the ventilation system, I want to able to basic operations

  Scenario: System stops when ventilation config file is missing
    Given the system is started without a ventilation config file
    When the system attempts to read the ventilation configuration
    Then the system should set its state to indicate that the configuration file is missing






