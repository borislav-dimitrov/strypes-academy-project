import tkinter as tk
import Services.tkinterServices as TkServ
import Models.Db.fakeDB as DB
import Views.importAllViews as Views


class MainScreen:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols, logged_user):
        self.m_screen = m_screen
        self.page_name = page_name
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.logged_user = logged_user
        DB.curr_user = self.logged_user
        self.logout_status = False

        m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        m_screen.title(title)

        TkServ.setup_grid(self.m_screen, self.width, self.height, self.grid_cols, self.grid_rows)

        welcome_lbl = tk.Label(self.m_screen, text=f"Hello {self.logged_user.user_name}!", font=("Arial", 12),
                               name="user_section")
        welcome_lbl.grid(row=0, column=0)

        logout_btn = tk.Button(self.m_screen, text="Logout", font=("Arial", 12, "bold"), bg="coral", name="logout_btn",
                               command=lambda: self.logout())
        logout_btn.grid(row=0, column=7)

        # render user buttons
        section_hdr = tk.Label(self.m_screen, text="Main Operations", font=("Arial", 16, "bold"))
        section_hdr.grid(row=3, column=2, columnspan=3, sticky="we")
        view_stock_btn = tk.Button(self.m_screen, width=15, text="View Stock", font=("Arial", 12), bg="lightgreen",
                                   name="stock_btn",
                                   command=lambda: self.view_stock())
        view_stock_btn.grid(row=5, column=0)

        transactions_btn = tk.Button(self.m_screen, width=15, text="Transactions", font=("Arial", 12), bg="lightgreen",
                                     name="history_btn",
                                     command=lambda: self.transactions())
        transactions_btn.grid(row=5, column=2)

        sales_btn = tk.Button(self.m_screen, width=15, text="Sales", font=("Arial", 12), bg="lightgreen",
                              name="sell_btn",
                              command=lambda: self.sales())
        sales_btn.grid(row=7, column=1)

        purchases_btn = tk.Button(self.m_screen, width=15, text="Purchases", font=("Arial", 12), bg="lightgreen",
                                  name="buy_btn",
                                  command=lambda: self.purchases())
        purchases_btn.grid(row=7, column=3)

        # render admin buttons
        if self.logged_user.user_type == "Administrator":
            section2_hdr = tk.Label(self.m_screen, text="Administrator Options", font=("Arial", 16, "bold"))
            section2_hdr.grid(row=13, column=2, columnspan=3, sticky="we")

            users_btn = tk.Button(self.m_screen, width=15, text="Users", font=("Arial", 12),
                                  bg="lightblue", name="users_btn",
                                  command=lambda: self.users())
            users_btn.grid(row=15, column=0)

            warehouses_btn = tk.Button(self.m_screen, width=15, text="Warehouses", font=("Arial", 12),
                                       bg="lightblue", name="new_whs_btn",
                                       command=lambda: self.warehouses())
            warehouses_btn.grid(row=15, column=2)

            clients_btn = tk.Button(self.m_screen, width=15, text="Clients", font=("Arial", 12),
                                    bg="lightblue", name="clients_btn",
                                    command=lambda: self.clients())
            clients_btn.grid(row=15, column=4)

            suppliers_btn = tk.Button(self.m_screen, width=15, text="Suppliers", font=("Arial", 12),
                                      bg="lightblue", name="suppliers_btn",
                                      command=lambda: self.suppliers())
            suppliers_btn.grid(row=17, column=1)

            products_btn = tk.Button(self.m_screen, width=15, text="Products", font=("Arial", 12),
                                     bg="lightblue", name="products_btn",
                                     command=lambda: self.products())
            products_btn.grid(row=17, column=3)
            self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        DB.opened_pages = []
        DB.curr_user = ""
        DB.my_logger.log(__file__, "Saving...", "INFO")
        DB.save_all_data()
        DB.my_logger.log(__file__, "Saving done! Exiting..", "INFO")
        DB.my_logger.log(__file__, f"User {self.logged_user.user_name} has logged out!", "INFO")
        self.m_screen.destroy()
        quit()

    def logout(self):
        DB.opened_pages = []
        DB.curr_user = ""
        DB.my_logger.log(__file__, "Saving...", "INFO")
        DB.save_all_data()
        DB.my_logger.log(__file__, "Saving done! Exiting..", "INFO")
        DB.my_logger.log(__file__, f"User {self.logged_user.user_name} has logged out!", "INFO")
        self.logged_user = "none"
        self.logout_status = True
        self.m_screen.destroy()

    def view_stock(self):
        if "stock" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Stock page is already opened!")
            return

        stock_screen = tk.Toplevel(self.m_screen)
        stock_page = Views.Stock(stock_screen, "stock",
                                 "Stock", self.width,
                                 self.height, self.grid_rows,
                                 self.grid_cols)
        stock_screen.mainloop()

    def transactions(self):
        if "transactions" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Transactions page is already opened!")
            return

        transactions_screen = tk.Toplevel(self.m_screen)
        transactions_page = Views.Transactions(transactions_screen, "transactions",
                                               "Transactions", self.width,
                                               self.height, self.grid_rows,
                                               self.grid_cols)
        transactions_screen.mainloop()

    def sales(self):
        if "sales" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Sales page is already opened!")
            return

        sales_screen = tk.Toplevel(self.m_screen)
        sales_page = Views.Sales(sales_screen, "sales",
                                 "Sales", self.width,
                                 self.height, self.grid_rows,
                                 self.grid_cols)
        sales_screen.mainloop()

    def purchases(self):
        if "purchases" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Purchases page is already opened!")
            return

        purchases_screen = tk.Toplevel(self.m_screen)
        purchases_page = Views.Purchases(purchases_screen, "purchases",
                                         "Purchases", self.width,
                                         self.height, self.grid_rows,
                                         self.grid_cols)
        purchases_screen.mainloop()

    def users(self):
        if "users" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Users page is already opened!")
            return

        usr_screen = tk.Toplevel(self.m_screen)
        usr_page = Views.Users(usr_screen, "users",
                               "Users", self.width,
                               self.height, self.grid_rows,
                               self.grid_cols)
        usr_screen.mainloop()

    def warehouses(self):
        if "warehouses" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Warehouses page is already opened!")
            return

        warehouses_screen = tk.Toplevel(self.m_screen)
        warehouses_page = Views.Warehouses(warehouses_screen, "warehouses",
                                           "Warehouses", self.width,
                                           self.height, self.grid_rows,
                                           self.grid_cols)
        warehouses_screen.mainloop()

    def clients(self):
        if "clients" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Clients page is already opened!")
            return

        clients_screen = tk.Toplevel(self.m_screen)
        clients_page = Views.Clients(clients_screen, "clients",
                                     "Clients", self.width,
                                     self.height, self.grid_rows,
                                     self.grid_cols)
        clients_screen.mainloop()

    def suppliers(self):
        if "suppliers" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Suppliers page is already opened!")
            return

        suppliers_screen = tk.Toplevel(self.m_screen)
        suppliers_page = Views.Suppliers(suppliers_screen, "suppliers",
                                         "Suppliers", self.width,
                                         self.height, self.grid_rows,
                                         self.grid_cols)
        suppliers_screen.mainloop()

    def products(self):
        if "products" in DB.opened_pages:
            TkServ.create_custom_msg(self.m_screen, "Warning!", "Products page is already opened!")
            return

        products_screen = tk.Toplevel(self.m_screen)
        usr_page = Views.Products(products_screen, "products",
                                  "Products", self.width,
                                  self.height, self.grid_rows,
                                  self.grid_cols)
        products_screen.mainloop()
