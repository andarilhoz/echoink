from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/glitch')
def glitch():
    return "Modo glitch ativado (simulado)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
