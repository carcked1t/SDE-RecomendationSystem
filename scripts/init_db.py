"""Initialize the SQLite DB and add sample products for testing."""
from app.db import engine, Base
from app import models
from app.db import SessionLocal

sample = [
    # Electronics
    {"name": "Wireless Mouse", "category": "Electronics", "price": 25.99, "rating": 4.2, "stock": 100, "views": 10, "clicks": 3},
    {"name": "Mechanical Keyboard", "category": "Electronics", "price": 79.99, "rating": 4.6, "stock": 50, "views": 8, "clicks": 2},
    {"name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.99, "rating": 4.8, "stock": 20, "views": 20, "clicks": 5},
    {"name": "USB-C Charger", "category": "Electronics", "price": 19.99, "rating": 4.0, "stock": 300, "views": 12, "clicks": 4},
    {"name": "Bluetooth Speaker", "category": "Electronics", "price": 45.00, "rating": 4.3, "stock": 80, "views": 6, "clicks": 1},

    # Home
    {"name": "Water Bottle", "category": "Home", "price": 15.00, "rating": 4.0, "stock": 200, "views": 5, "clicks": 0},
    {"name": "Coffee Mug", "category": "Home", "price": 8.5, "rating": 4.1, "stock": 150, "views": 7, "clicks": 1},
    {"name": "Desk Lamp", "category": "Home", "price": 29.99, "rating": 4.4, "stock": 60, "views": 9, "clicks": 2},
    {"name": "Throw Pillow", "category": "Home", "price": 22.0, "rating": 4.0, "stock": 120, "views": 3, "clicks": 0},

    # Sports
    {"name": "Running Shoes", "category": "Sports", "price": 120.0, "rating": 4.4, "stock": 40, "views": 15, "clicks": 6},
    {"name": "Yoga Mat", "category": "Sports", "price": 30.0, "rating": 4.2, "stock": 150, "views": 4, "clicks": 0},
    {"name": "Fitness Tracker", "category": "Sports", "price": 99.99, "rating": 4.3, "stock": 70, "views": 11, "clicks": 3},

    # Stationery
    {"name": "Notebook", "category": "Stationery", "price": 2.5, "rating": 3.9, "stock": 500, "views": 2, "clicks": 0},
    {"name": "Gel Pens (Pack of 10)", "category": "Stationery", "price": 6.99, "rating": 4.1, "stock": 400, "views": 1, "clicks": 0},
    {"name": "Planner", "category": "Stationery", "price": 12.0, "rating": 4.5, "stock": 100, "views": 4, "clicks": 1},

    # Books
    {"name": "Learn Python", "category": "Books", "price": 29.99, "rating": 4.7, "stock": 50, "views": 18, "clicks": 7},
    {"name": "Data Structures", "category": "Books", "price": 39.99, "rating": 4.6, "stock": 30, "views": 9, "clicks": 2},

    # Clothing
    {"name": "T-Shirt (Unisex)", "category": "Clothing", "price": 15.0, "rating": 4.0, "stock": 300, "views": 3, "clicks": 0},
    {"name": "Jeans", "category": "Clothing", "price": 45.0, "rating": 4.2, "stock": 80, "views": 6, "clicks": 1},

    # Kitchen
    {"name": "Chef Knife", "category": "Kitchen", "price": 49.99, "rating": 4.5, "stock": 40, "views": 5, "clicks": 0},
    {"name": "Cutting Board", "category": "Kitchen", "price": 18.99, "rating": 4.1, "stock": 150, "views": 2, "clicks": 0},

    # Beauty
    {"name": "Face Cream", "category": "Beauty", "price": 24.99, "rating": 4.3, "stock": 200, "views": 7, "clicks": 1},

    # Toys
    {"name": "Building Blocks", "category": "Toys", "price": 34.99, "rating": 4.4, "stock": 90, "views": 4, "clicks": 1},
    {"name": "Remote Car", "category": "Toys", "price": 59.99, "rating": 4.5, "stock": 30, "views": 6, "clicks": 2},

    # Garden
    {"name": "Garden Gloves", "category": "Garden", "price": 9.99, "rating": 4.0, "stock": 120, "views": 1, "clicks": 0},
    {"name": "Watering Can", "category": "Garden", "price": 19.99, "rating": 4.2, "stock": 60, "views": 2, "clicks": 0},

    # Electronics - More similar price ranges for better related recommendations
    {"name": "Wireless Earbuds", "category": "Electronics", "price": 49.99, "rating": 4.2, "stock": 100, "views": 9, "clicks": 3},
    {"name": "Portable SSD 1TB", "category": "Electronics", "price": 129.99, "rating": 4.6, "stock": 40, "views": 7, "clicks": 2},
    {"name": "Webcam HD", "category": "Electronics", "price": 39.99, "rating": 4.0, "stock": 65, "views": 5, "clicks": 1}
]


def init():
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Clear existing products to avoid duplicates when re-running
    print("Clearing existing products (if any)...")
    db.query(models.Product).delete()
    db.commit()

    print("Adding sample products...")
    for p in sample:
        prod = models.Product(**p)
        db.add(prod)
    db.commit()

    count = db.query(models.Product).count()
    print(f"Seeded {count} products.")
    db.close()
    print("Done. Run the app and try endpoints.")

if __name__ == "__main__":
    init()
