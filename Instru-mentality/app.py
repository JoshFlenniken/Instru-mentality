
from flask import Flask, render_template, request, redirect
import database.db_connector as db
from config import Config
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)

PORT = 10986

# ########################################
# ########## ROUTE HANDLERS

# READ ROUTES
@app.route("/", methods=["GET"])
def home():
    try:
        return render_template("home.j2")

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500


@app.route("/customers", methods=["GET"])
def customers():
    try:
        dbConnection = db.connectDB()  # Open database connection

        # Create and execute queries
        query1 = "SELECT * FROM Customers;"
        customers = db.query(dbConnection, query1).fetchall()

        # Render the customers.j2 file
        return render_template(
            "customers.j2", customers=customers
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/employees", methods=["GET"])
def employees():
    try:
        dbConnection = db.connectDB()  # Open database connection

        # Create and execute queries
        query1 = "SELECT * FROM Employees;"
        employees = db.query(dbConnection, query1).fetchall()

        # Render the employees.j2 file
        return render_template(
            "employees.j2", employees=employees
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/orders", methods=["GET"])
def orders():
    try:
        dbConnection = db.connectDB()  # Open database connection

        # Create and execute queries
        query1 = "SELECT * FROM Orders;"
        orders = db.query(dbConnection, query1).fetchall()

        query2 = "SELECT customerID FROM Customers;"
        customers = db.query(dbConnection, query2).fetchall()

        query3 = "SELECT employeeID FROM Employees;"
        employees = db.query(dbConnection, query3).fetchall()

        # Render the orders.j2 file
        return render_template(
            "orders.j2", orders=orders, customers=customers, employees=employees
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


@app.route("/products", methods=["GET"])
def products():
    try:
        dbConnection = db.connectDB()  # Open database connection

        # Create and execute queries
        query1 = "SELECT * FROM Products;"
        products = db.query(dbConnection, query1).fetchall()

        # Render the products.j2 file
        return render_template(
            "products.j2", products=products
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/orderdetails", methods=["GET"])
def orderdetails():
    try:
        dbConnection = db.connectDB() # Open database connection
        
        # JOIN clause creates intersections between Orders and Products tables.
        query1 = "SELECT * FROM OrderDetails;"
        orderdetails = db.query(dbConnection, query1).fetchall()

        query2 = "SELECT productID, productName FROM Products;"
        products = db.query(dbConnection, query2).fetchall()

        query3 = """
          SELECT
            Orders.orderID,
            Customers.firstName,
            Customers.lastName
          FROM Orders
          JOIN Customers
            ON Orders.customerID = Customers.customerID;
        """
        orders = db.query(dbConnection, query3).fetchall()
        
        # Render the orderdetails.j2 file
        return render_template(
            "orderdetails.j2",
            orderdetails=orderdetails,
            products=products,
            orders=orders
        )

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# RESET ROUTES
@app.route("/home/reset", methods=["POST"])
def reset_database():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_ResetDatabase();"
        cursor.execute(query1, ())

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        print(f"Resetting database data")

        # Redirect the user to the updated webpage
        return redirect("/")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# DELETE ROUTES FOR CUSTOMERS
@app.route("/customers/delete", methods=["POST"])
def delete_customers():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        customer_id = request.form["delete_customer_id"]
        customer_name = request.form["delete_customer_name"]

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteCustomer(%s);"
        cursor.execute(query1, (customer_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE Customer. ID: {customer_id} Name: {customer_name}")

        # Redirect the user to the updated webpage
        return redirect("/customers")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# DELETE ROUTES FOR EMPLOYEES
@app.route("/employees/delete", methods=["POST"])
def delete_employees():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        employee_id = request.form["delete_employee_id"]
        employee_name = request.form["delete_employee_name"]

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteEmployee(%s);"
        cursor.execute(query1, (employee_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE Employee. ID: {employee_id} Name: {employee_name}")

        # Redirect the user to the updated webpage
        return redirect("/employees")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# DELETE ROUTES FOR ORDERS
@app.route("/orders/delete", methods=["POST"])
def delete_orders():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        order_id = request.form["delete_order_id"]

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteOrder(%s);"
        cursor.execute(query1, (order_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE Order. ID: {order_id}")

        # Redirect the user to the updated webpage
        return redirect("/orders")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# DELETE ROUTES FOR PRODUCTS
@app.route("/products/delete", methods=["POST"])
def delete_products():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        product_id = request.form["delete_product_id"]
        product_name = request.form["delete_product_name"]

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteProduct(%s);"
        cursor.execute(query1, (product_id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE Product. ID: {product_id} Name: {product_name}")

        # Redirect the user to the updated webpage
        return redirect("/products")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# DELETE ROUTES FOR ORDER DETAILS
@app.route("/orderdetails/delete", methods=["POST"])
def delete_orderdetails():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        orderdetails_id = int(request.form["delete_orderdetails_id"])

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_DeleteOrderDetail(%s);"
        cursor.execute(query1, (orderdetails_id,))
        dbConnection.commit()

        print(f"DELETE OrderDetails. ID: {orderdetails_id}")
        return redirect("/orderdetails")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# UPDATE ROUTES FOR CUSTOMERS
@app.route("/customers/update", methods=["POST"])
def update_customers():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        customer_id = request.form["update_customer_id"]

        # Cleanse data - If the email or phoneNumber aren't valid, make them NULL.
        email = request.form.get("update_customer_email", "").strip()
        try:
            phone_number = int(request.form["update_customer_phoneNumber"])
        except (ValueError):
            phone_number = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateCustomer(%s, %s, %s);"
        cursor.execute(query1, (customer_id, email, phone_number))

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        query2 = "SELECT firstName, lastName FROM Customers WHERE customerID = %s;"
        cursor.execute(query2, (customer_id,))
        rows = cursor.fetchone()  # Fetch name info on updated employee

        print(f"UPDATE Customers. ID: {customer_id} Name: {rows[0]} {rows[1]}")

        # Redirect the user to the updated webpage
        return redirect("/customers")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# UPDATE ROUTES FOR EMPLOYEES
@app.route("/employees/update", methods=["POST"])
def update_employees():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        employee_id = request.form["update_employee_id"]

        # Cleanse data - If the email or phoneNumber aren't valid, make them NULL.
        email = request.form.get("update_employee_email", "").strip()
        try:
            phone_number = int(request.form["update_employee_phoneNumber"])
        except (ValueError):
            phone_number = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateEmployee(%s, %s, %s);"
        cursor.execute(query1, (employee_id, email, phone_number))

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        query2 = "SELECT firstName, lastName FROM Employees WHERE employeeID = %s;"
        cursor.execute(query2, (employee_id,))
        rows = cursor.fetchone()  # Fetch name info on updated employee

        print(f"UPDATE Employees. ID: {employee_id} Name: {rows[0]} {rows[1]}")

        # Redirect the user to the updated webpage
        return redirect("/employees")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# UPDATE ROUTES FOR ORDERS
@app.route("/orders/update", methods=["POST"])
def update_orders():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        order_id = request.form["update_order_id"]

        # Cleanse data - If the customerID, employeeID or orderDate aren't valid, make them NULL.
        try:
            customer_id = int(request.form["update_order_customerID"])
        except (ValueError):
            customer_id = None

        try:
            employee_id = int(request.form["update_order_employeeID"])
        except (ValueError):
            employee_id = None

        order_date = request.form.get("update_order_orderDate", None)

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateOrder(%s, %s, %s, %s);"
        cursor.execute(query1, (order_id, customer_id, employee_id, order_date))

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        query2 = "SELECT orderID FROM Orders WHERE orderID = %s;"
        cursor.execute(query2, (order_id,))
        rows = cursor.fetchone()  # Fetch info on updated order

        print(f"UPDATE Orders. ID: {rows[0]}")

        # Redirect the user to the updated webpage
        return redirect("/orders")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


# UPDATE ROUTES FOR PRODUCTS
@app.route("/products/update", methods=["POST"])
def update_products():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        product_id = request.form["update_product_id"]

        # Cleanse data - If name, category, price, stock or isActive aren't valid, make them NULL.
        name = request.form.get("update_product_productName", "").strip()
        category = request.form.get("update_product_productCategory", "").strip()
        try:
            price = float(request.form["update_product_productPrice"])
        except (ValueError):
            price = None
        try:
            stock = int(request.form["update_product_productStock"])
        except (ValueError):
            stock = None
        try:
            is_active = int(request.form["update_product_isActive"])
        except (ValueError):
            is_active = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateProduct(%s, %s, %s, %s, %s, %s);"
        cursor.execute(query1, (product_id, name, category, price, stock, is_active))

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        query2 = "SELECT productName FROM Products WHERE productID = %s;"
        cursor.execute(query2, (product_id,))
        rows = cursor.fetchone()  # Fetch name info on updated product

        print(f"UPDATE Products. ID: {product_id} Name: {rows[0]}")

        # Redirect the user to the updated webpage
        return redirect("/products")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# UPDATE ROUTES FOR ORDER DETAILS
@app.route("/orderdetails/update", methods=["POST"])
def update_orderdetails():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        orderdetails_id = int(request.form["update_orderdetails_id"])
        order_id        = int(request.form["update_orderdetails_orderID"])
        product_id      = int(request.form["update_orderdetails_productID"])
        order_quantity  = int(request.form["update_orderdetails_orderQuantity"])

        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_UpdateOrderDetail(%s, %s, %s, %s);"
        cursor.execute(query1, (
            orderdetails_id,
            order_id,
            product_id,
            order_quantity
        ))
        cursor.nextset()
        dbConnection.commit()

        print(f"UPDATE OrderDetails. ID: {orderdetails_id}")
        return redirect("/orderdetails")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()



# CREATE ROUTES FOR CUSTOMERS
@app.route("/customers/create", methods=["POST"])
def create_customers():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        firstName = request.form["create_customer_firstName"]
        lastName = request.form["create_customer_lastName"]
        email = request.form["create_customer_email"]

        try:
            phoneNumber = int(request.form["create_customer_phoneNumber"])
        except ValueError:
            phoneNumber = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_CreateCustomer(%s, %s, %s, %s, @new_id);"
        cursor.execute(query1, (firstName, lastName, email, phoneNumber))

        # Store ID of last inserted row
        new_id = cursor.fetchone()[0]

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        print(f"CREATE Customers. ID: {new_id} Name: {firstName} {lastName}")

        # Redirect the user to the updated webpage
        return redirect("/customers")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# CREATE ROUTES FOR EMPLOYEES
@app.route("/employees/create", methods=["POST"])
def create_employees():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        firstName = request.form["create_employee_firstName"]
        lastName = request.form["create_employee_lastName"]
        email = request.form["create_employee_email"]

        # Cleanse data - If phoneNumber isn't a number, make it NULL.
        try:
            phoneNumber = int(request.form["create_employee_phoneNumber"])
        except ValueError:
            phoneNumber = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_CreateEmployee(%s, %s, %s, %s, @new_id);"
        cursor.execute(query1, (firstName, lastName, email, phoneNumber))

        # Store ID of last inserted row
        new_id = cursor.fetchone()[0]

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        print(f"CREATE Employees. ID: {new_id} Name: {firstName} {lastName}")

        # Redirect the user to the updated webpage
        return redirect("/employees")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# CREATE ROUTES FOR ORDERS
@app.route("/orders/create", methods=["POST"])
def create_orders():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        customerID = request.form["create_order_customerID"]
        employeeID = request.form["create_order_employeeID"]

        try:
            orderDate = request.form["create_order_orderDate"]
        except ValueError:
            orderDate = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_CreateOrder(%s, %s, %s, @new_id);"
        cursor.execute(query1, (customerID, employeeID, orderDate))

        # Store ID of last inserted row
        new_id = cursor.fetchone()[0]

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        print(f"CREATE Orders. ID: {new_id} Cust: {customerID} Emp: {employeeID}")

        # Redirect the user to the updated webpage
        return redirect("/orders")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# CREATE ROUTES FOR PRODUCTS
@app.route("/products/create", methods=["POST"])
def create_products():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        productName = request.form["create_product_productName"]
        productCategory = request.form["create_product_productCategory"]

        try:
            productPrice = int(request.form["create_product_productPrice"])
        except ValueError:
            productPrice = None

        try:
            productStock = int(request.form["create_product_productStock"])
        except ValueError:
            productStock = None

        try:
            isActive = int(request.form["create_product_isActive"])
        except ValueError:
            isActive = None

        # Create and execute queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_CreateProduct(%s, %s, %s, %s, %s, @new_id);"
        cursor.execute(query1, (productName, productCategory, productPrice, productStock, isActive))

        # Store ID of last inserted row
        new_id = cursor.fetchone()[0]

        # Consume the result set (if any) before running the next query
        cursor.nextset()  # Move to the next result set (for CALL statements)

        dbConnection.commit()  # commit the transaction

        print(f"CREATE Products. ID: {new_id} Name: {productName}")

        # Redirect the user to the updated webpage
        return redirect("/products")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# CREATE ROUTES FOR ORDER DETAILS
@app.route("/orderdetails/create", methods=["POST"])
def create_orderdetails():
    try:
        dbConnection = db.connectDB()  # Open database connection
        cursor = dbConnection.cursor()

        # Get form data
        order_id       = int(request.form["create_orderdetails_orderID"])
        product_id     = int(request.form["create_orderdetails_productID"])
        order_quantity = int(request.form["create_orderdetails_orderQuantity"])

        # Using parameterized queries (Prevents SQL injection attacks)
        query1 = "CALL sp_CreateOrderDetail(%s, %s, %s, @new_id);"
        cursor.execute(query1, (order_id, product_id, order_quantity))

        new_id = cursor.fetchone()[0]
        cursor.nextset()
        dbConnection.commit()

        print(f"CREATE OrderDetails. ID: {new_id}")
        return redirect("/orderdetails")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return "An error occurred while executing the database queries.", 500

    finally:
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

# ########################################
# ########## LISTENER

if __name__ == "__main__":
    app.run(
        port=PORT, debug=True
    )  # debug is an optional parameter. Behaves like nodemon in Node.
