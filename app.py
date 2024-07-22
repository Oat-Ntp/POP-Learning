from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, current_app, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
import re
from datetime import datetime
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from jinja2 import Environment
import os
import io
from operator import itemgetter



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # เลือกวิธีการเก็บ session ใน filesystem

Session(app)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pop_learning'

mysql = MySQL(app)



login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, role, first_name, last_name, username, email):
        self.id = id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
class Admin(UserMixin):
    def __init__(self, id, role, first_name, last_name, username, email, tel):
        self.id = id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.tel = tel
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
class Instructor(UserMixin):
    def __init__(self, id, role, first_name, last_name, username, email, tel):
        self.id = id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.tel = tel
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Query the 'user' table for a regular user
    cursor.execute('SELECT * FROM user WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data['id'], role=user_data['role'],
                    first_name=user_data['first_name'], last_name=user_data['last_name'],
                    username=user_data['username'], email=user_data['email'])

    # Query the 'admin' table for an admin user
    cursor.execute('SELECT * FROM admin WHERE id = %s', (user_id,))
    admin_data = cursor.fetchone()
    if admin_data:
        return Admin(id=admin_data['id'], role=admin_data['role'],
                     first_name=admin_data['first_name'], last_name=admin_data['last_name'],
                     username=admin_data['username'], email=admin_data['email'], tel=admin_data['tel'])

    # Query the 'instructor' table for an instructor user
    cursor.execute('SELECT * FROM instructor WHERE id = %s', (user_id,))
    instructor_data = cursor.fetchone()
    if instructor_data:
        return Instructor(id=instructor_data['id'], role=instructor_data['role'],
                           first_name=instructor_data['first_name'], last_name=instructor_data['last_name'],
                           username=instructor_data['username'], email=instructor_data['email'], tel=instructor_data['tel'])

    cursor.close()
    return None

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้.', 'danger')
            return redirect(url_for('login'))
        if current_user.role != 'admin':
            flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------

def instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้.', 'danger')
            return redirect(url_for('login'))
        if current_user.role != 'instructor':
            flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function



# ---------------------------------------------------------------------------------------------



# ----------------------------------- ล็อคอินเข้าระบบ ---------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check in user table
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            user_obj = User(id=user['id'], role=user['role'], first_name=user['first_name'],
                            last_name=user['last_name'], username=user['username'], email=user['email'])
            login_user(user_obj)
            session['loggedin'] = True
            session['id'] = user['id']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['username'] = user['username']
            session['email'] = user['email']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))

        # Check in admin table if not found in user table
        cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
        admin = cursor.fetchone()
        if admin:
            user_obj = Admin(id=admin['id'], role='admin', first_name=admin['first_name'],
                            last_name=admin['last_name'], username=admin['username'], email=admin['email'], tel=admin['tel'])
            login_user(user_obj)
            session['loggedin'] = True
            session['id'] = admin['id']
            session['first_name'] = admin['first_name']
            session['last_name'] = admin['last_name']
            session['username'] = admin['username']
            session['email'] = admin['email']
            session['tel'] = admin['tel']
            flash('Admin logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Check in instructor table if not found in user or admin table
        cursor.execute('SELECT * FROM instructor WHERE email = %s AND password = %s', (email, password))
        instructor = cursor.fetchone()
        if instructor:
            user_obj = Instructor(id=instructor['id'], role='instructor', first_name=instructor['first_name'],
                                last_name=instructor['last_name'], username=instructor['username'], email=instructor['email'], tel=instructor['tel'])
            login_user(user_obj)
            session['loggedin'] = True
            session['id'] = instructor['id']
            session['first_name'] = instructor['first_name']
            session['last_name'] = instructor['last_name']
            session['username'] = instructor['username']
            session['email'] = instructor['email']
            session['tel'] = instructor['tel']
            flash('Instructor logged in successfully!', 'success')
            return redirect(url_for('instructor_dashboard'))


        flash('Please enter correct email / password!', 'error')
            
    return render_template('registration/login.html')

# ---------------------------------------------------------------------------------------------

# -------------------------------------- ออกจากระบบ ------------------------------------------------------

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------------------------

# ----------------------------------- สมัครใช้งานระบบ ----------------------------------------------------------
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ensure all required fields are present
        required_fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name', 'birth', 'gender']
        if all(field in request.form for field in required_fields):
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            email = request.form['email']
            birth = request.form['birth']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            gender = request.form['gender']

            # Connect to the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            user = cursor.fetchone()

            # Validate inputs
            if user:
                flash('Account already exists!', 'error')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!', 'error')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!', 'error')
            elif password != confirm_password:
                flash('Passwords do not match!', 'error')
            elif len(password) < 8:
                flash("Password must be at least 8 characters long", 'error')
            elif not any(c.isupper() for c in password):
                flash("Password must contain at least 1 uppercase letter", 'error')
            elif not any(c.islower() for c in password):
                flash("Password must contain at least 1 lowercase letter", 'error')
            elif not any(c.isdigit() for c in password):
                flash("Password must contain at least 1 digit", 'error')
            elif not username or not password or not email:
                flash('Please fill out the form!', 'error')
            elif gender not in ['Male', 'Female']:
                flash('Please select a valid gender!', 'error')
            else:
                registration_date = datetime.today()

                # Insert user into the database
                cursor.execute(
                    'INSERT INTO user (first_name, last_name, username, email, birth_date, registration_date, password, gender, role) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                    (first_name, last_name, username, email, birth, registration_date, password, gender, 'user')
                )

                mysql.connection.commit()
                flash('You have successfully registered!', 'success')
                return redirect(url_for('register'))
        else:
            flash('Please fill out the form!', 'error')
    
    return render_template('registration/register.html')
# ---------------------------------------------------------------------------------------------

# ------------------------------------ อัปเดตโปรไฟล์ ---------------------------------------------------------

app.config['UPLOAD_FOLDER_USER_UPDATED'] = 'static/img/updated/user'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/profile_update', methods=['GET', 'POST'])
@login_required
def profile_update():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        userimage = request.files['userimage'] if 'userimage' in request.files else None
        adminimage = request.files['adminimage'] if 'adminimage' in request.files else None
        instructorimage = request.files['instructorimage'] if 'instructorimage' in request.files else None

        # Set the userimage path if the filename is provided and is allowed
        userimage_filename = None
        if userimage and allowed_file(userimage.filename):
            filename = secure_filename(userimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_USER_UPDATED'], filename)
            userimage.save(filepath)
            userimage_filename = f"../{app.config['UPLOAD_FOLDER_USER_UPDATED']}/{filename}"

        adminimage_filename = None
        if adminimage and allowed_file(adminimage.filename):
            filename = secure_filename(adminimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_ADMIN_UPDATED'], filename)
            adminimage.save(filepath)
            adminimage_filename = f"../{app.config['UPLOAD_FOLDER_ADMIN_UPDATED']}/{filename}"

        instructorimage_filename = None
        if instructorimage and allowed_file(instructorimage.filename):
            filename = secure_filename(instructorimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED'], filename)
            instructorimage.save(filepath)
            instructorimage_filename = f"../{app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED']}/{filename}"

        if len(password) < 8:
            flash("Password must be at least 8 characters long", 'error')
        elif not any(c.isupper() for c in password):
            flash("Password must contain at least 1 uppercase letter", 'error')
        elif not any(c.islower() for c in password):
            flash("Password must contain at least 1 lowercase letter", 'error')
        elif not any(c.isdigit() for c in password):
            flash("Password must contain at least 1 digit", 'error')
        else:
            session_username = session.get('username')
            cur = mysql.connection.cursor()
            
            cur.execute("UPDATE user SET first_name=%s, last_name=%s, username=%s, email=%s, password=%s, userimage=%s WHERE username=%s",
                        (first_name, last_name, username, email, password, userimage_filename, session_username))
            
            cur.execute("UPDATE admin SET first_name=%s, last_name=%s, username=%s, email=%s, password=%s, adminimage=%s WHERE username=%s",
                        (first_name, last_name, username, email, password, adminimage_filename, session_username))
            
            cur.execute("UPDATE instructor SET first_name=%s, last_name=%s, username=%s, email=%s, password=%s, instructorimage=%s WHERE username=%s",
                        (first_name, last_name, username, email, password, instructorimage_filename, session_username))
            
            mysql.connection.commit()
            cur.close()
            
            flash("Your Profile has been successfully updated", 'success')
            return redirect('/profile_update')

    session_username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username=%s", (session_username,))
    user = cur.fetchone()
    cur.close()

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, icon, name FROM categories")
        categories = cur.fetchall()

        cur.execute("""
                SELECT c.id, c.title, c.slug, cat.name as category_name
                FROM courses c
                JOIN categories cat ON c.category_id = cat.id
            """)
        all_courses = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        categories = []
        all_courses = []

    finally:
        cur.close()

    categories = [{'id': row[0], 'icon': row[1], 'name': row[2]} for row in categories]
    courses = [{'id': row[0], 'title': row[1], 'slug': row[2], 'category_name': row[3]} for row in all_courses]

    return render_template('registration/profile_update.html', user=user, categories=categories, courses=courses, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)

# ---------------------------------------------------------------------------------------------



# ------------------------------------- หน้าแดชบอร์ด แอดมิน(Admin) --------------------------------------------------------
 
@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_dashboard():

        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        # Execute SQL command to get the total number of users
        cur.execute("SELECT COUNT(*) FROM user")
        total_users = cur.fetchone()[0]

        # Execute SQL command to get the total number of instructors
        cur.execute("SELECT COUNT(*) FROM instructor")
        total_instructor = cur.fetchone()[0]

        # Execute SQL command to get the total number of enrollments
        cur.execute("SELECT COUNT(*) FROM user_enroll")
        total_enroll = cur.fetchone()[0]

        # Execute SQL command to get the total number of quizzes
        cur.execute("SELECT COUNT(*) FROM quiz")
        total_quiz = cur.fetchone()[0]

        # Execute SQL command to get admin image URL
        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"


        # Execute SQL command to get enrollment data
        cur.execute("""
            SELECT courses.title, COUNT(user_enroll.enroll_id) as enroll_count
            FROM user_enroll
            JOIN courses ON user_enroll.course_id = courses.id
            GROUP BY courses.title;
        """)
        enroll_data = cur.fetchall()

        # Format the data for Highcharts
        chart_enroll = [{"name": row[0], "y": row[1]} for row in enroll_data]

        # Sort the data from highest to lowest
        sorted_chart_enroll = sorted(chart_enroll, key=itemgetter('y'), reverse=True)

        # Close the cursor
        cur.close()

        # Pass total_users, total_instructor, and sorted_chart_enroll to the template
        return render_template('admin/admin_dashboard.html', total_users=total_users, total_instructor=total_instructor, total_enroll=total_enroll, total_quiz=total_quiz, chart_enroll=sorted_chart_enroll, admin_image_url=admin_image_url)








# ตารางแอดมิน
@app.route('/admin_table')
@login_required
@admin_required
def admin_table():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, first_name, last_name, email, tel, DATE_FORMAT(birth_date, '%d/%m/%Y') AS formatted_date, password, gender, role, adminimage FROM admin''')
    data = cur.fetchall()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"
    cur.close()
    sweet_alert = request.args.get('sweet_alert')
    return render_template('admin/admin_table.html', data=data, sweet_alert=sweet_alert, admin_image_url=admin_image_url)




app.config['UPLOAD_FOLDER_ADMIN'] = 'static/img/uploads/admin'

@app.route('/insert_admin', methods=['GET', 'POST'])
@login_required
@admin_required
def insert_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"  # Initialize with a default value if no image is found

    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        tel = request.form['tel']
        birth = request.form['birth']
        password = request.form['password']
        gender = request.form['gender']

        # File handling (if applicable)
        adminimage_path = None
        if 'adminimage' in request.files:
            adminimage = request.files['adminimage']
            if adminimage.filename != '':
                adminimage_filename = secure_filename(adminimage.filename)
                adminimage.save(os.path.join(app.config['UPLOAD_FOLDER_ADMIN'], adminimage_filename))
                adminimage_path = f"../static/img/uploads/admin/{adminimage_filename}"

        # Form validation
        if not all([first_name, last_name, username, email, tel, birth, password, gender]):
            flash('Please fill out the form completely!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            flash('Username must contain only characters and numbers!', 'error')
        elif len(password) < 8:
            flash("Password must be at least 8 characters long", 'error')
        elif not any(c.isupper() for c in password):
            flash("Password must contain at least 1 uppercase letter", 'error')
        elif not any(c.islower() for c in password):
            flash("Password must contain at least 1 lowercase letter", 'error')
        elif not any(c.isdigit() for c in password):
            flash("Password must contain at least 1 digit", 'error')
        else:
            try:
                # Check if account already exists
                cur.execute("SELECT * FROM admin WHERE username = %s OR email = %s", (username, email))
                admin = cur.fetchone()

                if admin:
                    flash('Account already exists!', 'error')
                else:
                    # If validation passes and no existing admin, proceed with database insertion
                    registration_date = datetime.now()
                    cur.execute('''INSERT INTO admin (first_name, last_name, username, email, tel, birth_date, registration_date, password, gender, role, adminimage) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                                (first_name, last_name, username, email, tel, birth, registration_date, password, gender, 'admin', adminimage_path))
                    mysql.connection.commit()
                    flash('Admin successfully added', 'success')
                    return redirect(url_for('admin_table'))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')
            finally:
                cur.close()

    # If it's a GET request or there are validation errors, render the form
    return render_template('admin/insert_admin.html', admin_image_url=admin_image_url)







# แก้ไขแอดมิน
@app.route('/edit_admin/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_admin(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM admin WHERE id = %s', (id,))
    admin = cur.fetchone()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    cur.close()
    return render_template('admin/updated_admin.html', admin=admin, admin_image_url=admin_image_url)






app.config['UPLOAD_FOLDER_ADMIN_UPDATED'] = 'static/img/updated/admin'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/updated_admin', methods=['POST'])
@login_required
@admin_required  # Assuming you have a decorator like this for admin access control
def updated_admin():
    if request.method == 'POST':
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        tel = request.form.get('tel')
        birth = request.form.get('birth')
        gender = request.form.get('gender')
        adminimage = request.files.get('adminimage')

        adminimage_filename = None
        if adminimage and allowed_file(adminimage.filename):
            filename = secure_filename(adminimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_ADMIN_UPDATED'], filename)
            adminimage.save(filepath)
            adminimage_filename = f"../{app.config['UPLOAD_FOLDER_ADMIN_UPDATED']}/{filename}"  # เปลี่ยนเส้นทางเพื่อให้สามารถเข้าถึงไฟล์ได้ในแอปพลิเคชัน Flask

        # Validate email and username
        if not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
            return redirect(url_for('admin_table'))
        if not username or not re.match(r'^[A-Za-z0-9]+$', username):
            flash('Username must contain only letters and numbers!', 'error')
            return redirect(url_for('admin_table'))

        # Update admin information in the database
        cur = mysql.connection.cursor()
        cur.execute('''
            UPDATE admin 
            SET first_name = %s, last_name = %s, username = %s, email = %s, tel = %s, birth_date = %s, gender = %s, adminimage = %s 
            WHERE id = %s
        ''', (first_name, last_name, username, email, tel, birth, gender, adminimage_filename, id))
        mysql.connection.commit()
        cur.close()

        flash('Admin successfully updated', 'success')

    return redirect(url_for('admin_table'))


# ลบแอดมิน
@app.route('/delete_admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_admin(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM admin WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    flash('Admin successfully Deleted', 'success')
    return redirect(url_for('admin_table'))


@app.route('/edit_password_admin/<id>', methods=['GET', 'POST'])
@login_required
def edit_password_admin(id):
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
        return redirect(url_for('home'))
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM admin WHERE id = %s''', (id,))
    admin = cur.fetchone()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"

    if request.method == "POST":
        # Fetch form data
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if new_password != confirm_password:
            flash("รหัสผ่านทั้งสองไม่ตรงกัน กรุณากรอกใหม่", 'error')
        elif not new_password or len(new_password) < 8:
            flash("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร", 'error')
        elif not any(c.isupper() for c in new_password):
            flash("รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว", 'error')
        elif not any(c.islower() for c in new_password):
            flash("รหัสผ่านต้องมีตัวอักษรพิมพ์เล็กอย่างน้อย 1 ตัว", 'error')
        elif not any(c.isdigit() for c in new_password):
            flash("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว", 'error')
        else:
            try:
                # Update the database with the new password
                cur.execute('''UPDATE admin SET password = %s WHERE id = %s''', 
                            (new_password, id))
                mysql.connection.commit()
                cur.close()

                flash("รหัสผ่านของคุณได้รับการอัปเดตเรียบร้อยแล้ว", 'success')
                return redirect(url_for('admin_table', id=id))

            except Exception as e:
                flash("เกิดข้อผิดพลาดในการอัปเดตรหัสผ่าน: {}".format(e), 'error')

    # Render the password update form for GET requests
    return render_template('admin/edit_password_admin.html', admin=admin, admin_image_url=admin_image_url)


# ---------------------------------------------------------------------------------------------

# ----------------------------------- หน้าแดชบอร์ด ผู้สอน(instructor) ----------------------------------------------------------

current_time = datetime.now()
current_year = current_time.year

@app.route('/instructor_dashboard', methods=['GET', 'POST'])
@login_required
@instructor_required
def instructor_dashboard():
    # สร้าง cursor object เพื่อทำการ execute SQL คำสั่ง
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM quiz_attempts")
    total_attempts  = cur.fetchone()[0]

    # Execute SQL คำสั่งเพื่อดึงข้อมูลจำนวนคอร์ส
    cur.execute("SELECT COUNT(*) FROM courses")
    course_count = cur.fetchone()[0]

    # Execute SQL คำสั่งเพื่อดึงข้อมูลจำนวนควิซ
    cur.execute("SELECT COUNT(*) FROM quiz")
    quiz_count = cur.fetchone()[0]

    cur.execute("SELECT SUM(question_count) FROM quiz_attempts")
    total_questions = cur.fetchone()[0]

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    # Execute SQL คำสั่งเพื่อดึงข้อมูลการเข้าเรียนแต่ละวัน
    cur.execute("""
        SELECT DATE(user_enroll.enroll_date) as enroll_date, COUNT(user_enroll.enroll_id) as enroll_count
        FROM user_enroll
        JOIN courses ON user_enroll.course_id = courses.id
        GROUP BY DATE(user_enroll.enroll_date)
        ORDER BY DATE(user_enroll.enroll_date);
    """)
    enroll_daily = cur.fetchall()

    # Format the data for Highcharts
    chart_enroll_list_daily = [{"name": row[0].strftime('%d-%m-%Y'), "y": row[1]} for row in enroll_daily]


    # Execute SQL คำสั่งเพื่อดึงข้อมูลการเข้าเรียนแต่ละเดือน-ปีไหน
    cur.execute("""
        SELECT 
            CASE
                WHEN MONTH(user_enroll.enroll_date) = 1 THEN 'มกราคม'
                WHEN MONTH(user_enroll.enroll_date) = 2 THEN 'กุมภาพันธ์'
                WHEN MONTH(user_enroll.enroll_date) = 3 THEN 'มีนาคม'
                WHEN MONTH(user_enroll.enroll_date) = 4 THEN 'เมษายน'
                WHEN MONTH(user_enroll.enroll_date) = 5 THEN 'พฤษภาคม'
                WHEN MONTH(user_enroll.enroll_date) = 6 THEN 'มิถุนายน'
                WHEN MONTH(user_enroll.enroll_date) = 7 THEN 'กรกฎาคม'
                WHEN MONTH(user_enroll.enroll_date) = 8 THEN 'สิงหาคม'
                WHEN MONTH(user_enroll.enroll_date) = 9 THEN 'กันยายน'
                WHEN MONTH(user_enroll.enroll_date) = 10 THEN 'ตุลาคม'
                WHEN MONTH(user_enroll.enroll_date) = 11 THEN 'พฤศจิกายน'
                WHEN MONTH(user_enroll.enroll_date) = 12 THEN 'ธันวาคม'
            END as enroll_month_thai,
            YEAR(user_enroll.enroll_date) as enroll_year,
            COUNT(user_enroll.enroll_id) as enroll_count
        FROM user_enroll
        JOIN courses ON user_enroll.course_id = courses.id
        WHERE YEAR(user_enroll.enroll_date) IN (%s, %s, %s)
        GROUP BY enroll_month_thai, enroll_year
        ORDER BY enroll_year, MONTH(user_enroll.enroll_date);
    """, (datetime.now().year, datetime.now().year - 1, datetime.now().year - 2))

    enroll_monthly = cur.fetchall()

    # Format the data for Highcharts
    chart_enroll_list_monthly = []
    for row in enroll_monthly:
        if len(row) >= 3:  # Ensure row has at least three elements
            chart_enroll_list_monthly.append({"name": f"{row[0]}-{row[1]}", "y": row[2]})

 
    # Execute SQL คำสั่งเพื่อดึงข้อมูลการเข้าเรียนแต่ละปี
    cur.execute("""
            SELECT 
                EXTRACT(YEAR FROM user_enroll.enroll_date) as enroll_year,
                COUNT(user_enroll.enroll_id) as enroll_count
            FROM user_enroll
            JOIN courses ON user_enroll.course_id = courses.id
            GROUP BY enroll_year
            ORDER BY enroll_year;
        """)
    enroll_yearly = cur.fetchall()

        # Format the data for Highcharts
    chart_enroll_list_yearly = [{"name": str(row[0]), "y": row[1]} for row in enroll_yearly]

    # ปิดการใช้ cursor
    cur.close()

    return render_template('instructor/instructor_dashboard.html', total_attempts =total_attempts , course_count=course_count, quiz_count=quiz_count, total_questions=total_questions, chart_enroll_list_daily=chart_enroll_list_daily, chart_enroll_list_monthly=chart_enroll_list_monthly, chart_enroll_list_yearly=chart_enroll_list_yearly, instructor_image_url=instructor_image_url)





# ตาราง ผู้สอน
@app.route('/instructor_table')
@login_required
@admin_required
def instructor_table():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, first_name, last_name, email, tel, DATE_FORMAT(birth_date, '%d/%m/%Y'), password, gender, role, instructorimage FROM instructor''')
    data = cur.fetchall()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    cur.close()
    sweet_alert = request.args.get('sweet_alert')
    return render_template('instructor/instructor_table.html', data=data, sweet_alert=sweet_alert, admin_image_url=admin_image_url)



app.config['UPLOAD_FOLDER_INSTRUCTOR'] = 'static/img/uploads/instructor'

# เพิ่ม ผู้สอน
@app.route('/insert_instructor', methods=['GET', 'POST'])
@login_required
@admin_required
def insert_instructor():
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    cur.close()

    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        tel = request.form['tel']
        birth = request.form['birth']
        password = request.form['password']
        gender = request.form['gender']


        # File handling (if applicable)
        if 'instructorimage' in request.files:
            instructorimage = request.files['instructorimage']
            if instructorimage.filename != '':
                instructorimage_filename = secure_filename(instructorimage.filename)
                instructorimage.save(os.path.join(app.config['UPLOAD_FOLDER_INSTRUCTOR'], instructorimage_filename))
                instructorimage_path = "../static/img/uploads/instructor/" + instructorimage_filename

        # Validate input data
        if not all([first_name, last_name, username, email, tel, birth, password, gender]):
            flash('Please fill out the form completely!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            flash('Username must contain only characters and numbers!', 'error')
        elif len(password) < 8:
            flash("Password must be at least 8 characters long", 'error')
        elif not any(c.isupper() for c in password):
            flash("Password must contain at least 1 uppercase letter", 'error')
        elif not any(c.islower() for c in password):
            flash("Password must contain at least 1 lowercase letter", 'error')
        elif not any(c.isdigit() for c in password):
            flash("Password must contain at least 1 digit", 'error')
        else:
            try:
                # Check if account already exists
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM instructor WHERE username = %s OR email = %s", (username, email))
                instructor = cur.fetchone()
                
                if instructor:
                    if instructor['username'] == username:
                        flash('Username already exists!', 'error')
                    elif instructor['email'] == email:
                        flash('Email address already exists!', 'error')
                    return render_template('instructor/insert_instructor.html', admin_image_url=admin_image_url)

                # If validation passes and no existing instructor, proceed with database insertion
                registration_date = datetime.now()
                cur.execute('''INSERT INTO instructor (first_name, last_name, username, email, tel, birth_date, registration_date, password, gender, role, instructorimage) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                            (first_name, last_name, username, email, tel, birth, registration_date, password, gender, 'instructor', instructorimage_path))
                mysql.connection.commit()
                flash('Instructor successfully added', 'success')
                return redirect(url_for('instructor_table'))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')
            finally:
                cur.close()
    
    # If it's a GET request or there are validation errors, render the form
    return render_template('instructor/insert_instructor.html', admin_image_url=admin_image_url)








# แก้ไข ผู้สอน
@app.route('/edit_instructor/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_instructor(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM instructor WHERE id = %s', (id,))
    instructor = cur.fetchone()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    cur.close()
    return render_template('instructor/updated_instructor.html', instructor=instructor, admin_image_url=admin_image_url)



app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED'] = 'static/img/updated/instructor'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/updated_instructor', methods=['POST'])
@login_required
@admin_required  # Assuming you have a decorator like this for admin access control
def updated_instructor():
    if request.method == 'POST':
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        tel = request.form.get('tel')
        birth = request.form.get('birth')
        gender = request.form.get('gender')
        instructorimage = request.files.get('instructorimage')  # Get the file from the form

        instructorimage_filename = None
        if instructorimage and allowed_file(instructorimage.filename):
            filename = secure_filename(instructorimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED'], filename)
            instructorimage.save(filepath)
            instructorimage_filename = f"../{app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED']}/{filename}"  # Set the correct path to access the file in Flask app

        # Check if instructor exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM instructor WHERE id = %s", (id,))
        instructor = cur.fetchone()
        cur.close()

        if not instructor:
            flash('ไม่พบผู้สอน!', 'error')
        elif not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('ที่อยู่อีเมลที่ไม่ถูกต้อง!', 'error')
        elif not username or not re.match(r'^[A-Za-z0-9]+$', username):
            flash('ชื่อผู้ใช้จะต้องมีตัวอักษรและตัวเลขเท่านั้น!', 'error')
        else:
            # Update the instructor in the database
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE instructor 
                SET first_name = %s, last_name = %s, username = %s, email = %s, tel = %s, birth_date = %s, gender = %s, instructorimage = %s 
                WHERE id = %s
            ''', (first_name, last_name, username, email, tel, birth, gender, instructorimage_filename, id))
            mysql.connection.commit()
            cur.close()

            flash('อัปเดตข้อมูลผู้สอนเรียบร้อยแล้ว', 'success')

    return redirect(url_for('instructor_table'))


# ลบ ผู้สอน
@app.route('/delete_instructor/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_instructor(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM instructor WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    flash('Instructor successfully Deleted', 'success')
    return redirect(url_for('instructor_table'))


# แก้ไขรหัสของ ผู้สอน
@app.route('/edit_password_instructor/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_password_instructor(id):
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
        return redirect(url_for('home'))
    
    # Establish database connection
    cur = mysql.connection.cursor()
    
    # Fetch instructor data by id
    cur.execute('''SELECT * FROM instructor WHERE id = %s''', (id,))
    instructor = cur.fetchone()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"

    if request.method == "POST":
        # Fetch form data
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match and meet passing_percentage
        if new_password != confirm_password:
            flash("รหัสผ่านทั้งสองไม่ตรงกัน กรุณากรอกใหม่", 'error')
        elif not new_password or len(new_password) < 8:
            flash("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร", 'error')
        elif not any(c.isupper() for c in new_password):
            flash("รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว", 'error')
        elif not any(c.islower() for c in new_password):
            flash("รหัสผ่านต้องมีตัวอักษรพิมพ์เล็กอย่างน้อย 1 ตัว", 'error')
        elif not any(c.isdigit() for c in new_password):
            flash("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว", 'error')
        else:
            try:
                # Update the database with the new password
                cur.execute('''UPDATE instructor SET password = %s WHERE id = %s''', 
                            (new_password, id))
                mysql.connection.commit()
                cur.close()

                flash("รหัสผ่านของคุณได้รับการอัปเดตเรียบร้อยแล้ว", 'success')
                return redirect(url_for('instructor_table'))  # Redirect to appropriate page

            except Exception as e:
                flash("เกิดข้อผิดพลาดในการอัปเดตรหัสผ่าน: {}".format(e), 'error')

    # Render the password update form for GET requests
    return render_template('instructor/edit_password_instructor.html', instructor=instructor, admin_image_url=admin_image_url)

    
# --------------------------------------------------------------------------------------------------

# ---------------------------------------- อัปเดตโปรไฟล์ส่วนตัวในหน้า Dashboard ----------------------------------------

app.config['UPLOAD_FOLDER_ADMIN_UPDATED'] = 'static/img/updated/admin'
app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED'] = 'static/img/updated/instructor'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/updated_profile', methods=['GET', 'POST'])
@login_required
def updated_profile():
    cur = mysql.connection.cursor()
    
    # Fetch current user's admin image URL
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    
    # Fetch current user's instructor image URL
    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/instructor.png"
    
    cur.close()

    # Check if the current user has the appropriate role
    if current_user.role not in ['admin', 'instructor']:
        flash("You are not authorized to access this page.", 'danger')
        return redirect(url_for('home'))

    if request.method == "POST":
        # Fetch form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        tel = request.form['tel']
        
        adminimage = request.files.get('adminimage', None)
        instructorimage = request.files.get('instructorimage', None)

        adminimage_filename = None
        if adminimage and allowed_file(adminimage.filename):
            filename = secure_filename(adminimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_ADMIN_UPDATED'], filename)
            adminimage.save(filepath)
            adminimage_filename = f"../{app.config['UPLOAD_FOLDER_ADMIN_UPDATED']}/{filename}"

        instructorimage_filename = None
        if instructorimage and allowed_file(instructorimage.filename):
            filename = secure_filename(instructorimage.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED'], filename)
            instructorimage.save(filepath)
            instructorimage_filename = f"../{app.config['UPLOAD_FOLDER_INSTRUCTOR_UPDATED']}/{filename}"

        try:
            # Update profile based on role
            cur = mysql.connection.cursor()
            user_id = current_user.id

            if current_user.role == 'admin':
                cur.execute('''UPDATE admin SET first_name = %s, last_name = %s, email = %s, tel = %s, adminimage = %s WHERE id = %s''', 
                            (first_name, last_name, email, tel, adminimage_filename, user_id))
                session['adminimage'] = adminimage_filename

            elif current_user.role == 'instructor':
                cur.execute('''UPDATE instructor SET first_name = %s, last_name = %s, email = %s, tel = %s, instructorimage = %s WHERE id = %s''', 
                            (first_name, last_name, email, tel, instructorimage_filename, user_id))
                session['instructorimage'] = instructorimage_filename

            mysql.connection.commit()
            cur.close()

            # Update session data with new profile information
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['email'] = email
            session['tel'] = tel

            flash("Your profile has been successfully updated", 'success')
            if current_user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif current_user.role == 'instructor':
                return redirect(url_for('instructor_dashboard'))

        except Exception as e:
            flash(f"An error occurred while updating your profile: {e}", 'danger')
            app.logger.error('Error updating profile', exc_info=True)

    # Render the profile update form for GET requests
    return render_template('instructor/updated_profile.html', admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)




# --------------------------------------------------------------------------------------------------

# ---------------------------------------- อัปเดตรหัสส่วนตัวในหน้า Dashboard ----------------------------------------


# อัปเดตรหัสของ admin และ instructor
@app.route('/updated_password', methods=['GET', 'POST'])
@login_required
def updated_password():

    cur = mysql.connection.cursor()
    
    # Fetch current user's admin image URL
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    
    # Fetch current user's instructor image URL
    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/instructor.png"
    
    cur.close()

    if current_user.role not in ['admin', 'instructor']:
        flash("You are not authorized to access this page.", 'danger')
        return redirect(url_for('home'))
    
    if request.method == "POST":
        # Fetch form data
        id = session.get('id')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match and meet passing_percentage
        if new_password != confirm_password:
            flash("รหัสผ่านทั้งสองไม่ตรงกัน กรุณากรอกใหม่", 'error')
        elif len(new_password) < 8:
            flash("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร", 'error')
        elif not any(c.isupper() for c in new_password):
            flash("รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว", 'error')
        elif not any(c.islower() for c in new_password):
            flash("รหัสผ่านต้องมีตัวอักษรพิมพ์เล็กอย่างน้อย 1 ตัว", 'error')
        elif not any(c.isdigit() for c in new_password):
            flash("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว", 'error')
        else:
            try:
                # Update the database with the new password for admin
                cur = mysql.connection.cursor()
                cur.execute('''UPDATE admin SET password = %s WHERE id = %s''', 
                            (new_password, id))
                mysql.connection.commit()
                
                # Update the database with the new password for instructor
                cur.execute('''UPDATE instructor SET password = %s WHERE id = %s''', 
                            (new_password, id))
                mysql.connection.commit()
                
                cur.close()

                flash("รหัสผ่านของคุณได้รับการอัปเดตเรียบร้อยแล้ว", 'success')

                # Redirect to a profile page or dashboard after password update
                return redirect(url_for('updated_password'))  # Replace 'dashboard' with your route for the profile/dashboard

            except Exception as e:
                flash("เกิดข้อผิดพลาดในการอัปเดตรหัสผ่าน: {}".format(e), 'error')

    # Render the password update form for GET requests
    return render_template('instructor/updated_password.html', admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)


# ---------------------------------------------------------------------------------------------


# ------------------------------------ ส่วนของ ผู้ใช้(user) ---------------------------------------------------------

# ตารางผู้ใช้
@app.route('/user_table')
@login_required
def user_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT id, first_name, last_name, email, DATE_FORMAT(birth_date, '%d/%m/%Y'), password, gender, role, userimage FROM user''')
        data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
        
        # Fetch current user's instructor image URL
        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/instructor.png"
        cur.close()
        sweet_alert = request.args.get('sweet_alert')
        return render_template('user/user_table.html', data=data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))




app.config['UPLOAD_FOLDER_USER'] = 'static/img/uploads/users'

@app.route('/insert_user', methods=['GET', 'POST'])
@login_required
def insert_user():
    cur = mysql.connection.cursor()
    
    # Fetch current user's admin image URL
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "default_admin_image_path"
    
    # Fetch current user's instructor image URL
    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/instructor.png"
    
    cur.close()

    if current_user.role not in ['admin', 'instructor']:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        birth = request.form['birth']
        password = request.form['password']
        gender = request.form['gender']

        # Initialize userimage_path with a default value
        userimage_path = None
        
        # File handling (if applicable)
        if 'userimage' in request.files:
            userimage = request.files['userimage']
            if userimage.filename != '':
                userimage_filename = secure_filename(userimage.filename)
                userimage.save(os.path.join(app.config['UPLOAD_FOLDER_USER'], userimage_filename))
                userimage_path = f"../static/img/uploads/users/{userimage_filename}"

        # Check if account already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
        user = cur.fetchone()
            
        if user:
            if user[3] == username:  # Using index 3 for username in the tuple
                flash('Username already exists!', 'error')
            elif user[4] == email:  # Using index 4 for email in the tuple
                flash('Email address already exists!', 'error')
            cur.close()
            return render_template('user/insert_user.html')

        cur.close()

        # Validate input data
        if not all([first_name, last_name, username, email, birth, password, gender]):
            flash('Please fill out the form completely!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            flash('Username must contain only characters and numbers!', 'error')
        elif len(password) < 8:
            flash("Password must be at least 8 characters long", 'error')
        elif not any(c.isupper() for c in password):
            flash("Password must contain at least 1 uppercase letter", 'error')
        elif not any(c.islower() for c in password):
            flash("Password must contain at least 1 lowercase letter", 'error')
        elif not any(c.isdigit() for c in password):
            flash("Password must contain at least 1 digit", 'error')
        else:
            # If validation passes, proceed with database insertion
            registration_date = datetime.now()
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO user (first_name, last_name, username, email, birth_date, registration_date, password, gender, role, userimage) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (first_name, last_name, username, email, birth, registration_date, password, gender, 'user', userimage_path))
            mysql.connection.commit()
            cur.close()
            flash('User successfully added', 'success')
            return redirect(url_for('user_table'))

    # If it's a GET request or there are validation errors, render the form
    return render_template('user/insert_user.html', admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



# แก้ไขผู้ใช้
@app.route('/edit_user/<id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE id = %s', (id,))
        user = cur.fetchone()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()
        return render_template('user/updated_user.html', user=user, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))



app.config['UPLOAD_FOLDER_USER_UPDATED'] = 'static/img/updated/user'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/updated_user', methods=['POST'])
@login_required
def updated_user():
    if current_user.role in ['admin', 'instructor']:
        if request.method == 'POST':
            id = request.form.get('id')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            username = request.form.get('username')
            email = request.form.get('email')
            birth = request.form.get('birth')
            gender = request.form.get('gender')
            userimage = request.files.get('userimage')  # Get the file from the form

            # Set the userimage path if the filename is provided and is allowed
            userimage_filename = None
            if userimage and allowed_file(userimage.filename):
                filename = secure_filename(userimage.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER_USER_UPDATED'], filename)
                userimage.save(filepath)
                userimage_filename = f"../{app.config['UPLOAD_FOLDER_USER_UPDATED']}/{filename}"  # Set the correct path to access the file in Flask app

            # Check if account already exists
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE id = %s", (id,))
            user = cur.fetchone()
            cur.close()

            if not user:
                flash('ไม่พบชื่อผู้ใช้!', 'error')
            elif not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('ที่อยู่อีเมลที่ไม่ถูกต้อง!', 'error')
            elif not username or not re.match(r'^[A-Za-z0-9]+$', username):
                flash('ชื่อผู้ใช้จะต้องมีตัวอักษรและตัวเลขเท่านั้น!', 'error')
            else:
                # Update the user in the database
                cur = mysql.connection.cursor()
                cur.execute('''
                    UPDATE user 
                    SET first_name = %s, last_name = %s, username = %s, email = %s, birth_date = %s, gender = %s, userimage = %s 
                    WHERE id = %s
                ''', (first_name, last_name, username, email, birth, gender, userimage_filename, id))
                mysql.connection.commit()
                cur.close()

                flash('อัปเดตข้อมูลผู้ใช้เรียบร้อยแล้ว', 'success')

        return redirect(url_for('user_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))


# ลบผู้ใช้
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.role in ['admin', 'instructor']:
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM user WHERE id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('User successfully deleted', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting user: {str(e)}', 'error')
        
        return redirect(url_for('user_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
        return redirect(url_for('home'))
    
# แก้ไขรหัสของผู้ใช้
@app.route('/edit_password_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_password_user(id):
    if current_user.role not in ['admin', 'instructor']:
        flash("You are not authorized to access this page.", 'danger')
        return redirect(url_for('home'))

    # Establish database connection
    cur = mysql.connection.cursor()
    
    # Fetch user data by id
    cur.execute('''SELECT * FROM user WHERE id = %s''', (id,))
    user = cur.fetchone()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    if request.method == "POST":
        # Fetch form data
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match and meet passing_percentage
        if new_password != confirm_password:
            flash("รหัสผ่านทั้งสองไม่ตรงกัน กรุณากรอกใหม่", 'error')
        elif not new_password or len(new_password) < 8:
            flash("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร", 'error')
        elif not any(c.isupper() for c in new_password):
            flash("รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว", 'error')
        elif not any(c.islower() for c in new_password):
            flash("รหัสผ่านต้องมีตัวอักษรพิมพ์เล็กอย่างน้อย 1 ตัว", 'error')
        elif not any(c.isdigit() for c in new_password):
            flash("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว", 'error')
        else:
            try:
                # Update the database with the new password
                cur.execute('''UPDATE user SET password = %s WHERE id = %s''', 
                            (new_password, id))
                mysql.connection.commit()
                cur.close()

                flash("รหัสผ่านของคุณได้รับการอัปเดตเรียบร้อยแล้ว", 'success')
                return redirect(url_for('user_table'))  # Redirect to appropriate page

            except Exception as e:
                flash("เกิดข้อผิดพลาดในการอัปเดตรหัสผ่าน: {}".format(e), 'error')

    # Render the password update form for GET requests
    return render_template('user/edit_password_user.html', user=user, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)


# ---------------------------------------------------------------------------------------------




# ------------------------------------ ส่วนของ enroll ---------------------------------------------------------


@app.route('/enroll_table')
@login_required
def enroll_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT enroll_id, user_id, course_id, DATE_FORMAT(enroll_date, '%d/%m/%Y : %H:%i:%s') AS formatted_date FROM user_enroll""")
        data = cur.fetchall()

        cur.execute('SELECT id, first_name, last_name FROM user')
        user_data = cur.fetchall()

        cur.execute('SELECT id, title FROM courses')
        course_data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()

        sweet_alert = request.args.get('sweet_alert')
        return render_template('enroll/enroll_table.html', data=data, user_data=user_data, course_data=course_data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

# -------------------------------------------------------------------------------------------------



# ------------------------------------ ส่วนของ Quiz_attempts ---------------------------------------------------------


@app.route('/attempts_table')
@login_required
def attempts_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT attempt_id, user_id, quiz_id, lesson_id, score, DATE_FORMAT(attempt_date, '%d/%m/%Y : %H:%i:%s') AS formatted_date FROM quiz_attempts''')
        data = cur.fetchall()

        cur.execute('SELECT id, first_name, last_name FROM user')
        user_data = cur.fetchall()

        cur.execute('SELECT quiz_id, quiz_name FROM quiz')
        quiz_data = cur.fetchall()

        cur.execute('SELECT lesson_id, lesson_name FROM lesson')
        lesson_data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()

        sweet_alert = request.args.get('sweet_alert')
        return render_template('quiz_attempts/attempts_table.html', data=data, user_data=user_data, quiz_data=quiz_data, lesson_data=lesson_data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))
    


@app.route('/view_attempts/<id>')
def view_attempts(id):
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT courses.title AS course_title, quiz.quiz_name, lesson.lesson_name, CONCAT(instructor.first_name, ' ', instructor.last_name) AS instructor_name, quiz_attempts.question_count, quiz.passing_percentage, CONCAT(user.first_name, ' ', user.last_name) AS user_name, quiz_attempts.attempt_date
                        FROM courses
                        JOIN lesson ON courses.id = lesson.course_id
                        JOIN quiz ON lesson.lesson_id = quiz.lesson_id
                        JOIN instructor ON courses.instructor_id = instructor.id
                        LEFT JOIN question ON quiz.quiz_id = question.quiz_id
                        JOIN quiz_attempts ON quiz.quiz_id = quiz_attempts.quiz_id
                        JOIN user ON quiz_attempts.user_id = user.id
                        WHERE quiz_attempts.attempt_id = %s
                        GROUP BY courses.title, quiz.quiz_name, lesson.lesson_name, instructor_name, quiz_attempts.question_count, quiz.passing_percentage, user_name, quiz_attempts.attempt_date;
                    """, (id,))
        data = cur.fetchall()

        # Fetch the attempt details
        cur.execute("""SELECT question_count, passing_percentage, score
                        FROM quiz_attempts
                        JOIN quiz ON quiz_attempts.quiz_id = quiz.quiz_id
                        WHERE quiz_attempts.attempt_id = %s
                    """, (id,))
        attempts_data = cur.fetchall()

        # Fetch user details
        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/instructor.png"

        cur.close()

        # Calculate the number of correct and incorrect answers
        detailed_attempts_data = []
        for attempt in attempts_data:
            question_count = attempt[0]
            passing_percentage = attempt[1]
            score = attempt[2]
            correct_answers = score
            incorrect_answers = question_count - correct_answers
            percentage_score = (correct_answers / question_count) * 100 if question_count > 0 else 0

            detailed_attempts_data.append({
                'question_count': question_count,
                'passing_percentage': passing_percentage,
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'percentage_score': percentage_score
            })

        return render_template('quiz_attempts/view_attempts.html', data=data, attempts_data=detailed_attempts_data, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))








# -----------------------------------------------------------------------------------------------------




# ------------------------------------ ส่วนของ category ---------------------------------------------------------
# ตารางหมวดหมู่
@app.route('/category_table')
@login_required
def category_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, icon, name FROM categories')
        data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()
        sweet_alert = request.args.get('sweet_alert')
        return render_template('category/category_table.html', data=data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

# เพิ่มหมวดหมู่
@app.route('/insert_category', methods=['GET', 'POST'])
@login_required
def insert_category():
    cur = mysql.connection.cursor()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Retrieve form data
        icon = request.form['icon']
        name = request.form['name']

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO categories (icon, name) 
                        VALUES (%s, %s)''', 
                        (icon, name))
        mysql.connection.commit()
        cur.close()
        flash('category successfully added', 'success')
        return redirect(url_for('category_table'))

    # If it's a GET request or there are validation errors, render the form
    return render_template('category/insert_category.html', admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)

# แก้ไขหมวดหมู่
@app.route('/edit_category/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM categories WHERE id = %s', (id,))
        category = cur.fetchone()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()
        return render_template('category/updated_category.html', category=category, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

# อัปเดตหมวดหมู่
@app.route('/updated_category', methods=['POST'])
@login_required
def updated_category():
    if current_user.role in ['admin', 'instructor']:
        if request.method == 'POST':
            id = request.form.get('id')
            icon = request.form.get('icon')
            name = request.form.get('name')


                # Update the category in the database
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE categories SET icon = %s, name = %s WHERE id = %s''', 
                            (icon, name, id))
            mysql.connection.commit()
            cur.close()

            flash('Category successfully updated', 'success')
    
        # Redirect to the category_table page regardless of the outcome
        return redirect(url_for('category_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))

# ลบหมวดหมู่
@app.route('/delete_category/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    if current_user.role in ['admin', 'instructor']:
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM categories WHERE id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('category successfully deleted', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting category: {str(e)}', 'error')
        
        return redirect(url_for('category_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
        return redirect(url_for('home'))


# ------------------------------------  ---------------------------------------------------------




# ------------------------------------ ส่วนของ คอร์สเรียน ---------------------------------------------------------

# ตารางคอร์ส
@app.route('/course_table')
@login_required
def course_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        
        # Fetch course data
        cur.execute('''SELECT id, featured_image, title, instructor_id, category_id, DATE_FORMAT(created_at, '%d/%m/%Y : %H:%i:%s') AS formatted_date, status FROM courses''')
        course_data = cur.fetchall()
        
        # Fetch instructor data
        cur.execute('SELECT id, first_name, last_name FROM instructor')
        instructor_data = cur.fetchall()
        
        # Fetch category data
        cur.execute('SELECT id, name FROM categories')
        category_data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        
        cur.close()
        
        sweet_alert = request.args.get('sweet_alert')
        
        return render_template('course/course_table.html', course_data=course_data, instructor_data=instructor_data, category_data=category_data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))



app.config['UPLOAD_FOLDER_COURSE'] = 'static/img/uploads/course'

# เพิ่ม บทเรียน
@app.route('/insert_course', methods=['GET', 'POST'])
@login_required
def insert_course():
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    
    if current_user.role not in ['admin', 'instructor']:
        flash("You are not authorized to access this page.", 'danger')
        return redirect(url_for('home'))

    instructor = []
    categories = []

    try:
        # Fetch instructors from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, first_name, last_name FROM instructor")
        instructor = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching instructors: {e}", 'danger')

    try:
        # Fetch categories from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, icon, name FROM categories")
        categories = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching categories: {e}", 'danger')

    if request.method == 'POST':
        try:
            # Retrieve form data
            featured_image = request.files.get('featured_image')
            featured_video = request.form.get('featured_video')
            title = request.form.get('title')
            instructor_id = request.form.get('instructor_id')
            category_id = request.form.get('category_id')
            description = request.form.get('description')          
            language = request.form.get('language')
            deadline = request.form.get('deadline')
            slug = request.form.get('slug')
            status = request.form.get('status')
            certificate = request.form.get('certificate')

            # Check if category_id exists in categories table
            if category_id:
                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM categories WHERE id = %s", (category_id,))
                category = cur.fetchone()
                cur.close()

                if not category:
                    flash("Invalid category selected. Please select a valid category.", 'danger')
                    return redirect(url_for('insert_course'))
            else:
                flash("Category is required. Please select a category.", 'danger')
                return redirect(url_for('insert_course'))

            # Initialize featured_image_path with a default value
            featured_image_path = "../static/img/avatars/default.png"

            # File handling (if applicable)
            if featured_image:
                featured_image_filename = secure_filename(featured_image.filename)
                featured_image.save(os.path.join(app.config['UPLOAD_FOLDER_COURSE'], featured_image_filename))
                featured_image_path = f"../static/img/uploads/course/{featured_image_filename}"

            # Add data to the database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO courses (featured_image, featured_video, title, created_at, instructor_id, category_id, description, language, deadline, slug, status, certificate)
                VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
            """, (featured_image_path, featured_video, title, instructor_id, category_id, description, language, deadline, slug, status, certificate))
            mysql.connection.commit()
            cur.close()

            # Redirect to the course table with a success message
            flash("Course successfully added.", 'success')
            return redirect(url_for('course_table'))

        except Exception as e:
            flash(f"An error occurred while inserting the course: {e}", 'danger')

    # Render form for adding data
    return render_template('course/insert_course.html', instructor=instructor, categories=categories, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



# แก้ไขคอร์สเรียน
@app.route('/edit_course/<id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role in ['admin', 'instructor']:

        instructor = []
        categories = []

        try:
            # Fetch instructors from the database
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, first_name, last_name FROM instructor")
            instructor = cur.fetchall()
            cur.close()           
        except Exception as e:
            flash("Failed to fetch instructors.", 'danger')
            print(str(e))

        try:
            # Fetch categories from the database
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, icon, name FROM categories")
            categories = cur.fetchall()
            cur.close()
        except Exception as e:
            flash("Failed to fetch categories.", 'danger')
            print(str(e))

        try:
            # Fetch the course details
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM courses WHERE id = %s', (id,))
            course = cur.fetchone()
            cur.close()
        except Exception as e:
            flash("Failed to fetch course details.", 'danger')
            print(str(e))
            course = None

        return render_template('course/updated_course.html', course=course, instructor=instructor, categories=categories, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))





app.config['UPLOAD_FOLDER_COURSE_UPDATED'] = 'static/img/updated/course'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/updated_course', methods=['GET', 'POST'])
@login_required
def updated_course():
    if current_user.role not in ['admin', 'instructor']:
        flash("You are not authorized to access this page.", 'danger')
        return redirect(url_for('home'))

    instructor = []
    categories = []

    try:
        # Fetch instructors from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, first_name, last_name FROM instructor")
        instructor = cur.fetchall()
        cur.close()
    except Exception as e:
        flash("Failed to fetch instructors.", 'danger')
        print(str(e))

    try:
        # Fetch categories from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, icon, name FROM categories")
        categories = cur.fetchall()
        cur.close()
    except Exception as e:
        flash("Failed to fetch categories.", 'danger')
        print(str(e))

    if request.method == 'POST':
        try:
            # Retrieve form data
            id = request.form.get('id')
            featured_image = request.files.get('featured_image')
            featured_video = request.form.get('featured_video')
            title = request.form.get('title')
            instructor_id = request.form.get('instructor_id')
            category_id = request.form.get('category_id')
            description = request.form.get('description')
            language = request.form.get('language')
            deadline = request.form.get('deadline')
            slug = request.form.get('slug')
            status = request.form.get('status')
            certificate = request.form.get('certificate')

            # Check if category_id exists in categories table
            if category_id:
                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM categories WHERE id = %s", (category_id,))
                category = cur.fetchone()
                cur.close()

                if not category:
                    flash("Invalid category selected. Please select a valid category.", 'danger')
                    return redirect(url_for('updated_course'))
            else:
                flash("Category is required. Please select a category.", 'danger')
                return redirect(url_for('updated_course'))

            # Initialize featured_image_path with a default value
            featured_image_path = None
            if featured_image and allowed_file(featured_image.filename):
                filename = secure_filename(featured_image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER_COURSE_UPDATED'], filename)
                featured_image.save(filepath)
                featured_image_path = os.path.join(app.config['UPLOAD_FOLDER_COURSE_UPDATED'], filename)

            # Update data in the database
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE courses 
                SET featured_image=%s, featured_video=%s, title=%s, created_at=NOW(), instructor_id=%s, category_id=%s, description=%s, language=%s, deadline=%s, slug=%s, status=%s, certificate=%s
                WHERE id=%s
            """, (featured_image_path, featured_video, title, instructor_id, category_id, description, language, deadline, slug, status, certificate, id))
            mysql.connection.commit()
            cur.close()

            # Redirect to the course table with a success message
            flash("Course successfully updated.", 'success')
            return redirect(url_for('course_table'))
        except Exception as e:
            flash("Failed to update course.", 'danger')
            print(str(e))

    # Render form for updating data
    return render_template('course/updated_course.html', instructor=instructor, categories=categories)






# ลบคอร์สเรียน
@app.route('/delete_course/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    if current_user.role in ['admin', 'instructor']:
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM courses WHERE id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('course successfully deleted', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting course: {str(e)}', 'error')
        
        return redirect(url_for('course_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบ.', 'danger')
        return redirect(url_for('home'))

# ------------------------------------------  End Course ------------------------------------------------------


# ------------------------------------------  ส่วนของชั้นเรียน / Lesson ------------------------------------------------------

@app.route('/lesson_table')
@login_required
def lesson_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT lesson_id, lesson_name, DATE_FORMAT(lesson_date, '%d/%m/%Y : %H:%i:%s') AS formatted_date, course_id FROM lesson''')
        data = cur.fetchall()

        cur.execute('SELECT id, title FROM courses')
        course_data = cur.fetchall()
        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()

        sweet_alert = request.args.get('sweet_alert')
        return render_template('lesson/lesson_table.html', data=data, course_data=course_data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))


@app.route('/insert_lesson', methods=['GET', 'POST'])
@login_required
def insert_lesson():
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))
    
    course = []

    try:
        # Fetch instructors from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title FROM courses")
        course = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching instructors: {e}", 'danger')
    
    if request.method == 'POST':
        # Retrieve form data
        lesson_name = request.form.get('lesson_name')
        course_id = request.form.get('course_id')
        
        # Validate form data
        if not lesson_name:
            flash('Please provide all the required fields', 'error')
            return redirect(url_for('insert_lesson'))

        try:
            cur = mysql.connection.cursor()
            # Check if lesson already exists
            cur.execute("SELECT * FROM lesson WHERE lesson_name = %s", (lesson_name,))
            existing_lesson = cur.fetchone()
            
            if existing_lesson:
                flash('Lesson already exists', 'error')
                return redirect(url_for('insert_lesson'))

            # Insert lesson into the database
            cur.execute('''INSERT INTO lesson (lesson_name, course_id) VALUES (%s, %s)''', (lesson_name, course_id))
            mysql.connection.commit()

            flash('Lesson successfully added', 'success')
            return redirect(url_for('lesson_table'))
        
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            return redirect(url_for('insert_lesson'))
        
        finally:
            cur.close()

    # If it's a GET request or there are validation errors, render the form
    return render_template('lesson/insert_lesson.html', course=course, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)






@app.route('/edit_lesson/<id>', methods=['GET', 'POST'])
@login_required
def edit_lesson(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

    try:
        # Fetch lessons from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title FROM courses")
        course = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching lessons: {e}", 'danger')


    try:
        # Fetch the quiz details from the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM lesson WHERE lesson_id = %s', (id,))
        lesson = cur.fetchone()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching the quiz: {e}", 'danger')


    return render_template('lesson/updated_lesson.html', course=course, lesson=lesson, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)






@app.route('/updated_lesson', methods=['GET', 'POST'])
@login_required
def updated_lesson():
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))
    

    course = []

    try:
        # Fetch courses from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title FROM courses")
        course = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching courses: {e}", 'danger')

    if request.method == 'POST':
        lesson_id = request.form.get('lesson_id')
        lesson_name = request.form.get('lesson_name')
        course_id = request.form.get('course_id')

        # Validate form data
        if not all([lesson_id, lesson_name, course_id]):
            flash('กรุณากรอกข้อมูลให้ครบถ้วน.', 'danger')
            return redirect(url_for('lesson_table'))

        try:
            lesson_id = int(lesson_id)
        except ValueError:
            flash('รหัสบทเรียนไม่ถูกต้อง.', 'danger')
            return redirect(url_for('lesson_table'))

        try:
            cur = mysql.connection.cursor()

            # ตรวจสอบว่ามีบทเรียนนี้อยู่ในระบบหรือไม่
            cur.execute("SELECT * FROM lesson WHERE lesson_id = %s", (lesson_id,))
            lesson = cur.fetchone()

            if not lesson:
                flash('ไม่พบทเรียน.', 'danger')
                return redirect(url_for('lesson_table'))

            # อัปเดตข้อมูลบทเรียนในฐานข้อมูล
            cur.execute('''UPDATE lesson SET lesson_name = %s, lesson_date = NOW(), course_id = %s WHERE lesson_id = %s''',
                        (lesson_name, course_id, lesson_id))
            mysql.connection.commit()

            flash('อัปเดตบทเรียนเรียบร้อยแล้ว', 'success')
        except Exception as e:
            flash(f'เกิดข้อผิดพลาด: {str(e)}', 'danger')
        finally:
            cur.close()

    return redirect(url_for('lesson_table', course=course))




@app.route('/delete_lesson/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_lesson(id):
    if current_user.role in ['admin', 'instructor']:
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM lesson WHERE lesson_id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('Lesson successfully deleted', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting lesson: {str(e)}', 'error')
        
        return redirect(url_for('lesson_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
        return redirect(url_for('home'))

# ------------------------------------------  End Lesson ------------------------------------------------------


# ------------------------------------------  ส่วนของ Video / Quiz ------------------------------------------------------


@app.route('/add_quiz_video/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def add_quiz_video(lesson_id):
    if current_user.role not in ['admin', 'instructor']:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

    # Establish a database cursor within the block where authorization is checked
    cur = mysql.connection.cursor()
    
    # Fetch existing quiz videos for the specific lesson_id
    cur.execute('SELECT video_id, title, youtube_link, description, time_duration, quiz_id FROM quiz_video WHERE lesson_id = %s', (lesson_id,))
    data = cur.fetchall()

    # Fetch quiz data for dropdown options
    cur.execute('SELECT quiz_id, quiz_name FROM quiz')
    quiz_data = cur.fetchall()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    
    # Get sweet_alert message if passed as a query parameter
    sweet_alert = request.args.get('sweet_alert')

    # Close the database cursor after fetching data
    cur.close()

    # Render the template with fetched data and variables
    return render_template('quiz_video/add_quiz_video.html', data=data, sweet_alert=sweet_alert, lesson_id=lesson_id, quiz_data=quiz_data, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



    

@app.route('/edit_quiz_video/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quiz_video(id):
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()

        # Fetch quiz video data
        cur.execute('SELECT * FROM quiz_video WHERE video_id = %s', (id,))
        quiz_video = cur.fetchone()

        # Fetch quizzes related to the lesson of the quiz video
        cur.execute("""
            SELECT quiz.quiz_id, CONCAT(quiz.quiz_name, ' | ', lesson.lesson_name) as quiz_lesson_name 
            FROM quiz
            LEFT JOIN lesson ON quiz.lesson_id = lesson.lesson_id
            LEFT JOIN quiz_video ON quiz_video.lesson_id = lesson.lesson_id
            WHERE quiz_video.video_id = %s
        """, (id,))  # Using lesson_id from the fetched quiz_video
        quizzes = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

        cur.close()

        return render_template('quiz_video/updated_quiz_video.html', quiz_video=quiz_video, quizzes=quizzes, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))





app.config['UPLOAD_FOLDER_VIDEO_UPDATED'] = 'static/img/updated/video_img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/updated_quiz_video/<int:id>', methods=['POST'])
@login_required
def updated_quiz_video(id):
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))

    try:
        # Retrieve form data
        title = request.form.get('title')
        youtube_link = request.form.get('youtube_link')
        description = request.form.get('description')
        time_duration = request.form.get('time_duration')
        preview = request.form.get('preview')
        preview = 1 if preview == '1' else 0  # Convert preview to 1 or 0
        quiz_id = request.form.get('quiz_id')

        video_image = None
        if 'video_image' in request.files:
            video_image = request.files['video_image']
            if video_image and allowed_file(video_image.filename):
                filename = secure_filename(video_image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER_VIDEO_UPDATED'], filename)
                video_image.save(filepath)
                videoimage_filename = f"../{app.config['UPLOAD_FOLDER_VIDEO_UPDATED']}/{filename}"  # Update path to be accessible in Flask app

        # Database operations
        cur = mysql.connection.cursor()

        # Fetch lesson_id associated with video_id
        cur.execute("SELECT lesson_id FROM quiz_video WHERE video_id = %s", (id,))
        video_data = cur.fetchone()

        if not video_data:
            flash('ไม่พบคำถาม.', 'danger')
            return redirect(url_for('home'))

        lesson_id = video_data[0]

        # Update quiz video information
        if video_image:
            cur.execute('''UPDATE quiz_video SET title = %s, youtube_link = %s, description = %s, time_duration = %s, preview = %s, video_image = %s, quiz_id = %s WHERE video_id = %s''',
                        (title, youtube_link, description, time_duration, preview, videoimage_filename, quiz_id, id))
        else:
            cur.execute('''UPDATE quiz_video SET title = %s, youtube_link = %s, description = %s, time_duration = %s, preview = %s, quiz_id = %s WHERE video_id = %s''',
                        (title, youtube_link, description, time_duration, preview, quiz_id, id))

        mysql.connection.commit()

        flash('อัปเดตเรียบร้อยแล้ว', 'success')

    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'danger')
        app.logger.error(f'Database error: {err}')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        app.logger.error(f'An error occurred: {e}')
    finally:
        cur.close()

    return redirect(url_for('add_quiz_video', lesson_id=lesson_id))






@app.route('/delete_quiz_video/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quiz_video(id):
    if current_user.role in ['admin', 'instructor']:
        # หา quiz_id ของคำถามที่ต้องการลบ
        cur = mysql.connection.cursor()
        cur.execute('SELECT lesson_id FROM quiz_video WHERE video_id = %s', (id,))
        video_id_data = cur.fetchone()
        if video_id_data:
            video_id = video_id_data[0]  # รับ quiz_id จากการ query
            # ลบคำถาม
            cur.execute('DELETE FROM quiz_video WHERE video_id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('Successfully deleted', 'success')

            return redirect(url_for('add_quiz_video', lesson_id=video_id))  # ระบุ quiz_id ไว้ในการสร้าง URL
        else:
            flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
            return redirect(url_for('home'))




@app.route('/add_quiz/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def add_quiz(lesson_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))
    
    quizzes = []

    try:
        # Fetch existing quizzes from the database
        cur = mysql.connection.cursor()
        cur.execute("""SELECT quiz.quiz_id, CONCAT(quiz.quiz_name, ' | ', lesson.lesson_name) as quiz_lesson_name 
                       FROM quiz 
                       LEFT JOIN lesson ON quiz.lesson_id = lesson.lesson_id""")
        quizzes = cur.fetchall()
    except Exception as e:
        flash(f"An error occurred while fetching quizzes: {e}", 'danger')
    finally:
        cur.close()

    if request.method == 'POST':
        # Retrieve form data
        quiz_id = request.form.get('quiz_id')

        if not quiz_id:
            flash('Please provide the quiz id', 'error')
            return redirect(url_for('add_quiz', lesson_id=lesson_id))

        try:
            cur = mysql.connection.cursor()
            
            # Check if quiz already exists for this lesson
            cur.execute("SELECT * FROM quiz_video WHERE lesson_id = %s AND quiz_id = %s", (lesson_id, quiz_id))
            existing_quiz = cur.fetchone()

            if existing_quiz:
                flash('This quiz is already associated with the lesson.', 'error')
            else:
                # Insert quiz into the database
                cur.execute("INSERT INTO quiz_video (quiz_id, lesson_id) VALUES (%s, %s)", (quiz_id, lesson_id))
                mysql.connection.commit()

                # Fetch the related video_id for redirection
                # cur.execute("SELECT video_id FROM quiz_video WHERE lesson_id = %s", (lesson_id,))
                # video_id = cur.fetchone()

                flash('Quiz successfully added', 'success')
                return redirect(url_for('add_quiz_video', lesson_id=lesson_id))  # Replace 'add_quiz_video' with the actual endpoint for the video page
        except Exception as e:
            flash(f"An error occurred while adding the quiz: {e}", 'danger')
        finally:
            cur.close()

    # If it's a GET request or there are validation errors, render the form
    return render_template('quiz_video/add_quiz.html', quizzes=quizzes, lesson_id=lesson_id, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)





app.config['UPLOAD_FOLDER_VIDEO'] = 'static/img/uploads/video_img'

@app.route('/add_video/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def add_video(lesson_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            # Retrieve form data
            title = request.form.get('title')
            youtube_link = request.form.get('youtube_link')
            description = request.form.get('description')
            time_duration = request.form.get('time_duration')
            preview = request.form.get('preview', '0')
            preview = 1 if preview == '1' else 0  # Convert preview to 1 or 0

            # File upload handling
            videoimage_path = None
            if 'video_image' in request.files:
                video_image = request.files['video_image']
                if video_image.filename != '':
                    videoimage_filename = secure_filename(video_image.filename)
                    video_image.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEO'], videoimage_filename))
                    videoimage_path = f"../static/img/uploads/video_img/{videoimage_filename}"

            # Validate form data
            if not title or not youtube_link or not description:
                flash('Please provide all the required fields', 'error')
                return redirect(url_for('add_video', lesson_id=lesson_id))

            # Database operations
            cur = mysql.connection.cursor()

            # Check if video already exists for the lesson
            cur.execute("SELECT * FROM quiz_video WHERE lesson_id = %s", (lesson_id,))
            existing_video = cur.fetchone()

            if existing_video:
                flash('A video for this lesson already exists', 'error')

            # Insert video into the database
            cur.execute('''INSERT INTO quiz_video (title, youtube_link, description, time_duration, preview, video_image, lesson_id) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (title, youtube_link, description, time_duration, preview, videoimage_path, lesson_id))
            mysql.connection.commit()

            flash('Video successfully added', 'success')
            return redirect(url_for('add_quiz_video', lesson_id=lesson_id))  # Replace with the actual endpoint for the video listing page

        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            app.logger.error(f'Database error: {err}')
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            app.logger.error(f'An error occurred: {e}')
        finally:
            cur.close()

    # If it's a GET request or there are validation errors, render the form
    return render_template('quiz_video/add_video.html', lesson_id=lesson_id, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



# ------------------------------------------  ส่วนของแบบทดสอบ / Quiz ------------------------------------------------------

# ตารางแบบทดสอบ
@app.route('/quiz_table')
@login_required
def quiz_table():
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        
        # Fetch quiz data with question count
        cur.execute('''
            SELECT quiz.quiz_id, quiz.quiz_name, quiz.lesson_id, quiz.passing_percentage, DATE_FORMAT(quiz.quiz_date, '%d/%m/%Y : %H:%i:%s') AS formatted_date, COUNT(question.question_id) AS question_count
            FROM quiz
            LEFT JOIN question ON quiz.quiz_id = question.quiz_id
            GROUP BY quiz.quiz_id, quiz.quiz_name, quiz.lesson_id, quiz.passing_percentage, quiz.quiz_date
        ''')
        quiz_data = cur.fetchall()
        
        # Fetch lesson data
        cur.execute('SELECT lesson_id, lesson_name FROM lesson')
        lesson_data = cur.fetchall()

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

        cur.close()
        
        sweet_alert = request.args.get('sweet_alert')
        
        return render_template('quiz/quiz_table.html', quiz_data=quiz_data, lesson_data=lesson_data, sweet_alert=sweet_alert, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))




# เพิ่มแบบทดสอบ
@app.route('/insert_quiz', methods=['GET', 'POST'])
@login_required
def insert_quiz():
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))
    
    lesson = []

    try:
        # Fetch instructors from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT lesson_id, lesson_name FROM lesson")
        lesson = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching instructors: {e}", 'danger')
    
    if request.method == 'POST':
        # Retrieve form data
        quiz_name = request.form.get('quiz_name')
        lesson_id = request.form.get('lesson_id')
        passing_percentage = request.form.get('passing_percentage')
        
        if not all([quiz_name, passing_percentage]):
            flash('Please provide all the required fields', 'error')
            return redirect(url_for('insert_quiz'))

        try:
            cur = mysql.connection.cursor()
            # Check if question already exists
            cur.execute("SELECT * FROM quiz WHERE quiz_name = %s AND passing_percentage = %s", 
                        (quiz_name, passing_percentage))
            existing_question = cur.fetchone()
            
            if existing_question:
                flash('Question already exists', 'error')
                return redirect(url_for('insert_quiz'))

            # Insert question into the database
            cur.execute('''INSERT INTO quiz (quiz_name, lesson_id, passing_percentage) VALUES (%s, %s, %s)''', 
                        (quiz_name, lesson_id, passing_percentage))
            mysql.connection.commit()

            flash('Question successfully added', 'success')
            return redirect(url_for('quiz_table'))
       
        finally:
            cur.close()

    # If it's a GET request or there are validation errors, render the form
    return render_template('quiz/insert_quiz.html', lesson=lesson, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)




# แก้ไขแบบทดสอบ
@app.route('/edit_quiz/<id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
    cur.close()
    if current_user.role not in ['admin', 'instructor']:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('home'))

    try:
        # Fetch lessons from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT lesson_id, lesson_name FROM lesson")
        lesson = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching lessons: {e}", 'danger')


    try:
        # Fetch the quiz details from the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM quiz WHERE quiz_id = %s', (id,))
        quiz = cur.fetchone()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching the quiz: {e}", 'danger')


    return render_template('quiz/updated_quiz.html', quiz=quiz, lesson=lesson, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)




# อัปเดตแบบทดสอบ
@app.route('/updated_quiz', methods=['GET', 'POST'])
@login_required
def updated_quiz():
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))
    
    lesson = []

    try:
        # Fetch lessons from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT lesson_id, lesson_name FROM lesson")
        lesson = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"An error occurred while fetching lessons: {e}", 'danger')
        return redirect(url_for('quiz_table'))

    quiz_id = request.form.get('quiz_id')
    quiz_name = request.form.get('quiz_name')
    lesson_id = request.form.get('lesson_id')
    passing_percentage = request.form.get('passing_percentage')

    if not all([quiz_id, lesson_id, quiz_name, passing_percentage]):
        flash('กรุณากรอกข้อมูลให้ครบถ้วน.', 'danger')
        return redirect(url_for('quiz_table'))

    try:
        cur = mysql.connection.cursor()

        # ตรวจสอบว่ามีแบบทดสอบนี้อยู่ในระบบหรือไม่
        cur.execute("SELECT * FROM quiz WHERE quiz_id = %s", (quiz_id,))
        quiz = cur.fetchone()

        if not quiz:
            flash('ไม่พบแบบทดสอบ.', 'danger')
            cur.close()
            return redirect(url_for('quiz_table'))

        # อัปเดตข้อมูลแบบทดสอบในฐานข้อมูล
        cur.execute('''UPDATE quiz SET quiz_name = %s, lesson_id = %s, passing_percentage = %s, quiz_date = NOW() WHERE quiz_id = %s''',
                    (quiz_name, lesson_id, passing_percentage, quiz_id))
        mysql.connection.commit()

        flash('อัปเดตแบบทดสอบเรียบร้อยแล้ว', 'success')
    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {str(e)}', 'danger')
    finally:
        cur.close()

    # Redirect to the quiz table page with lessons and quiz data
    return redirect(url_for('quiz_table', lesson=lesson))





# ลบแบบทดสอบ
@app.route('/delete_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quiz(id):
    if current_user.role in ['admin', 'instructor']:
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM quiz WHERE quiz_id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('quiz successfully deleted', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting quiz: {str(e)}', 'error')
        
        return redirect(url_for('quiz_table'))
    else:
        flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
        return redirect(url_for('home'))


# --------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------ ส่วนของคำถาม / Question --------------------------------------------------------------------------

@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    # Ensure only authorized roles can access this route
    if current_user.role not in ['admin', 'instructor']:
        flash('You do not have the necessary permissions', 'error')
        return redirect(url_for('some_other_route'))

    if request.method == 'POST':
        # Retrieve and validate form data
        score = request.form.get('score')
        question_name = request.form.get('question_name')
        choice_a = request.form.get('choice_a')
        choice_b = request.form.get('choice_b')
        choice_c = request.form.get('choice_c')
        choice_d = request.form.get('choice_d')
        correct_answer = request.form.get('correct_answer')

        if not all([score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer]):
            flash('Please provide all the required fields', 'error')
            return redirect(url_for('add_question', quiz_id=quiz_id))

        # Check if question already exists
        cur = mysql.connection.cursor()
        query = """SELECT * FROM question 
                   WHERE score = %s AND question_name = %s AND choice_a = %s AND choice_b = %s 
                   AND choice_c = %s AND choice_d = %s AND correct_answer = %s AND quiz_id = %s"""
        cur.execute(query, (score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer, quiz_id))
        existing_question = cur.fetchone()
        cur.close()

        if existing_question:
            flash('Question already exists', 'error')
            return redirect(url_for('add_question', quiz_id=quiz_id))

        # Insert question into the database
        cur = mysql.connection.cursor()
        insert_query = """INSERT INTO question (score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer, quiz_id) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(insert_query, (score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer, quiz_id))
        mysql.connection.commit()
        cur.close()

        flash('Question successfully added', 'success')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    # If it's a GET request, retrieve existing questions to display
    cur = mysql.connection.cursor()
    cur.execute("""SELECT question_id, score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer 
                   FROM question WHERE quiz_id = %s""", (quiz_id,))
    data = cur.fetchall()

    cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
    admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

    cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
    instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    cur.close()

    sweet_alert = request.args.get('sweet_alert')

    return render_template('question/add_question.html', data=data, sweet_alert=sweet_alert, quiz_id=quiz_id, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



@app.route('/edit_question/<id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    if current_user.role in ['admin', 'instructor']:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM question WHERE question_id = %s', (id,))
        question = cur.fetchone()
        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"
        cur.close()
         
        # If user is not authorized, return a response here
        return render_template('question/updated_question.html', question=question, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)
    else:
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('home'))



@app.route('/updated_question/<int:id>', methods=['GET', 'POST'])
@login_required
def updated_question(id):
    if current_user.role not in ['admin', 'instructor']:
        flash('คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้.', 'danger')
        return redirect(url_for('home'))

    score = request.form.get('score')
    question_name = request.form.get('question_name')
    choice_a = request.form.get('choice_a')
    choice_b = request.form.get('choice_b')
    choice_c = request.form.get('choice_c')
    choice_d = request.form.get('choice_d')
    correct_answer = request.form.get('correct_answer')

    try:
        cur = mysql.connection.cursor()

        # ตรวจสอบว่ามีคำถามนี้อยู่ในระบบและดึง quiz_id
        cur.execute("SELECT quiz_id FROM question WHERE question_id = %s", (id,))
        quiz_data = cur.fetchone()
        
        if quiz_data:
            quiz_id = quiz_data[0]  # รับ quiz_id จากการ query

            # อัปเดตข้อมูลคำถามในฐานข้อมูล
            cur.execute('''UPDATE question SET score = %s, question_name = %s, choice_a = %s, choice_b = %s, choice_c = %s, choice_d = %s, correct_answer = %s WHERE question_id = %s''',
                        (score, question_name, choice_a, choice_b, choice_c, choice_d, correct_answer, id))
            mysql.connection.commit()

            flash('อัปเดตคำถามเรียบร้อยแล้ว', 'success')
        else:
            flash('ไม่พบคำถาม.', 'danger')
            return redirect(url_for('home'))

    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {str(e)}', 'danger')
    finally:
        # ปิดคอนเน็กชันของฐานข้อมูล
        cur.close()

    # ส่งผู้ใช้กลับไปยังหน้าเพิ่มคำถามด้วย quiz_id
    return redirect(url_for('add_question', quiz_id=quiz_id))




@app.route('/delete_question/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_question(id):
    if current_user.role in ['admin', 'instructor']:
        # หา quiz_id ของคำถามที่ต้องการลบ
        cur = mysql.connection.cursor()
        cur.execute('SELECT quiz_id FROM question WHERE question_id = %s', (id,))
        quiz_id_data = cur.fetchone()
        if quiz_id_data:
            quiz_id = quiz_id_data[0]  # รับ quiz_id จากการ query
            # ลบคำถาม
            cur.execute('DELETE FROM question WHERE question_id = %s', (id,))
            mysql.connection.commit()
            cur.close()

            flash('Question successfully deleted', 'success')

            return redirect(url_for('add_question', quiz_id=quiz_id))  # ระบุ quiz_id ไว้ในการสร้าง URL
        else:
            flash('คุณไม่ได้รับอนุญาตให้ดำเนินการลบผู้ใช้นี้.', 'danger')
            return redirect(url_for('home'))




# --------------------------------------------------------------------------------------------------------------------------------

@app.route('/home')
@login_required
def home():
    try:
        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        # Execute SQL command to retrieve course details
        cur.execute("""
            SELECT 
                c.id, c.title, c.description, c.featured_image,
                c.featured_video,
                cat.name as category_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                i.instructorimage,
                c.language, 
                c.deadline, 
                c.certificate, 
                c.slug
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
            JOIN instructor i ON c.instructor_id = i.id
        """)
        
        # Fetch all course results
        courses_rows = cur.fetchall()

        # Execute SQL command to retrieve category details
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories_rows = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        courses_rows = []
        categories_rows = []

    finally:
        # Close cursor
        cur.close()

    # Create list of course dictionaries for easier template rendering
    courses = [
        {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'featured_image': row[3],
            'featured_video': row[4],
            'category_name': row[5],
            'instructor_name': row[6],
            'instructor_image': row[7],
            'language': row[8],
            'deadline': row[9],
            'certificate': row[10],
            'slug': row[11]
        } for row in courses_rows
    ]

    # Create list of category dictionaries for easier template rendering
    categories = [
        {
            'id': row[0],
            'icon': row[1],
            'name': row[2]
        } for row in categories_rows
    ]

    # Render the template with the retrieved courses and categories
    return render_template('main/home.html', courses=courses, categories=categories, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)





@app.route('/about')
def about():
    try:
        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        # Execute SQL command to retrieve course details
        cur.execute("""
            SELECT 
                c.id, c.title, c.description, c.featured_image,
                c.featured_video,
                cat.name as category_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                i.instructorimage,
                c.language, 
                c.deadline, 
                c.certificate, 
                c.slug
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
            JOIN instructor i ON c.instructor_id = i.id
        """)
        
        # Fetch all course results
        courses_rows = cur.fetchall()

        # Execute SQL command to retrieve category details
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories_rows = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        courses_rows = []
        categories_rows = []

    finally:
        # Close cursor
        cur.close()

    # Create list of course dictionaries for easier template rendering
    courses = [
        {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'featured_image': row[3],
            'featured_video': row[4],
            'category_name': row[5],
            'instructor_name': row[6],
            'instructor_image': row[7],
            'language': row[8],
            'deadline': row[9],
            'certificate': row[10],
            'slug': row[11]
        } for row in courses_rows
    ]

    # Create list of category dictionaries for easier template rendering
    categories = [
        {
            'id': row[0],
            'icon': row[1],
            'name': row[2]
        } for row in categories_rows
    ]

    # Render the template with the retrieved courses and categories
    return render_template('main/about.html', courses=courses, categories=categories, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)


@app.route('/contact')
def contact():
    try:
        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        # Execute SQL command to retrieve course details
        cur.execute("""
            SELECT 
                c.id, c.title, c.description, c.featured_image,
                c.featured_video,
                cat.name as category_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                i.instructorimage,
                c.language, 
                c.deadline, 
                c.certificate, 
                c.slug
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
            JOIN instructor i ON c.instructor_id = i.id
        """)
        
        # Fetch all course results
        courses_rows = cur.fetchall()

        # Execute SQL command to retrieve category details
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories_rows = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        courses_rows = []
        categories_rows = []

    finally:
        # Close cursor
        cur.close()

    # Create list of course dictionaries for easier template rendering
    courses = [
        {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'featured_image': row[3],
            'featured_video': row[4],
            'category_name': row[5],
            'instructor_name': row[6],
            'instructor_image': row[7],
            'language': row[8],
            'deadline': row[9],
            'certificate': row[10],
            'slug': row[11]
        } for row in courses_rows
    ]

    # Create list of category dictionaries for easier template rendering
    categories = [
        {
            'id': row[0],
            'icon': row[1],
            'name': row[2]
        } for row in categories_rows
    ]

    # Render the template with the retrieved courses and categories
    return render_template('main/contact.html', courses=courses, categories=categories, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)



@app.route('/courses')
def courses():
    try:
        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        # Fetch total number of courses
        cur.execute("SELECT COUNT(*) FROM courses")
        total_courses = cur.fetchone()[0]

        # Execute SQL command to retrieve course details
        cur.execute("""
            SELECT 
                c.id, c.title, c.description, c.featured_image,
                c.featured_video,
                cat.name as category_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                i.instructorimage,
                c.language, 
                c.deadline, 
                c.certificate, 
                c.slug
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
            JOIN instructor i ON c.instructor_id = i.id
        """)
        
        # Fetch all course results
        courses_rows = cur.fetchall()

        # Execute SQL command to retrieve category details
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories_rows = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        courses_rows = []
        categories_rows = []

    finally:
        # Close cursor
        cur.close()

    # Create list of course dictionaries for easier template rendering
    courses = [
        {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'featured_image': row[3],
            'featured_video': row[4],
            'category_name': row[5],
            'instructor_name': row[6],
            'instructor_image': row[7],
            'language': row[8],
            'deadline': row[9],
            'certificate': row[10],
            'slug': row[11]
        } for row in courses_rows
    ]

    # Create list of category dictionaries for easier template rendering
    categories = [
        {
            'id': row[0],
            'icon': row[1],
            'name': row[2]
        } for row in categories_rows
    ]

    # Render the template with the retrieved courses and categories
    return render_template('course/courses.html', total_courses=total_courses, courses=courses, categories=categories, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)




class Course:
    def __init__(self, id, title, description, featured_image, featured_video, category_name, instructor_name, instructor_image, language, deadline, certificate, slug, video_id, quiz_id):
        self.id = id
        self.title = title
        self.description = description
        self.featured_image = featured_image
        self.featured_video = featured_video
        self.category = {'name': category_name}
        self.instructor_name = {'name': instructor_name}
        self.instructor = {'instructorimage': instructor_image}
        self.language = language
        self.deadline = deadline
        self.certificate = certificate
        self.slug = slug
        self.video_id = video_id
        self.quiz_id = quiz_id
        

    def get_absolute_url(self):
        return url_for('course_details', slug=self.slug)


@app.route('/<slug>')
def course_details(slug):
    total_time_duration = 0
    lesson_count = 0
    user_enroll_count = 0
    check_enroll = False
    questions = []
    enroll_data = ()

    try:
        with mysql.connection.cursor() as cur:
            # Get course details
            cur.execute("""
                SELECT 
                    c.id, c.title, c.description, c.featured_image, c.featured_video,
                    cat.name as category_name,
                    CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                    i.instructorimage,
                    c.language, 
                    c.deadline, 
                    c.certificate, 
                    c.slug,
                    qv.video_id,
                    qv.quiz_id
                FROM courses c
                JOIN categories cat ON c.category_id = cat.id
                JOIN instructor i ON c.instructor_id = i.id
                JOIN lesson l ON l.course_id = c.id
                JOIN quiz_video qv ON qv.lesson_id = l.lesson_id
                LEFT JOIN quiz q ON qv.quiz_id = q.quiz_id
                WHERE c.slug = %s
            """, [slug])
            
            course_row = cur.fetchone()

            if course_row:
                course_id = course_row[0]

                # Check if the user is enrolled in the course
                user_id = current_user.id if current_user.is_authenticated else None
                if user_id:
                    cur.execute("""
                        SELECT 
                            user_id,
                            course_id,
                            enroll_date,	
                            is_completed,
                            enroll_id,
                            completed_at  
                        FROM user_enroll
                        WHERE user_id = %s AND course_id = %s
                    """, [user_id, course_id])
                    enroll_data = cur.fetchone()
                    check_enroll = enroll_data is not None
                    

                cur.execute("SELECT l.lesson_id, l.lesson_name FROM lesson l WHERE l.course_id = %s", [course_id])
                lesson_names = cur.fetchall()

                lessons = []
                for lesson in lesson_names:
                    lesson_id = lesson[0]
                    cur.execute("""
                        SELECT q.quiz_id, q.quiz_name, qv.video_id, qv.title, qv.youtube_link, qv.description, qv.time_duration, qv.preview, COUNT(que.question_id) AS question_count
                        FROM quiz_video qv
                        LEFT JOIN question que ON qv.quiz_id = que.quiz_id
                        LEFT JOIN quiz q ON q.quiz_id = qv.quiz_id
                        WHERE qv.lesson_id = %s
                        GROUP BY qv.video_id, qv.title, qv.youtube_link, qv.description, qv.time_duration, qv.preview;
                    """, [lesson_id])
                    quizzes = cur.fetchall()

                    quizzes_data = [{'quiz_id': q[0], 'quiz_name': q[1], 'video_id': q[2], 'title': q[3], 'youtube_link': q[4], 'description': q[5], 'time_duration': q[6], 'preview': q[7], 'question_count': q[8]} for q in quizzes]

                    lesson_data = {
                        'lesson_id': lesson_id,
                        'lesson_name': lesson[1],
                        'quizzes': quizzes_data
                    }
                    lessons.append(lesson_data)

                cur.execute("""
                    SELECT SUM(qv.time_duration) AS total_time_duration
                    FROM quiz_video qv
                    WHERE qv.lesson_id IN (
                        SELECT l.lesson_id
                        FROM lesson l
                        WHERE l.course_id = %s
                    )
                """, [course_id])
                total_time_duration_result = cur.fetchone()
                if total_time_duration_result and total_time_duration_result[0] is not None:
                    total_time_duration = int(total_time_duration_result[0])

                cur.execute("""
                    SELECT COUNT(l.lesson_id) AS lesson_count
                    FROM lesson l
                    JOIN courses c ON l.course_id = c.id
                    WHERE c.slug = %s
                """, [slug])
                lesson_count = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(DISTINCT ur.user_id) AS enroll_count
                    FROM user_enroll ur
                    JOIN courses c ON ur.course_id = c.id
                    WHERE c.slug = %s
                """, [slug])
                user_enroll_count = cur.fetchone()[0]

            else:
                lessons = []

            # Fetch all categories for the dropdown menu
            cur.execute("SELECT id, icon, name FROM categories")
            categories = cur.fetchall()

            # Fetch all courses for navigation
            cur.execute("""
                SELECT c.id, c.title, c.slug, cat.name as category_name
                FROM courses c
                JOIN categories cat ON c.category_id = cat.id
            """)
            all_courses = cur.fetchall()

            cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
            user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

            cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
            admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

            cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
            instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

            def random_questions(quiz_id, limit):
                cur.execute(""" 
                    SELECT q.question_id, q.quiz_id, q.score, qz.quiz_name, q.question_name, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer
                    FROM question q
                    JOIN quiz qz ON q.quiz_id = qz.quiz_id
                    WHERE q.quiz_id = %s
                    ORDER BY RAND()
                    LIMIT %s
                """, (quiz_id, limit))
                return cur.fetchall()

            # Fetch random questions for the quiz (assuming quiz_id is correctly defined)
            if course_row:
                quiz_id = course_row[13]  # Adjust as per your application logic
                questions = random_questions(quiz_id, 15)  # Adjust limit as needed

            questions_data = [{'question_id': q[0], 'quiz_id': q[1], 'score': q[2], 'quiz_name': q[3], 'question_name': q[4], 'choice_a': q[5], 'choice_b': q[6], 'choice_c': q[7], 'choice_d': q[8], 'correct_answer': q[9]} for q in questions]

    except Exception as e:
        print(f"An error occurred: {e}")
        course_row = None
        categories = []
        lessons = []
        all_courses = []
        user_image_url = []
        admin_image_url = []
        instructor_image_url = []
        questions_data = []

    finally:
        cur.close()

    if course_row:
        course = Course(
            id= course_row[0],
            title= course_row[1],
            description= course_row[2],
            featured_image= course_row[3],
            featured_video= course_row[4],
            category_name= course_row[5],
            instructor_name= course_row[6],
            instructor_image= course_row[7],
            language= course_row[8],
            deadline= course_row[9],
            certificate= course_row[10],
            slug= course_row[11],
            video_id= course_row[12],
            quiz_id= course_row[13]
        )
    else:
        course = None

    categories = [{'id': row[0], 'icon': row[1], 'name': row[2]} for row in categories]
    courses = [{'id': row[0], 'title': row[1], 'slug': row[2], 'category_name': row[3]} for row in all_courses]

    return render_template('course/course_details.html', 
                           course=course, 
                           categories=categories, 
                           lessons=lessons, 
                           courses=courses, 
                           total_time_duration=total_time_duration, 
                           lesson_count=lesson_count, 
                           user_enroll_count=user_enroll_count, 
                           check_enroll=check_enroll,
                           questions=questions_data,
                           limit=len(questions_data),
                           user_image_url=user_image_url,
                           admin_image_url=admin_image_url,
                           instructor_image_url=instructor_image_url,
                           enroll_data=enroll_data)






@app.route('/enroll/<slug>')
def enroll_course(slug):
    try:
        cur = mysql.connection.cursor()

        # Get user ID (replace with actual method to get current user ID)
        user_id = current_user.id

        # Get course ID based on slug
        cur.execute("SELECT id FROM courses WHERE slug = %s", [slug])
        course_id = cur.fetchone()[0]

        # Insert into user_enroll table
        cur.execute("""
            INSERT INTO user_enroll (user_id, course_id, enroll_date)
            VALUES (%s, %s, %s)
        """, [user_id, course_id, datetime.now()])

        mysql.connection.commit()
        flash('You have successfully enrolled in the course!', 'success')

    except Exception as e:
        print(f"An error occurred: {e}")
        mysql.connection.rollback()
        flash('Failed to enroll in the course. Please try again later.', 'danger')

    finally:
        cur.close()

    if 'learning_status' not in session:
        session['learning_status'] = {}
    session['learning_status'][slug] = False

    return redirect(url_for('course_details', slug=slug))




class Quiz_video:
    def __init__(self, id, title, category_name, slug, video_id, video_title, youtube_link, video_description, time_duration, video_image, quiz_id, lesson_id):
        self.id = id
        self.title = title
        self.category = {'name': category_name}
        self.slug = slug
        self.video_id = video_id
        self.video_title = video_title
        self.youtube_link = youtube_link
        self.video_description = video_description
        self.time_duration = time_duration
        self.video_image = video_image
        self.quiz_id = quiz_id
        self.quiz_id = lesson_id

    def get_absolute_url(self):
        return url_for('course_details', slug=self.slug)



@app.route('/quiz/<slug>/<quiz_id>')
def take_quiz(slug, quiz_id):
    user_id = current_user.id if current_user.is_authenticated else None
    try:
        # Connect to MySQL
        cur = mysql.connection.cursor()

        # Fetch course details and video information
        cur.execute("""
            with all_quiz as (
                SELECT 
                    c.id, c.title,
                    cat.name AS category_name,
                    c.slug,
                    qv.video_id,
                    qv.title AS video_title,
                    qv.youtube_link,
                    qv.description AS video_description,
                    qv.time_duration,
                    qv.video_image,
                    qv.quiz_id,
                    l.lesson_id,  -- Add lesson_id here
                    LEAD( 
                        CASE WHEN qv.quiz_id is not null 
                        then qv.quiz_id else qv.video_id 
                        end 
                    ) over () as next_element_id,
                    LEAD( 
                        CASE WHEN qv.quiz_id is not null 
                        then 'quiz' else 'video'
                        end 
                    ) over () as next_element_type
                FROM courses c
                JOIN categories cat ON c.category_id = cat.id
                JOIN lesson l ON l.course_id = c.id
                JOIN quiz_video qv ON qv.lesson_id = l.lesson_id
                LEFT JOIN quiz q ON qv.quiz_id = q.quiz_id
                WHERE c.slug = %s
            )
            select * from all_quiz where quiz_id = %s
        """, (slug, quiz_id))
        
        video_row = cur.fetchone()

        if video_row:
            # Extract course ID and lesson ID from the fetched row
            course_id = video_row[0]
            lesson_id = video_row[11]  # Ensure lesson_id is correctly assigned
            quiz_limit = 15

            # Fetch lessons associated with this course
            cur.execute("SELECT l.lesson_id, l.lesson_name FROM lesson l WHERE l.course_id = %s", [course_id])
            lesson_names = cur.fetchall()

            lessons = []
            for lesson in lesson_names:
                current_lesson_id = lesson[0]
                # Fetch quizzes associated with each lesson
                cur.execute("""
                WITH latest_quiz_attempts AS (
                    SELECT 
                        quiz_id, 
                        MAX(attempt_id) AS latest_attempt_id
                    FROM quiz_attempts
                    WHERE user_id = %s
                    GROUP BY quiz_id
                ), lastest_video_attemts as (
                    SELECT 
                        video_id, 
                        MAX(attempt_id) AS latest_attempt_id
                    FROM video_attempts
                    WHERE user_id = %s
                    GROUP BY video_id
                )         
                SELECT qv.lesson_id, q.quiz_id, q.quiz_name, qv.video_id, qv.title, qv.youtube_link, qv.description, qv.time_duration, qv.preview, qv.video_image, COUNT(que.question_id) AS question_count, COALESCE(quiz_attempts.passed, va.passed, 0) AS passed
                FROM quiz_video qv
                LEFT JOIN question que ON qv.quiz_id = que.quiz_id
                LEFT JOIN quiz q ON q.quiz_id = qv.quiz_id
                LEFT JOIN (
                    SELECT qa.quiz_id, qa.passed
                    FROM quiz_attempts qa
                    JOIN latest_quiz_attempts lqa
                        on lqa.latest_attempt_id = qa.attempt_id
                ) quiz_attempts ON q.quiz_id = quiz_attempts.quiz_id
                LEFT JOIN (
                    select va.video_id, va.passed from video_attempts va
                    join lastest_video_attemts lva
                        on lva.latest_attempt_id = va.attempt_id
                ) as va on va.video_id = qv.video_id 
                WHERE qv.lesson_id = %s
                GROUP BY qv.video_id, qv.title, qv.youtube_link, qv.description, qv.time_duration, qv.preview, qv.video_image, q.quiz_id, q.quiz_name, quiz_attempts.passed, va.passed;
                """, [user_id, user_id, current_lesson_id])
                quizzes = cur.fetchall()

                quizzes_data = [
                    {
                        'lesson_id': q[0], 
                        'quiz_id': q[1], 
                        'quiz_name': q[2], 
                        'video_id': q[3], 
                        'title': q[4], 
                        'youtube_link': q[5], 
                        'description': q[6], 
                        'time_duration': q[7], 
                        'preview': q[8], 
                        'video_image': q[9], 
                        'question_count': q[10] if q[10] < quiz_limit else quiz_limit, 
                        'passed': q[11]
                    } for q in quizzes
                ]

                lesson_data = {
                    'lesson_id': current_lesson_id, 
                    'lesson_name': lesson[1],
                    'quizzes': quizzes_data
                }
                
                lessons.append(lesson_data)

        else:
            # If no course found with the given slug, set lessons to empty list
            lessons = []

        # Function to fetch random questions
        def random_questions(quiz_id, limit):
            cur.execute(""" 
                SELECT q.question_id, q.quiz_id, q.score, qz.quiz_name, q.question_name, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer
                FROM question q
                JOIN quiz qz ON q.quiz_id = qz.quiz_id
                WHERE q.quiz_id = %s
                ORDER BY RAND()
                LIMIT %s
            """, (quiz_id, limit))
            return cur.fetchall()

        # Fetch random questions for the quiz
        questions = random_questions(quiz_id, 15)  # Adjust limit as needed

        questions_data = [{'question_id': q[0], 'quiz_id': q[1], 'score': q[2], 'quiz_name': q[3], 'question_name': q[4], 'choice_a': q[5], 'choice_b': q[6], 'choice_c': q[7], 'choice_d': q[8], 'correct_answer': q[9]} for q in questions]

        # Fetch passing score from database
        cur.execute("SELECT passing_percentage FROM quiz WHERE quiz_id = %s", (quiz_id,))
        passing_score = cur.fetchone()[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        video_row = None
        lessons = []
        questions_data = []
        passing_score = None

    finally:
        cur.close()

    # Initialize course object if found, else None
    if video_row:
        video = {
            'id': video_row[0],
            'title': video_row[1],
            'category_name': video_row[2],
            'slug': video_row[3],
            'video_id': video_row[4],
            'video_title': video_row[5],
            'youtube_link': video_row[6],
            'video_description': video_row[7],
            'time_duration': video_row[8],
            'video_image': video_row[9],
            'quiz_id': video_row[10],
            'lesson_id': video_row[11]
        }

        next_element = {
            'element_id': video_row[12],
            'element_type': video_row[13],
        } 
    else:
        next_element = None
        video = None

    if 'last_visited_pages' not in session:
        session['last_visited_pages'] = {}
    session['last_visited_pages'][slug] = {'type': 'quiz', 'id': quiz_id}

    # Render the template with all necessary data
    return render_template(
        'course/quiz.html', 
        video=video, 
        lessons=lessons, 
        questions=questions_data, 
        quiz_id=quiz_id, 
        lesson_id=lesson_id, 
        passing_score=passing_score,
        next_element=next_element
    )








# ตัวอย่างการคำนวณคะแนน
def calculate_score(form_data, quiz_id):
    cur = mysql.connection.cursor()
    
    query = "SELECT question_id, score, correct_answer FROM question WHERE quiz_id = %s"
    cur.execute(query, (quiz_id,))
    questions = cur.fetchall()
    
    score = 0
    for question in questions:
        question_id = question[0]
        correct_answer = question[2]  # Index 2 for correct_answer
        user_answer = form_data.get(f'question_{question_id}')
        
        # Remove 'choice_' prefix before comparison
        if user_answer and user_answer.startswith('choice_'):
            user_answer = user_answer.replace('choice_', '')
        
        # Debug print to check each question and answer
        print(f"Question ID: {question_id}, Correct Answer: {correct_answer}, User Answer: {user_answer}")
        
        if user_answer == correct_answer:
            score += question[1]  # Index 1 for score
    
    cur.close()
    
    # Return score and the number of questions
    return score, len(questions)




@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    # Extract data from the form
    user_id = request.form.get('user_id')
    quiz_id = request.form.get('quiz_id')
    lesson_id = request.form.get('lesson_id')
    
    # Calculate score and get question count
    score, question_count = calculate_score(request.form, quiz_id)

    # Connect to MySQL and get passing score
    cur = mysql.connection.cursor()
    cur.execute("SELECT passing_percentage FROM quiz WHERE quiz_id = %s", (quiz_id,))
    passing_score = cur.fetchone()[0]
    
    # Calculate the percentage score
    percentage_score = (score / question_count) * 100 if question_count > 0 else 0

    # Check if the score is passing
    passed = percentage_score >= passing_score

    print('passed', passed)
    # Insert quiz attempt data into quiz_attempts table
    try:
        cur.execute(
            "INSERT INTO quiz_attempts (user_id, quiz_id, lesson_id, score, question_count, passed) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, quiz_id, lesson_id, score, question_count, passed)
        )
        mysql.connection.commit()
    except Exception as e:
        print(f"Error while inserting into quiz_attempts: {e}")
        mysql.connection.rollback()
        return jsonify(success=False, error=str(e))

    cur.close()  # Close the cursor

    # Return the original score and pass status as JSON
    return jsonify(score=score, passed=passed)


@app.route('/generate_certificate', methods=['GET'])
def generate_certificate():
    
    user_id = current_user.id if current_user.is_authenticated else None
    enroll_id = request.args.get('enroll_id')
    

    #fetch certificate data
        # Connect to MySQL and get passing score
    cur = mysql.connection.cursor()

    certificate_data_sql = """
        SELECT 
            c.title ,
            ue.enroll_id as cer_number,
            u.first_name ,
            u.last_name ,
            ue.completed_at 
        FROM user_enroll ue 
        JOIN `user` u 
            on ue.user_id = u.id
        JOIN courses c 
            on c.id = ue.course_id 
        where ue.enroll_id = %s
        and ue.user_id = %s
        and ue.is_completed is true
    """
    cur.execute(certificate_data_sql, (enroll_id, user_id))
    certificate_data = cur.fetchone()

    if not certificate_data:
        jsonify(success=False, error=f'Missing certificate data for user: {user_id}')

    user_name = f"{certificate_data[2]} {certificate_data[3]}"  # first_name
    course_name = certificate_data[0]  # title
    date = certificate_data[4].strftime('%d-%m-%Y')  # completed_at
    certificate_number = str(certificate_data[1])  # cer_number
    
    cur.close()  # Close the cursor

    # Load the certificate template
    template_path = 'static/img/certificate/certificate_template.png'
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    # Define font and text position
    font_path = 'static/fonts/great_vibes/GreatVibes-Regular.ttf'  # Path to your font file
    font_large = ImageFont.truetype(font_path, 140)
    font = ImageFont.truetype(font_path, 50)


    # Get image dimensions
    image_width, image_height = template.size
    
    # Helper function to center text
    def draw_centered_text(draw, text, position_y, font, fill='black'):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        position_x = (image_width - text_width) / 2
        draw.text((position_x, position_y), text, font=font, fill=fill)

    def draw_centered_text_adv(draw, text, position, font, fill='black', justify='center'):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        position_x = position[0]
        if justify == 'center': 
            position_x = position_x - text_width
        draw.text((position_x, position[1]), text, font=font, fill=fill)
    
    
    # Position for user's name
    name_position_y = 700  # Adjust based on your template
    # Position for course name
    course_position = (825, 1075)  # Adjust based on your template
    # Position for date
    date_position = ( 1420, 1075)  # Adjust based on your template
    # Position for certificate number
    certificate_number_position = (1725, 210)  # Adjust based on your template

    # Draw the name, course name, date, and certificate number on the template
    draw_centered_text(draw, user_name, name_position_y, font_large)
    draw_centered_text_adv(draw, course_name, course_position , font)
    draw_centered_text_adv(draw, date, date_position , font)
    draw_centered_text_adv(draw, certificate_number, certificate_number_position , font, justify='left')

    # Save the certificate to a BytesIO object
    certificate_io = io.BytesIO()
    template.save(certificate_io, 'PNG')
    certificate_io.seek(0)

    return send_file(certificate_io, mimetype='image/png', as_attachment=True, download_name='certificate.png')


@app.route('/finish_course', methods=['PATCH'])
def finish_course():
    # Extract data from the form
    data = request.get_json()
    course_id = data.get('course_id')
    user_id = current_user.id if current_user.is_authenticated else None
    


    # Connect to MySQL and get passing score
    cur = mysql.connection.cursor()

    check_pass_all_lesson_sql = """
        WITH latest_quiz_attempts AS (
            SELECT 
                quiz_id, 
                MAX(attempt_id) AS latest_attempt_id
            FROM quiz_attempts
            WHERE user_id = %s -- ใส่ ID ของผู้ใช้ที่ล็อกอินอยู่
            GROUP BY quiz_id
        )  
        SELECT 
            c.slug ,
            c.certificate,
            l.lesson_name,
            q.quiz_name ,
            CASE WHEN lq.passed = 1 THEN true ELSE false END AS passed
        FROM courses c
        JOIN lesson l 
            on l.course_id = c.id
        JOIN quiz q 
            ON q.lesson_id  = l.lesson_id 
        LEFT JOIN (
            SELECT qa.quiz_id, qa.passed
            FROM quiz_attempts qa
            JOIN latest_quiz_attempts lqa
                on lqa.latest_attempt_id = qa.attempt_id
        ) lq ON lq.quiz_id = q.quiz_id
        WHERE c.id = %s
        and q.quiz_name = 'Post-Test'
    """
    cur.execute(check_pass_all_lesson_sql, (user_id, course_id))
    test_results = cur.fetchall()

    is_pass_all_test = True
    
    for test_result in test_results:
        is_pass = test_result[4]
        if(not is_pass):
            is_pass_all_test = False
            break

    if(is_pass_all_test):
        try:
            cur.execute("""
                UPDATE pop_learning.user_enroll 
                set is_completed = true , completed_at = CURRENT_TIMESTAMP
                where user_id = %s and course_id = %s
            """, ( user_id, course_id ))
            mysql.connection.commit()

            # Fetch user name and course name from database
            cur.execute("SELECT enroll_id FROM user_enroll WHERE user_id = %s", (user_id,))
            enroll_id = cur.fetchone()[0]


            # URL for generating the certificate with the user's name and course name
            certificate_url = url_for('generate_certificate', enroll_id=enroll_id, _external=True)
            
        except Exception as e:
            print(f"Error while updating course complete status: {e}")
            mysql.connection.rollback()
            return jsonify(success=False, error=str(e))
    else:
        return jsonify(success=True, passed=False)

    cur.close()  # Close the cursor

    # Return the original score and pass status as JSON
    return jsonify(success=True, passed=is_pass_all_test, certificate_url=certificate_url)





@app.route('/video/<slug>/<video_id>')
def watch_video(slug, video_id):
    user_id = current_user.id if current_user.is_authenticated else None
    try:
        cur = mysql.connection.cursor()

        # Fetch video details based on video ID and course slug
        cur.execute("""
            with all_quiz as (
                SELECT 
                    c.id, c.title,
                    cat.name AS category_name,
                    c.slug,
                    qv.video_id,
                    qv.title AS video_title,
                    qv.youtube_link,
                    qv.description AS video_description,
                    qv.time_duration,
                    qv.video_image,
                    qv.quiz_id,
                    l.lesson_id,  -- Add lesson_id here
                    LEAD( 
                        CASE WHEN qv.quiz_id is not null 
                        then qv.quiz_id else qv.video_id 
                        end 
                    ) over () as next_element_id,
                    LEAD( 
                        CASE WHEN qv.quiz_id is not null 
                        then 'quiz' else 'video'
                        end 
                    ) over () as next_element_type,
                    va.passed
                FROM courses c
                JOIN categories cat ON c.category_id = cat.id
                JOIN lesson l ON l.course_id = c.id
                JOIN quiz_video qv ON qv.lesson_id = l.lesson_id
                LEFT JOIN quiz q ON qv.quiz_id = q.quiz_id
                LEFT JOIN video_attempts va
                	on va.video_id = qv.video_id 
                	and user_id = %s  -- ใส่ ID ของผู้ใช้ที่ล็อกอินอยู่
                WHERE c.slug = %s
            )
            select * from all_quiz where video_id = %s
        """, (user_id, slug, video_id))
        
        video_row = cur.fetchone()

        if not video_row:
            abort(404)  # หรือ handle appropriately if no video found
        
        # Extract course ID and lesson ID from the fetched row
        course_id = video_row[0]
        lesson_id = video_row[11]  # ตรวจสอบให้แน่ใจว่า lesson_id ถูกต้อง
        quiz_limit = 15

        # Fetch lessons associated with this course
        cur.execute("SELECT l.lesson_id, l.lesson_name FROM lesson l WHERE l.course_id = %s", [course_id])
        lesson_names = cur.fetchall()

        lessons = []
        for lesson in lesson_names:
            current_lesson_id = lesson[0]
            # Fetch quizzes associated with each lesson
            cur.execute("""
                WITH latest_quiz_attempts AS (
                    SELECT 
                        quiz_id, 
                        MAX(attempt_id) AS latest_attempt_id
                    FROM quiz_attempts
                    WHERE user_id = %s -- ใส่ ID ของผู้ใช้ที่ล็อกอินอยู่
                    GROUP BY quiz_id
                ), lastest_video_attemts as (
                    SELECT 
                        video_id, 
                        MAX(attempt_id) AS latest_attempt_id
                    FROM video_attempts
                    WHERE user_id = %s -- ใส่ ID ของผู้ใช้ที่ล็อกอินอยู่
                    GROUP BY video_id
                )         
                SELECT 
                    q.quiz_id, q.quiz_name, qv.video_id, qv.title, qv.youtube_link, qv.description, 
                    qv.time_duration, qv.preview, qv.video_image, COUNT(que.question_id) AS question_count, 
                    COALESCE (qa.passed, va.passed , 0) AS passed
                FROM quiz_video qv
                LEFT JOIN question que ON qv.quiz_id = que.quiz_id
                LEFT JOIN quiz q ON q.quiz_id = qv.quiz_id
                LEFT JOIN (
                    SELECT qa.quiz_id, qa.passed
                    FROM quiz_attempts qa
                    JOIN latest_quiz_attempts lqa
                        on lqa.latest_attempt_id = qa.attempt_id
                ) qa ON q.quiz_id = qa.quiz_id
                LEFT JOIN (
                    select va.video_id, va.passed from video_attempts va
                    join lastest_video_attemts lva
                        on lva.latest_attempt_id = va.attempt_id
                ) as va on va.video_id = qv.video_id 
                WHERE qv.lesson_id = %s
                GROUP BY qv.video_id, qv.title, qv.youtube_link, qv.description, 
                        qv.time_duration, qv.preview, qv.video_image, q.quiz_id, q.quiz_name, qa.passed, va.passed;
            """, [user_id, user_id, current_lesson_id])

            quizzes = cur.fetchall()

            quizzes_data = [{
                'quiz_id': q[0], 
                'quiz_name': q[1], 
                'video_id': q[2], 
                'title': q[3], 
                'youtube_link': q[4], 
                'description': q[5], 
                'time_duration': q[6], 
                'preview': q[7], 
                'video_image': q[8], 
                'question_count': q[9] if q[9] < quiz_limit else quiz_limit, 
                'passed': q[10]} for q in quizzes]

            lesson_data = {
                'lesson_id': current_lesson_id,
                'lesson_name': lesson[1],
                'quizzes': quizzes_data
            }
            lessons.append(lesson_data)

        # Initialize course object if found, else None
        video = {
            'id': video_row[0],
            'title': video_row[1],
            'category_name': video_row[2],
            'slug': video_row[3],
            'video_id': video_row[4],
            'video_title': video_row[5],
            'youtube_link': video_row[6],
            'video_description': video_row[7],
            'time_duration': video_row[8],
            'video_image': video_row[9],
            'quiz_id': video_row[10],
            'lesson_id': video_row[11],  # ตรวจสอบให้แน่ใจว่า lesson_id ถูกต้อง
            'passed': video_row[14]
        }

        next_element = {
            'element_id': video_row[12],
            'element_type': video_row[13],
        } 

        questions_data = []  # Initialize an empty list
        
        if video_row[10]:  # Check if there's a quiz_id associated with the video
            # Fetch random questions for the quiz
            def random_questions(quiz_id, limit):
                cur.execute(""" 
                    SELECT q.question_id, q.quiz_id, q.score, qz.quiz_name, q.question_name, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer
                    FROM question q
                    JOIN quiz qz ON q.quiz_id = qz.quiz_id
                    WHERE q.quiz_id = %s
                    ORDER BY RAND()
                    LIMIT %s
                """, (quiz_id, limit))
                return cur.fetchall()

            questions = random_questions(video_row[10], 15)  # Adjust limit as needed

            questions_data = [
                {
                    'question_id': q[0], 
                    'quiz_id': q[1], 
                    'score': q[2], 
                    'quiz_name': q[3], 
                    'question_name': q[4], 
                    'choice_a': q[5], 
                    'choice_b': q[6], 
                    'choice_c': q[7], 
                    'choice_d': q[8], 
                    'correct_answer': q[9]
                } for q in questions
            ]

    except Exception as e:
        print(f"An error occurred: {e}")
        video = None
        lessons = []
        questions_data = []

    finally:
        cur.close()

    if 'last_visited_pages' not in session:
        session['last_visited_pages'] = {}
    session['last_visited_pages'][slug] = {'type': 'video', 'id': video_id}

    # Render the template with all necessary data
    return render_template('course/video.html', 
        video=video,
        lessons=lessons,
        questions=questions_data, 
        lesson_id=lesson_id,
        next_element=next_element
    )



def get_first_lesson(slug):
    cur = mysql.connection.cursor()
    query = """
        SELECT q.quiz_id, qv.video_id
        FROM quiz_video qv
        LEFT JOIN question que ON qv.quiz_id = que.quiz_id
        LEFT JOIN quiz q ON q.quiz_id = qv.quiz_id
        WHERE qv.lesson_id IN (
            SELECT lesson_id FROM lesson WHERE course_id = (
                SELECT id FROM courses WHERE slug = %s
            )
        )
        ORDER BY qv.lesson_id ASC
        LIMIT 1
    """
    cur.execute(query, (slug,))
    first_lesson = cur.fetchone()
    cur.close()
    return first_lesson




@app.route('/start_course/<slug>')
def start_course(slug):
    first_lesson = get_first_lesson(slug)
    if first_lesson:
        quiz_id = first_lesson[0]  # Assuming index 0 is quiz_id
        video_id = first_lesson[1]  # Assuming index 1 is video_id
        
        # Determine lesson_type based on available data or additional logic
        lesson_type = None
        if quiz_id:
            lesson_type = 'quiz'
        elif video_id:
            lesson_type = 'video'
        
        if lesson_type:
            # Set the learning status to True after the user starts learning
            session['learning_status'][slug] = True
            
            # Check if the lesson is a quiz or a video and redirect accordingly
            if lesson_type == 'quiz':
                return redirect(url_for('take_quiz', slug=slug, quiz_id=quiz_id))
            elif lesson_type == 'video':
                return redirect(url_for('watch_video', slug=slug, video_id=video_id))
    
    # If no valid lesson found or logic fails to determine lesson_type, redirect back to course detail page
    return redirect(url_for('course_details', slug=slug))








# สร้างลิงก์ URL สำหรับปุ่ม "CONTINUE"
@app.route('/continue_page/<slug>')
def continue_page(slug):
    last_visited_pages = session.get('last_visited_pages', {})
    last_visited_info = last_visited_pages.get(slug)
    if last_visited_info:
        if last_visited_info['type'] == 'video':
            return redirect(url_for('watch_video', slug=slug, video_id=last_visited_info['id']))
        elif last_visited_info['type'] == 'quiz':
            return redirect(url_for('take_quiz', slug=slug, quiz_id=last_visited_info['id']))
    return redirect(url_for('course_details', slug=slug))  # ใช้ชื่อฟังก์ชันที่ปรับใหม่





@app.route('/my-course')
def my_course():
    total_courses = 0  # Initialize total_courses with a default value
    
    try:
        # Assuming you have a way to get user_id of the currently logged in user
        user_id = current_user.id  # Replace with your logic to get user ID

        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT COUNT(*) 
            FROM courses c
            JOIN user_enroll ur ON c.id = ur.course_id
            WHERE ur.user_id = %s
        """, (user_id,))  # Total courses count
        total_courses = cur.fetchone()[0]

        # Execute SQL command to retrieve enrolled courses details for the current user
        cur.execute("""
            SELECT 
                c.id, 
                c.title, 
                c.description, 
                c.featured_image,
                c.featured_video,
                cat.name AS category_name,
                CONCAT(i.first_name, ' ', i.last_name) AS instructor_name, 
                i.instructorimage,
                c.language, 
                c.deadline, 
                c.certificate, 
                c.slug,
                qv.video_id,
                qv.quiz_id  
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
            JOIN instructor i ON c.instructor_id = i.id
            JOIN user_enroll ur ON c.id = ur.course_id
            LEFT JOIN quiz_video qv ON c.id = qv.video_id 
            WHERE ur.user_id = %s
        """, (user_id,))
        
        # Fetch all enrolled course results
        courses_rows = cur.fetchall()

        # Execute SQL command to retrieve all categories (if needed for filtering)
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories = cur.fetchall()

        cur.execute("""
            SELECT c.id, c.title, c.slug, cat.name as category_name
            FROM courses c
            JOIN categories cat ON c.category_id = cat.id
        """)
        all_courses = cur.fetchall()

        cur.execute("SELECT userimage FROM user WHERE id = %s", (current_user.id,))
        user_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/user.png"

        cur.execute("SELECT adminimage FROM admin WHERE id = %s", (current_user.id,))
        admin_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img/avatars/admin.png"

        cur.execute("SELECT instructorimage FROM instructor WHERE id = %s", (current_user.id,))
        instructor_image_url = cur.fetchone()[0] if cur.rowcount > 0 else "/static/img//avatars/instructor.png"

    except Exception as e:
        print(f"An error occurred: {e}")
        courses_rows = None
        categories = []
        all_courses = []

    finally:
        # Make sure to close cursor if it's been opened
        if 'cur' in locals() or 'cur' in globals():
            cur.close()

    # Create Course objects for each row
    course = [
        Course(
            id=row[0],
            title=row[1],
            description=row[2],
            featured_image=row[3],
            featured_video=row[4],
            category_name=row[5],
            instructor_name=row[6],
            instructor_image=row[7],
            language=row[8],
            deadline=row[9],
            certificate=row[10],
            slug=row[11],
            video_id=row[12],
            quiz_id=row[13]
        ) for row in courses_rows
    ]

    # Convert categories to a list of dictionaries for easier template rendering
    categories = [
        {
            'id': row[0], 
            'icon': row[1],  # Make sure to include 'icon' field from database
            'name': row[2]
        } for row in categories
    ]

    courses = [{'id': row[0], 'title': row[1], 'slug': row[2], 'category_name': row[3]} for row in all_courses]

    # Render the template with the retrieved courses and categories
    return render_template('course/my-course.html', total_courses=total_courses, courses=courses, categories=categories, course=course, user_image_url=user_image_url, admin_image_url=admin_image_url, instructor_image_url=instructor_image_url)







@app.route('/search')
def search_course():
    try:
        # Create cursor object to execute SQL commands
        cur = mysql.connection.cursor()
        
        query = request.args.get('query')
        cur.execute("SELECT * FROM courses WHERE title LIKE %s", ('%' + query + '%',))

        # Fetch all course results
        courses = cur.fetchall()

        # Execute SQL command to retrieve category details
        cur.execute("SELECT id, icon, name FROM categories")
        
        # Fetch all category results
        categories = cur.fetchall()

    except Exception as e:
        print(f"An error occurred: {e}")
        courses = []
        categories = []

    finally:
        # Close cursor
        cur.close()

    # Convert courses to a list of dictionaries for easier template rendering
    courses_list = []
    for row in courses:
        course_dict = {
            'id': row[0], 
            'title': row[1], 
            'category': {'name': row[2]},  # Adjust based on your schema
            # Add more fields as needed
        }
        courses_list.append(course_dict)

    # Convert categories to a list of dictionaries for easier template rendering
    categories_list = [
        {
            'id': row[0], 
            'icon': row[1], 
            'name': row[2]
        } for row in categories
    ]

    # Render the template with the context
    return render_template('search/search.html', courses=courses_list, categories=categories_list)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404



def truncatewords_filter(s, length):
    words = s.split()
    if len(words) > length:
        words = words[:length]
        words.append('...')
    return ' '.join(words)

# Assuming you have an environment set up, add the filter to it
env = Environment()
env.filters['truncatewords'] = truncatewords_filter

if __name__ == "__main__":
    app.run(debug=True)
