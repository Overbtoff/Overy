import cx_Oracle

conn = cx_Oracle.connect("PYUSER", "123456")
cursor = conn.cursor()