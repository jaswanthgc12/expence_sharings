# Daily Expenses Sharing Application

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd expensesharing
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:
    ```bash
    python manage.py runserver
    ```

7. Access the API at `http://127.0.0.1:8000/api/`.

## API Endpoints

- `POST /api/users/`: Create a new user.
- `GET /api/users/`: Retrieve user details.
- `POST /api/expenses/`: Add a new expense.
- `GET /api/expenses/`: Retrieve expenses.
- `POST /api/token/`: Obtain JWT token.
- `POST /api/token/refresh/`: Refresh JWT token.

## Example Requests

### Create User

```bash
curl -X POST http://127.0.0.1:8000/api/users/ -d '{"email": "user@example.com", "name": "User Name", "mobile": "1234567890"}' -H "Content-Type: application/json"



curl -X POST http://127.0.0.1:8000/api/expenses/ -d '{"description": "Dinner", "amount": 3000, "split_method": "equal", "participants": [{"user": 1}, {"user": 2}, {"user": 3}]}' -H "Content-Type: application/json"

