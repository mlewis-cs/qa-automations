Feature: Cases

    Scenario: Go to web app from cases
    Given I am on the login page
    When I log in as "single account attorney"
    Then I am logged in after the account page
    When I go to the web app from cases
    Then I am redirected to the web app login page
