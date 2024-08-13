# Created by Michael Lindre at 03/08/2024
Feature: MVHR System basic information
  As a user of the ventilation system, I want to able to basic operations

  Scenario: As a user of the ventilation system
            I want to verify the temperature before and after the MVHR system
            So that I can ensure the system is operating correctly
    Given the MVHR system is operational
    And the system is in exchange mode
    And the ventilation set-point is 22
    And the outside temp is 10
    When I retrieve the temperature before and after the MVHR system
    Then the temperature before the MVHR system should be 10
    And the temperature after the MVHR should be between 20 to 22


