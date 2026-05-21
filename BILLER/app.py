from flask import Flask, request, redirect, render_template_string, session
from markupsafe import escape
import secrets

app = Flask(__name__)

# Secure secret key
app.secret_key = secrets.token_hex(32)

# Product storage
products = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BILLER</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body{
            font-family: Arial;
            background:#0f0f0f;
            color:white;
            text-align:center;
            margin:20px;
        }

        h1{
            color:cyan;
        }

        input{
            padding:10px;
            margin:5px;
            border:none;
            border-radius:6px;
            width:180px;
        }

        button{
            padding:10px 20px;
            background:cyan;
            border:none;
            border-radius:6px;
            font-weight:bold;
            cursor:pointer;
        }

        button:hover{
            background:white;
        }

        table{
            width:95%;
            margin:auto;
            border-collapse:collapse;
            margin-top:20px;
        }

        th, td{
            border:1px solid gray;
            padding:10px;
        }

        th{
            background:cyan;
            color:black;
        }

        .total{
            margin-top:20px;
            font-size:25px;
            color:lime;
        }

        .footer{
            margin-top:30px;
            color:gray;
        }
    </style>
</head>

<body>

<h1>⚡ BILLER</h1>

<form method="POST" autocomplete="off">

    <input
        type="text"
        name="name"
        placeholder="Product Name"
        maxlength="50"
        required
    >

    <input
        type="number"
        name="price"
        placeholder="Price"
        min="1"
        max="100000"
        required
    >

    <input
        type="number"
        name="qty"
        placeholder="Quantity"
        min="1"
        max="1000"
        required
    >

    <button type="submit">Add Product</button>

</form>

<table>

<tr>
    <th>Product</th>
    <th>Price</th>
    <th>Quantity</th>
    <th>Total</th>
</tr>

{% for p in products %}
<tr>
    <td>{{ p[0] }}</td>
    <td>₹{{ p[1] }}</td>
    <td>{{ p[2] }}</td>
    <td>₹{{ p[3] }}</td>
</tr>
{% endfor %}

</table>

<div class="total">
    Grand Total: ₹{{ grand_total }}
</div>

<div class="footer">
    Secure Billing Website
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:
        session["user"] = "shopkeeper"

    if request.method == "POST":

        try:
            # Secure inputs
            name = escape(request.form.get("name"))

            price = int(request.form.get("price"))
            qty = int(request.form.get("qty"))

            # Validation
            if price <= 0 or qty <= 0:
                return redirect("/")

            total = price * qty

            products.append((name, price, qty, total))

        except:
            return redirect("/")

        return redirect("/")

    grand_total = sum(p[3] for p in products)

    return render_template_string(
        HTML,
        products=products,
        grand_total=grand_total
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
