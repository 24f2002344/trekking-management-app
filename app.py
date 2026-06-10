from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['secret_key']='secret_key_for_my_project'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "home."

if __name__ =='__main__':
    app.run(debug=True)