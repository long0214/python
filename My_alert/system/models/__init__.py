from system import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/Malert'
app.config['SQLALCHEMY_POOL_SIZE'] = 100
db = SQLAlchemy(app)
