import sqlite3

# Kiểm tra username đã nhập để đăng ký có tồn tại hay chưa
def checkUserAccount(username):
	conn = sqlite3.connect('userAccount.db')
	cur = conn.cursor()

	cur.execute("""SELECT count(name) FROM sqlite_master\
		WHERE type = 'table' AND name = 'Accounts' """)
	if cur.fetchone()[0] == 0:
		cur.execute("""CREATE TABLE Accounts(username, password)""")

	cur.execute("SELECT * FROM Accounts")
	List = cur.fetchall()
	
	if List:
		for user in List:
			if user[0] == username:		# Nếu userName đã tồn tại
				conn.close()
				return True

	conn.close()
	return False

#-----------------------------------------------------
# Hàm kiểm tra username và password có nằm trong database hay chưa
def isValidAccount(username, password):
	conn = sqlite3.connect('userAccount.db')
	cur = conn.cursor()

	cur.execute("""SELECT count(name) FROM sqlite_master\
		WHERE type = 'table' AND name = 'Accounts' """)
	if cur.fetchone()[0] == 0:
		cur.execute("""CREATE TABLE Accounts(username, password)""")

	cur.execute("SELECT * FROM Accounts")
	List = cur.fetchall()
	if List:
		for user in List:
			if user[0] == username:
				if user[1] == password:
					conn.close()
					return 0			# Trả về 0, đăng nhập thành công
				else:
					conn.close()
					return 1			# Trả về 1, mật khẩu không đúng

	conn.close()
	return 2			# Trả về 2, tên đăng nhập không tồn tại