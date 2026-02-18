from flask import Flask,request,redirect,url_for,render_template,make_response
from datetime import datetime
app=Flask(__name__)
customers={}
orders={}
prices={'Biryani':250,'Vada Pav':100,'Butter Chicken':200,'Idli':50,'Dal Makhani':20,'Lassi':50,'Chicken Friedrice':100}
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    error = None

    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        phno=request.form['phno']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if password==confirm_password:
            if username not in customers:
                customers[username]={'name':username,'Email':email,'Phno':phno,'Password':password}
                return redirect(url_for('login'))
            else:
                error = '❌username already exists'
        else:
            error = '❌ Password doesnot match to conform password'    
   
    return render_template('register.html',error=error)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None   # default

    if request.method == 'POST':
        login_username = request.form['username']
        login_password = request.form['password']

        if login_username in customers:
            register_password = customers[login_username]['Password']
            if login_password == register_password:
                cookie = make_response(redirect(url_for('dashboard')))
                cookie.set_cookie('username', login_username)
                return cookie
            else:
                error = "❌ Incorrect password"
        else:
            error = "❌ Username does not exist"

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if request.cookies.get('username'):
        username=request.cookies.get('username')
        return render_template('dashboard.html',username=username)
@app.route('/food orders',methods=['GET','POST'])    
def food_order():
    username = request.cookies.get('username')

    if not username or username not in customers:
        return redirect(url_for('login'))
    if request.method=='POST':
        customer_name=request.form['name']
        phno=request.form['phno']
        # Address=request.form['Address']
        item=request.form['item']
        quantity=int(request.form['quantity'])
        if customer_name not in orders:
            date=datetime.now().strftime("%d-%m-%Y")
            time=datetime.now().strftime("%H:%M:%S")
            if item in prices:
                price=int(prices[item])*int(quantity)
                orders[customer_name]={'Customer_name':customer_name,'Item':[],'Quantity':[],'phno':phno,'total_price':price,'date':date,'time':time,'order_status':'Successful','pay_information':'Successful'}
                orders[customer_name]['Item'].append(item)
                orders[customer_name]['Quantity'].append(quantity)
                return redirect(url_for('view_orders'))

            else:
                return 'Order is not available'
        else:
            orders[customer_name]['Quantity'].append(quantity)
            orders[customer_name]['Item'].append(item)
            orders[customer_name]['total_price']+=int(prices[item])
            return redirect(url_for('view_orders'))
    return render_template('food_order.html')
@app.route('/view_orders')
def view_orders():
    return render_template('view_orders.html',orders=orders)

@app.route('/update_order_info',methods=['GET','POST'])
def update_order_info():
    username = request.cookies.get('username')
    order = None

    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        order = orders.get(customer_name)

    return render_template("update_order_info.html", order=order,username=username)
@app.route('/delete_order', methods=['GET', 'POST'])
def delete_order():
    message = None

    if request.method == 'POST':
        customer_name = request.form['customer_name']

        if customer_name in orders:
            del orders[customer_name]
            message = "✅ Order deleted successfully"
        else:
            message = "❌ Customer has not ordered yet"

    return render_template('delete_order.html', message=message)

@app.route('/logout',methods=['GET','POST'])
def logout():
    error=None
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        if username in customers:
           resp = make_response(redirect(url_for('login')))
           resp.delete_cookie('username')
           return resp
        else:
            error= '❌ First login to logout'
    return render_template('logout.html',error=error)
@app.route('/delete Account',methods=['GET','POST'])
def delete_account():
    if request.method=='POST':
            username=request.cookies.get('username')
            if username in customers:
                customers.pop(username)
                resp=make_response(redirect(url_for('welcome')))
                resp.delete_cookie('username')
                return resp
            else:
                return 'please login to delete account'
    return render_template('delete_account.html')    

app.run(debug=True,use_reloader=True)