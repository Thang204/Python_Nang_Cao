import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from datetime import datetime
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đăng nhập Hệ thống")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection variables
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        
        self.create_login_widgets()

    def create_login_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        title_label = ttk.Label(main_frame, text="ĐĂNG NHẬP HỆ THỐNG", 
                               font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Connection fields
        ttk.Label(main_frame, text="Tên Database:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.db_name, width=25).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Username:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.user, width=25).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.password, show="*", width=25).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Host:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.host, width=25).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Port:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.port, width=25).grid(row=5, column=1, padx=5, pady=5)

        # Login button
        style = ttk.Style()
        style.configure('Custom.TButton', padding=5)
        login_btn = ttk.Button(main_frame, text="Đăng nhập", style='Custom.TButton',
                             command=self.login)
        login_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def login(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.root.destroy()
            CustomerManagementSystem(conn)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đăng nhập thất bại: {e}")

class CustomerManagementSystem:
    def __init__(self, conn):
        self.root = tk.Tk()
        self.root.title("Quản lý Thông tin Khách hàng")
        self.root.geometry("1000x600")
        self.conn = conn
        self.cur = conn.cursor()
        
        # Create customer table if not exists
        self.create_customer_table()
        
        self.create_gui()

    def create_customer_table(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo bảng: {e}")

    def create_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f0f0f0')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10", style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="QUẢN LÝ THÔNG TIN KHÁCH HÀNG",
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0,20))

        # Customer list
        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Tên', 'SĐT', 'Email', 'Địa chỉ', 'Ngày tạo'),
                                show='headings', height=15)
        
        # Column headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên', text='Tên khách hàng')
        self.tree.heading('SĐT', text='Số điện thoại')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Địa chỉ', text='Địa chỉ')
        self.tree.heading('Ngày tạo', text='Ngày tạo')
        
        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Tên', width=150)
        self.tree.column('SĐT', width=100)
        self.tree.column('Email', width=150)
        self.tree.column('Địa chỉ', width=200)
        self.tree.column('Ngày tạo', width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, fill=tk.X)

        ttk.Button(button_frame, text="Thêm khách hàng", command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sửa thông tin", command=self.open_edit_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa khách hàng", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.load_customers).pack(side=tk.LEFT, padx=5)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10, fill=tk.X)

        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_customers).pack(side=tk.LEFT, padx=5)

        # Load initial data
        self.load_customers()

    def load_customers(self):
        try:
            self.cur.execute("SELECT * FROM customers ORDER BY id")
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                # Format datetime
                created_date = row[5].strftime('%Y-%m-%d %H:%M:%S')
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], created_date))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def open_add_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm Khách hàng")
        add_window.geometry("400x300")

        # Create form fields
        ttk.Label(add_window, text="Tên khách hàng:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Số điện thoại:").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(add_window, width=30)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(add_window, width=30)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Địa chỉ:").grid(row=3, column=0, padx=5, pady=5)
        address_entry = ttk.Entry(add_window, width=30)
        address_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_customer():
            try:
                self.cur.execute("""
                    INSERT INTO customers (name, phone, email, address)
                    VALUES (%s, %s, %s, %s)
                """, (name_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get()))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã thêm khách hàng mới!")
                add_window.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm khách hàng: {e}")

        ttk.Button(add_window, text="Lưu", command=save_customer).grid(row=4, column=0, columnspan=2, pady=20)

    def open_edit_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần sửa")
            return

        item = self.tree.item(selected_item)
        values = item['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa Thông tin Khách hàng")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Tên khách hàng:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.insert(0, values[1])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Số điện thoại:").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(edit_window, width=30)
        phone_entry.insert(0, values[2])
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(edit_window, width=30)
        email_entry.insert(0, values[3])
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Địa chỉ:").grid(row=3, column=0, padx=5, pady=5)
        address_entry = ttk.Entry(edit_window, width=30)
        address_entry.insert(0, values[4])
        address_entry.grid(row=3, column=1, padx=5, pady=5)

        def update_customer():
            try:
                self.cur.execute("""
                    UPDATE customers 
                    SET name=%s, phone=%s, email=%s, address=%s
                    WHERE id=%s
                """, (name_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get(), values[0]))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng!")
                edit_window.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin: {e}")

        ttk.Button(edit_window, text="Cập nhật", command=update_customer).grid(row=4, column=0, columnspan=2, pady=20)

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?"):
            try:
                item = self.tree.item(selected_item)
                customer_id = item['values'][0]
                self.cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
                self.load_customers()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa khách hàng: {e}")

    def search_customers(self):
        search_term = self.search_var.get()
        try:
            self.cur.execute("""
                SELECT * FROM customers 
                WHERE name ILIKE %s 
                OR phone ILIKE %s 
                OR email ILIKE %s 
                OR address ILIKE %s
            """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                created_date = row[5].strftime('%Y-%m-%d %H:%M:%S')
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], created_date))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")

if __name__ == "__main__":
    login = LoginWindow()
    login.root.mainloop()