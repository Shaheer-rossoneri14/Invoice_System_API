Invoice Generation API
This project is an API that allows users to manage a list of items for sale, create purchase orders, update those orders, and generate invoices in PDF format. The application facilitates the following actions:

View available items with their details (name, price, description).
Create and update a purchase order with the list of items and quantities.
Generate and download invoices for purchases in PDF format.
Features
Item Management: Allows the user to view available items with their details.
Purchase Management: Enables creating and updating purchase orders with selected items.
Invoice Generation: Generates and returns a PDF invoice for a given purchase.
Prerequisites
Make sure you have the following installed:

Python 3.8+
Django 3.2+
Django Rest Framework
ReportLab (for generating PDFs)
SQLite (or any other database)
Installation
Clone the repository:

git clone https://github.com/your-username/invoice-generator-api.git
cd invoice-generator-api
Create a virtual environment:

python -m venv env
Activate the virtual environment:

For macOS/Linux:
source env/bin/activate
For Windows:
.\env\Scripts\activate
Install the required dependencies:

pip install -r requirements.txt
Apply database migrations:

python manage.py migrate
Create a superuser (optional, for accessing the Django admin panel):

python manage.py createsuperuser
API Endpoints
Item Management
GET /api/items/
Fetch all available items in the system. The response will include fields like name, price, description, and stock.
Purchase Management
POST /api/purchases/
Create a new purchase by sending a list of items with corresponding quantities.

PUT /api/purchases/{id}/
Update an existing purchase by modifying the list of items.

Invoice Generation
GET /api/invoices/{purchase_id}/
Generate a PDF invoice for a given purchase. The invoice will include all details such as the purchased items, quantities, total price, and purchase information.
Example API Requests
Create Purchase
To create a new purchase, send a POST request to /api/purchases/ with the following payload:

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
Update Purchase
To update an existing purchase, send a PUT request to /api/purchases/{id}/ with the following payload:

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
Generate Invoice
To generate a PDF invoice for a purchase, send a GET request to /api/invoices/{purchase_id}/. The API will return a PDF file containing the invoice.
