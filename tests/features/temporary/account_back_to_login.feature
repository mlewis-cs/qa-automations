Feature: Account page navigation

  Scenario: Back to Signin from the account page
    Given I am on the login page
    When I log in as "multi account attorney"
    Then I am redirected to the account page
    When I go back to the login page from the account page
    Then I am on the login page
