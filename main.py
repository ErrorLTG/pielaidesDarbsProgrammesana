from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from customtkinter import *
from tkcalendar import DateEntry
import sqlite3
import bcrypt


class Login:
  def __init__(self):
    self.loginWindow = Tk()
    self.loginWindow.title("Paroļu atgādnis")
    self.loginWindow.geometry("590x500")
    self.loginWindow.resizable(False, False)
    self.loginWindow.configure(bg = "#1a3a3a")

    self.dataFrame = CTkFrame(self.loginWindow, 
                              fg_color = "#F0CEA0", 
                              width=340, 
                              height=220, 
                              corner_radius=12)
    self.dataFrame.place(x=125, y=140)

    self.usernameEntry = CTkEntry(self.dataFrame, 
                                  height=35, 
                                  width=250,
                                  placeholder_text="Lietotājvārds", 
                                  font=("Calibri", 20))
    self.usernameEntry.place(x=45, y=31)

    self.passEntry = CTkEntry(self.dataFrame, 
                              height=35, 
                              width=250, 
                              placeholder_text="Parole", 
                              font=("Calibri", 20), 
                              show="*")
    self.passEntry.place(x=45, y=76)

    self.submitButton = CTkButton(self.dataFrame, 
                                  height=35, 
                                  width=250, 
                                  text="Apstiprināt", 
                                  font=("Calibri", 20), 
                                  corner_radius=10, 
                                  fg_color="#248232", 
                                  hover_color="#1B6426",
                                  command=self.submit)
    self.submitButton.place(x=45, y=135)

    self.signupButton = CTkButton(self.dataFrame,
                                   height=35, 
                                   width=250, 
                                   text="Jauns Lietotājs", 
                                   font=('Calibri', 20), 
                                   corner_radius=10, 
                                   fg_color="#4381C1", 
                                   hover_color="#346493",
                                   anchor=CENTER,
                                   command=self.signUp)
    self.signupButton.place(x=45, y=175)

    self.dataFrame.bind('<ButtonRelease-1>', lambda event: self.loginWindow.focus_set())
    self.loginWindow.bind('<Return>', self.submit)
    self.loginWindow.mainloop()

  def signUp(self):
    self.signUpFrame = CTkFrame(self.loginWindow, 
                              fg_color = "#346493", 
                              width=340, 
                              height=220, 
                              corner_radius=12)
    self.signUpFrame.place(x=125, y=140)

    self.newUsernameEntry = CTkEntry(self.signUpFrame, 
                                  height=35, 
                                  width=250,
                                  placeholder_text="Jaunā lietotāja lietotājvārds", 
                                  font=("Calibri", 20))
    self.newUsernameEntry.place(x=45, y=31)

    self.newPassEntry = CTkEntry(self.signUpFrame, 
                              height=35, 
                              width=250, 
                              placeholder_text="Jaunā lietotāja parole", 
                              font=("Calibri", 20))
    self.newPassEntry.place(x=45, y=76)

    self.registerSubmitButton = CTkButton(self.signUpFrame, 
                                  height=35, 
                                  width=250, 
                                  text="Reģistrēt", 
                                  font=("Calibri", 20), 
                                  corner_radius=10, 
                                  fg_color="#248232", 
                                  hover_color="#1B6426",
                                  command=self.register)
    self.registerSubmitButton.place(x=45, y=135)

    self.registerCancelButton = CTkButton(self.signUpFrame, 
                                  height=35, 
                                  width=250, 
                                  text="Atcelt", 
                                  font=("Calibri", 20), 
                                  corner_radius=10, 
                                  fg_color="#8D171E", 
                                  hover_color="#5D0F15",
                                  command=self.cancelSignup)
    self.registerCancelButton.place(x=45, y=175)

    self.signUpFrame.bind('<ButtonRelease-1>', lambda event: self.loginWindow.focus_set())

  def cancelSignup(self):
    self.signUpFrame.destroy()

  def register(self):
    newUserUsrname = self.newUsernameEntry.get()
    newUserPass = self.newPassEntry.get()

    _newUserPassCrypted = self._encryptPass(newUserPass)


    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    query = "INSERT INTO user (Username, Password) VALUES (?,?)"
    cursor.execute(query, (newUserUsrname, _newUserPassCrypted))
    connection.commit()
    connection.close()

    self.signUpFrame.destroy()

  def _encryptPass(self, password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

  def submit(self, event=None):
    if self.usernameEntry.get() != "" and self.passEntry.get() != "":
      correctInfo = self.checkInfo()

      if correctInfo:
        self.loginWindow.destroy()
        MainApp(self.userID)
        
      else:
        messagebox.showerror("Paroļu atgādnis", "Nepareizi piekļuves dati. Mēģiniet vēlreiz.")
    else:
      messagebox.showerror("Paroļu atgādnis", "Lūdzu, aizpildiet visus lauciņus.")

  def checkInfo(self):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute('SELECT Username FROM user')
    userNameResult = cursor.fetchall()
    listOfUsernames = [username[0] for username in userNameResult]
    connection.close()

    enteredUsername = self.usernameEntry.get()

    return enteredUsername in listOfUsernames and self._checkPass(enteredUsername)

  def _checkPass(self, username):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    query = "SELECT Password FROM user WHERE username = ?"
    cursor.execute(query, (username,))
    passInDb = cursor.fetchone()[0]
    query = "SELECT ID FROM user WHERE username = ?"
    cursor.execute(query, (username,))
    self.userID = cursor.fetchone()[0]
    connection.close()

    enteredPass = self.passEntry.get()
    correctPassword = bcrypt.checkpw(enteredPass.encode('utf-8'), passInDb)

    return correctPassword
      
class MainApp:
  def __init__(self, userID):
    self.userID = userID
    self.appWindow = Tk()
    self.appWindow.title("Paroļu atgādnis")
    self.appWindow.geometry("800x478")
    self.appWindow.resizable(False, False)
    self.appWindow.configure(bg = "#1a3a3a")

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    query = "SELECT vietne, lietotajvards, parole, datums FROM savedData WHERE userID = ?"
    cursor.execute(query, (self.userID,))
    allSavedData = cursor.fetchall()
    connection.close()

    self.table = ttk.Treeview(self.appWindow, columns = ('site', 'usrname', 'pass', 'date'), show = 'headings', selectmode=BROWSE)
    self.table.heading('site', text = 'Vietne')
    self.table.heading('usrname', text = 'Lietotājvārds')
    self.table.heading('pass', text = 'Parole')
    self.table.heading('date', text = 'Datums')
    self.table.column('site', anchor='center')
    self.table.column('usrname', anchor='center')
    self.table.column('pass', anchor='center')
    self.table.column('date', anchor='center')
    
    self.table.place(x= -2, y=-2)

    for dataRow in allSavedData:
      site = dataRow[0]
      usrname = dataRow[1]
      passw = dataRow[2]
      date = dataRow[3]
      valueData = (site, usrname, passw, date)
      self.table.insert('', 'end', values = valueData)
    self.updateTableHeight()

    self.table.bind('<Double-1>', self.onDoubleClick)


    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure("Treeview",
                    background = "#1a3a3a",
                    foreground = "white", 
                    rowheight = 25,
                    font = ("Noto Sans", 14))
    self.style.map("Treeview",
              background = [('selected', '#698672')])
    self.style.configure("Treeview.Heading", 
                    background = "#2B6262",
                    foreground = "White",
                    font = ("Noto Sans", 16))
    self.style.map("Treeview.Heading",
                    background = [('selected', '#1a3a3a')])



    self.addDataButton = CTkButton(self.appWindow,
                                   height=14, 
                                   width=65, 
                                   text="+", 
                                   font=(None, 55), 
                                   corner_radius=10, 
                                   fg_color="#4381C1", 
                                   hover_color="#346493",
                                   anchor=CENTER,
                                   command=self.addData)
    self.addDataButton.place(x=720, y=394)




    self.appWindow.mainloop()

  def onDoubleClick(self, event=None): 
    region = self.table.identify("region", event.x, event.y)

    if region == "cell":
      selectedCell = self.table.focus()
      
      if selectedCell:
          cellData = self.table.item(selectedCell).get('values')[2]
          self.appWindow.clipboard_clear()
          self.appWindow.clipboard_append(cellData)
          self.appWindow.update_idletasks()

  def updateTableHeight(self):
    maxHeight = 18
    num_items = len(self.table.get_children())
    self.table.config(height=min(num_items, maxHeight))

  def addData(self):
    self.addDataButton.configure(state='disabled')

    self.addDataWindow = CTkFrame(self.appWindow, width=400, height=300)
    self.addDataWindow.place(x = 384, y = 162)
    self.addDataWindow.configure(fg_color = '#4381C1', border_color = '#000000', border_width = 4)

    self.websiteEntry = CTkEntry(self.addDataWindow, 
                                height=35, 
                                width=250,
                                placeholder_text="Vietne",
                                border_color='#000000',
                                font=("Calibri", 25))
    self.websiteEntry.place(x=75, y=35)

    self.usrnameEntry = CTkEntry(self.addDataWindow, 
                                height=35, 
                                width=250,
                                placeholder_text="Lietotājvārds", 
                                border_color='#000000',
                                font=("Calibri", 25))
    self.usrnameEntry.place(x=75, y=85)

    self.passEntry = CTkEntry(self.addDataWindow, 
                                height=35, 
                                width=250,
                                placeholder_text="Parole", 
                                border_color='#000000',
                                font=("Calibri", 25))
    self.passEntry.place(x=75, y=135)

    self.dateEntry = DateEntry(self.addDataWindow, font = ('Noto Sans', 14))
    self.dateEntry.place(x=124, y=190)

    self.addDataSubmitButton = CTkButton(self.addDataWindow, 
                                  height=35, 
                                  width=250, 
                                  text="Pievienot", 
                                  font=("Noto Sans", 20), 
                                  corner_radius=10, 
                                  border_width=2,
                                  border_color='#000000',
                                  fg_color="#248232", 
                                  hover_color="#1B6426",
                                  command=self.addDataSubmit)
    self.addDataSubmitButton.place(x=75, y=245)
    
    self.addDataWindow.bind('<ButtonRelease-1>', lambda event: self.addDataWindow.focus_set())

  def addDataSubmit(self):
    if self.websiteEntry.get() != '' and self.passEntry.get() != '' and self.usrnameEntry.get() != '':
      website = self.websiteEntry.get()
      username = self.usrnameEntry.get()
      password = self.passEntry.get()
      date = self.dateEntry.get_date()
      dateFormated = date.strftime('%d.%m.%Y')

      connection = sqlite3.connect("data.db")
      cursor = connection.cursor()

      query = "INSERT INTO savedData (vietne, lietotajvards, parole, datums, userID) VALUES (?,?,?,?,?)"
      cursor.execute(query, (website, username, password, dateFormated, self.userID))
      connection.commit()
      connection.close()

      self.table.insert('', 'end', values = (website, username, password, dateFormated))
      self.updateTableHeight()

      self.addDataButton.configure(state='normal')

      self.addDataWindow.destroy()
    else:
      messagebox.showerror("Paroļu atgādnis", "Lūdzu, aizpildiet visus lauciņus.")

class CreateDB:
  def __init__(self):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS "user" (
        "ID" INTEGER UNIQUE,
        "Username" TEXT UNIQUE,
        "Password" BLOB,
        PRIMARY KEY("ID" AUTOINCREMENT)
    );
    '''

    cursor.execute(query)
    connection.commit()

    query = '''
    CREATE TABLE IF NOT EXISTS "savedData" (
        "ID"	INTEGER,
        "vietne"	TEXT,
        "lietotajvards"	TEXT,
        "parole"	TEXT,
        "datums"	TEXT,
        "userID"	INTEGER,
        PRIMARY KEY("ID"),
        FOREIGN KEY("userID") REFERENCES "user"("ID")
    );
    '''
    cursor.execute(query)
    connection.commit()


    connection.close()

    Login()



if __name__ == "__main__":
  app = CreateDB()
