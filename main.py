#Window Position Center
import sys
import mysql.connector
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QStackedWidget, QTableWidget, QWidget
import random
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
auth = None
#MainScreen
class MainScreen(QDialog):

    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi('ui/fone.ui', self)
        self.login.clicked.connect(self.go_to_login)
        self.reg.clicked.connect(self.go_to_register)
        self.donate.clicked.connect(self.go_to_donate)
        self.browse.clicked.connect(self.go_to_browse)
        self.about.clicked.connect(self.go_to_about)
        self.connect.clicked.connect(self.go_to_connect)
        self.random_fact()

    def random_fact(self):
        #Displays random fact
        f = open("randm.txt", "r",  encoding="utf8")
        lines = f.readlines()
        length = len(lines)
        rand = random.randint(0, length - 1)
        self.fact.setText(lines[rand])
        f.close

    def back_function(self):
        if auth == True:
            mains = MsTrueLogin()
            widget.addWidget(mains)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            mains = MainScreen()
            widget.addWidget(mains)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_login(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_register(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_donate(self):
        donate = DonateScreen()
        widget.addWidget(donate)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def go_to_browse(self):
        browse = BrowseScreen()
        widget.addWidget(browse)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_about(self):
        about = AboutScreen()
        widget.addWidget(about)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_connect(self):
        connectf = ConnectScreen()
        widget.addWidget(connectf)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_er(self):
        er = ErScreen()
        widget.addWidget(er)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#MainScreen After Authentication
class MsTrueLogin(QDialog):

    def __init__(self):
        super(MsTrueLogin, self).__init__()
        loadUi('ui/fone1.ui', self)
        self.greet.setText('Hello' + ' ' + username + '!')
        self.logout.clicked.connect(self.logout_func)
        self.info.clicked.connect(self.go_to_myinfo)
        self.donate.clicked.connect(MainScreen.go_to_donate)
        self.browse.clicked.connect(MainScreen.go_to_browse)
        self.about.clicked.connect(MainScreen.go_to_about)
        self.connect.clicked.connect(MainScreen.go_to_connect)
        self.random_fact()

    #Displays a random fact
    def random_fact(self):
        f = open("randm.txt", "r",  encoding="utf8")
        lines = f.readlines()
        length = len(lines)
        rand = random.randint(0, length - 1)
        self.fact.setText(lines[rand])
        f.close  

    def logout_func(self):
        global auth
        auth = False
        mains = MainScreen()
        widget.addWidget(mains)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        print('Successfully Logged Out')

    def go_to_myinfo(self):
        milogin = MiTrueLogin()
        widget.addWidget(milogin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#Login Screen
class LoginScreen(QDialog):
    
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('ui/login.ui', self)
        self.log.clicked.connect(self.login_func)
        self.acc.clicked.connect(MainScreen.go_to_register)
        self.back.clicked.connect(MainScreen.back_function)

    def login_func(self):
        global username
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username) == 0 or len(password) == 0:
            self.incorrect.setText('       Empty Field(s)')
        else:
            try:
                connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
                mycursor = connection.cursor()
                query = 'SELECT password FROM login WHERE username = %s'
                mycursor.execute(query, (username,))
                result = mycursor.fetchone()
                if result is not None:
                    result_pass = result[0]
                    if result_pass == password:
                        print('Successfully Logged In')
                        self.incorrect.setText('')
                        self.correct.setText('           Logged in')

                        global auth
                        auth = True

                        if auth == True:
                            mains = MsTrueLogin()
                            widget.addWidget(mains)
                            widget.setCurrentIndex(widget.currentIndex() + 1)

                    else:
                        self.incorrect.setText('Incorrect Credentials')
                else:
                    self.incorrect.setText('Incorrect Credentials')
            except Exception as e:
                print(e)
                self.incorrect.setText('Incorrect Credentials')
#RegisterScreen
class RegisterScreen(QDialog):

    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi('ui/register.ui', self)
        self.regis.clicked.connect(self.register_func)
        self.log.clicked.connect(MainScreen.go_to_login)
        self.back.clicked.connect(MainScreen.back_function)

    def register_func(self):
        global username
        username = self.usern.text()
        password = self.password.text()
        conpassword = self.conpassword.text()

        if len(username) == 0 or len(password) == 0 or len(conpassword) == 0:
            self.incorrect.setText('          Empty Field(s)')

        elif password != conpassword:
            self.incorrect.setText('Passwords Do Not Match')

        else:
            try:
                connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
                mycursor = connection.cursor()
                userdetails = [username, password]
                # %s is a parameter marker
                mycursor.execute('INSERT INTO login (username, password) VALUES (%s, %s)', userdetails)
                connection.commit()
                connection.close()
                self.correct.setText('  Account Registered')

                print('Registered Successfully')

                myinfo = MyInfo()
                widget.addWidget(myinfo)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            except Exception as e:
                print(e)
                self.incorrect.setText('        Username Exists')

class MyInfo(QDialog):
    
    def __init__(self):
        super(MyInfo, self).__init__()
        loadUi('ui/myinfo.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.browse.clicked.connect(self.change_img)
        self.submit.clicked.connect(self.push_details)
        global path
        path = 'C:/Users/ARYA/Desktop/CoSc/College/S4/DBMS/DBMS Project/Images/user2.png'

    def change_img(self):
        try:
            display_picture = QFileDialog.getOpenFileName(self, 'Open File', 'C:/Users/ARYA/Desktop/CoSc/College/S4/DBMS/DBMS Project/Images', 'Images (*.png *.jpg *.jpeg *.webp *.xmp)')
            global path
            path = display_picture[0]
            changeimage = [path, username]
            connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
            mycursor = connection.cursor()
            mycursor.execute('UPDATE userinfo SET dp = %s WHERE username = %s', changeimage)
            connection.commit()
            connection.close()
            global image
            image = QPixmap(path)
            self.userimg.setPixmap(image)
        
        except Exception as e:
            print(e)
            path = 'C:/Users/ARYA/Desktop/CoSc/College/S4/DBMS/DBMS Project/Images/user2.png'
    
    def push_details(self):
        firstname = self.firstname.text()
        lastname = self.lastname.text()
        email = self.email.text()
        
        if firstname == '' or lastname == '' or email == '':
            self.label.setText('')
            self.details.setText(' Incomplete Data')

        else:
            try:
                connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
                mycursor = connection.cursor()
                placeholder_img = path
                details = [placeholder_img, username, firstname, lastname, email]
                mycursor.execute('INSERT INTO userinfo (dp, username, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)', details)
                connection.commit()
                connection.close()
                self.label.setText('   Details Updated')
                # self.details.setText('')
                self.firstname.setText('')
                self.lastname.setText('')
                self.email.setText('')

            except Exception as e:
                print(e)
                self.details.setText('                  Error!')
#MyInfo after login
class MiTrueLogin(QDialog):
    
    def __init__(self):
        super(MiTrueLogin, self).__init__()
        loadUi('ui/myinfo1.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.browse.clicked.connect(self.change_img)
        self.delacc.clicked.connect(self.go_to_dts)
        self.update.clicked.connect(self.update_info)
        connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
        mycursor = connection.cursor()
        
        usern = [username,]
        mycursor.execute('SELECT dp FROM userinfo WHERE username = %s', usern)
        
        result = mycursor.fetchone()
        if result is not None:
            result = result[0]
        else:
            # Handle the case where no rows are fetched
            print("No rows fetched from the database")

        print(result)
        image = QPixmap(result)
        self.userimg.setPixmap(image)
        
        query = 'SELECT * FROM userinfo where username = %s', usern
        mycursor.execute('SELECT * FROM userinfo where username = %s', usern)
        display_details = mycursor.fetchone()
        print(display_details)

        self.firstname.setText(display_details[2])
        self.lastname.setText(display_details[3])
        self.email.setText(display_details[4])

        connection.close()

    def change_img(self):
        try:
            display_picture = QFileDialog.getOpenFileName(self, 'Open File', 'C:/Users/ARYA/Desktop/CoSc/College/S4/DBMS/DBMS Project/Images', 'Images (*.png *.jpg *.jpeg *.webp *.xmp)')
            global path
            path = display_picture[0]
            changeimage = [path, username]
            connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
            mycursor = connection.cursor()
            mycursor.execute('UPDATE userinfo SET dp = %s WHERE username = %s', changeimage)
            connection.commit()
            connection.close()
            global image
            image = QPixmap(path)
            self.userimg.setPixmap(image)
        except Exception as e:
            print(e)
            path = 'C:/Users/ARYA/Desktop/CoSc/College/S4/DBMS/DBMS Project/Images/user2.png'

    def go_to_dts(self):
        dltscreen = DeleteScreen()
        widget.addWidget(dltscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def update_info(self):

        firstname = self.firstname.text()
        lastname = self.lastname.text()
        email = self.email.text()
        details = [firstname, lastname, email, username]

        connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
        mycursor = connection.cursor()
        mycursor.execute('UPDATE userinfo SET first_name = %s, last_name = %s, email = %s WHERE username = %s', details)
        print('Details Updated')
        self.details.setText('   Details Updated')
        connection.commit()
        connection.close()


#DeleteScreen
class DeleteScreen(QDialog):
    
    def __init__(self):
        super(DeleteScreen, self).__init__()
        loadUi('ui/delete.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.deluser.clicked.connect(self.delete_user)

    def delete_user(self):
        self.correct.setText('')
        username = self.usern.text()
        password = self.password.text()
        conpassword = self.conpassword.text()
        if username == '' or password == '' or conpassword == '':
            self.incorrect.setText('Incomplete Data')
        else:
            try:
                self.incorrect.setText('')
                self.correct.setText('')
                connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
                mycursor = connection.cursor()
                
                # Check if the user exists and password matches
                query = "SELECT password FROM login WHERE username = %s"
                mycursor.execute(query, (username,))
                result_pass = mycursor.fetchone()
                
                if result_pass is not None and result_pass[0] == password == conpassword:
                    # Delete associated rows from userinfo table
                    delete_query = "DELETE FROM userinfo WHERE username = %s"
                    mycursor.execute(delete_query, (username,))
                    
                    # Now, delete the user from login table
                    delete_query = "DELETE FROM login WHERE username = %s"
                    mycursor.execute(delete_query, (username,))
                    
                    connection.commit()
                    connection.close()
                    self.usern.setText('')
                    self.password.setText('')
                    self.conpassword.setText('')
                    self.correct.setText('User Deleted')
                    global auth
                    auth = False
                else:
                    self.incorrect.setText('Incorrect Credentials')
            except Exception as e:
                print(e)
                self.incorrect.setText('User Not Found!')

#DonateScreen
class DonateScreen(QDialog):

    def __init__(self):
        super(DonateScreen, self).__init__()
        loadUi('ui/donate.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.browse.clicked.connect(self.open_img)
        self.submit.clicked.connect(self.donate_item)

    def open_img(self):
        filepath = QFileDialog.getOpenFileName(self, 'Open File', 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads', 'Images (*.png *.jpg *.jpeg *.webp *.xmp)')
        self.imgpath.setText(filepath[0])
    
    def donate_item(self):
        imgpath = self.imgpath.text()
        item = self.item.text()
        contact = self.contact.text()
        loctn = self.loctn.text()
        
        if item == '' or contact == '' or loctn == '' or imgpath == '':
            self.success.setText('')
            self.error.setText('Incomplete Data')

        else:
            try:
                self.error.setText('')
                connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
                mycursor = connection.cursor()
                itemdetails = [imgpath, item, contact, loctn]
                mycursor.execute('INSERT INTO donate_items (img, item, contact, location) VALUES (load_file(%s), %s, %s, %s)', itemdetails)
                connection.commit()
                connection.close()
                self.error.setText('')
                self.success.setText('Item Uploaded')
                print('Item Uploaded Successfully')
                self.imgpath.setText('')
                self.item.setText('')
                self.contact.setText('')
                self.loctn.setText('')

            except Exception as e:
                print(e)
                self.success.setText('')
                self.error.setText('          Error!')

#BrowseScreen
class BrowseScreen(QDialog):

    def __init__(self):
        super(BrowseScreen, self).__init__()
        loadUi('ui/browse.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.tableWidget.setHorizontalHeaderLabels(['Sr No.', 'Image', 'Item', 'Contact', 'Location'])
        # stylesheet = "::section{Background-color:rgba(190,1,1);border-style:solid;}"
        # self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        # self.tableWidget.verticalHeader().setStyleSheet(stylesheet)

        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 600)
        self.tableWidget.setColumnWidth(4, 250)
        self.load_table_data()

    def load_table_data(self):
        connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
        mycursor = connection.cursor()
        query = 'SELECT * FROM donate_items'
        mycursor.execute(query)
        result = mycursor.fetchall()
            
        for row_num, row_data in enumerate(result):
            self.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = str(col_data);
                if col_num == 1:
                    item = self.gen_img_label(col_data)
                    self.tableWidget.setCellWidget(row_num, col_num, item)
                    
                else:
                    self.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(item))
        
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        #The below line enables readonly mode like functionality
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
    def gen_img_label(self, image):
        img_label = QtWidgets.QLabel(self.imgwid)
        img_label.setText('')
        img_label.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'jpg')
        img_label.setPixmap(pixmap)
        return img_label

#AboutScreen
class AboutScreen(QDialog):

    def __init__(self):
        super(AboutScreen, self).__init__()
        loadUi('ui/about.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.er.clicked.connect(MainScreen.go_to_er)


class ConnectScreen(QDialog):
    
    def __init__(self):
        super(ConnectScreen, self).__init__()
        loadUi('ui/connect.ui', self)
        self.back.clicked.connect(MainScreen.back_function)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'State', 'Address', 'Contact No.', 'Email'])
        # stylesheet = "::section{Background-color:rgba(190,1,1);border-style:solid;}"
        # self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        # self.tableWidget.verticalHeader().setStyleSheet(stylesheet)

        self.tableWidget.setColumnWidth(0, 450)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 1000)
        self.tableWidget.setColumnWidth(3, 135)
        self.tableWidget.setColumnWidth(4, 320)
        self.load_table_data()

    def load_table_data(self):
        connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("SQL_KEY"), database=os.getenv("DATABASE"))
        mycursor = connection.cursor()
        query = 'SELECT * FROM ngolist'
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        self.tableWidget.setRowCount(13)
        trowindex = 0
        
        for row in result:
            self.tableWidget.setItem(trowindex, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(trowindex, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(trowindex, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(trowindex, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(trowindex, 4, QtWidgets.QTableWidgetItem(row[4]))
            
            trowindex += 1

        #The below line enables readonly mode like functionality
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

class ErScreen(QDialog):
        def __init__(self):
            super(ErScreen, self).__init__()
            loadUi('ui/er.ui', self)
            self.back.clicked.connect(self.back_function)

        def back_function(self):
            about = AboutScreen()
            widget.addWidget(about)
            widget.setCurrentIndex(widget.currentIndex() + 1)



#main
app = QApplication(sys.argv)
mains = MainScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mains)
widget.setFixedWidth(950)
widget.setFixedHeight(730) 
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit")