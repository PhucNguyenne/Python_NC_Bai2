import psycopg2
from psycopg2 import sql

class DbConn:
    def __init__(self, database="student_management", table="students", user="postgres", password="123456789", host="localhost", port="5432"):
        self.database = database
        self.table = table  
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except Exception as ex:
            print(f"Error connecting to database: {ex}")
            raise ex
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def check_student_exists(self, mssv):
        query = sql.SQL("SELECT * FROM {table} WHERE mssv = %s").format(
            table=sql.Identifier(self.table)
        )
        self.cur.execute(query, (mssv,))
        return self.cur.fetchone() is not None

    def select(self, columns=None, **conditions):
        if columns is None:
            columns = ['*']
        columns_str = ', '.join(columns)
        query = f'SELECT {columns_str} FROM "{self.table}"'
        if conditions:
            condition_clauses = [f'"{key}" = %s' for key in conditions.keys()]
            query += ' WHERE ' + ' AND '.join(condition_clauses)
        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(conditions.values()))
            return cursor.fetchall()

    def insert(self, **kwargs):
        mssv = kwargs.get('mssv')
        if mssv and self.check_student_exists(mssv):
            print(f"Sinh viên với MSSV {mssv} đã tồn tại.")
            return False
        
        try:
            columns = kwargs.keys()
            values = kwargs.values()
            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
                table=sql.Identifier(self.table),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            self.cur.execute(query, tuple(values))
            self.conn.commit()
            print("Insert thành công")
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error during insert: {ex}")
            return False

    def update(self, update_data, **conditions):
        if not conditions:
            raise ValueError("No conditions provided for update.")
        
        mssv = conditions.get('mssv')
        if mssv and not self.check_student_exists(mssv):
            print(f"Sinh viên với MSSV {mssv} không tồn tại.")
            return False

        updates = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in update_data.keys()]
        conds = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in conditions.keys()]

        query = sql.SQL("UPDATE {table} SET {updates} WHERE {conds}").format(
            table=sql.Identifier(self.table),
            updates=sql.SQL(", ").join(updates),
            conds=sql.SQL(" AND ").join(conds)
        )

        try:
            self.cur.execute(query, tuple(update_data.values()) + tuple(conditions.values()))
            self.conn.commit()
            print("Update thành công")
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error during update: {ex}")
            return False

    def delete(self, **conditions):
        if not conditions:
            raise ValueError("No conditions provided for deletion.")

        mssv = conditions.get('mssv')
        if mssv and not self.check_student_exists(mssv):
            print(f"Sinh viên với MSSV {mssv} không tồn tại.")
            return False

        conds = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in conditions.keys()]
        query = sql.SQL("DELETE FROM {table} WHERE {conds}").format(
            table=sql.Identifier(self.table),
            conds=sql.SQL(" AND ").join(conds)
        )
        self.cur.execute(query, tuple(conditions.values()))
        self.conn.commit()
        print("Delete thành công")
        return True

    def check_login(self, username, password):
        query = sql.SQL("SELECT * FROM users WHERE username = %s AND password = %s")
        try:
            self.cur.execute(query, (username, password))
            user = self.cur.fetchone()
            if user:
                print("Login thành công")
                return True
            else:
                print("Sai tên đăng nhập hoặc mật khẩu")
                return False
        except Exception as ex:
            print(f"Error during login: {ex}")
            return False
