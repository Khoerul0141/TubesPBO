import tkinter as tk
from tkinter import simpledialog, messagebox
from enum import Enum
import json
from datetime import datetime

class UserRole:
    KASIR = "kasir"
    MANAGER = "manager"

class DialogType(Enum):
    INFO = "info"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Menu:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        self.total_sales = 0

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, menu, quantity):
        self.items.append({"menu": menu, "quantity": quantity})
        menu.total_sales += quantity

class CashierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Kasir dan Manajer")

        self.load_data()  # Load existing data

        self.current_user = None
        self.order = None
        self.create_login_page()

    def load_data(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.users = [User(**user_data) for user_data in data.get("users", [])]
                self.menus = [Menu(**menu_data) for menu_data in data.get("menus", [])]
        except FileNotFoundError:
            # If the file doesn't exist, initialize with default data
            self.users = [
                User("kasir", "kasir123", UserRole.KASIR),
                User("manager", "manager123", UserRole.MANAGER)
            ]

            self.menus = [
                Menu("Es Teh", 3, 30),
                Menu("Espresso", 10, 20),
                Menu("Americano", 12, 15),
                Menu("Latte", 18, 10),
            ]

    def save_data(self):
        data = {
            "users": [{"username": user.username, "password": user.password, "role": user.role} for user in self.users],
            "menus": [{"name": menu.name, "price": menu.price, "stock": menu.stock, "total_sales": menu.total_sales} for menu in self.menus]
        }
        with open("data.json", "w") as file:
            json.dump(data, file, indent=2)





    def create_login_page(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=200, pady=200)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                self.login_frame.destroy()
                self.create_dashboard()

    def create_dashboard(self):
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(padx=20, pady=20)

        tk.Label(self.dashboard_frame, text=f"Selamat datang, {self.current_user.username}!").pack()

        if self.current_user.role == UserRole.KASIR:
            self.create_kasir_page()
        elif self.current_user.role == UserRole.MANAGER:
            self.create_manager_page()

    def create_kasir_page(self):
        tk.Label(self.dashboard_frame, text="Fitur Kasir").pack()

        tk.Button(self.dashboard_frame, text="Lihat Menu Terlaris", command=self.lihat_menu_terlaris).pack()
        tk.Button(self.dashboard_frame, text="Lihat Stok Menu", command=self.lihat_stok_menu).pack()
        tk.Button(self.dashboard_frame, text="Lihat Harga Menu", command=self.lihat_harga_menu).pack()
        tk.Button(self.dashboard_frame, text="Tambah Pesanan", command=self.tambah_pesanan).pack()
        tk.Button(self.dashboard_frame, text="Lihat Harga Total Pesanan", command=self.lihat_harga_total).pack()

    def lihat_menu_terlaris(self):
        sorted_menus = sorted(self.menus, key=lambda x: x.total_sales, reverse=True)
        popular_menu = sorted_menus[0] if sorted_menus else None
        if popular_menu:
            messagebox.showinfo("Menu Terlaris", f"{popular_menu.name} adalah menu terlaris dengan total penjualan {popular_menu.total_sales}")
        else:
            messagebox.showinfo("Menu Terlaris", "Belum ada penjualan untuk menentukan menu terlaris.")

    def lihat_stok_menu(self):
        stok_info = "\n".join([f"{menu.name}: {menu.stock} pcs" for menu in self.menus])
        messagebox.showinfo("Stok Menu", stok_info)

    def lihat_harga_menu(self):
        menu_names = [menu.name for menu in self.menus]
        selected_menu = self.show_menu_selection(menu_names, "Pilih Menu")
        if selected_menu:
            menu = next((menu for menu in self.menus if menu.name == selected_menu), None)
            messagebox.showinfo("Harga Menu", f"{menu.name} memiliki harga Rp{menu.price} per porsi.")
 
    def tambah_pesanan(self):
        self.order = Order()
        for menu in self.menus:
            quantity = self.show_quantity_dialog(menu)
            if quantity:
                self.order.add_item(menu, quantity)
                menu.stock -= quantity
        messagebox.showinfo("Pemesanan", "Pesanan berhasil ditambahkan.")

    def lihat_harga_total(self):
        if self.order:
            total_harga = sum(item["menu"].price * item["quantity"] for item in self.order.items)
            messagebox.showinfo("Harga Total Pesanan", f"Harga total pesanan adalah Rp{total_harga}.")
        else:
            messagebox.showinfo("Harga Total Pesanan", "Anda belum menambahkan pesanan.")

    def show_menu_selection(self, menu_names, title):
        selected_menu = simpledialog.askstring(title, "Pilih menu:", parent=self.root, items=menu_names)
        return selected_menu

    def show_quantity_dialog(self, menu):
        quantity = simpledialog.askinteger("Pesan Menu", f"Pesan {menu.name} (Stok: {menu.stock}):", parent=self.root, minvalue=0, maxvalue=menu.stock)
        return quantity

    def create_manager_page(self):
        tk.Label(self.dashboard_frame, text="Fitur Manager").pack()

        tk.Button(self.dashboard_frame, text="Tambah Stok Menu", command=self.tambah_stok_menu).pack()
        tk.Button(self.dashboard_frame, text="Tambah Menu", command=self.tambah_menu).pack()
        tk.Button(self.dashboard_frame, text="Hapus Menu", command=self.hapus_menu).pack()
        tk.Button(self.dashboard_frame, text="Lihat Menu Terlaris", command=self.lihat_menu_terlaris_manager).pack()
        tk.Button(self.dashboard_frame, text="Lihat Riwayat Penjualan", command=self.lihat_riwayat_penjualan).pack()
        tk.Button(self.dashboard_frame, text="Lihat Ringkasan Penjualan Hari Ini", command=self.lihat_ringkasan_penjualan_hari_ini).pack()

    def tambah_stok_menu(self):
        menu_names = [menu.name for menu in self.menus]
        selected_menu = self.show_menu_selection(menu_names, "Tambah Stok Menu")
        if selected_menu:
            menu = next((menu for menu in self.menus if menu.name == selected_menu), None)
            additional_stock = self.show_additional_stock_dialog(menu)
            if additional_stock:
                menu.stock += additional_stock
                messagebox.showinfo("Tambah Stok Menu", f"Stok untuk {menu.name} ditambahkan sebanyak {additional_stock} pcs.")

    def tambah_menu(self):
        menu_name = simpledialog.askstring("Tambah Menu", "Masukkan nama menu baru:", parent=self.root)
        if menu_name:
            menu_price = self.show_price_dialog("Tambah Menu", "Masukkan harga menu baru (Rp):")
            if menu_price:
                menu_stock = self.show_stock_dialog("Tambah Menu", "Masukkan stok menu baru:")
                if menu_stock:
                    new_menu = Menu(menu_name, menu_price, menu_stock)
                    self.menus.append(new_menu)
                    messagebox.showinfo("Tambah Menu", f"Menu {menu_name} ditambahkan.")

    def hapus_menu(self):
        menu_names = [menu.name for menu in self.menus]
        selected_menu = self.show_menu_selection(menu_names, "Hapus Menu")
        if selected_menu:
            self.menus = [menu for menu in self.menus if menu.name != selected_menu]
            messagebox.showinfo("Hapus Menu", f"Menu {selected_menu} berhasil dihapus.")

    def lihat_menu_terlaris_manager(self):
        sorted_menus = sorted(self.menus, key=lambda x: x.total_sales, reverse=True)
        popular_menu = sorted_menus[0] if sorted_menus else None
        if popular_menu:
            messagebox.showinfo("Menu Terlaris", f"{popular_menu.name} adalah menu terlaris dengan total penjualan {popular_menu.total_sales}")
        else:
            messagebox.showinfo("Menu Terlaris", "Belum ada penjualan untuk menentukan menu terlaris.")

    def lihat_riwayat_penjualan(self):
        sales_info = "\n".join([f"{menu.name}: {menu.total_sales}" for menu in self.menus])
        messagebox.showinfo("Riwayat Penjualan", f"Riwayat Penjualan:\n{sales_info}")

    def lihat_ringkasan_penjualan_hari_ini(self):
        today = datetime.today().strftime("%Y-%m-%d")
        daily_sales = sum(menu.total_sales for menu in self.menus)
        messagebox.showinfo("Ringkasan Penjualan Hari Ini", f"Total penjualan hari ini ({today}): Rp{daily_sales}.")

    def show_price_dialog(self, title, prompt):
        menu_price = simpledialog.askinteger(title, prompt, parent=self.root, minvalue=0)
        return menu_price

    def show_stock_dialog(self, title, prompt):
        menu_stock = simpledialog.askinteger(title, prompt, parent=self.root, minvalue=0)
        return menu_stock

    def show_additional_stock_dialog(self, menu):
        additional_stock = simpledialog.askinteger("Tambah Stok Menu", f"Tambahkan stok untuk {menu.name}:", parent=self.root, minvalue=0)
        return additional_stock

root = tk.Tk()
app = CashierApp(root)
root.protocol("WM_DELETE_WINDOW", app.save_data)
root.mainloop()







