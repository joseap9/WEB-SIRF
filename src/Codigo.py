from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("Pricipal.html")

@app.route('/Registro')
def Registro():
    return render_template("Registro.html")

@app.route('/Lista')
def Listado():
    return render_template("Listado.html")

@app.route('/Dashboard')
def datos():
    return render_template("Dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)