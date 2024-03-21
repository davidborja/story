
# Stori Accounts Django App

This Django app named "Stori Accounts" provides CRUD (Create, Read, Update, Delete) functionality for various endpoints related to users, accounts, transactions, account types, templates and send mail.

## Installation

1. Clone this repository:


git clone <repository_url>
cd stori
Install dependencies using the provided requirements.txt file:

pip install -r requirements.txt
Create a .env file in the root directory with the following content:

```bash
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=xxxxxx
EMAIL_HOST_PASSWORD=xxxxx
EMAIL_PORT=2525

ENGINE=django.db.backends.postgresql_psycopg2
DATABASE_NAME=xxxxx
DATABASE_USER=xxxxx
DATABASE_PASSWORD=xxxxx
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
PORT=8000
HOST=0.0.0.0
```

Run database migrations to initialize the database schema:

- python manage.py makemigrations
- python manage.py migrate
CRUD Endpoints


## Endpoints

### Users

- `GET /users/`: Retrieve all users
- `POST /users/`: Create a new user
- `DELETE /users/<id>/`: Delete a user by ID
- `PUT /users/<id>/`: Update a user by ID
- `PATCH /users/<id>/`: Partially update a user by ID

### Accounts

- `GET /accounts/`: Retrieve all accounts
- `POST /accounts/`: Create a new account
- `DELETE /accounts/<id>/`: Delete an account by ID
- `PUT /accounts/<id>/`: Update an account by ID
- `PATCH /accounts/<id>/`: Partially update an account by ID

### Transactions

- `GET /transactions/`: Retrieve all transactions
- `POST /transactions/`: Create a new transaction
- `DELETE /transactions/<id>/`: Delete a transaction by ID
- `PUT /transactions/<id>/`: Update a transaction by ID
- `PATCH /transactions/<id>/`: Partially update a transaction by ID

### Account Types

- `GET /account_types/`: Retrieve all account types
- `POST /account_types/`: Create a new account type
- `DELETE /account_types/<id>/`: Delete an account type by ID
- `PUT /account_types/<id>/`: Update an account type by ID
- `PATCH /account_types/<id>/`: Partially update an account type by ID

### Template

- `GET /template/`: Retrieve all templates
- `POST /template/`: Create a new template
- `DELETE /template/<id>/`: Delete a template by ID
- `PUT /template/<id>/`: Update a template by ID
- `PATCH /template/<id>/`: Partially update a template by ID

## Command: send_emails

A custom Django management command called `send_emails` is available. It receives a CSV file with the following information:

AccountId, Date, Transaction
1,10/01/2024,+50
2,23/02/2024,-1000
1,23/02/2024,+1000


This command processes the CSV file and sends emails to respective account holders regarding their transactions.

To use this command, run the following:

```bash
python manage.py send_emails path/to/csv_file.csv

Replace path/to/csv_file.csv with the path to your CSV file containing transaction information.
