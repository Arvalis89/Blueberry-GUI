"""
Program: BlueberryGUI.py
Author: Zach Richards
Last Date Modified: 5/16/2022

This purpose of this program is to be able to take a customers total amount of blueberries ordere/picked and calculate their total cost
and also schedule pick-a-dates for them to come out to our farm and handpick their own blueberries with family or friends. The 
ordering section asks the customer how much blueberries they would like to purchase.
The scheduling section lets the user input a customer's First name, Last name, Phone number, and the date selected (given between seasonal dates 
June 15th to August 15th) and submit it to a database. Not only can the it be submitted, but information can be queried, deleted, and
updated as needed.  
"""
# All Imports needed for program to function
from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import sqlite3

# Create Database using sqlite3
connection = sqlite3.connect("Blueberry GUI Application/pickDates.db") #pickDates.db will be created or opened

# Create Cursor object
cursor = connection.cursor()

# Create Table
cursor.execute("CREATE TABLE IF NOT EXISTS scheduledDates (f_name TEXT, l_name TEXT, phone_number INTEGER, date INTEGER)")

# Commit Changes
connection.commit()

# Close Connection
connection.close()


# Create a Class for the GUI
class blueberryGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        # Adding a title to the window
        self.title("Rykers Ridge Blueberry")

        # Window size
        self.resizable(0, 0)
        
        # Icon
        self.iconbitmap(r"BlueBerry GUI Application/blueberryICO.ico")

        # Calls on widgets
        self.create_widgets()
    
    # Widgets are defined here
    def create_widgets(self):

        # Input Validation
        def qValid(input):
            if input.isdigit():
                return True

            elif input == "":
                return True

            else:
                return False
        
        def cValid(input):
            if isFloat(input):
                return True

            elif input == "":
                return True

            else:
                return False

        def isFloat(x):
            try:
                float(x)
                return True

            except ValueError:
                return False

        # Displays error message when blank entry is in "Cost per Weight"
        def errPopup(row):
            messagebox.showerror("Error", f"Quantity and cost must have a number to calculate total.\nMissing value in row {row}.")

        # Lists of input to be passed to totalAdd
        quantityList = []  
        costList = []

        # Displays total from adding quantityList[] and costList[]
        def totalAdd():
            totalCost["text"] = ""
            total = 0
            for i in range(len(quantityList)):
                if quantityList[i].get() == "" or costList[i].get() == "":  # Input Validation
                    errPopup(i + 1)
                else:
                    total += int(quantityList[i].get()) * float(costList[i].get())
            totalCost["text"] = f"{total: .2f}"
        
        
        # Creates a new window for scheduling dates for picking. Lines 98 to Lines 353
        def Scheduling():
            
            top = Toplevel()
            # Adding a title to the window
            top.title("Rykers Ridge Blueberry - Pick-a-Date")

            # Icon
            top.iconbitmap(r"BlueBerry GUI Application/blueberryICO.ico")

            # Window size
            top.resizable(300, 300)

            # Banner - Top Window
            imageLabel = Label(top, relief=RAISED, bd=4)
            imageLabel.grid(row=0, column=0, columnspan=4, padx=8, pady=8)
            top.image = PhotoImage(file = "BlueBerry GUI Application/calendar_month_year_date.ppm")
            imageLabel["image"] = top.image

            # Labels in widget to show in toplevel
            scheduleLabel = Label(top, text="When would you like to come pick blueberries?")
            scheduleLabel.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

            scheduleLabel2 = Label(top, text="Please Note: Our season runs from June 15 to August 15.")
            scheduleLabel2.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            
            # Exit button
            returnButton = Button(top, text="Return to Main Menu", padx=15, command=top.destroy)
            returnButton.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
           
            # Entry boxes for First name, Last name, Phone Number, and Date
            f_name = Entry(top, width=30, borderwidth=2)
            f_name.grid(row=3, column=1, padx=20, pady=(10, 0))

            l_name = Entry(top, width=30, borderwidth=2)
            l_name.grid(row=4, column=1)
            
            phone_number = Entry(top, width=30, borderwidth=2)
            phone_number.grid(row=5, column=1)

            date = Entry(top, width=30, borderwidth=2)
            date.grid(row=6, column= 1)

            delete_box = Entry(top, width=30)
            delete_box.grid(row=10, column=1, padx=10, pady=10)

            # Text box labels
            f_name_label = Label(top, text="First Name:")
            f_name_label.grid(row=3, column=0, pady=(10, 0))

            l_name_label = Label(top, text="Last Name: ")
            l_name_label.grid(row=4, column=0)

            phone_number_label = Label(top, text="Phone number: ")
            phone_number_label.grid(row=5, column=0)

            date_Label = Label(top, text="Pick-a-date: ")
            date_Label.grid(row=6, column=0)

            delete_box_label = Label(top, text="Select ID Number")
            delete_box_label.grid(row=10, column=0, padx=10, pady=10)

            # Create edit function to update a record
            def update():
                # Connects to database
                connection = sqlite3.connect('pickDates.db')
            
                # Creates cursor
                cursor = connection.cursor()

                recordID = delete_box.get()
                
                # Updates information in corresponding fields
                cursor.execute("""UPDATE scheduledDates SET
                    f_name = :first,
                    l_name = :last,
                    phone_number = :phone_number,
                    date = :date

                    WHERE oid = :oid""",
                    {
                        'first': f_name_editor.get(),
                        'last': l_name_editor.get(),
                        'phone_number': phone_number_editor.get(),
                        'date': date_editor.get(),
                        'oid': recordID
                    })

                # Commit Changes
                connection.commit()

                # Close Connection
                connection.close()

                # Messagebox
                messagebox.showinfo("Update a Record", "Changes were saved!")

                # Once changes are made, box destroys itself
                editor.destroy()

            # Open new window
            def edit():
                # Created global variable for editor.destory()
                global editor

                # Opens new window to edit record
                editor = Tk()

                # Title of new window
                editor.title('Update A Record')

                # Icon 
                editor.iconbitmap(r"BlueBerry GUI Application/blueberryICO.ico")
                
                # Window Size
                editor.geometry("300x250")

                # Connects to database
                connection = sqlite3.connect('pickDates.db')
            
                # Creates cursor
                cursor = connection.cursor()

                record_id = delete_box.get()

                # Query the Database
                cursor.execute("SELECT * FROM scheduledDates WHERE oid = " + record_id)
                records = cursor.fetchall()

                # Create global variables for text box names
                global f_name_editor
                global l_name_editor
                global phone_number_editor
                global date_editor

                # Entry boxes for First name, Last name, Phone Number, and Date
                f_name_editor = Entry(editor, width=25, borderwidth=2)
                f_name_editor.grid(row=2, column=1, padx=20, pady=(10, 0))

                l_name_editor = Entry(editor, width=25, borderwidth=2)
                l_name_editor.grid(row=3, column=1)
                
                phone_number_editor = Entry(editor, width=25, borderwidth=2)
                phone_number_editor.grid(row=4, column=1)

                date_editor = Entry(editor, width=25, borderwidth=2)
                date_editor.grid(row=5, column= 1)

                # Text box labels
                f_name_label = Label(editor, text="First Name:")
                f_name_label.grid(row=2, column=0, pady=(10, 0))

                l_name_label = Label(editor, text="Last Name: ")
                l_name_label.grid(row=3, column=0)

                phone_number_label = Label(editor, text="Phone number: ")
                phone_number_label.grid(row=4, column=0)

                date_Label = Label(editor, text="Pick-a-date: ")
                date_Label.grid(row=5, column=0)

                # Loop through results
                for record in records:
                    f_name_editor.insert(0, record[0])
                    l_name_editor.insert(0, record[1])
                    phone_number_editor.insert(0, record[2])
                    date_editor.insert(0, record[3])

                # Create Save button to save a record
                saveButton = Button(editor, text="Save Record", command=update)
                saveButton.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

            # Create function to delete a record
            def delete():
                # Connects to database
                connection = sqlite3.connect('pickDates.db')
            
                # Creates cursor
                cursor = connection.cursor()

                # Delete a record within the table
                cursor.execute("DELETE from scheduledDates WHERE oid= " + delete_box.get())

                delete_box.delete(0, END)

                # Commit Changes
                connection.commit()

                # Close Connection
                connection.close()

            # Create submit function for database
            def submit():
            # Connects to database
                connection = sqlite3.connect('pickDates.db')
            
                # Creates cursor
                cursor = connection.cursor()
            
                # Insert into table
                cursor.execute("INSERT INTO scheduledDates VALUES (:f_name, :l_name, :phone_number, :date)",
                            {
                                'f_name': f_name.get(),
                                'l_name': l_name.get(),
                                'phone_number': phone_number.get(),
                                'date': date.get()
                            })

                # Commit Changes
                connection.commit()

                # Close Connection
                connection.close()

                # Clear entry boxes after submission
                f_name.delete(0, END)
                l_name.delete(0, END)
                phone_number.delete(0, END)
                date.delete(0, END)

            def query():
                # Connects to database
                connection = sqlite3.connect('pickDates.db')
            
                # Creates cursor
                cursor = connection.cursor()

                # Query the Database
                cursor.execute("SELECT *, oid FROM scheduledDates")
                records = cursor.fetchall()

                # Loop through results
                print_records = ''
                for record in records: # Prints First name, Last name, Phone Number, Date selected, ID number
                    print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + " " + "\t" + str(record[4]) + "\n"

                query_label = Label(top, text=print_records)
                query_label.grid(row=13, column=0, columnspan=2)

                # Commit Changes
                connection.commit()

                # Close connection
                connection.close()

                return()
            
            # Create submit button
            submitButton = Button(top, text="Sumbit Information", command=submit)
            submitButton.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

            # Create query button
            query_button = Button(top, text="Show Records", command=query)
            query_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx= 137)
        
            # Create delete button
            deleteButton = Button(top, text="Delete Record", command=delete)
            deleteButton.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

            # Create update button
            updateButton = Button(top, text="Edit Record", command=edit)
            updateButton.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=142)

        # totalBox Label and grid
        totalCost = Label(self, relief=SUNKEN, bd=4, width=7, anchor='w')
        totalCost.grid(row=4, column=2)
        totalLabel = Label(self, text="Total Cost")
        totalLabel.grid(row=4, column=1, padx=5, pady=5)

        # Banner - Main Window
        imageLabel = Label(self, relief=RAISED, bd=4)
        imageLabel.grid(row=0, column=0, columnspan=4, padx=8, pady=8)
        self.image = PhotoImage(file = "C:/Users/Zach/Desktop/Python/BlueBerry GUI Application/blueberrybanner1.ppm")
        imageLabel["image"] = self.image
        
        # Header labels
        descLabel = Label(self, text="Description of item")
        descLabel.grid(row=1, column=0, padx=5, pady=5)

        quantityLabel = Label(self, text="Quantity of blueberries")
        quantityLabel.grid(row=1, column=1, padx=5, pady=5)

        costLabel = Label(self, text="Cost per weight")
        costLabel.grid(row=1, column=2, padx=5, pady=5)
        
        # Entry Fields
        dropOptions = [
            "Pound of Blueberries", "Half pound of Blueberries"]
        
        # Row 1 - Calculates total for Row 1
        selected1 = StringVar()
        selected1.set(dropOptions[0])
        compDrop1 = OptionMenu(self, selected1, *dropOptions)
        compDrop1.grid(row=2, column=0, padx=2, pady=2)

        quantityInput1 = Entry(self, borderwidth=5, width=3)
        quantityInput1.grid(row=2, column=1)
        quantityInput1.insert(0, '1')
        regQ1 = self.register(qValid)       # Input validation
        quantityInput1.config(validate ="key", validatecommand=(regQ1, '%P'))   # Input validation
        quantityList.append(quantityInput1) # Input added to list to be passed to totalAdd function

        costInput1 = Entry(self, borderwidth=5, width=8)
        costInput1.grid(row=2, column=2)
        costInput1.insert(0, "0.00")
        regC1 = self.register(cValid)       # Input validation
        costInput1.config(validate ="key", validatecommand=(regC1, '%P'))   # Input validation
        costList.append(costInput1) # Input added to list to be passed to totalAdd function

        # Row 2 - Calculates total for Row 2
        selected2 = StringVar()
        selected2.set(dropOptions[1])
        compDrop2 = OptionMenu(self, selected2, *dropOptions)
        compDrop2.grid(row=3, column=0, padx=2, pady=2)

        quantityInput2 = Entry(self, borderwidth=5, width=3) 
        quantityInput2.grid(row=3, column=1)
        quantityInput2.insert(0, '1')
        quantityInput2.config(validate ="key", validatecommand=(regQ1, '%P'))   # Input validation
        quantityList.append(quantityInput2) # Input added to list to be passed to totalAdd function

        costInput2 = Entry(self, borderwidth=5, width=8)
        costInput2.grid(row=3, column=2)
        costInput2.insert(0, "0.00")
        costInput2.config(validate ="key", validatecommand=(regC1, '%P'))   # Input validation
        costList.append(costInput2) # Input added to list to be passed to totalAdd function

        # Creating the buttons
        scheduleButton = Button(self, text="Schedule a 'Pick-a-Date'", command=Scheduling)
        scheduleButton.grid(row=5, column=1, padx=5, pady=5)

        calcButton = Button(self, text="Calculate", command=totalAdd)
        calcButton.grid(row=6, column=2, padx=5, pady=5)

        exitButton = Button(self, text="Exit", padx=15, command=self.destroy)
        exitButton.grid(row=6, column=0, padx=5, pady=5)


def main():
    blueberryGUI().mainloop()

if __name__ == "__main__":
    main()
