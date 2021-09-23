# Backend Challenge

Scenario
Sample company has set up in five countries in Africa and intends to sell its products to
its customers in those markets. Products can be the same or vary in each country. Each
country will have its own staff and management. The first point of contact for each
customer will be the Sales Agent, who will be collecting the KYC details as well as
mapping the location for each customer, however, once the customer has been set up in
the system, they can download the app created to make their own orders. Agents will
need to know when customers make these orders even if the customers make them for
themselves via the customer app. Management will need to know how many customers
they have, orders made and how much product has been sold.
#### Expected deliverables

From the services highlighted, pick two or more services and develop them using the
stack highlighted above. They will need to run showing inputs and outputs.


### Requirements

* Python3.6+
* Postgres 10+

### Run

Run develop server.

```shell
# Install required python libraries
pip install -r requirements.txt
# Copy env.example to .env
cp env.example .env
# Migrate migrations
./manage.py migrate
# Create Super user
./manage.py createsuperuser
# Run server
./manage.py runserver

```


### API Collection

[POSTMAN Collection](https://www.getpostman.com/collections/4a9738ded176bb80570c)

### Usage

This application covers the following:

1. User account creation
2. Role allocation
   1. Sales agent
   2. Management
   3. Staff
   4. Customers
3. Product CRUD
4. Order CRUD

