from flask import Flask, json, redirect, url_for, request, render_template, jsonify, Response, make_response, session, flash, send_file
from flask_paginate import Pagination, get_page_parameter
import pdfkit
import MySQLdb.cursors
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import logging
import paypalrestsdk


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurant'
mysql = MySQL(app)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AaWkh0qTgjWJuE1gr3P-jF89oVa5fziQ1h2U1BbXEYvbA1-SzsluclwAiJkyk6hWciuQE-LpjUKywwy0",
  "client_secret": "EIERP2jzxGQDs2AefHv3ILW6ALcyxm6CPFO_6oHb5BSQ4wUCgHTvOPcEpeZbFY87CwZYRyfiYdD37E9s" })

# Define admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

app.config['UPLOAD_FOLDER'] = 'C:\\xampp\\htdocs\\app\\static'

@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    login_type = request.form.get('loginType')
    if login_type == 'admin':
        return redirect(url_for('admin_login'))
    elif login_type == 'employee':
        return redirect(url_for('employee_login'))
    else:
        pass  

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')

# Admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')
# Employee info route
@app.route('/employee_info')
def employee_info():
    try:
        search_term = request.args.get('search_term', '')
        page = request.args.get('page', 1, type=int)
        per_page = 5  
        offset = (page - 1) * per_page
        cur = mysql.connection.cursor()

        if search_term:
            query = """
                SELECT * FROM employee 
                WHERE name LIKE %s OR email LIKE %s 
                ORDER BY id DESC 
                LIMIT %s OFFSET %s
            """
            cur.execute(query, ('%' + search_term + '%', '%' + search_term + '%', per_page, offset))
        else:
            query = """
                SELECT * FROM employee 
                ORDER BY id DESC 
                LIMIT %s OFFSET %s
            """
            cur.execute(query, (per_page, offset))

        data = cur.fetchall()
        
        # Get total number of records for pagination
        if search_term:
            count_query = "SELECT COUNT(*) FROM employee WHERE name LIKE %s OR email LIKE %s"
            cur.execute(count_query, ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            count_query = "SELECT COUNT(*) FROM employee"
            cur.execute(count_query)
        
        total = cur.fetchone()[0]
        cur.close()
        
        total_pages = (total + per_page - 1) // per_page 
        return render_template(
            'employee_info.html',
            employees=data,
            search_term=search_term,
            page=page,
            total_pages=total_pages
        )
    except Exception as e:
        print("An error occurred while fetching employee data:", e)
        return "An error occurred while fetching employee data. Please try again later."


# Add employee route
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    error_message = None
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        # Server-side validation
        if not name or not email or not phone or not username or not password:
            error_message = "All fields are required."
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            error_message = "Invalid email format. Please enter a valid email address."
        elif not re.match(r'^\d{10}$', phone):
            error_message = "Invalid phone number. Please enter a 10-digit number without any special characters."
        else:
            try:
                # Insert data into the database
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO employee (name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s)",
                            (name, email, phone, username, password))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('employee_info'))
            except Exception as e:
                print("An error occurred while adding employee:", e)
                error_message = "An error occurred while adding employee. Please try again later."
    return render_template('add_employee.html', error_message=error_message)

# View employee route
@app.route('/view_employee/<int:employee_id>')
def view_employee(employee_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
        data = cur.fetchone()
        cur.close()
        if data:
            return render_template('view_employee.html', data=data)
        else:
            return 'Employee not found', 404
    except Exception as e:
        print("An error occurred while fetching employee data:", e)
        return "An error occurred while fetching employee data. Please try again later."

# Delete employee route
@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    try:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM employee WHERE id = %s", (employee_id,))
            mysql.connection.commit()
            cur.close()
            print(f"Employee with ID {employee_id} deleted successfully")
            return redirect(url_for('employee_info'))
    except Exception as e:
        print("An error occurred while deleting employee:", e)
        return jsonify({'success': False}), 500

# Edit employee route
@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        try:
            # Update employee data in the database
            cur = mysql.connection.cursor()
            cur.execute("UPDATE employee SET name = %s, email = %s, phone = %s, username = %s, password = %s WHERE id = %s",
                        (name, email, phone, username, password, employee_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('employee_info'))
        except Exception as e:
            print("An error occurred while updating employee:", e)
            return "An error occurred while updating employee. Please try again later."
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
            data = cur.fetchone()
            cur.close()
            if data:
                employee_data = {
                    'id': data[0],
                    'name': data[1],
                    'email': data[2],
                    'phone': data[3],
                    'username': data[4],
                    'password': data[5]
                }
                return render_template('edit_employee.html', data=employee_data)
            else:
                error_message = f"Employee with ID {employee_id} not found"
                return render_template('error.html', error_message=error_message), 404
        except Exception as e:
            print("An error occurred while fetching employee data:", e)
            return "An error occurred while fetching employee data. Please try again later."

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/generate_pdf/<int:employee_id>')
def generate_pdf(employee_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
        data = cur.fetchone()
        cur.close()
        if data:
            html_content = f"""
            <html>
            <head>
                <title>Employee Information</title>
            </head>
            <body>
                <h1>Employee Information</h1>
                <p><strong>ID:</strong> {data[0]}</p>
                <p><strong>Name:</strong> {data[1]}</p>
                <p><strong>Email:</strong> {data[2]}</p>
                <p><strong>Phone:</strong> {data[3]}</p>
                <p><strong>Username:</strong> {data[4]}</p>
                <p><strong>Password:</strong> {data[5]}</p>
            </body>
            </html>
            """

            # Path to wkhtmltopdf executable
            wkhtmltopdf_path = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

            # Generate PDF from HTML content and specify wkhtmltopdf path
            pdf = pdfkit.from_string(html_content, False, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))

            # Send the generated PDF as response
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=employee_{employee_id}_info.pdf'
            return response
        else:
            return 'Employee not found', 404
    except Exception as e:
        print("An error occurred while generating PDF:", e)
        return "An error occurred while generating PDF. Please try again later."

@app.route('/menu_category')
def menu_category():
    try:
        search_term = request.args.get('search_term', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = 5  # Number of categories per page
        offset = (page - 1) * per_page
        
        cur = mysql.connection.cursor()
        
        if search_term:
            search_query = f"%{search_term}%"
            cur.execute("SELECT COUNT(*) FROM category WHERE category_name LIKE %s", (search_query,))
            total_categories = cur.fetchone()[0]
            total_pages = (total_categories + per_page - 1) // per_page  # Calculate total pages
            
            cur.execute("SELECT * FROM category WHERE category_name LIKE %s ORDER BY id DESC LIMIT %s OFFSET %s", 
                        (search_query, per_page, offset))
        else:
            cur.execute("SELECT COUNT(*) FROM category")
            total_categories = cur.fetchone()[0]
            total_pages = (total_categories + per_page - 1) // per_page  
            
            cur.execute("SELECT * FROM category ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
        
        data = cur.fetchall()
        cur.close()
        
        return render_template('menu_category.html', categories=data, page=page, total_pages=total_pages, search_term=search_term)
    except Exception as e:
        print("An error occurred while fetching category data:", e)
        return "An error occurred while fetching category data. Please try again later."
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            try:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO category (category_name) VALUES (%s)", (category_name,))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('menu_category'))
            except Exception as e:
                print("An error occurred while adding category:", e)
                return "An error occurred while adding category. Please try again later."
        else:
            return redirect(url_for('add_category'))
    else:
        return render_template('add_category.html')
@app.route('/view_category/<int:category_id>')
def view_category(category_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        data = cur.fetchone()
        cur.close()
        if data:
            return render_template('view_category.html', data=data)
        else:
            return 'Category not found', 404
    except Exception as e:
        print("An error occurred while fetching category data:", e)
        return "An error occurred while fetching category data. Please try again later."
    
@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        category_name = request.form.get('category_name')  
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE category SET category_name = %s WHERE id = %s",
                        (category_name, category_id))  
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('menu_category'))  
        except Exception as e:
            print("An error occurred while updating category:", e)
            return "An error occurred while updating category. Please try again later."
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM category WHERE id = %s", (category_id,))
            data = cur.fetchone()
            cur.close()
            if data:
                category_data = {
                    'id': data[0],
                    'category_name': data[1],
                }
                return render_template('edit_category.html', data=category_data)
            else:
                error_message = f"Category with ID {category_id} not found"
                return render_template('error.html', error_message=error_message), 404
        except Exception as e:
            print("An error occurred while fetching category data:", e)
            return "An error occurred while fetching category data. Please try again later."    
@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    try:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM category WHERE id = %s", (category_id,))
            mysql.connection.commit()
            cur.close()
            print(f"Category with ID {category_id} deleted successfully")
            return redirect(url_for('menu_category'))
    except Exception as e:
        print("An error occurred while deleting category:", e)
        return jsonify({'success': False}), 500
    
@app.route('/menu_management')
def menu_management():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5 

        search_term = request.args.get('q', '')

        cur = mysql.connection.cursor()

        if search_term:
            cur.execute("SELECT COUNT(*) FROM menu WHERE menu_name LIKE %s OR category LIKE %s OR price LIKE %s", 
                        ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        else:
            cur.execute("SELECT COUNT(*) FROM menu")

        total_items = cur.fetchone()[0]

        total_pages = (total_items + per_page - 1) // per_page

        offset = (page - 1) * per_page

        if search_term:
            cur.execute("SELECT * FROM menu WHERE menu_name LIKE %s OR category LIKE %s OR price LIKE %s ORDER BY id DESC LIMIT %s OFFSET %s", 
                        ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', per_page, offset))
        else:
            cur.execute("SELECT * FROM menu ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))

        menu_data = cur.fetchall()

        cur.close()

        return render_template('menu_management.html', menu_data=menu_data, page=page, per_page=per_page, total_pages=total_pages, search_term=search_term)
    except Exception as e:
        print("An error occurred while fetching menu data:", e)
        return "An error occurred while fetching menu data. Please try again later."
    
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'POST':
        category = request.form.get('category')
        menu_name = request.form.get('menu_name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO menu (category, menu_name, description, price, image) VALUES (%s, %s, %s, %s, %s)",
                        (category, menu_name, description, price, filename))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('menu_management'))
        except Exception as e:
            print("An error occurred while adding menu:", e)
            return "An error occurred while adding menu. Please try again later."
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT DISTINCT category FROM menu")
            categories = cur.fetchall()
            cur.close()
            return render_template('add_menu.html', categories=categories)
        except Exception as e:
            print("An error occurred while fetching categories:", e)
            return "An error occurred while fetching categories. Please try again later."
@app.route('/view_menu/<int:menu_id>')
def view_menu(menu_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM menu WHERE id = %s", (menu_id,))
        menu_data = cur.fetchone()
        cur.close()
        if menu_data:
            return render_template('view_menu.html', menu_data=menu_data)
        else:
            return 'Menu not found', 404
    except Exception as e:
        print("An error occurred while fetching menu data:", e)
        return "An error occurred while fetching menu data. Please try again later."
@app.route('/edit_menu/<int:menu_id>', methods=['GET', 'POST'])
def edit_menu(menu_id):
    if request.method == 'POST':
        category = request.form.get('category')
        menu_name = request.form.get('menu_name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        try:
            cur = mysql.connection.cursor()

            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("UPDATE menu SET category = %s, menu_name = %s, description = %s, price = %s, image = %s WHERE id = %s",
                            (category, menu_name, description, price, filename, menu_id))
            else:
                cur.execute("UPDATE menu SET category = %s, menu_name = %s, description = %s, price = %s WHERE id = %s",
                            (category, menu_name, description, price, menu_id))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('menu_management'))
        except Exception as e:
            print("An error occurred while updating menu:", e)
            return "An error occurred while updating menu. Please try again later."
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM menu WHERE id = %s", (menu_id,))
            data = cur.fetchone()
            cur.close()
            if data:
                menu_data = {
                    'id': data[0],
                    'category': data[1],
                    'menu_name': data[2],
                    'description': data[3],
                    'price': data[4],
                    'image': data[5]
                }
                categories = ["Appetizers", "Entrees", "Sides", "Beverages", "Desserts", "Kids Menu", "Drinks", "Special Dietary Needs"]
                return render_template('edit_menu.html', data=menu_data, categories=categories, menu_id=menu_id)
            else:
                error_message = f"Menu with ID {menu_id} not found"
                return render_template('error.html', error_message=error_message), 404
        except Exception as e:
            print("An error occurred while fetching menu data:", e)
            return "An error occurred while fetching menu data. Please try again later."
@app.route('/delete_menu/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    try:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM menu WHERE id = %s", (menu_id,))
            mysql.connection.commit()
            cur.close()
            print(f"Menu with ID {menu_id} deleted successfully")
            return redirect(url_for('menu_management'))
    except Exception as e:
        print("An error occurred while deleting menu:", e)
        return jsonify({'success': False}), 500
@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE username = %s AND password = %s", (username, password))
            employee = cur.fetchone()
            cur.close()

            if employee:
                session['logged_in'] = True 
                return redirect(url_for('order_management'))
            else:
                error = 'Invalid username or password. Please try again.'
                return render_template('employee_login.html', error=error)
        except Exception as e:
            print("An error occurred while logging in:", e)
            error = 'An error occurred. Please try again later.'
            return render_template('employee_login.html', error=error)
    return render_template('employee_login.html')

@app.route('/orders')
def orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5  
        search_term = request.args.get('search', '')

        orders_data, total_pages = get_paginated_orders(page, per_page, search_term)
        return render_template('orders.html', orders_data=orders_data, page=page, total_pages=total_pages, search_term=search_term)
    except Exception as e:
        print("An error occurred while fetching orders data:", e)
        return "An error occurred while fetching orders data. Please try again later."
def get_paginated_orders(page, per_page, search_term=''):
    offset = (page - 1) * per_page
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if search_term:
        search_query = f"%{search_term}%"
        cur.execute("SELECT COUNT(*) as total FROM orders WHERE firstname LIKE %s OR email LIKE %s OR phone LIKE %s OR product LIKE %s", (search_query, search_query, search_query, search_query))
        total = cur.fetchone()['total']
        
        cur.execute("SELECT * FROM orders WHERE firstname LIKE %s OR email LIKE %s OR phone LIKE %s OR product LIKE %s ORDER BY id DESC LIMIT %s OFFSET %s", (search_query, search_query, search_query, search_query, per_page, offset))
    else:
        cur.execute("SELECT COUNT(*) as total FROM orders")
        total = cur.fetchone()['total']
        
        cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    
    orders_data = cur.fetchall()
    total_pages = (total + per_page - 1) // per_page  
    cur.close()
    return orders_data, total_pages
@app.route('/view_orders/<int:order_id>')
def view_order(order_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order_data = cur.fetchone()
        cur.close()
        if order_data:
            return render_template('view_orders.html', order_data=order_data)
        else:
            return "Order not found", 404
    except Exception as e:
        print("An error occurred while fetching the order details:", e)
        return "An error occurred while fetching the order details. Please try again later."
    
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        mysql.connection.commit()
        cur.close()
        flash("Order deleted successfully", "success")
        return redirect(url_for('orders'))
    except MySQLdb.Error as db_error:
        logging.error(f"MySQL error: {db_error}")
        flash("A database error occurred. Please try again later.", "danger")
        return redirect(url_for('orders'))
    except Exception as e:
        logging.error(f"An error occurred while deleting the order: {e}")
        flash("An error occurred while deleting the order. Please try again later.", "danger")
        return redirect(url_for('orders'))
@app.route('/download_pdf/<int:order_id>')
def download_pdf(order_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cur.fetchone()
        cur.close()

        if not order:
            return "Order not found", 404
        # Generate PDF
        filename = f"order_{order_id}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.drawString(100, height - 100, f"Order ID: {order['id']}")
        c.drawString(100, height - 120, f"Name: {order['firstname']}")
        c.drawString(100, height - 140, f"Email: {order['email']}")
        c.drawString(100, height - 160, f"Phone: {order['phone']}")
        c.drawString(100, height - 180, f"Product: {order['product']}")
        c.drawString(100, height - 200, f"Price: {order['price']}")
        c.drawString(100, height - 220, f"Quantity: {order['quantity']}")
        c.drawString(100, height - 240, f"Subtotal: {order['subtotal']}")

        c.save()

        return send_file(filename, as_attachment=True)
    except Exception as e:
        print("An error occurred while generating the PDF:", e)
        return "An error occurred while generating the PDF. Please try again later."
@app.route('/get_notification_count')
def get_notification_count():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT COUNT(*) as count FROM orders WHERE seen = 0")
        count = cur.fetchone()['count']
        cur.close()
        return jsonify({'count': count})
    except Exception as e:
        print("An error occurred while fetching the notification count:", e)
        return jsonify({'count': 0}), 500
@app.route('/get_notifications')
def get_notifications():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM orders WHERE seen = 0 ORDER BY id DESC LIMIT 10")
        notifications = cur.fetchall()
        if notifications:
            ids = tuple(n['id'] for n in notifications if n['id'])
            if len(ids) == 1:
                ids = f"({ids[0]})"
            else:
                ids = str(ids)
            cur.execute(f"UPDATE orders SET seen = 1 WHERE id IN {ids}")
            mysql.connection.commit()

        cur.close()
        return jsonify({'notifications': notifications})
    except Exception as e:
        print("An error occurred while fetching the notifications:", e)
        return jsonify({'notifications': []}), 500

@app.route('/mark_notifications_as_seen', methods=['POST'])
def mark_notifications_as_seen():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE orders SET seen = 1 WHERE seen = 0")
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    except Exception as e:
        print("An error occurred while marking notifications as seen:", e)
        return jsonify({'success': False}), 500
@app.route('/order_management')
def order_management():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        search_term = request.args.get('q', '')
        if search_term:
            search_query = f"%{search_term}%"
            cur.execute("SELECT * FROM menu WHERE name LIKE %s OR category LIKE %s", (search_query, search_query))
        else:
            cur.execute("SELECT * FROM menu")
        menu_data = cur.fetchall()
        cur.close()
        return render_template('order_management.html', menu_data=menu_data, search_term=search_term)
    
    if request.method == 'POST':
        order_details = request.form.get('order_details')
        if order_details:
            order_details = json.loads(order_details)
            session['order_details'] = []

            for item_id, quantity in order_details.items():
                cur.execute("SELECT * FROM menu WHERE id = %s", (item_id,))
                menu_item = cur.fetchone()
                subtotal = menu_item['price'] * quantity  
                session['order_details'].append({
                    'id': menu_item['id'],
                    'name': menu_item['name'],
                    'price': menu_item['price'],
                    'quantity': quantity,
                    'subtotal': subtotal  
                })
            session['grand_total'] = sum(item['subtotal'] for item in session['order_details'])
            cur.close()
            return redirect(url_for('confirm_order'))
@app.route('/checkout', methods=['POST'])
def checkout():
    cur = mysql.connection.cursor()

    # Extract form data
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    order_details = json.loads(request.form['order_details'])
    amount = request.form['amount']
    transaction_id = request.form['transaction_id']
    payer_id = request.form['payer_id']
    payment_status = request.form['payment_status']

    # Lists to store product details
    products = []
    prices = []
    quantities = []
    subtotals = []

    for item in order_details:
        product = item['name']
        price = float(item['price'])
        quantity = int(item['quantity'])
        subtotal = price * quantity
        
        products.append(product)
        prices.append(price)
        quantities.append(quantity)
        subtotals.append(subtotal)

    # Calculate total price
    total_price = sum(subtotals)

    # Concatenate product names into a single string
    product_str = ', '.join(products)

    # Insert order into database with additional fields
    cur.execute("""
        INSERT INTO orders (firstname, lastname, phone, email, address, product, price, quantity, subtotal, transaction_id, payer_id, payment_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (firstname, lastname, phone, email, address, product_str, total_price, sum(quantities), total_price, transaction_id, payer_id, payment_status))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('order_success'))


@app.route('/order_success')
def order_success():
    return "Order placed successfully!"

if __name__ == '__main__':
    app.run(debug=True)