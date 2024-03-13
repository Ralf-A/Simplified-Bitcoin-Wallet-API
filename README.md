# Simplified-Bitcoin-Wallet-API


# Starting the API
## 1. Using Docker(recommended)

## 2. From command line 
### 1. Initialize environment scripts
`myenv\Scripts\activate`
### 2. Initialize database and migrate if needed
`python manage.py makemigrations`
`python manage.py migrate`
### 3. Run the server
`python manage.py runserver`
### 4. Run tests 
`python manage.py test btc_wallet.tests`
