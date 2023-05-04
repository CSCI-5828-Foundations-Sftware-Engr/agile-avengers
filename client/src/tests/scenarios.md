# Scenarios for User Acceptance-tests

## Scenario 1: Sign up 
- Open the webpage for Sign up.
- Enter username and non-matching passwords - check if the banner is present. 
- Reenter the correct password and click Submit.
- Go to the next page, enter the rest of the info with invalid mobile number.
- Check if the banner appears and then reenter the valid mobile number and click submit.
- Finally check if the banner appears for 'Accoutn created successfully'.
- Two users are created with this so that the send and recieve functionality can be tested.

## Scenario 2: Login and Logout
- Open the webpage for Login.
- Enter username and password.
- Click Submit.
- Check if the tabs for 'Send or Request Payment', 'Add Payment Methods' and 'Transaction' are present.
- Click on the logout button and verify if the logout action got executed.

## Scenario 3: Add payment using Credit card, Debit card and Bank account
- Open the webpage for Login.
- Enter username and password.
- Click Submit.
- Check if the tabs for 'Send or Request Payment', 'Add Payment Methods' and 'Transaction' are present.
- Click on 'Add Payment Methods' tab and from the dropdown, select 'Credit Card'.
- Enter the required information and click on 'Save'.
- Verify if the banner appears stating 'Credit card has been successfully added'.
- The last three steps are performed for Bank account and Debit card as well.

## Scenario 4: Send Payment
- Open the webpage for Login.
- Enter username and password.
- Click Submit.
- Check if the tabs for 'Send or Request Payment', 'Add Payment Methods' and 'Transaction' are present.
- Click on 'Send or Request Payment' tab and from the dropdown, select 'Send'.
- Enter the respective values and click 'Save'.
- Verify if the payment got send by the banner notification.

## Scenario 5: Request Payment
- Open the webpage for Login.
- Enter username and password.
- Click Submit.
- Check if the tabs for 'Send or Request Payment', 'Add Payment Methods' and 'Transaction' are present.
- Click on 'Send or Request Payment' tab and from the dropdown, select 'Request'.
- Enter the respective values and click 'Save'.
- Verify if the payment was recieved based on the banner notification.

## Scenario 6: Pending Payments
- Open the webpage for Login.
- Enter username and password.
- Click Submit.
- Check if the tabs for 'Send or Request Payment', 'Add Payment Methods' and 'Transaction' are present.
- Click on 'Send or Request Payment' tab and from the dropdown, select 'Pending Payment Requests'.
- Enter the respective values and click 'Save'.
- Verify if the pending payment was resolved the banner notification.