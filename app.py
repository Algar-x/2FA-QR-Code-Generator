from flask import Flask, render_template, request
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)

# Guardamos el secreto aquí de forma temporal (en una app real usaríamos sesión o base de datos)
temp_secret = pyotp.random_base32()

@app.route("/", methods=["GET", "POST"])
def index():
    global temp_secret
    message = None

    uri = pyotp.totp.TOTP(temp_secret).provisioning_uri(name="usuario@ejemplo.com", issuer_name="MiAppSegura")
    qr = qrcode.make(uri)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if request.method == "POST":
        user_code = request.form.get("code")
        totp = pyotp.TOTP(temp_secret)
        if totp.verify(user_code):
            message = "✅ Código válido"
        else:
            message = "❌ Código inválido"

    return render_template("index.html", qr_code=img_str, message=message)

if __name__ == "__main__":
    app.run(debug=True)