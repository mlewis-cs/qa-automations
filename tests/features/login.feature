Feature: Login

    Scenario: Login as a user with a single account
    Given I am on the login page
    When I log in as "single account attorney"
    Then I am logged in after the account page

    Scenario: Login as a user with multiple accounts
    Given I am on the login page
    When I log in as "multi account attorney"
    Then I am redirected to the account page
    When I select a random account
    Then I am logged in

    Scenario: Shorthand
    Given I'm in firm "Mobile Testing" as "multi account attorney"

    Scenario: Invalid credentials show an error
    Given I am on the login page
    When I log in with invalid credentials
    Then I see an invalid credentials error message
    And I am on the login page
