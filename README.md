# Simplified-Bitcoin-Wallet-API
## Description

A simple Bitcoin Wallet REST API based on a simplified Bitcoin transaction model using Django NinjaAPI and sqlite3.
Endpoints to view transactions, view balance, add balance, transfer balance.
Features a range of tests.

# Starting the API
### 1. Using Docker(recommended)

### 2. From command line 
### 1. Initialize environment scripts
`myenv\Scripts\activate`
### 2. Initialize database and migrate if needed
`python manage.py makemigrations`
`python manage.py migrate`
### 3. Run the server
`python manage.py runserver`
### 4. Run tests 
`python manage.py test btc_wallet.tests`


# API Documentation

- Default port 8000
- Documentation/usage also can be found on /api/docs
  
#### Transactions

- **GET /api/transactions**
  - Description: Retrieves a list of all transactions.
  - Parameters: None
  - Responses:
    - `200 OK`: Successfully retrieved the list of transactions.
      - Content-Type: `application/json`
      - Schema:
        ```json
        [
          {
            "transaction_id": "uuid",
            "amount": "number",
            "spent": "boolean",
            "created_at": "date-time"
          }
        ]
        ```

#### Balance

- **GET /api/balance**
  - Description: Displays the current balance in BTC and EUR.
  - Parameters: None
  - Responses:
    - `200 OK`: Successfully retrieved the balance.
      - Content-Type: `application/json`
      - Schema:
        ```json
        {
          "balance_btc": "number",
          "balance_eur": "number"
        }
        ```

#### Transfer

- **POST /api/transfer**
  - Description: Initiates a transfer of funds.
  - Parameters: None
  - Request Body:
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "amount_eur": "number"
      }
      ```
  - Responses:
    - `201 Created`: Transfer was successfully created.

#### Add Balance

- **POST /api/add**
  - Description: Adds balance to the account in EUR.
  - Parameters: None
  - Request Body:
    - Content-Type: `application/json`
    - Schema:
      ```json
      {
        "amount_eur": "number"
      }
      ```
  - Responses:
    - `201 Created`: Balance was successfully added.


- **AddBalanceIn**
  - `amount_eur`: Number or String

