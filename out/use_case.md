## __UC-000: Create account__

__Use case:__ Create account

__Primary actor:__ Client

__Scope:__ Account system

__Level:__ User

__Stakeholders:__ Client wants to create a new account

__Preconditions:__ 

1. Email is valid
2. Username is available

__Postconditions:__ 

1. A new account is created

__Nominal case:__ 

1. User types an email
2. User types a username
3. User types a password

__Extensions:__ 

* __Extension 1:__ Invalid email

	1.0 User types an invalid email

	1.1 System notifies user

* __Extension 2:__ Unavailable username

	2.0 User types an unavailable username

	2.1 System notifies user

__Other:__ The system sends an email to the user to authenticate the account
