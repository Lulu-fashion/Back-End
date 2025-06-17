from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Replace with your real credentials
BUSINESS_EMAIL = os.getenv("BUSINESS_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    user = data.get("user", {})
    product = data.get("product", {})

    if not user or not product:
        return jsonify({"success": False, "error": "Missing data"}), 400

    try:
        yag = yagmail.SMTP(BUSINESS_EMAIL, APP_PASSWORD)

        # ✅ 1. Email to business
        business_message = f"""
🧾 NEW ORDER RECEIVED:

PRODUCT:
- Name: {product.get('name')}
- Code: {product.get('code')}
- Price: ₹{product.get('price')}

USER INFO:
- Name: {user.get('name')}
- Address: {user.get('address')}
- Phone: {user.get('phone')}
- Pincode: {user.get('pincode')}
- Email: {user.get('email')}
"""
        yag.send(
            to=BUSINESS_EMAIL,
            subject="📦 New Order - Lulu Fashion",
            contents=business_message
        )

        # ✅ 2. Fancy confirmation email to customer
        user_html = f"""
        <h1 style="font-family: 'Times New Roman'; color:black;>LULU FASHION</h1>
        <div style="font-family: 'Times New Roman', sans-serif; padding: 20px; border: 1px solid #eee;">
          <h2 style="color:#333;">🛍️ Thanks for your order, {user.get('name')}!</h2>
          <p>We received your order and are preparing it for shipping.</p>
          <h3 style="color:#555;">Your Order:</h3>
          <ul>
            <li><strong>Product:</strong> {product.get('name')}</li>
            <li><strong>Price:</strong> ₹{product.get('price')}</li>
          </ul>
          <h3 style="color:#555;">Delivery Details:</h3>
          <p>
            {user.get('address')}<br>
            Phone: {user.get('phone')}<br>
            Pincode: {user.get('pincode')}
          </p>
          <hr>
          <p style="color:gray;">You’ll receive another email when it ships. ❤️<br>
          – Lulu Fashion Team</p>
        </div>
        """

        yag.send(
            to=user.get("email"),
            subject="🧾 Order Confirmation – Lulu Fashion",
            contents=user_html
        )

        return jsonify({"success": True})

    except Exception as e:
        print("Email sending failed:", e)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
