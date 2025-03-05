import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk 
import mysql.connector

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="employee_management"
    )

# Add Employee Page
class AddEmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/view.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.bg_image = ImageTk.PhotoImage(self.apply_opacity(self.original_image, 0.7))  # Apply 70% opacity (0.7)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        self.columnconfigure(0, weight=1)

        tk.Label(self, text="Add Employee", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        # Left column fields
        tk.Label(self, text="Name:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Aadhar No:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entry_aadhar = tk.Entry(self)
        self.entry_aadhar.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Education:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entry_education = tk.Entry(self)
        self.entry_education.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Designation:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.entry_designation = tk.Entry(self)
        self.entry_designation.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Salary:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Right column fields
        tk.Label(self, text="Email:").grid(row=4, column=2, sticky="w", padx=10, pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Birthdate:").grid(row=5, column=2, sticky="w", padx=10, pady=5)
        self.entry_birthdate = DateEntry( self, date_pattern="yyyy-mm-dd")  # DateEntry widget
        self.entry_birthdate.grid(row=5, column=3, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Address:").grid(row=6, column=2, sticky="w", padx=10, pady=5)
        self.entry_address = tk.Entry(self)
        self.entry_address.grid(row=6, column=3, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Phone No:").grid(row=7, column=2, sticky="w", padx=10, pady=5)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=7, column=3, padx=10, pady=5, sticky="ew")

        # Add Employee and Back Buttons
        tk.Button(self, text="Add Employee", command=self.add_employee).grid(row=9, column=0, columnspan=4, pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(AdminDashboardPage),).grid(row=10, column=0, columnspan=4, pady=10)

    def add_employee(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        aadhar = self.entry_aadhar.get().strip()
        birthdate = self.entry_birthdate.get()
        education = self.entry_education.get().strip()
        address = self.entry_address.get().strip()
        designation = self.entry_designation.get().strip()
        phone = self.entry_phone.get().strip()
        salary = self.entry_salary.get().strip()

        # Required fields validation
        if not all([name, email, phone, aadhar, education]):
            messagebox.showerror("Input Error", "Name, Email, Phone No, Aadhar No, and Education are required fields.")
            return

        # Validate email format
        if "@" not in email or "." not in email:
            messagebox.showerror("Input Error", "Enter a valid email address.")
            return

        # Validate phone number length
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Input Error", "Phone number must be at least 10 digits long.")
            return

        # Validate Aadhar number (assuming it should be exactly 12 digits)
        if not aadhar.isdigit() or len(aadhar) != 12:
            messagebox.showerror("Input Error", "Aadhar number must be exactly 12 digits.")
            return

        # Validate salary as a number
        try:
            salary = float(salary) if salary else None
        except ValueError:
            messagebox.showerror("Input Error", "Salary must be a numeric value.")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Employee (Name, Email, Aadhar_No, Birthdate, Education, Address, Designation, Phone_No, Salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, aadhar, birthdate, education, address, designation, phone, salary))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Employee '{name}' added successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        # Clear inputs
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_aadhar.delete(0, tk.END)
        self.entry_birthdate.set_date(None) 
        self.entry_education.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_designation.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_salary.delete(0, tk.END)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.apply_opacity(resized_image, 0.7))  # Reapply opacity after resizing

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)
        return image

class ViewEmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/view.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        self.columnconfigure(0, weight=1)

        tk.Label(self, text="View Employee", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

        # Employee Details Table
        columns = ("ID", "Name", "Email", "Aadhar No", "Birthdate", "Education", "Address", "Designation", "Phone No", "Salary")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        # Reload Button
        tk.Button(self, text="Reload", command=self.load_all_employees).grid(row=2, column=0, pady=5)

        # Back to Main Menu Button
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(AdminDashboardPage)).grid(row=3, column=0, pady=10)

        # Load all employee data directly
        self.load_all_employees()

    def load_all_employees(self):
        """Load all employee data from the database and display it in the Treeview."""
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employee")
            employees = cursor.fetchall()
            conn.close()
            
            # Clear previous data
            for row in self.tree.get_children():
                self.tree.delete(row)

            if employees:
                for employee in employees:
                    self.tree.insert("", "end", values=employee)
            else:
                messagebox.showinfo("No Employees", "No employee records found.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def resize_background(self, event):
        """Resize the background image when the window is resized."""
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        """Apply opacity to the background image."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Edit Employee Details 
class EditEmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.emp_id = None  # Store selected employee ID

        # Load the background image
        self.original_image = Image.open("img/details.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        # Centering the frame
        self.grid_columnconfigure(1, weight=1)  # Allow the second column to expand

        # Title
        tk.Label(self, text="Edit Employee Details", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Employee ID Selection Dropdown with Name
        tk.Label(self, text="Select Employee ID:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.selected_emp_id = tk.StringVar()
        self.emp_id_dropdown = tk.OptionMenu(self, self.selected_emp_id, "", command=self.load_employee_details)
        self.emp_id_dropdown.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Employee Name
        tk.Label(self, text="Name:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # Load Employee IDs
        self.load_employee_ids()

        # Employee Details Form
        self.entries = {}
        fields = [
            ("Email:", "Aadhar No:"),
            ("Birthdate:", "Education:"),
            ("Address:", "Designation:"),
            ("Phone No:", "Salary:")
        ]

        row = 3  # Start from row 3
        for label1, label2 in fields:
            # First Field (Label + Entry)
            tk.Label(self, text=label1).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            self.entries[label1] = tk.Entry(self)
            self.entries[label1].grid(row=row, column=1, sticky="ew", padx=10, pady=5)

            # Second Field (Label + Entry)
            tk.Label(self, text=label2).grid(row=row + 1, column=0, sticky="w", padx=10, pady=5)
            self.entries[label2] = tk.Entry(self)
            self.entries[label2].grid(row=row + 1, column=1, sticky="ew", padx=10, pady=5)

            row += 2  # Move to the next pair of rows
        
         # **Reload Button**
        self.reload_button = tk.Button(self, text="Reload", command=self.load_employee_ids)
        self.reload_button.grid(row=row, column=0, columnspan=2, pady=10)

        # Save Changes and Back Buttons
        tk.Button(self, text="Save Changes", command=self.update_employee).grid(row=row + 1, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(ViewEmployeePage)).grid(row=row + 2, column=0, columnspan=2, pady=10)

    def load_employee_ids(self):
        """Fetch all employee IDs and update dropdown menu"""
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM Employee")
            employee_ids = [str(row[0]) for row in cursor.fetchall()]
            conn.close()

            self.selected_emp_id.set("Select ID")
            self.emp_id_dropdown['menu'].delete(0, 'end')
            for emp_id in employee_ids:
                self.emp_id_dropdown['menu'].add_command(label=emp_id, command=tk._setit(self.selected_emp_id, emp_id, self.load_employee_details))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def load_employee_details(self, emp_id):
        self.emp_id = emp_id
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employee WHERE ID = %s", (emp_id,))
            employee = cursor.fetchone()
            conn.close()

            if employee:
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, employee[1])

                for i, key in enumerate(self.entries.keys()):
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, employee[i + 2])
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def update_employee(self):
        """Update employee details in database"""
        updated_data = (
            self.entry_name.get(),
            self.entries["Email:"].get(),
            self.entries["Aadhar No:"].get(),
            self.entries["Birthdate:"].get(),
            self.entries["Education:"].get(),
            self.entries["Address:"].get(),
            self.entries["Designation:"].get(),
            self.entries["Phone No:"].get(),
            self.entries["Salary:"].get(),
            self.emp_id
        )

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Employee 
                SET Name=%s, Email=%s, Aadhar_No=%s, Birthdate=%s, Education=%s, Address=%s, Designation=%s, Phone_No=%s, Salary=%s 
                WHERE ID=%s
            """, updated_data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee details updated successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Delete Employee Page
class DeleteEmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/delete.png").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        self.columnconfigure(0, weight=1)  # Center all content horizontally

        # Label
        tk.Label(self, text="Select Employee ID:", font=("Arial", 12)).pack(pady=10)

        # Dropdown (Combobox) to display employee IDs
        self.emp_combobox = ttk.Combobox(self, font=("Arial", 10), state="readonly")
        self.emp_combobox.pack(pady=5)

        # Set default text in the dropdown
        self.emp_combobox.set("Select Employee ID")

        # Load employee IDs immediately when the page opens
        self.load_employees()

        # Delete Button
        tk.Button(self, text="Delete Employee", font=("Arial", 10), command=self.delete_employee).pack(pady=10)

        # Reload Button
        tk.Button(self, text="Reload", font=("Arial", 10), command=self.load_employees).pack(pady=10)

        # Back to Main Menu Button
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(AdminDashboardPage)).pack(pady=10)

    def connect_to_db(self):
        """Connect to the database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="employee_management"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def load_employees(self):
        """Automatically load employee IDs into the dropdown."""
        conn = self.connect_to_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Employee")  # Fetch only IDs
            employees = cursor.fetchall()

            if not employees:
                messagebox.showinfo("Info", "No employees found!")
                return

            # Populate combobox with only IDs
            emp_list = [str(emp[0]) for emp in employees]
            self.emp_combobox["values"] = emp_list

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_employee(self):
        """Delete the selected employee."""
        emp_id = self.emp_combobox.get()
        
        # Validate if an actual employee ID is selected
        if not emp_id or emp_id == "Select Employee ID":
            messagebox.showerror("Error", "Please select a valid employee ID!")
            return

        conn = self.connect_to_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee ID {emp_id}?")
            if not confirm:
                return

            # Delete the employee
            cursor.execute("DELETE FROM Employee WHERE id=%s", (emp_id,))
            conn.commit()
            messagebox.showinfo("Success", "Employee deleted successfully")

            # Reload updated employee list
            self.load_employees()

            # Reset combobox selection
            self.emp_combobox.set("Select Employee ID")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Login Admin, Employee Page
class AdminLoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/print.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tk.Label(self, text="Login", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Radio buttons for selecting login type
        self.login_type = tk.StringVar(value="admin")  # Default to admin login

        tk.Radiobutton(self, text="Admin Login", variable=self.login_type, value="admin").grid(row=1, column=0, columnspan=2, pady=5)
        tk.Radiobutton(self, text="Employee Login", variable=self.login_type, value="employee").grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(self, text="Username:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Password:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        tk.Button(self, text="Login", command=self.login).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=6, column=0, columnspan=2, pady=10)

    def apply_opacity(self, image, opacity):
        """Apply opacity to the image."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        login_type = self.login_type.get()  # Get the selected login type (admin or employee)

        if not username or not password:
            messagebox.showerror("Input Error", "Username and password are required.")
            return

        try:
            # Connect to the database
            conn = connect_to_db()
            cursor = conn.cursor()

            # Fetch the password and role for the given username
            query = "SELECT password, role FROM login WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                stored_password, role = result
                # Check if the password matches and the role matches the selected login type
                if stored_password == password and role == login_type:
                    messagebox.showinfo("Login Success", f"Welcome, {login_type.capitalize()}!")
                    self.clear_entries()  # Clear the input boxes
                    if login_type == "admin":
                        self.controller.show_frame(AdminDashboardPage)
                    else:
                        self.controller.show_frame(EmployeeDashboardPage)
                else:
                    messagebox.showerror("Login Failed", "Invalid username, password, or role.")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def clear_entries(self):
        """Clear the username and password entry fields."""
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

# Registration Admin Employee Page
class AdminRegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/print.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tk.Label(self, text="Registration", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Role selection (Admin or Employee)
        tk.Label(self, text="Role:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.role_var = tk.StringVar(value="admin")  # Default to admin
        tk.Radiobutton(self, text="Admin", variable=self.role_var, value="admin").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(self, text="Employee", variable=self.role_var, value="employee").grid(row=4, column=1, padx=10, pady=5, sticky="w")

        tk.Button(self, text="Register", command=self.register).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=6, column=0, columnspan=2, pady=10)

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.role_var.get()  # Get the selected role (admin or employee)

        if not username or not password:
            messagebox.showerror("Input Error", "Username and password are required.")
            return

        try:
            # Connect to the database
            conn = connect_to_db()
            cursor = conn.cursor()

            if role == "employee":
                # Check if the username exists in the employee table
                cursor.execute("SELECT name FROM employee WHERE name = %s", (username,))
                if not cursor.fetchone():
                    messagebox.showerror("Registration Error", "Username does not exist in the employee table.")
                    return

            # Check if the username already exists in the login table
            cursor.execute("SELECT username FROM login WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Username already exists.")
                return

            # Insert the new user into the database with the selected role
            cursor.execute("INSERT INTO login (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", f"{role.capitalize()} registered successfully.")

            # Reset input fields after successful registration
            self.reset_input_fields()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def reset_input_fields(self):
        """Reset the username, password fields, and role selection."""
        self.entry_username.delete(0, tk.END)  # Clear the username field
        self.entry_password.delete(0, tk.END)  # Clear the password field
        self.role_var.set("admin")  # Reset role selection to "admin"

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Employee Attendance View Page        
class ViewAttendancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/view.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.bg_image = ImageTk.PhotoImage(self.apply_opacity(self.original_image, 0.7))  # Apply 70% opacity (0.7)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        # Configure grid layout for the entire frame
        self.grid_columnconfigure(0, weight=1)  # Left spacer
        self.grid_columnconfigure(1, weight=0)  # Center content
        self.grid_columnconfigure(2, weight=1)  # Right spacer

        # Title Label
        tk.Label(self, text="View Attendance", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=5, sticky="n")

        # Employee Dropdown
        tk.Label(self, text="Select Employee:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(self, textvariable=self.employee_var, state="readonly")
        self.employee_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.populate_employee_dropdown()

        # Date Range Picker
        tk.Label(self, text="Select Date Range:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.start_date_picker = DateEntry(self, date_pattern="yyyy-mm-dd")  # Start date picker
        self.start_date_picker.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.end_date_picker = DateEntry(self, date_pattern="yyyy-mm-dd")  # End date picker
        self.end_date_picker.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # View Attendance Button
        tk.Button(self, text="View Attendance", command=self.view_attendance).grid(row=3, column=1, pady=5)

        # Reload Button
        tk.Button(self, text="Reload", command=self.reload_data).grid(row=4, column=1, pady=5)

        # Attendance Details Table
        columns = ("ID", "Name", "Date", "Time In", "Time Out")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Back to Main Menu Button
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(AdminDashboardPage)).grid(row=6, column=0, columnspan=3, pady=10)

    def populate_employee_dropdown(self):
        """Fetch all employee names from the database and populate the dropdown"""
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM employee")  # Assuming 'employees' table has a 'name' column
            employee_names = [row[0] for row in cursor.fetchall()]
            conn.close()

            self.employee_dropdown['values'] = employee_names
            if employee_names:
                self.employee_dropdown.current(0)  # Set the first employee as default
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def view_attendance(self):
        """Fetch and display attendance records for the selected employee and date range"""
        selected_employee = self.employee_var.get()
        start_date = self.start_date_picker.get_date()
        end_date = self.end_date_picker.get_date()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM attendance 
                WHERE name = %s AND date BETWEEN %s AND %s
            """, (selected_employee, start_date, end_date))
            attendance_records = cursor.fetchall()
            conn.close()

            # Clear previous data
            for row in self.tree.get_children():
                self.tree.delete(row)

            if attendance_records:
                for record in attendance_records:
                    self.tree.insert("", "end", values=record)
            else:
                messagebox.showinfo("No Records", f"No attendance records found for {selected_employee} between {start_date} and {end_date}.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def reload_data(self):
        """Reload employee dropdown and clear attendance table"""
        # Reload employee dropdown
        self.populate_employee_dropdown()

        # Clear attendance table
        for row in self.tree.get_children():
            self.tree.delete(row)

        messagebox.showinfo("Reload", "Data reloaded successfully.")

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.apply_opacity(resized_image, 0.7))  # Reapply opacity after resizing

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)
        return image

# Employee Login to Dashboard Page        
class EmployeeDashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/admindash.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        tk.Label(self, text="Employee Dashboard", font=("Arial", 16)).pack(pady=10)

        # Employee Name Dropdown (Combobox)
        tk.Label(self, text="Select Employee:", font=("Arial", 12)).pack(pady=5)
        self.employee_var = tk.StringVar()
        self.employee_combobox = ttk.Combobox(self, textvariable=self.employee_var, font=("Arial", 12), state="readonly")
        self.employee_combobox.pack(pady=5)

        # Load employee names into the combobox
        self.load_employee_names()

        # Time In and Time Out Buttons
        self.checkin_button = tk.Button(self, text="Time In", font=("Arial", 12), command=self.check_in)
        self.checkin_button.pack(pady=10)

        self.checkout_button = tk.Button(self, text="Time Out", font=("Arial", 12), command=self.check_out)
        self.checkout_button.pack(pady=5)

        # Reload Button
        self.reload_button = tk.Button(self, text="Reload", font=("Arial", 12), command=self.reload_data)
        self.reload_button.pack(pady=10)

        # Attendance Table (Treeview)
        self.frame = tk.Frame(self)
        self.frame.pack(pady=20)

        self.attendance_table = ttk.Treeview(self.frame, columns=("Name", "Date", "Time-in", "Time-out"), show="headings")
        self.attendance_table.heading("Name", text="Name")
        self.attendance_table.heading("Date", text="Date")
        self.attendance_table.heading("Time-in", text="Time-in")
        self.attendance_table.heading("Time-out", text="Time-out")

        self.attendance_table.column("Name", width=150)
        self.attendance_table.column("Date", width=100)
        self.attendance_table.column("Time-in", width=150)
        self.attendance_table.column("Time-out", width=150)

        self.attendance_table.pack()

        # Load Data Initially
        self.load_attendance()

        # Back to Main Menu Button
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

    # Database configuration
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "",  # Leave empty if no password is set for XAMPP MySQL
        "database": "employee_management"
    }

    # Connect to MySQL database
    def get_db_connection(self):
        return mysql.connector.connect(**self.DB_CONFIG)

    def load_employee_names(self):
        """Load employee names from the database into the combobox."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM employee")  # Fetch all employee names
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Extract names from the rows and set them in the combobox
        employee_names = [row[0] for row in rows]
        self.employee_combobox["values"] = employee_names
        if employee_names:
            self.employee_combobox.current(0)  # Set the first employee as default

    def check_in(self):
        name = self.employee_var.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please select an employee!")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (name, date, time_in)
            VALUES (%s, %s, %s)
        """, (name, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", f"{name} Time in at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.load_attendance()  # Refresh the table

    def check_out(self):
        name = self.employee_var.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please select an employee!")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM attendance
            WHERE name = %s AND time_out IS NULL
        """, (name,))
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                UPDATE attendance
                SET time_out = %s
                WHERE id = %s
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result[0]))
            conn.commit()
            messagebox.showinfo("Success", f"{name} Time out at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            messagebox.showerror("Error", "Employee not Time in or already Time out.")

        cursor.close()
        conn.close()
        self.load_attendance()  # Refresh the table

    def load_attendance(self):
        """Loads attendance records into the table."""
        for row in self.attendance_table.get_children():
            self.attendance_table.delete(row)

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, date, time_in, time_out
            FROM attendance
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            self.attendance_table.insert("", "end", values=row)

    def reload_data(self):
        """Reloads both employee names and attendance records."""
        self.load_employee_names()  # Reload employee names
        self.load_attendance()  # Reload attendance records

# Admin Login To dashboard Page
class AdminDashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/admindash.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)
        
        # Add the admin buttons inside the frame using pack
        tk.Label(self, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Add Employee", command=lambda: controller.show_frame(AddEmployeePage)).pack(pady=5)
        tk.Button(self, text="Edit Employee", command=lambda: controller.show_frame(EditEmployeePage)).pack(pady=5)
        tk.Button(self, text="View Employee", command=lambda: controller.show_frame(ViewEmployeePage)).pack(pady=5)
        tk.Button(self, text="Delete Employee", command=lambda: controller.show_frame(DeleteEmployeePage)).pack(pady=5)
        tk.Button(self, text="View Attendance", command=lambda: controller.show_frame(ViewAttendancePage)).pack(pady=5)
        tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Main Menu
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load the background image
        self.original_image = Image.open("img/front.jpg").convert("RGBA")  # Convert to RGBA for transparency
        self.apply_opacity(self.original_image, 0.7)  # Apply 70% opacity (0.7)
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a label with the background image
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        # Bind window resize event to update image size
        self.bind("<Configure>", self.resize_background)

        # Center content vertically & horizontally
        self.columnconfigure(0, weight=1)  
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=1) 

        self.rowconfigure(0, weight=1) 
        self.rowconfigure(1, weight=0)  
        self.rowconfigure(2, weight=0)  
        self.rowconfigure(3, weight=1) 

        # Buttons (placed in the center without stretching)
        tk.Button(self, text="Registration", command=lambda: controller.show_frame(AdminRegistrationPage), font=("Arial", 14)).grid(row=1, column=1, pady=10)
        tk.Button(self, text="Dashboard", command=lambda: controller.show_frame(AdminLoginPage), font=("Arial", 14)).grid(row=2, column=1, pady=10)
       
    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the image while maintaining aspect ratio
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.apply_opacity(resized_image, 0.7)  # Reapply opacity after resizing
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        self.background_label.config(image=self.bg_image)
        self.background_label.image = self.bg_image  # Prevent garbage collection

    def apply_opacity(self, image, opacity):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Modify the alpha channel
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        image.putalpha(alpha)

# Main Application
class EmployeeManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.geometry("700x600")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)  # Center vertically
        container.grid_columnconfigure(0, weight=1)  # Center horizontally

        self.frames = {}
        for Page in (MainMenu, AddEmployeePage, ViewEmployeePage, EditEmployeePage, DeleteEmployeePage, EmployeeDashboardPage, AdminDashboardPage, AdminLoginPage, AdminRegistrationPage, ViewAttendancePage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# Run the Application
app = EmployeeManagementApp()
app.mainloop()