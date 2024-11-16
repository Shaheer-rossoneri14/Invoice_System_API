# Invoice Generation API

This project is an API that allows users to manage a list of items for sale, create purchase orders, update those orders, and generate invoices in PDF format. The application facilitates the following actions:

- View available items with their details (name, price, description).
- Create and update a purchase order with the list of items and quantities.
- Generate and download invoices for purchases in PDF format.

## Features

- **Item Management**: Allows the user to view available items with their details.
- **Purchase Management**: Enables creating and updating purchase orders with selected items.
- **Invoice Generation**: Generates and returns a PDF invoice for a given purchase.

## Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Django 3.2+
- Django Rest Framework
- ReportLab (for generating PDFs)
- SQLite (or any other database)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/invoice-generator-api.git
    cd invoice-generator-api
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment**:

   - For macOS/Linux:
     ```bash
     source env/bin/activate
     ```
   - For Windows:
     ```bash
     .\env\Scripts\activate
     ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply database migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional, for accessing the Django admin panel)**:

    ```bash
    python manage.py createsuperuser
    ```

## API Endpoints

### Item Management

- **GET** `/api/items/`  
  Fetch all available items in the system. The response will include fields like `name`, `price`, `description`, and `stock`.

### Purchase Management

- **POST** `/api/purchases/`  
  Create a new purchase by sending a list of items with corresponding quantities.

- **PUT** `/api/purchases/{id}/`  
  Update an existing purchase by modifying the list of items.

### Invoice Generation

- **GET** `/api/invoices/{purchase_id}/`  
  Generate a PDF invoice for a given purchase. The invoice will include all details such as the purchased items, quantities, total price, and purchase information.

## Example API Requests

### Create Purchase
To create a new purchase, send a POST request to /api/purchases/ with the following payload:

bash
```{
  "items": [
    {
      "id": 1,
      "quantity": 2
    },
    {
      "id": 3,
      "quantity": 1
    }
  ]
}
```

### Update Purchase
To update an existing purchase, send a PUT request to /api/purchases/{id}/ with the following payload:

bash
```{
  "items": [
    {
      "id": 1,
      "quantity": 5
    },
    {
      "id": 2,
      "quantity": 3
    }
  ]
}
```

### Generate Invoice
To generate a PDF invoice for a purchase, send a GET request to /api/invoices/{purchase_id}/. The API will return a PDF file containing the invoice.
