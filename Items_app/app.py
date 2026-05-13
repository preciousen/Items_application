# Import Flask functions needed for the web application
from flask import Flask, render_template, request, redirect

# Import sqlite3 so that we can work with the SQLite database
import sqlite3

# Import os so that we can work with file paths
import os


# Create the Flask application
app = Flask(__name__)


# Create a folder path where uploaded images will be stored
UPLOAD_FOLDER = "static/uploads"

# Store the upload folder inside Flask configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------------------------------------------
# DATABASE SECTION
# ---------------------------------------------------

# Function used to create the database table
def create_table():

    # Connect to the SQLite database
    # If the database does not exist, it will be created automatically
    conn = sqlite3.connect("items.db")

    # Create a cursor object
    # The cursor allows us to run SQL commands
    cursor = conn.cursor()

    # SQL command to create the items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (

            -- Automatically generated number
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Item name column
            item_name TEXT NOT NULL,

            -- Unique item code / barcode column
            item_code TEXT UNIQUE NOT NULL,

            -- Image filename column
            photo TEXT NOT NULL
        )
    """)

    # Save database changes
    conn.commit()

    # Close the database connection
    conn.close()


# Call the function when the program starts
create_table()


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

# Route for the home page
@app.route("/")

# Function that opens the Add Item page
def add_page():

    # Display add_item.html
    return render_template("add_item.html")


# ---------------------------------------------------
# ADD ITEM SECTION
# ---------------------------------------------------

# Route used to save an item into the database
# methods=["POST"] means the form will send data securely
@app.route("/add", methods=["POST"])

def add_item():

    # Get the item name from the form
    item_name = request.form["item_name"]

    # Get the unique item code from the form
    item_code = request.form["item_code"]

    # Get the uploaded image file
    photo = request.files["photo"]


    # Get the image filename
    photo_name = photo.filename

    # Create the full image path
    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_name)

    # Save the uploaded image inside the uploads folder
    photo.save(photo_path)


    # Connect to the database
    conn = sqlite3.connect("items.db")

    # Create a cursor object
    cursor = conn.cursor()


    # Insert the item into the database
    cursor.execute("""
        INSERT INTO items (item_name, item_code, photo)
        VALUES (?, ?, ?)
    """, (item_name, item_code, photo_name))


    # Save database changes
    conn.commit()

    # Close database connection
    conn.close()


    # Move the user to the search page after saving
    return redirect("/search")


# ---------------------------------------------------
# SEARCH PAGE
# ---------------------------------------------------

# Route for the search page
@app.route("/search")

def search_page():

    # Open the search page
    # item=None means no item has been searched yet
    return render_template("search_item.html", item=None)


# ---------------------------------------------------
# FIND ITEM SECTION
# ---------------------------------------------------

# Route used to search for an item
@app.route("/find", methods=["POST"])

def find_item():

    # Get the item code entered by the user
    item_code = request.form["item_code"]


    # Connect to the database
    conn = sqlite3.connect("items.db")

    # Create a cursor object
    cursor = conn.cursor()


    # SQL query to search for the item
    cursor.execute("SELECT * FROM items WHERE item_code = ?", (item_code,))

    # Get the first matching item
    item = cursor.fetchone()


    # Close the database connection
    conn.close()


    # Open the search page again
    # Send the found item information to HTML
    return render_template("search_item.html", item=item)


# ---------------------------------------------------
# START THE FLASK APPLICATION
# ---------------------------------------------------

# Run the Flask server
if __name__ == "__main__":

    # debug=True automatically updates changes while coding
    app.run(debug=True)