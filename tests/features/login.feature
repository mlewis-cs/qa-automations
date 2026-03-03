Feature: Login

    Scenario: Login as a user with a single account
    Given I am on the login page
    When I log in as "single account attorney"
    Then I am redirected to the cases page after the account page

    Scenario: Login as a user with multiple accounts
    Given I am on the login page
    When I log in as "multi account attorney"
    Then I am redirected to the account page
    When I select a random account
    Then I am redirected to the cases page

    

    
