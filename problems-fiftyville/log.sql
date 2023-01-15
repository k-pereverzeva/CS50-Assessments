-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description 
    FROM crime_scene_reports 
    WHERE year = 2020  
    AND month = 7 
    AND day = 28 
    AND street = "Chamberlin Street"

-- time = 10:15am place = courthouse
SELECT transcript 
    FROM interviews 
    WHERE year = 2020  
    AND month = 7 AND day = 28
    AND transcript LIKE "%courthouse%"
    
-- ~10:25 a car in the courthouse parking lot; ATM on Fifer Street; phone call (less then 1 min); the earliest flight out of Fiftyville tomorrow (29.07.2020)
SELECT name FROM people
    JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
    WHERE day = 28 AND month = 7 AND year = 2020
    AND hour = 10
    AND minute >= 15 AND minute < 25
    AND activity = "exit"
    INTERSECT
-- people's names who left the building at that time
SELECT name FROM people
    JOIN bank_accounts ON bank_accounts.person_id = people.id
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE year = 2020  AND month = 7 AND day = 28 
    AND atm_location = "Fifer Street" 
    AND transaction_type =  "withdraw"
    INTERSECT
-- who used a card
SELECT name FROM people
    JOIN phone_calls ON phone_calls.caller = people.phone_number
    WHERE year = 2020  AND month = 7
    AND day = 28
    AND duration <= 60
    INTERSECT
-- phone calls less then minute
SELECT name FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    WHERE flight_id = (
    SELECT id FROM flights 
    WHERE day = 29 AND month = 7 AND year = 2020
    ORDER BY hour, minute LIMIT 1);
-- people who bought a ticket

SELECT name FROM people
    JOIN phone_calls ON phone_calls.receiver = people.phone_number
    WHERE day = 28 AND month = 7 AND year = 2020
    AND duration < 60
    AND caller = (
    SELECT phone_number FROM people
    WHERE name = "Ernest");
-- person's name who helped 

SELECT city FROM airports
    JOIN flights ON flights.destination_airport_id = airports.id
    JOIN passengers ON passengers.flight_id = flights.id
    JOIN people ON people.passport_number = passengers.passport_number
    WHERE people.passport_number = (
    SELECT passport_number FROM people
    WHERE name = "Ernest");
-- city's name