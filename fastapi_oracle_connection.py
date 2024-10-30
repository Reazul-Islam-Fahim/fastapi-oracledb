import oracledb


usrname = "fahim"
password = "123"
dsn = "192.168.2.106:1521/XEPDB1"

connection = oracledb.connect(user= usrname, password= password, dsn= dsn)