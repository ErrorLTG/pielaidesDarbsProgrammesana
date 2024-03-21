from tkinter import *
from tkinter import messagebox
from customtkinter import *
import sqlite3
import bcrypt


class Login:
  def __init__(self):
    self.loginWindow = Tk()
    self.loginWindow.title("Finance Helper")
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
                                  placeholder_text="Username", 
                                  font=("Calibri", 20))
    self.usernameEntry.place(x=45, y=31)

    self.passEntry = CTkEntry(self.dataFrame, 
                              height=35, 
                              width=250, 
                              placeholder_text="Password", 
                              font=("Calibri", 20), 
                              show="*")
    self.passEntry.place(x=45, y=76)

    self.submitButton = CTkButton(self.dataFrame, 
                                  height=35, 
                                  width=250, 
                                  text="Submit", 
                                  font=("Calibri", 20), 
                                  corner_radius=10, 
                                  fg_color="#248232", 
                                  hover_color="#1B6426",
                                  command=self.submit)
    self.submitButton.place(x=45, y=155)

    self.loginWindow.mainloop()

  def submit(self):
    if self.usernameEntry.get() != "" and self.passEntry.get() != "":
      correctInfo = self.checkInfo()

      if correctInfo:
        self.loginWindow.destroy()
        MainApp()
        
      else:
        messagebox.showerror("Finance Helper", "Incorrect credentials. Try again.")
    else:
      messagebox.showerror("Finance Helper", "Please fill out all required fields")

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

    result = cursor.fetchone()[0]
    connection.close()

    enteredPass = self.passEntry.get()
    return bcrypt.checkpw(enteredPass.encode(), result.encode())
      
class MainApp:
  def __init__(self):
    self.appWindow = Tk()
    self.appWindow.title("Finance Helper")
    self.appWindow.geometry("590x500")
    self.appWindow.resizable(False, False)
    self.appWindow.configure(bg = "#1a3a3a")



    self.appWindow.mainloop()


if __name__ == "__main__":
  app = Login()
    
# if __name__ == "__main__":
#   app = MainApp()