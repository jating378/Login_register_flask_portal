from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary to store registered user data.
registered_users = {}


@app.route('/')
def dashboard():
    return render_template('dashboard.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.form.get('username', '').lower()
        password = request.form.get('password', '')

        if username in registered_users:
            stored_password = registered_users[username]['password']
            if password == stored_password:
                message = 'Login successful'
            else:
                message = 'Login failed. Please check your credentials.'
        else:
            message = 'Username not found. Please register first.'

    return render_template('login.html', message=message, username=username, password=password)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message=""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        confirm_pass = request.form.get('confirm password','')
        email = request.form.get('email', '')

        if username in registered_users:
            message = 'Username already taken. Please choose a different one.'
        elif email in registered_users:
            message = "Email already registered , please try again"
        elif confirm_pass != password:
            message = "password dont match try again"
        else:
            # Store the user data in the 'user_data.txt' file
            user_data = f"Username: {username}, Password: {password}, Email: {email}\n"

            with open('user_data.txt', 'a') as file:
                file.write(user_data)

            # Update the registered_users dictionary with the new user
            registered_users[username] = {'password': password, 'email': email}

            message = 'Registration successful. You can now login.'

    return render_template('register.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)

