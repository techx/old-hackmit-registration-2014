from flask import Flask

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.prod.ProductionConfig')
@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
