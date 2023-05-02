from tkinter import *
from tkinter import messagebox
import mysql.connector


root=Tk()
root.title("Sign In")
root.geometry('540x440')
root.geometry("+550+150")
frame = Frame(root, bg="lightblue")
root.configure(bg="lightblue")
global balance
# for login
def sign_in():
    global account_number
    global password
    account_number=tbaccount_number.get()
    password=tbPassword.get()
    connection = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    mycursor = connection.cursor()
    sqlquery = "SELECT * FROM xyzbank WHERE AccountNumber=%s and Pswd=%s"
    mycursor.execute(sqlquery,[(account_number),(password)])
    results = mycursor.fetchall()

    if results:
        tbaccount_number.delete(0,END)
        tbPassword.delete(0,END)
        homescreen()
        
    else:
        messagebox.showerror(title="Error",message="Login failed")
        tbaccount_number.delete(0,END)
        tbPassword.delete(0,END)

    

#creating an account function
def Create_an_Account():
    global AccountNumber
    global Password
    global Confirm_Password
    top=Toplevel(root)
    top.grab_set() # to disable user from accessing main window
    top.configure(bg="lightblue")
    top.geometry("+300+300")
    top.title("Create an Account")
    frame1 = Frame(top,bg="lightblue")
    Title = Label(frame1, text = "Create Your Account", font=('bold',20),bg="lightblue", justify="center")
    AccountNumber_LB=Label(frame1, text="Account Number",bg="lightblue",font=('bold',15))
    AccountNumber = Entry(frame1, width=30)

    Password_LB = Label(frame1, text="Password", bg="lightblue",font=('bold',15))
    Password = Entry(frame1, width=30,show="*")

    Confirm_Password_LB=Label(frame1,text="Confirm Password",bg="lightblue",font=('bold',15))
    Confirm_Password=Entry(frame1, width=30, show="*")
    create = Button(frame1, text = "Create Account", font=('bold', 12),command=lambda:create_account_validation(AccountNumber.get(),Password.get(),Confirm_Password.get()),width=15)
    exit = Button(frame1,text="Exit",font=('bold',15),command=top.destroy, width=5)

    create.place(x=45,y=280)


    Title.grid(row=0,column=0,columnspan=2,sticky="news",pady=40)
    AccountNumber_LB.grid(row=1,column=0)
    AccountNumber.grid(row=1,column=1,pady=20)
    Password_LB.grid(row=3,column=0)
    Password.grid(row=3,column=1,pady=20)
    Confirm_Password_LB.grid(row=4,column=0)
    Confirm_Password.grid(row=4,column=1)
    exit.grid(row=5,column=2,pady=20)

    
    frame1.pack()
    top.mainloop()


# Making the functionalities
def create_account_validation(acn,pwd,cpwd):
    global balance
    connection=mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    mycursor=connection.cursor()
    sqlquery = "INSERT INTO xyzbank(AccountNumber, Pswd, Balance) VALUES(%s,%s,%s)"
    sqlquery2 = "SELECT * FROM xyzbank WHERE AccountNumber=%s"
    mycursor.execute(sqlquery2,[(acn),])
    results = mycursor.fetchall()

    if (len(acn) < 8) or (len(acn) > 12):
        messagebox.showerror(message="Sorry, Account Number must be 8-12 digits.")

    elif results:
        messagebox.showerror(message="Account Number already exists.")
        AccountNumber.delete(0,END)
        Password.delete(0,END)
        Confirm_Password.delete(0,END) 
    
    elif cpwd == pwd:
        balance=0.00
        messagebox.showinfo(title="New user created", message="Welcome " + acn)
        mycursor.execute(sqlquery,[(acn),(pwd),(balance)])
        connection.commit()
        AccountNumber.delete(0,END)
        Password.delete(0,END)
        Confirm_Password.delete(0,END)              
    else:
        messagebox.showerror(title="Error",message="Invalid password. Please try again")
        Password.delete(0,END)
        Confirm_Password.delete(0,END)


 #closes main window
def exit():
    messagebox.showinfo(title="Exiting", message="Thanks for banking with us")
    root.destroy()


def homescreen():
    top=Toplevel()
    top.title("Homescreen")
    top.geometry("400x500")
    top.geometry("+500+200")
    top.focus_set()
    top.configure(bg="lightblue")
    frame1=Frame(top,bg="lightblue")
    Title=Label(frame1, text="Welcome " + account_number,font=('bold',20),bg="lightblue")
    Check_Balance=Button(frame1, text="Check Balance", font=('bold',15), command=lambda:check_balance(account_number))
    Withdraw=Button(frame1,text="Withdraw",font=('bold',15),command=withdraw)
    Deposit_Money=Button(frame1, text="Deposit Money", font=('bold',15),command=deposit)
    Edit_Account=Button(frame1,text="Edit Account",font=('bold',15),command=edit_account)
    Exit=Button(frame1,text="Exit", font=('bold',15),command=top.destroy,width=8)

    Title.grid(row=0,column=0,columnspan=2,sticky="news")
    Check_Balance.grid(row=2,column=0,padx=20,pady=10)
    Withdraw.grid(row=3,column=0,pady=40)
    Deposit_Money.grid(row=2,column=1,pady=10)
    Edit_Account.grid(row=3,column=1)
    Exit.grid(row=4,column=1)
    frame1.pack()
    top.mainloop()


def check_balance(acn):
    connection = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    cursor = connection.cursor()
    sqlquery = "SELECT Balance FROM xyzbank WHERE AccountNumber=%s"
    cursor.execute(sqlquery,[(acn)])
    balance = cursor.fetchone()[0]
    connection.commit()
    messagebox.showinfo(message="You have a balance of " + str(balance))




def withdraw():
    global withdraw_entry
    top=Toplevel()
    top.title("Withdraw")
    top.focus_set()
    top.configure(bg="lightblue")
    top.geometry("500x500")
    frame=Frame(top, bg="lightblue")
    Title=Label(frame, text="Withdraw", font=('bold',20),bg="lightblue")
    withdraw_LB=Label(frame,text="Withdraw",font=('bold',15),bg="lightblue")
    withdraw_entry=Entry(frame,width=30)
    withdraw_btn_OK=Button(frame,font=('bold',15),text="OK", command=lambda:withdraw_validation(withdraw_entry.get()))
    withdraw_btn_Cancel=Button(frame,font=('bold',15),text="Cancel",command=top.destroy)
    

    Title.grid(row=0,column=1,pady=20)
    withdraw_LB.grid(row=2,column=0,pady=20)
    withdraw_entry.grid(row=2,column=1,columnspan=2)
    withdraw_btn_OK.grid(row=3,column=0)
    withdraw_btn_Cancel.grid(row=3,column=2)

    frame.pack()
    top.mainloop()



def withdraw_validation(funds):
    connection  = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    cursor = connection.cursor()
    sqlquery = "SELECT Balance FROM xyzbank WHERE AccountNumber=%s"
    sqlquery2 = "UPDATE xyzbank SET Balance=%s WHERE AccountNumber=%s"
    cursor.execute(sqlquery,[(account_number)])
    balance = cursor.fetchone()[0]
    funds=float(funds)
    difference=balance-funds
    if difference >= 0:
        cursor.execute(sqlquery2,[(difference),(account_number)])
        connection.commit()
        messagebox.showinfo(title="Withdrawal",message="You have withdrawed " + str(funds) + " and now have a remaining balance of " + str(difference))
        withdraw_entry.delete(0,END)
    else:
        messagebox.showwarning(title="Warning", message="Cannot withdraw that amount because you have insufficient funds.")
        withdraw_entry.delete(0,END)
        

def deposit():
    global deposit_entry
    top=Toplevel()
    top.title("Deposit")
    top.focus_set()
    top.configure(bg="lightblue")
    top.geometry("500x500")
    frame=Frame(top, bg="lightblue")
    title=Label(frame, text="Deposit",font=('bold',20),bg="lightblue")
    deposit_LB = Label(frame, text="Deposit", font=('bold',20),bg="lightblue")
    deposit_entry = Entry(frame, width=50)
    deposit_btn_OK = Button(frame,font=('bold',15), text="OK",command=lambda:deposit_validation(deposit_entry.get()))
    deposit_btn_Cancel = Button(frame,font=('bold',15), text="Cancel",command = top.destroy)

    title.grid(row=0,column=1,pady=20)
    deposit_LB.grid(row=2,column=0,pady=20)
    deposit_entry.grid(row=2,column=1)
    deposit_btn_OK.grid(row=3,column=0)
    deposit_btn_Cancel.grid(row=3,column=1)   

    frame.pack()
    top.mainloop() 


def deposit_validation(funds):
    connection = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    mycursor = connection.cursor()
    sqlquery = "SELECT Balance FROM xyzbank WHERE AccountNumber=%s"
    sqlquery2 = "UPDATE xyzbank SET Balance=%s WHERE AccountNumber=%s"
    mycursor.execute(sqlquery,[(account_number)])
    balance = mycursor.fetchone()[0]
    connection.commit()
    print(balance)
    funds=float(funds)
    deposition = balance + funds
    mycursor.execute(sqlquery2,[(deposition),(account_number)])
    connection.commit()
    messagebox.showinfo(message="You have deposited " + str(funds) + " and you now have a balance of " + str(deposition))
    deposit_entry.delete(0,END)


def edit_account():
    top=Toplevel()
    top.configure(bg="lightblue")
    top.focus_set()
    top.geometry("500x500")
    top.geometry("+400+300")
    frame=Frame(top,bg="lightblue")
    title=Label(frame, text="Edit Account",font=('bold',20),bg="lightblue")
    Change_Password=Button(frame,text="Change Password",font=('bold',15),width=20,command=ChangePassword)
    Delete_Account = Button(frame, text="Delete Account",font=('bold',15),width=20, command=lambda:delete_account(account_number))
    title.grid(row=0,column=1,columnspan=2)
    Change_Password.grid(row=1,column=1,columnspan=2,pady=10)
    Delete_Account.grid(row=2,column=1,pady=10)
    frame.pack()
    top.mainloop()

def ChangePassword():
    global Current_Password_entry
    global New_Password_entry
    global Confirm_New_Password_entry
    top=Toplevel()
    top.configure(bg="lightblue")
    top.focus_set()
    top.geometry("500x600")
    top.geometry("+350+400")
    frame=Frame(top,bg="lightblue")
    title=Label(frame, text="Change Your Password",font=('bold',20),bg="lightblue")
    Current_Password_LB = Label(frame, text="Current Password",font=('bold',15),bg="lightblue")
    Current_Password_entry = Entry(frame,width=50,show="*")
    New_Password_LB = Label(frame, text="New Password", font=('bold',15),bg="lightblue")
    New_Password_entry = Entry(frame, width=50,show="*")
    Confirm_New_Password_LB = Label(frame, text="Confirm New Password", font=('bold',15), bg="lightblue")
    Confirm_New_Password_entry = Entry(frame, width=50,show="*")
    Create_New_Password = Button(frame,text="Create New Password",font=('bold',10),width=20,command=lambda:change_password_validation(account_number,New_Password_entry.get(),Current_Password_entry.get(),Confirm_New_Password_entry.get()))
    cancel = Button(frame, text="Cancel",font=('bold',10),command=top.destroy)

    title.grid(row=0,column=1,columnspan=2)
    Current_Password_LB.grid(row=2,column=0)
    Current_Password_entry.grid(row=2,column=1,columnspan=3)
    New_Password_LB.grid(row=3,column=0)
    New_Password_entry.grid(row=3,column=1,columnspan=3,pady=20)
    Confirm_New_Password_LB.grid(row=4,column=0)
    Confirm_New_Password_entry.grid(row=4,column=1,columnspan=3,pady=20)
    Create_New_Password.grid(row=5,column=1)
    cancel.grid(row=5,column=2)

    frame.pack()
    top.mainloop()

def change_password_validation(acn,newpwd,crntpwd ,cfrmnewpwd):
    connection = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    mycursor = connection.cursor()
    sqlquery = "UPDATE xyzbank SET Pswd=%s WHERE AccountNumber=%s"
    sqlquery2 = "SELECT Pswd FROM xyzbank WHERE AccountNumber=%s"
    mycursor.execute(sqlquery2,[(acn)])
    oldpwd = mycursor.fetchone()[0]
    if (newpwd == cfrmnewpwd) and (crntpwd == oldpwd):
        mycursor.execute(sqlquery,[(newpwd),(acn)])
        connection.commit()
        messagebox.showinfo(message="You're password has been successfully changed")
        New_Password_entry.delete(0,END)
        Confirm_New_Password_entry.delete(0,END)
    else:
        messagebox.showerror(message="Passwords don't match. Please try again")
        New_Password_entry.delete(0,END)
        Confirm_New_Password_entry.delete(0,END)

def delete_account(acn):
    connection = mysql.connector.connect(host="localhost",user="root",password="L0ngh0rn$1234",database="bankproject")
    cursor = connection.cursor()

    response = messagebox.askyesno(message="Are you sure?\n Once you delete it, your information will be deleted as well")

    if response == 1:
        delete = "DELETE FROM xyzbank WHERE AccountNumber=%s"
        cursor.execute(delete,([acn]))
        connection.commit()


    


#main frame widgets
lblMain = Label(frame, text="Welcome to XYZ Bank", font=('bold', 20), bg="lightblue")
lblaccount_number = Label(frame, text="Account Number", font=('bold',15), bg="lightblue")
tbaccount_number = Entry(frame, width=50)
lblPassword = Label(frame, text="Password", font=('bold',15),bg="lightblue")
tbPassword = Entry(frame, show="*", width=50)
btnSignIn = Button(frame, text = "Sign in", font=('bold', 15),width=10,command=sign_in)
Exit = Button(frame, text = "Exit", command=exit, font=('bold',15))
btnCreate_an_account = Button(frame, text = "Create an account", command= Create_an_Account, font=('bold',15))


#main frame placing the widgets
lblMain.grid(row=0,column=0,columnspan=2,sticky='news',pady=40)
lblaccount_number.grid(row=1,column=0)
tbaccount_number.grid(row=1,column=1,pady=20)
lblPassword.grid(row=2,column=0)
tbPassword.grid(row=2,column=1,pady=20)
btnSignIn.grid(row=3,column=1,pady=20)
Exit.grid(row=3,column=2,pady=15)
btnCreate_an_account.grid(row=3,column=0,pady=30)


frame.pack()
root.mainloop()