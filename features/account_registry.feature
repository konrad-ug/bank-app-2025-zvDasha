Feature: Account registry

  Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

  Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  # TODO 

  Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "12345678901"
    When I update "name" of account with pesel: "12345678901" to "johnny"
    Then Account with pesel "12345678901" has "name" equal to "johnny"

  Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "anna", last name: "smith", pesel: "98765432100"
    Then Account with pesel "98765432100" exists in registry
    And Account with pesel "98765432100" has "name" equal to "anna"
    And Account with pesel "98765432100" has "surname" equal to "smith"
    And Account with pesel "98765432100" has balance equal to "0"

  Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  # Nowe scenariusze na wykonywanie przelewów.

  Scenario: User makes a incoming transfer
    Given Account registry is empty
    And I create an account using name: "elon", last name: "musk", pesel: "09212972332"
    When I make an incoming transfer of "1000" to account with pesel "09212972332"
    Then Account with pesel "09212972332" has balance equal to "1000"

  Scenario: User makes a outgoing transfer
    Given Account registry is empty
    And I create an account using name: "jeff", last name: "bezos", pesel: "07212536486"
    And I make an incoming transfer of "500" to account with pesel "07212536486"
    When I make an outgoing transfer of "200" from account with pesel "07212536486"
    Then Account with pesel "07212536486" has balance equal to "300"

  Scenario: Outgoing transfer fails when not enough money
    Given Account registry is empty
    And I create an account using name: "broke", last name: "guy", pesel: "97080555966"
    And I make an incoming transfer of "50" to account with pesel "97080555966"
    When I try to make an outgoing transfer of "100" from account with pesel "97080555966"
    Then The transfer should fail with status code "422"
    And Account with pesel "97080555966" has balance equal to "50"

  Scenario: User can make express transfer with fee
    Given Account registry is empty
    And I create an account using name: "rodrigo", last name: "stole", pesel: "04262295493"
    # Поповнюємо на 100
    And I make an incoming transfer of "100" to account with pesel "04262295493"
    # Робимо експрес переказ на 50 (комісія 1)
    When I make an express transfer of "50" from account with pesel "04262295493"
    # Очікуємо 49 (100 - 50 - 1 = 49)
    Then Account with pesel "04262295493" has balance equal to "49"