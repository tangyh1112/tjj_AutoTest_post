import pymysql
import readConfig as readConfig
# from Public.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

class MyDB:
    def __init__(self):
        global host, username, password, port, config, hosts
        host = localReadConfig.get_db("host")
        username = localReadConfig.get_db("username")
        password = localReadConfig.get_db("password")
        port = localReadConfig.get_db("port")
        self.db = None
        self.cursor = None

    def connectDB(self, database):
        try:
            # connect to DB
            self.db = pymysql.connect(host=str(host), user=username, password=password, db=database, port=int(port))
            # create cursor
            self.cursor = self.db.cursor()
        except ConnectionError as ex:
            raise ex

    def executeSQL(self, sql, params="", database=""):
        self.connectDB(database)
        try:
            self.cursor.execute(sql, params)
            print("sql="+sql+"params="+str(params))
            results = self.cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    sqlResult = row[0]
            else:
                sqlResult = ""
                # 提交到数据库执行
                self.db.commit()
        except Exception as e:
            raise e
        finally:
            self.db.close()  # 关闭连接
        return sqlResult