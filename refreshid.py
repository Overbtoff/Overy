from dbconn import conn,cursor
def newid():
    sql=""" select max(graduation_id) from graduation"""
    cursor.execute(sql)
    data = cursor.fetchall()
    data=data[0][0]
    data=str(int(data)+1)
    data=data.zfill(10)
    print(data)
    return data

if __name__ == '__main__':
    newid()