import tkinter as tk
from tkinter import ttk, messagebox
from data.data_handler import DataManager

# Bảng màu mới theo mẫu Vibrant Visuals
PRIMARY_COLOR = "#FFA726"  # Cam sáng
SECONDARY_COLOR = "#FF9800"  # Cam đậm
BG_COLOR = "#FFF3E0"  # Vàng nhạt
CARD_COLOR = "#FFFFFF"  # Card trắng
BORDER_COLOR = "#ECECEC"  # Xám nhạt
TEXT_COLOR = "#222222"
PASTEL_BLUE = "#81D4FA"
PASTEL_PINK = "#F8BBD0"
PASTEL_PURPLE = "#CE93D8"
PASTEL_GREEN = "#A5D6A7"
RED = "#E57373"

class ECommerceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Quản Lý Bán Hàng")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)

        self.data_manager = DataManager()
        self.filtered_products = []
        self.current_page = None

        self.create_gui()

    def create_gui(self):
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        nav_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, height=60)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.home_btn = tk.Button(nav_frame, text="🏠 Trang Chủ", command=self.show_home, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 13, "bold"), bd=0, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR)
        self.home_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)

        self.profile_btn = tk.Button(nav_frame, text="👤 Tôi", command=self.show_profile, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 13, "bold"), bd=0, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR)
        self.profile_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)

        self.show_home()

    def update_nav_buttons(self):
        self.home_btn.config(bg=SECONDARY_COLOR if self.current_page == "home" else PRIMARY_COLOR)
        self.profile_btn.config(bg=SECONDARY_COLOR if self.current_page == "profile" else PRIMARY_COLOR)

    def show_home(self):
        self.current_page = "home"
        self.update_nav_buttons()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        top_frame = tk.Frame(self.main_frame, bg=PRIMARY_COLOR, height=60)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        search_frame = tk.Frame(top_frame, bg=PRIMARY_COLOR)
        search_frame.pack(side=tk.LEFT, padx=20, pady=10)

        self.search_entry = tk.Entry(search_frame, width=40, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        self.search_entry.delete(0, tk.END)
        self.search_entry.pack(side=tk.LEFT, ipady=6)
        self.search_entry.bind("<Return>", self.filter_products)

        search_btn = tk.Button(search_frame, text="🔍", command=self.filter_products, bg=CARD_COLOR, fg=PRIMARY_COLOR, font=("Segoe UI", 13, "bold"), bd=0, padx=10, pady=6)
        search_btn.pack(side=tk.LEFT, padx=8)

        cart_btn = tk.Button(top_frame, text="🛒 Giỏ Hàng", command=self.show_cart, bg=CARD_COLOR, fg=PRIMARY_COLOR, font=("Segoe UI", 12, "bold"), bd=0, padx=10, pady=2)
        cart_btn.pack(side=tk.RIGHT, padx=20)

        message_btn = tk.Button(top_frame, text="🔔 Thông báo", command=self.show_messages, bg=CARD_COLOR, fg=PRIMARY_COLOR, font=("Segoe UI", 12, "bold"), bd=0, padx=10, pady=2)
        message_btn.pack(side=tk.RIGHT, padx=10)

        product_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(product_frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_combined_products()
        self.display_products()

    def load_combined_products(self):
        self.filtered_products = self.data_manager.main_products.copy()
        for user, products in self.data_manager.user_products.items():
            for product in products:
                product_copy = product.copy()
                product_copy['booth'] = user
                self.filtered_products.append(product_copy)

    def display_products(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.filtered_products:
            tk.Label(self.scrollable_frame, text="Không tìm thấy sản phẩm!", bg=BG_COLOR, font=("Segoe UI", 15, "bold"), fg=RED).grid(row=0, column=0, padx=10, pady=10)
        else:
            for i, product in enumerate(self.filtered_products):
                frame = tk.Frame(self.scrollable_frame, bg=CARD_COLOR, relief=tk.RAISED, borderwidth=1, highlightbackground=BORDER_COLOR, highlightthickness=1)
                frame.grid(row=i//3, column=i%3, padx=18, pady=18, sticky="nsew")
                frame.grid_propagate(False)
                frame.config(width=240, height=180)

                label = tk.Label(frame, text=f"{product['name']}", bg=CARD_COLOR, font=("Segoe UI", 13, "bold"), fg=TEXT_COLOR)
                label.pack(pady=(18, 4))
                price = tk.Label(frame, text=f"{product['price']:,} VNĐ", bg=CARD_COLOR, font=("Segoe UI", 12), fg=PRIMARY_COLOR)
                price.pack()
                booth = tk.Label(frame, text=f"Gian hàng: {product['booth']}", bg=CARD_COLOR, font=("Segoe UI", 10), fg=TEXT_COLOR)
                booth.pack(pady=(0, 10))

                add_btn = tk.Button(frame, text="Thêm vào giỏ", command=lambda p=product: self.add_to_cart(p), bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=PRIMARY_COLOR, activeforeground=TEXT_COLOR, cursor="hand2")
                add_btn.pack(pady=(0, 10))

    def filter_products(self, event=None):
        keyword = self.search_entry.get().strip().lower()
        self.load_combined_products()
        if keyword:
            self.filtered_products = [p for p in self.filtered_products if keyword in p['name'].lower() or keyword in p['booth'].lower()]
        self.display_products()

    def show_cart(self):
        self.current_page = None
        self.update_nav_buttons()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        cart_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        cart_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(cart_frame, text="🛒 Giỏ Hàng", bg=PRIMARY_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=10)

        cart = self.data_manager.carts.get(self.data_manager.current_user, []) if self.data_manager.current_user else []
        if not cart:
            tk.Label(cart_frame, text="Giỏ hàng trống", bg=BG_COLOR, font=("Segoe UI", 14), fg=RED).pack(pady=20)
        else:
            for i, item in enumerate(cart):
                frame = tk.Frame(cart_frame, bg=CARD_COLOR)
                frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(frame, text=f"{item['name']} - {item['price']} VNĐ (Gian hàng: {item['booth']})", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(side=tk.LEFT)

                buy_btn = tk.Button(frame, text="Mua", command=lambda idx=i: self.buy_single_product(idx), bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=5, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR, cursor="hand2")
                buy_btn.pack(side=tk.RIGHT, padx=5)

                remove_btn = tk.Button(frame, text="Xóa", command=lambda idx=i: self.remove_from_cart(idx), bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=5, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR, cursor="hand2")
                remove_btn.pack(side=tk.RIGHT, padx=5)

        buy_all_btn = tk.Button(cart_frame, text="Mua Tất Cả", command=self.buy_products, width=15, height=2, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=10, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR, cursor="hand2")
        buy_all_btn.pack(side='right', anchor='se', pady=10, padx=10)

    def buy_single_product(self, index):
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để mua hàng!")
            self.show_profile()
            return
        cart = self.data_manager.carts.get(self.data_manager.current_user, [])
        if index >= len(cart):
            return

        product = cart[index]
        dialog = tk.Toplevel(self.root)
        dialog.title="Xác Nhận Mua Hàng"
        dialog.geometry("400x300")
        dialog.configure(bg=BG_COLOR)

        tk.Label(dialog, text=f"Mua sản phẩm: {product['name']}", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=10)
        tk.Label(dialog, text=f"Giá: {product['price']} VNĐ", bg=BG_COLOR, fg=PRIMARY_COLOR).pack()
        tk.Label(dialog, text=f"Gian hàng: {product['booth']}", bg=BG_COLOR, fg=PRIMARY_COLOR).pack()

        tk.Label(dialog, text="Số lượng", bg=BG_COLOR).pack()
        quantity_entry = tk.Entry(dialog, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        quantity_entry.pack(pady=5, ipady=6)
        quantity_entry.insert(0, "1")

        tk.Label(dialog, text="Địa chỉ giao hàng", bg=BG_COLOR).pack()
        address_entry = tk.Entry(dialog, width=40, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        address_entry.pack(pady=5, ipady=6)

        total_label = tk.Label(dialog, text="Tổng tiền: 0 VNĐ", bg=BG_COLOR)
        total_label.pack(pady=10)

        def update_total():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
                total = product['price'] * quantity
                total_label.config(text=f"Tổng tiền: {total:,} VNĐ")
            except ValueError:
                total_label.config(text="Tổng tiền: Vui lòng nhập số lượng hợp lệ")

        quantity_entry.bind("<KeyRelease>", lambda e: update_total())
        update_total()

        def confirm_purchase():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương!")
                return
            address = address_entry.get().strip()
            if not address:
                messagebox.showerror("Lỗi", "Vui lòng nhập địa chỉ giao hàng!")
                return

            self.data_manager.buy_single_product(product, quantity, address)
            cart.pop(index)
            self.data_manager.carts[self.data_manager.current_user] = cart
            self.data_manager.save_carts()

            messagebox.showinfo("Thành công", f"Đã mua {product['name']} ({quantity} cái)!")
            dialog.destroy()
            self.show_cart()

        tk.Button(dialog, text="Xác Nhận", command=confirm_purchase, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)
        tk.Button(dialog, text="Hủy", command=dialog.destroy, bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)

    def buy_products(self):
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để mua hàng!")
            self.show_profile()
            return
        cart = self.data_manager.carts.get(self.data_manager.current_user, []) if self.data_manager.current_user else []
        if not cart:
            messagebox.showerror("Lỗi", "Giỏ hàng trống!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title="Xác Nhận Mua Tất Cả"
        dialog.geometry("400x400")
        dialog.configure(bg=BG_COLOR)

        tk.Label(dialog, text="Mua tất cả sản phẩm trong giỏ hàng", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=10)

        quantities = []
        total_label = tk.Label(dialog, text="Tổng tiền: 0 VNĐ", bg=BG_COLOR)
        total_label.pack(pady=10)

        for item in cart:
            frame = tk.Frame(dialog, bg=BG_COLOR)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=f"{item['name']} - {item['price']} VNĐ (Gian hàng: {item['booth']})", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(side=tk.LEFT)
            quantity_entry = tk.Entry(frame, width=5, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            quantity_entry.pack(side=tk.LEFT, padx=5)
            quantity_entry.insert(0, "1")
            quantities.append(quantity_entry)

        tk.Label(dialog, text="Địa chỉ giao hàng", bg=BG_COLOR).pack()
        address_entry = tk.Entry(dialog, width=40, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        address_entry.pack(pady=5)

        def update_total():
            try:
                total = 0
                for i, entry in enumerate(quantities):
                    quantity = int(entry.get())
                    if quantity <= 0:
                        raise ValueError
                    total += cart[i]['price'] * quantity
                total_label.config(text=f"Tổng tiền: {total:,} VNĐ")
            except ValueError:
                total_label.config(text="Tổng tiền: Vui lòng nhập số lượng hợp lệ")

        for entry in quantities:
            entry.bind("<KeyRelease>", lambda e: update_total())
        update_total()

        def confirm_purchase():
            try:
                for entry in quantities:
                    quantity = int(entry.get())
                    if quantity <= 0:
                        raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương!")
                return
            address = address_entry.get().strip()
            if not address:
                messagebox.showerror("Lỗi", "Vui lòng nhập địa chỉ giao hàng!")
                return

            for i, item in enumerate(cart):
                quantity = int(quantities[i].get())
                self.data_manager.buy_single_product(item, quantity, address)

            self.data_manager.carts[self.data_manager.current_user] = []
            self.data_manager.save_carts()
            messagebox.showinfo("Thành công", "Đã mua tất cả sản phẩm!")
            dialog.destroy()
            self.show_cart()

        tk.Button(dialog, text="Xác Nhận", command=confirm_purchase, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)
        tk.Button(dialog, text="Hủy", command=dialog.destroy, bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)

    def remove_from_cart(self, index):
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để xóa sản phẩm!")
            self.show_profile()
            return
        if self.data_manager.remove_from_cart(index):
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm khỏi giỏ hàng!")
            self.show_cart()

    def add_to_cart(self, product):
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng!")
            self.show_profile()
            return
        self.data_manager.add_to_cart(product)
        messagebox.showinfo("Thành công", f"Đã thêm {product['name']} vào giỏ hàng!")

    def show_messages(self):
        self.current_page = None
        self.update_nav_buttons()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        messages_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        messages_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(messages_frame, text="🔔 Thông báo", bg=PRIMARY_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=10)

        messages = self.data_manager.messages.get(self.data_manager.current_user, []) if self.data_manager.current_user else []
        if not messages:
            tk.Label(messages_frame, text="Chưa có thông báo nào!", bg=BG_COLOR, font=("Segoe UI", 14), fg=RED).pack(pady=20)
        else:
            for i, msg in enumerate(messages):
                frame = tk.Frame(messages_frame, bg=CARD_COLOR)
                frame.pack(fill=tk.X, padx=10, pady=5)
                tk.Label(frame, text=msg, bg=CARD_COLOR, font=("Segoe UI", 13), fg=TEXT_COLOR, wraplength=700, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
                btn = tk.Button(frame, text="✕", command=lambda idx=i: self.delete_single_message(idx), bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=8, pady=2, activebackground=RED, activeforeground=TEXT_COLOR, cursor="hand2")
                btn.pack(side=tk.RIGHT, padx=4)

    def delete_single_message(self, idx):
        if not self.data_manager.current_user or not self.data_manager.messages.get(self.data_manager.current_user):
            return
        del self.data_manager.messages[self.data_manager.current_user][idx]
        self.data_manager.save_messages()
        self.show_messages()

    def show_reviews(self):
        self.current_page = None
        self.update_nav_buttons()
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để đánh giá sản phẩm!")
            self.show_profile()
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        reviews_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        reviews_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(reviews_frame, text="Đánh Giá Sản Phẩm", bg=PRIMARY_COLOR, font=("Segoe UI", 24, "bold"), fg=TEXT_COLOR).pack(pady=20)

        orders = self.data_manager.orders.get(self.data_manager.current_user, [])
        if not orders:
            tk.Label(reviews_frame, text="Chưa có sản phẩm nào để đánh giá!", bg=BG_COLOR, font=("Segoe UI", 14), fg=RED).pack(pady=20)
            return

        tk.Label(reviews_frame, text="Chọn sản phẩm:", bg=BG_COLOR, font=("Segoe UI", 16)).pack(pady=10)
        product_names = [order['product']['name'] for order in orders]
        product_var = tk.StringVar()

        # Tăng font-size cho Combobox
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Segoe UI", 15), padding=8)
        style.map("Custom.TCombobox", fieldbackground=[('readonly', 'white')])

        product_dropdown = ttk.Combobox(
            reviews_frame,
            textvariable=product_var,
            values=product_names,
            state="readonly",
            font=("Segoe UI", 15),
            style="Custom.TCombobox"
        )
        product_dropdown.pack(pady=10, ipady=6, ipadx=10)

        stars_frame = tk.Frame(reviews_frame, bg=BG_COLOR)
        stars_frame.pack(pady=10)

        def update_stars():
            selected_product = product_var.get()
            if not selected_product:
                return
            selected_order = next((o for o in orders if o['product']['name'] == selected_product), None)
            if not selected_order:
                return
            product = selected_order['product']
            user_reviews = self.data_manager.reviews.get(self.data_manager.current_user, [])
            current_rating = next((r['rating'] for r in user_reviews if r['product_id'] == product['id']), 0)

            for widget in stars_frame.winfo_children():
                widget.destroy()

            star_labels = []
            for j in range(5):
                star = tk.Label(stars_frame, text="★", font=("Segoe UI", 16, "bold"), fg="blue" if j >= current_rating else "Gold", bg=BG_COLOR)
                star.pack(side=tk.LEFT)
                star.bind("<Enter>", lambda e, idx=j: self.highlight_stars(star_labels, idx + 1))
                star.bind("<Leave>", lambda e: self.highlight_stars(star_labels, current_rating))
                star.bind("<Button-1>", lambda e, idx=j, prod=product: self.submit_review(prod, idx + 1))
                star_labels.append(star)

        product_dropdown.bind("<<ComboboxSelected>>", lambda e: update_stars())

    def highlight_stars(self, star_labels, num_stars):
        for i, star in enumerate(star_labels):
            star.config(fg="Gold" if i < num_stars else "black")

    def submit_review(self, product, rating):
        if self.data_manager.submit_review(product, rating):
            messagebox.showinfo("Thành công", f"Đã đánh giá {product['name']}: {rating} sao")
            self.show_reviews()

    def show_settings(self):
        self.current_page = None
        self.update_nav_buttons()
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để vào cài đặt!")
            self.show_profile()
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        settings_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(settings_frame, text="🛠 Cài Đặt", bg=PRIMARY_COLOR, font=("Segoe UI", 18, "bold"), fg=TEXT_COLOR).pack(pady=10)

        tk.Label(settings_frame, text="Thay Đổi Mật Khẩu", bg=BG_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=5)
        tk.Label(settings_frame, text="Mật khẩu cũ", bg=BG_COLOR).pack()
        old_password_entry = tk.Entry(settings_frame, show="*", font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        old_password_entry.pack(pady=5, ipady=6)

        tk.Label(settings_frame, text="Mật khẩu mới", bg=BG_COLOR).pack()
        new_password_entry = tk.Entry(settings_frame, show="*", font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        new_password_entry.pack(pady=5, ipady=6)

        tk.Label(settings_frame, text="Xác nhận mật khẩu mới", bg=BG_COLOR).pack()
        confirm_password_entry = tk.Entry(settings_frame, show="*", font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        confirm_password_entry.pack(pady=5, ipady=6)

        tk.Button(settings_frame, text="Thay Đổi", command=lambda: self.change_password(
            old_password_entry.get(), new_password_entry.get(), confirm_password_entry.get()
        ), bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 14, "bold"), bd=0, padx=10, pady=8, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)

        tk.Label(settings_frame, text="Xóa Tài Khoản", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
        tk.Button(settings_frame, text="Xóa Tài Khoản", command=self.delete_account, bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)

    def change_password(self, old_password, new_password, confirm_password):
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp!")
            return

        success, message = self.data_manager.change_password(old_password, new_password)
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)
        self.show_settings()

    def delete_account(self):
        if messagebox.askyesno("Xác Nhận", "Bạn có chắc chắn muốn xóa tài khoản? Tất cả dữ liệu sẽ bị xóa!"):
            if self.data_manager.delete_account():
                messagebox.showinfo("Thành công", "Tài khoản đã được xóa!")
                self.show_profile()

    def show_selling(self):
        self.current_page = None
        self.update_nav_buttons()
        if not self.data_manager.current_user:
            messagebox.showerror("Lỗi", "Vui lòng đăng nhập để bán hàng!")
            self.show_profile()
            return
    
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
        selling_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        selling_frame.pack(fill=tk.BOTH, expand=True)
    
        tk.Label(selling_frame, text="Bán Hàng", bg=PRIMARY_COLOR, font=("Segoe UI", 18, "bold"), fg=TEXT_COLOR).pack(pady=10)
    
        tk.Label(selling_frame, text="Đăng Sản Phẩm Mới", bg=BG_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=5)
        tk.Label(selling_frame, text="Tên sản phẩm", bg=BG_COLOR).pack()
        name_entry = tk.Entry(selling_frame, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        name_entry.pack(pady=5)
    
        tk.Label(selling_frame, text="Giá (VNĐ)", bg=BG_COLOR).pack()
        price_entry = tk.Entry(selling_frame, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        price_entry.pack(pady=5)
    
        tk.Button(
            selling_frame,
            text="Đăng Sản Phẩm",
            command=lambda: self.add_user_product(name_entry.get(), price_entry.get()),
            bg=PRIMARY_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 14, "bold"),
            bd=0,
            padx=10,
            pady=8,
            activebackground=SECONDARY_COLOR,
            activeforeground=TEXT_COLOR,
            cursor="hand2"
        ).pack(pady=10)
    
        tk.Label(selling_frame, text="Thống Kê Doanh Thu", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    
        user_prods = self.data_manager.user_products.get(self.data_manager.current_user, [])
        user_orders = self.data_manager.user_orders.get(self.data_manager.current_user, [])
        total_revenue = 0
    
        for prod in user_prods:
            prod_orders = [o for o in user_orders if o['product_id'] == prod['id']]
            total_quantity = sum(o['quantity'] for o in prod_orders)
            total_price = sum(o['total_price'] for o in prod_orders)
            total_revenue += total_price
    
            tk.Label(
                selling_frame,
                text=f"{prod['name']}: {total_quantity} sản phẩm, {total_price:,} VNĐ",
                bg=BG_COLOR,
                font=("Segoe UI", 12, "bold"),
                fg=TEXT_COLOR,
                anchor='w'
            ).pack(fill='x', padx=10)
    
        revenue_frame = tk.Frame(selling_frame, bg=BG_COLOR)
        revenue_frame.pack(fill='x', padx=10, pady=5)
    
        tk.Label(
            revenue_frame,
            text=f"Tổng doanh thu: {total_revenue:,} VNĐ",
            bg=BG_COLOR,
            font=("Segoe UI", 12, "bold"),
            fg=TEXT_COLOR,
            anchor='e'
        ).pack(fill='x')
    
        tk.Label(selling_frame, text="Sản Phẩm Đã Đăng", bg=BG_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    
        if not user_prods:
            tk.Label(selling_frame, text="Chưa có sản phẩm nào!", bg=BG_COLOR, font=("Segoe UI", 14), fg=RED).pack(pady=20)
        else:
            for i, prod in enumerate(user_prods):
                frame = tk.Frame(selling_frame, bg=CARD_COLOR)
                frame.pack(fill=tk.X, padx=10, pady=5)
    
                tk.Label(
                    frame,
                    text=f"{prod['name']} - {prod['price']} VNĐ",
                    bg=BG_COLOR,
                    font=("Segoe UI", 12, "bold"),
                    fg=TEXT_COLOR
                ).pack(side=tk.LEFT)
    
                edit_btn = tk.Button(
                    frame,
                    text="Sửa",
                    command=lambda idx=i: self.edit_user_product(idx),
                    bg=PRIMARY_COLOR,
                    fg=TEXT_COLOR,
                    font=("Segoe UI", 11, "bold"),
                    bd=0,
                    padx=5,
                    pady=4,
                    activebackground=SECONDARY_COLOR,
                    activeforeground=TEXT_COLOR,
                    cursor="hand2"
                )
                edit_btn.pack(side=tk.RIGHT, padx=5)
    
                remove_btn = tk.Button(
                    frame,
                    text="Gỡ",
                    command=lambda idx=i: self.remove_user_product(idx),
                    bg=RED,
                    fg=TEXT_COLOR,
                    font=("Segoe UI", 11, "bold"),
                    bd=0,
                    padx=5,
                    pady=4,
                    activebackground=SECONDARY_COLOR,
                    activeforeground=TEXT_COLOR,
                    cursor="hand2"
                )
                remove_btn.pack(side=tk.RIGHT, padx=5)

    def add_user_product(self, name, price):
        if not name or not price:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên và giá sản phẩm!")
            return
        try:
            price = int(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Giá phải là số nguyên dương!")
            return

        if self.data_manager.add_user_product(name, price):
            messagebox.showinfo("Thành công", f"Đã đăng sản phẩm {name}!")
            self.show_selling()

    def edit_user_product(self, index):
        user_prods = self.data_manager.user_products.get(self.data_manager.current_user, [])
        if index >= len(user_prods):
            return

        product = user_prods[index]
        dialog = tk.Toplevel(self.root)
        dialog.title="Sửa Sản Phẩm"
        dialog.geometry("300x200")
        dialog.configure(bg=BG_COLOR)

        tk.Label(dialog, text="Sửa sản phẩm", bg=PRIMARY_COLOR, font=("Segoe UI", 12, "bold"), fg=TEXT_COLOR).pack(pady=10)
        tk.Label(dialog, text="Tên sản phẩm", bg=BG_COLOR).pack()
        name_entry = tk.Entry(dialog, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        name_entry.pack(pady=5)
        name_entry.insert(0, product['name'])

        tk.Label(dialog, text="Giá (VNĐ)", bg=BG_COLOR).pack()
        price_entry = tk.Entry(dialog, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
        price_entry.pack(pady=5)
        price_entry.insert(0, str(product['price']))

        def confirm_edit():
            new_name = name_entry.get().strip()
            new_price = price_entry.get().strip()
            if not new_name or not new_price:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên và giá!")
                return
            try:
                new_price = int(new_price)
                if new_price <= 0:
                    raise ValueError("Giá phải là số nguyên dương!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e) if str(e) else "Giá phải là số nguyên dương!")
                return

            if self.data_manager.edit_user_product(index, new_name, new_price):
                messagebox.showinfo("Thành công", f"Đã sửa sản phẩm {new_name}!")
                dialog.destroy()
                self.show_selling()

        tk.Button(dialog, text="Xác Nhận", command=confirm_edit, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)
        tk.Button(dialog, text="Hủy", command=dialog.destroy, bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)

    def remove_user_product(self, index):
        if self.data_manager.remove_user_product(index):
            messagebox.showinfo("Thành công", "Đã gỡ sản phẩm!")
            self.show_selling()

    def show_profile(self):
        self.current_page = "profile"
        self.update_nav_buttons()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        profile_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        profile_frame.pack(fill=tk.BOTH, expand=True)

        if self.data_manager.current_user:
            tk.Label(profile_frame, text=f"Chào {self.data_manager.current_user}", bg=BG_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=10)
            tk.Button(profile_frame, text="Đăng Xuất", command=self.logout, width=30, height=2, bg=RED, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
            tk.Button(profile_frame, text="Cài Đặt", command=self.show_settings, width=30, height=2, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
            tk.Button(profile_frame, text="Lịch Sử Mua Hàng", command=self.show_orders, width=30, height=2, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
            tk.Button(profile_frame, text="Đánh Giá Sản Phẩm", command=self.show_reviews, width=30, height=2, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
            tk.Button(profile_frame, text="Bán Hàng", command=self.show_selling, width=30, height=2, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
        else:
            login_frame = tk.Frame(profile_frame, bg=BG_COLOR)
            login_frame.pack(pady=20)

            tk.Label(login_frame, text="Tài Khoản", bg=BG_COLOR, font=("Segoe UI", 14, "bold"), fg=TEXT_COLOR).pack(pady=10)

            login_form = tk.Frame(login_frame, bg=BG_COLOR)
            tk.Label(login_form, text="Tên đăng nhập", bg=BG_COLOR).pack()
            login_username_entry = tk.Entry(login_form, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            login_username_entry.pack(pady=5, ipady=6)

            tk.Label(login_form, text="Mật khẩu", bg=BG_COLOR).pack()
            login_password_entry = tk.Entry(login_form, show="*", font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            login_password_entry.pack(pady=5, ipady=6)

            tk.Button(login_form, text="Đăng Nhập", command=lambda: self.login(
                login_username_entry.get(), login_password_entry.get()
            ), bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)

            register_form = tk.Frame(login_frame, bg=BG_COLOR)
            tk.Label(register_form, text="Tên đăng nhập", bg=BG_COLOR).pack()
            register_username_entry = tk.Entry(register_form, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            register_username_entry.pack(pady=5, ipady=6)

            tk.Label(register_form, text="Mật khẩu", bg=BG_COLOR).pack()
            register_password_entry = tk.Entry(register_form, show="*", font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            register_password_entry.pack(pady=5, ipady=6)

            tk.Label(register_form, text="Số điện thoại", bg=BG_COLOR).pack()
            phone_entry = tk.Entry(register_form, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            phone_entry.pack(pady=5, ipady=6)

            tk.Label(register_form, text="Email", bg=BG_COLOR).pack()
            email_entry = tk.Entry(register_form, font=("Segoe UI", 13), bd=1, relief=tk.GROOVE)
            email_entry.pack(pady=5, ipady=6)

            tk.Button(register_form, text="Đăng Ký", command=lambda: self.register(
                register_username_entry.get(), register_password_entry.get(), phone_entry.get(), email_entry.get()
            ), bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=10)

            def show_login():
                register_form.pack_forget()
                login_form.pack()

            def show_register():
                login_form.pack_forget()
                register_form.pack()

            tk.Button(login_frame, text="Chuyển sang Đăng Ký", command=show_register, bg=BG_COLOR, fg=PRIMARY_COLOR, font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=4, activebackground=SECONDARY_COLOR, activeforeground=TEXT_COLOR).pack(pady=5)
            show_login()

    def login(self, username, password):
        if self.data_manager.login(username, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.show_profile()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu sai!")

    def register(self, username, password, phone, email):
        success, message = self.data_manager.register(username, password, phone, email)
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)
        self.show_profile()

    def logout(self):
        self.data_manager.logout()
        messagebox.showinfo("Thành công", "Đã đăng xuất!")
        self.show_profile()

    def show_orders(self):
        self.current_page = None
        self.update_nav_buttons()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        orders_frame = tk.Frame(self.main_frame, bg="white")
        orders_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(orders_frame, text="Lịch Sử Mua Hàng", bg="white", font=("Segoe UI", 24, "bold")).pack(pady=20)

        if not self.data_manager.current_user or self.data_manager.current_user not in self.data_manager.orders or not self.data_manager.orders[self.data_manager.current_user]:
            tk.Label(orders_frame, text="Chưa có đơn hàng nào!", bg="white", font=("Segoe UI", 14)).pack(pady=20)
        else:
            for i, order in enumerate(self.data_manager.orders[self.data_manager.current_user]):
                item = order['product']
                tk.Label(orders_frame, text=f"{item['name']} - {item['price']} VNĐ x {order['quantity']} (Gian hàng: {item['booth']}) - Địa chỉ: {order['address']}", bg="white", font=("Segoe UI", 16), pady=10).pack(pady=10) 
