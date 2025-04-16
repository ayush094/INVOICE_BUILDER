from flask import Flask, render_template, request
from db import get_connection
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        items = []
        total = 0

        products = request.form.getlist('product')
        qtys = request.form.getlist('qty')
        prices = request.form.getlist('price')

        for i in range(len(products)):
            pname = products[i]
            qty = int(qtys[i])
            price = float(prices[i])
            t = qty * price
            total += t
            items.append({'product': pname, 'qty': qty, 'price': price, 'total': t})
            

        conn = get_connection()
        cursor = conn.cursor()  

        cursor.execute("INSERT INTO invoices (customer_name, address, phone, total, date) VALUES (%s, %s, %s, %s, %s)",(name, address, phone, total, datetime.datetime.now()))
        invoice_id = cursor.lastrowid 

        for item in items:
            cursor.execute("INSERT INTO invoice_items (invoice_id, product_name, qty, price, total) VALUES (%s, %s, %s, %s, %s)", (invoice_id, item['product'], item['qty'], item['price'], item['total']))

        conn.commit()
        cursor.close()
        conn.close()
        

        return render_template("invoice.html", name=name, address=address, phone=phone, items=items, total=total, date=datetime.datetime.now())

    return render_template("invoice_form.html")

if __name__ == '__main__':
    app.run(debug=True)
