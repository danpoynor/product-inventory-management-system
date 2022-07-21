# Product Management Inventory System

Demo console application written in Python using SQLAlchemy and SQLite.

This app uses my knowledge of CSV, File I/O, and database ORMs to create a product management inventory system which allows users to easily interact with a stores product data. The data is cleaned from the CSV file before it is added to an SQLite  database. All interactions with the records use ORM methods for viewing records, creating records, and exporting a new CSV backup.

---

## Run the app

Clone this repo then `cd product-inventory-management-system`.

Assuming you have Python3 installed on a MacOS, run these commands (or something similar):

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

When done running the app, you can deactivate the virtual environment by running `deactivate`.

---

## Technology Used

- [Python](https://www.python.org/) Programming language that lets you work quickly
and integrate systems more effectively. ([docs](https://docs.python.org/3/))
- [SQLAlchemy](https://www.sqlalchemy.org/) The Python SQL Toolkit and Object Relational Mapper ([docs](https://docs.sqlalchemy.org/en/latest/))
- [SQLite](https://www.sqlite.org/) The most used database engine in the world. ([docs](https://www.sqlite.org/docs.html))

---

## Screenshot

Example showing "List All Products" feature (L) displaying list or products from the automatically generated `inventory.db` database and the "Product Analysis" (X) feature:

<img src="https://user-images.githubusercontent.com/764270/180823172-e3fcfa28-d393-489c-ab42-1e0edf32a6a8.png" data-canonical-src="https://user-images.githubusercontent.com/764270/180823172-e3fcfa28-d393-489c-ab42-1e0edf32a6a8.png" width="548" height="950" alt="Python command-line application for product inventory management system by Dan Poynor" />
