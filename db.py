import oracledb

user = "system"
pw = "1234"
host = "localhost:1521/xe"

def connect():
    conn = oracledb.connect(
            user= user,
            password= pw,
            dsn=host,
        )
    print("접속완료")
    return conn

