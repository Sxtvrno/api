from app import app
from flaskext.mysql import MySQL


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'Admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ACdKteSWBPK@JSTh'
app.config['MYSQL_DATABASE_DB'] = 'ferremas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)