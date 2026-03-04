Feature: Cases

    Scenario: Logout from cases page
    Given I'm in firm "Mass Cases" as "single account attorney"
    When I log out from the cases page
    Then I am on the login page

    Scenario: Go to web app from cases
    Given I'm in firm "Mass Cases" as "single account attorney"
    When I go to the web app from cases
    Then I am redirected to the web app login page
