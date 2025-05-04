import tkinter as tk
from tkinter import ttk, messagebox

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Library_managment"]  


books = db['books']


lending_records = db["lending_records"]     #create collection


root = tk.Tk()
root.title("Library Management System")
root.geometry("1920x1080")

root.configure(bg="#1E1E2F")
root.bind("<Escape>", lambda e: root.destroy())


# ----------- STYLE SETUP ----------- 
def on_enter(e): e.widget['background'] = "#00BFFF"
def on_leave(e): e.widget['background'] = "#00FFC6"


# ----------- WELCOME PAGE FRAME ----------- 
welcome_frame = tk.Frame(root, bg="#1E1E2F")
welcome_frame.pack(pady=100)

title = tk.Label(welcome_frame, text="📘 Library Management System", font=("Helvetica", 60, "bold"),
                 bg="#1E1E2F", fg="#FFFFFF")
title.pack(pady=30)

button_style = {
    "font": ("Helvetica", 18),
    "bg": "#00FFC6",
    "fg": "#1E1E2F",
    "activebackground": "#00BFFF",
    "activeforeground": "#FFFFFF",
    "relief": "flat",
    "bd": 0,
    "width": 30,
    "height": 2,
    "cursor": "hand2"
}

manage_btn = tk.Button(welcome_frame, text="📚 Manage Book Collection", **button_style)



manage_btn.pack(pady=20)
manage_btn.bind("<Enter>", on_enter)
manage_btn.bind("<Leave>", on_leave)

lending_btn = tk.Button(welcome_frame, text="🔄 Lending System", **button_style)
lending_btn.config(command=lambda: (
    welcome_frame.pack_forget(),
    lending_frame.pack(fill="both", expand=True)
))

lending_btn.pack(pady=20)
lending_btn.bind("<Enter>", on_enter)
lending_btn.bind("<Leave>", on_leave)

exit_btn = tk.Button(welcome_frame, text="Exit", **button_style)

exit_btn.pack(pady=20)
exit_btn.bind("<Enter>", on_enter)
exit_btn.bind("<Leave>", on_leave)

exit_btn.config(command=root.destroy)


# ----------- MANAGE BOOKS PAGE FRAME -----------
manage_frame = tk.Frame(root, bg="#1E1E2F")

# Pack this frame full screen (only when needed)
# Don’t pack it here. It will be packed via button.

# ----------- Top Bar ----------- 
top_bar = tk.Frame( manage_frame, bg="#1E1E2F")
top_bar.pack(fill="x", side="top", anchor="n")  # sticks to top full width

# Back Button
back_to_welcome_btn_manage = tk.Button(
    top_bar, text="◁ Back to Main Page", font=("Helvetica", 12),
    bg="#FF4C4C", fg="white", relief="flat", width=18, height=1, cursor="hand2"
)
back_to_welcome_btn_manage.pack(side="left", anchor="w", padx=10, pady=10)  # top-left

# Hover effects
back_to_welcome_btn_manage.bind("<Enter>", lambda e: back_to_welcome_btn_manage.config(bg="#FF6666"))
back_to_welcome_btn_manage.bind("<Leave>", lambda e: back_to_welcome_btn_manage.config(bg="#FF4C4C"))


# Back button function
back_to_welcome_btn_manage.config(command=lambda: (
    manage_frame.pack_forget(),
    welcome_frame.pack(pady=100)
))


# ----------- ADD BOOK FORM FRAME -----------
form_frame = tk.LabelFrame(
    manage_frame, text="📚 Add New Book", bg="#1E1E2F", fg="white", font=("Helvetica", 14)
)
form_frame.pack(pady=(10, 5), padx=20, fill="x", anchor="n")


inputs = ["Title", "Author", "Genre", "Quantity"]
entries = {}

# Label and Entry widgets creation
for i, label in enumerate(inputs):
    # Label aligned to the left
    lbl = tk.Label(form_frame, text=label + ":", font=("Helvetica", 14),
                   bg="#1E1E2F", fg="#D3D3D3")
    lbl.grid(row=i, column=0, padx=30, pady=5, sticky="e")  # Use sticky="w" to align labels to the left

    # Entry aligned to the right
    ent = tk.Entry(form_frame, font=("Helvetica", 14), bg="#2D2D3A", fg="white",
                   insertbackground="white", width=80)
    ent.grid(row=i, column=1, padx=5, pady=5, sticky="w")  # Use sticky="e" to align entries to the right
    entries[label] = ent
  


# Add Book Button
def add_book():
    title = entries["Title"].get().strip()
    author = entries["Author"].get().strip()
    genre = entries["Genre"].get().strip()
    quantity = entries["Quantity"].get().strip()

    if not (title and author and genre and quantity):
        messagebox.showwarning("Missing Info", "Please fill all fields!")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity must be a number.")
        return

    book_data = {
        "Title": title,
        "Author": author,
        "Genre": genre,
        "Quantity": quantity
    }

    try:
        books.insert_one(book_data)
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        load_books_from_db()  # refresh display
        for entry in entries.values():
            entry.delete(0, tk.END)  # clear form
    except Exception as e:
        messagebox.showerror("Error", f"Could not add book: {e}")




def load_books_from_db():
    try:
        tree.delete(*tree.get_children())  # Clear tree
        all_books = books.find()

        for book in all_books:
            tree.insert("", "end", values=(
                book.get("Title", "N/A"),
                book.get("Author", "N/A"),
                book.get("Genre", "N/A"),
                book.get("Quantity", 0)
            ))
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to load books: {e}")




def delete_by_title():
    title_to_delete = search_entry.get().strip()
    if not title_to_delete:
        messagebox.showwarning("Missing Info", "Please enter a book title to delete.")
        return

    result = books.delete_one({"Title": title_to_delete})
    if result.deleted_count > 0:
        load_books_from_db()  # Refresh tree after delete
        messagebox.showinfo("Deleted", f"Book '{title_to_delete}' deleted from database!")
    else:
        messagebox.showwarning("Not Found", f"No book titled '{title_to_delete}' found.")



# ----------- DELETE BOOK BY TITLE -----------
search_label = tk.Label(form_frame, text="🔍 Enter Book Title to Delete:", font=("Helvetica", 14),
                        bg="#1E1E2F", fg="#D3D3D3")
search_label.grid(row=len(inputs)+1, column=0, padx=50, pady=5, sticky="e")

search_entry = tk.Entry(form_frame, font=("Helvetica", 14), bg="#2D2D3A", fg="white",
                        insertbackground="white", width=80)
search_entry.grid(row=len(inputs)+1, column=1, padx=10, pady=5, sticky="w")


        # Add Book Button
add_btn = tk.Button(form_frame, text="➕ Add Book", font=("Helvetica", 12),
                    bg="#00FFC6", fg="#1E1E2F", relief="flat", width=20, cursor="hand2",
                    command=add_book)
add_btn.grid(row=len(inputs), columnspan=2, pady=(10, 5), padx=(250,0))


# Delete Button
delete_btn = tk.Button(form_frame, text="❌ Delete Book", font=("Helvetica", 12),
                       bg="#FF5C58", fg="white", relief="flat", width=20, cursor="hand2",
                       command=delete_by_title)
delete_btn.grid(row=len(inputs)+2, columnspan=2, pady=(5, 5), padx=(250,0))


refresh_btn = tk.Button(form_frame, text="🔄 Refresh Books", font=("Helvetica", 12),
                        bg="#00FFC6", fg="#1E1E2F", relief="flat", width=20, cursor="hand2",
                        command=load_books_from_db)
refresh_btn.grid(row=len(inputs)+3, columnspan=2, pady=(5, 20), padx=(250,0))


# ----------- VIEW BOOKS LIST -----------
view_frame = tk.LabelFrame(
    manage_frame, text="📖 View Books", bg="#1E1E2F", fg="white", font=("Helvetica", 14)
)
view_frame.pack(pady=(5, 20), padx=20, fill="both", expand=True)


# Scrollbar + Treeview
tree_scroll = tk.Scrollbar(view_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(view_frame, columns=inputs, show="headings", yscrollcommand=tree_scroll.set)
tree.pack(fill="both", expand=True)
tree_scroll.config(command=tree.yview)

load_books_from_db()

# Style tweaks
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#1E1E2F",
                foreground="white",
                rowheight=30,
                fieldbackground="#1E1E2F")
style.map("Treeview", background=[("selected", "#00FFC6")])

for col in inputs:
    tree.heading(col, text=col)
    tree.column(col, width=150)




# ----------- LENDING SYSTEM PAGE FRAME ----------- 
lending_frame = tk.Frame(root, bg="#1E1E2F")

# ----------- Top Bar ----------- 
top_bar = tk.Frame(lending_frame, bg="#1E1E2F")
top_bar.pack(fill="x", side="top", anchor="n")  # sticks to top full width

# Back Button
back_to_welcome_btn_manage = tk.Button(
    top_bar, text="◁ Back to Main Page", font=("Helvetica", 12),
    bg="#FF4C4C", fg="white", relief="flat", width=18, height=1, cursor="hand2"
)
back_to_welcome_btn_manage.pack(side="left", anchor="w", padx=10, pady=10)  # top-left

# Hover effects
back_to_welcome_btn_manage.bind("<Enter>", lambda e: back_to_welcome_btn_manage.config(bg="#FF6666"))
back_to_welcome_btn_manage.bind("<Leave>", lambda e: back_to_welcome_btn_manage.config(bg="#FF4C4C"))

# Back button function
back_to_welcome_btn_manage.config(command=lambda: (
    lending_frame.pack_forget(),
    welcome_frame.pack(pady=100)
))



# ---------- Lending Frame Sections ----------
top_lend_frame = tk.Frame(lending_frame, bg="#1E1E2F")
top_lend_frame.pack(pady=(20, 10), fill="x")

bottom_lend_frame = tk.Frame(lending_frame, bg="#1E1E2F")
bottom_lend_frame.pack(pady=(0, 20), fill="both", expand=True)

# ---------- Form for Lending (Top Section) ---------- 
form_lend = tk.Frame(top_lend_frame, bg="#1E1E2F")
form_lend.grid(row=0, column=0, padx=20, pady=10)

lend_inputs = ["Book Title", "Borrower Name", "Borrow Date", "Return Date"]
lend_entries = {}


for i, label in enumerate(lend_inputs):
    lbl = tk.Label(form_lend, text=label + ":", font=("Helvetica", 14),
                   bg="#1E1E2F", fg="#D3D3D3")
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    ent = tk.Entry(form_lend, font=("Helvetica", 14), bg="#2D2D3A", fg="#FFFFFF",
                   insertbackground="white", width=40)
    ent.grid(row=i, column=1, padx=10, pady=5)
    lend_entries[label] = ent


# ---------- Lending Buttons (Top Section) ---------- 
lend_button_frame = tk.Frame(top_lend_frame, bg="#1E1E2F")
lend_button_frame.grid(row=0, column=1, padx=30, pady=10, sticky="n")

add_lend_btn = tk.Button(lend_button_frame, text="📤 Lend Book", font=("Helvetica", 14),
                         bg="#00FFC6", fg="#1E1E2F", relief="flat", width=20, height=2, cursor="hand2")
add_lend_btn.pack(pady=10)
add_lend_btn.bind("<Enter>", lambda e: add_lend_btn.config(bg="#00FFAA"))
add_lend_btn.bind("<Leave>", lambda e: add_lend_btn.config(bg="#00FFC6"))

update_btn = tk.Button(lend_button_frame, text="✏️ Update Return Date", font=("Helvetica", 14),
                       bg="#00FFC6", fg="#1E1E2F", relief="flat", width=20, height=2, cursor="hand2")
update_btn.pack(pady=10)
update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#00FFAA"))
update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#00FFC6"))

delete_lend_btn = tk.Button(top_lend_frame, text="❌ Delete Record", font=("Helvetica", 14),
                            bg="#FF4C4C", fg="white", relief="flat", width=20, height=2, cursor="hand2")
delete_lend_btn.grid(row=0, column=2, padx=(175, 0), pady=50, sticky="ne")

delete_lend_btn.bind("<Enter>", lambda e: delete_lend_btn.config(bg="#FF6666"))
delete_lend_btn.bind("<Leave>", lambda e: delete_lend_btn.config(bg="#FF4C4C"))



# ---------- Lending Treeview (Bottom Section) ---------- 
lend_tree = ttk.Treeview(bottom_lend_frame, columns=lend_inputs, show="headings", height=10)
lend_tree.pack(padx=20, pady=10, fill="both", expand=True)

for col in lend_inputs:
    lend_tree.heading(col, text=col)
    lend_tree.column(col, width=150)

# ---------- Load Lending Records from DB ----------
def load_lending_records():
    lend_tree.delete(*lend_tree.get_children())  # Clear Treeview
    for record in lending_records.find():
        values = [record.get(col, "") for col in lend_inputs]
        lend_tree.insert("", "end", values=values)


 #🔄 Refresh Button (correct frame assumed: top_lend_frame or form_lend)
refresh_btn_lend = tk.Button(
    lend_button_frame, text="🔄 Refresh Books", font=("Helvetica", 14),
    bg="#00FFC6", fg="#1E1E2F", relief="flat", width=20, height=2, cursor="hand2",
    command=load_lending_records
)
refresh_btn_lend.pack(pady=10)
refresh_btn_lend.bind("<Enter>", lambda e: refresh_btn_lend.config(bg="#00FFAA"))
refresh_btn_lend.bind("<Leave>", lambda e: refresh_btn_lend.config(bg="#00FFC6"))


# Call to load data when the app starts
load_lending_records()


# ---------- Lending Logic ---------- 
def insert_lending_record():
    # Collect input values
    lending_data = {lend_inputs[i]: lend_entries[lb].get() for i, lb in enumerate(lend_inputs)}
    book_title = lending_data.get("Book Title")
    
    # Check if all required fields are filled
    if all(lending_data.values()):
        # Check if the book is available in the database
        book = books.find_one({"Title": book_title})  # Query the database for the book by title
        
        if book and book.get("Quantity", 0) > 0:  # If book exists and has quantity > 0
            # Proceed with lending the book (decrease quantity in database)
            lending_records.insert_one(lending_data)  # Insert record to MongoDB
            lend_tree.insert("", "end", values=list(lending_data.values()))  # Update Treeview

            # Update the book quantity in the database
            new_quantity = book["Quantity"] - 1
            books.update_one({"Title": book_title}, {"$set": {"Quantity": new_quantity}})

            # Clear the input fields
            [lend_entries[key].delete(0, tk.END) for key in lend_entries]

            messagebox.showinfo("Success", f"The book '{book_title}' has been successfully lent!")
        else:
            # If the book is not found or not available in stock
            messagebox.showwarning("Warning", f"The book '{book_title}' is not available for lending.")
    else:
        messagebox.showwarning("Warning", "Please fill all fields!")


add_lend_btn.config(command=insert_lending_record)

def update_lending_record():
    selected_item = lend_tree.selection()
    if selected_item and lend_entries["Return Date"].get():
        lending_records.update_one(
            {"Book Title": lend_tree.item(selected_item[0], "values")[0]},  # Matching by Book Title
            {"$set": {"Return Date": lend_entries["Return Date"].get()}}
        )
        lend_tree.item(selected_item[0], values=[
            lend_tree.item(selected_item[0], "values")[0],  # Book Title
            lend_tree.item(selected_item[0], "values")[1],  # Borrower Name
            lend_tree.item(selected_item[0], "values")[2],  # Borrow Date
            lend_entries["Return Date"].get()  # Updated Return Date
        ])
        lend_entries["Return Date"].delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Select a record and enter a new return date.")

update_btn.config(command=update_lending_record)

def delete_lending_record():
    selected_item = lend_tree.selection()
    if selected_item:
        lending_records.delete_one({"Book Title": lend_tree.item(selected_item[0], "values")[0]})
        lend_tree.delete(selected_item[0])
    else:
        messagebox.showwarning("Warning", "No record selected!")

delete_lend_btn.config(command=delete_lending_record)


# ----------- SWITCH PAGE LOGIC ----------- 
manage_btn.config(command=lambda: (
    welcome_frame.pack_forget(),
    manage_frame.pack(fill="both", expand=True)
))

# Show welcome message


# Run it all
root.mainloop()
