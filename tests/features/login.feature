Feature: Login

    Scenario: Valid login
    Given I am on the login page
    Then I log in as "test attorney"
    Then I should see the cases page
