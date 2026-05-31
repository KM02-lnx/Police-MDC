import mysql.connector
from mysql.connector import Error
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class MDCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Police MDC")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.destroy())

        try:
            self.conn = mysql.connector.connect(
                host="gateway01.eu-central-1.prod.aws.tidbcloud.com",          # 🔁 Replace with actual host
                port=4000,                      # ✅ TiDB uses port 4000 by default
                user="2qGm2G4eBNDudXV.root",          # 🔁 Replace with your username
                password="iay5Ct5xMUCATZu6",  # 🔁 Replace with your password
                database="police_database",  # 🔁 Replace with your DB name
                ssl_ca=r"C:\Users\User\Downloads\isrgrootx1.pem",   # ✅ SSL is required
                ssl_verify_cert=True
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            messagebox.showerror("Connection Error", f"Could not connect to TiDB:\n{e}")
            self.destroy()
            return

        self.officers = self._load_officers()
        self._create_login_frame()

    def _load_officers(self):
        self.cursor.execute("""
            SELECT p.id, p.name, p.surname, pp.badge_number, pp.division
            FROM police_personnel pp
            JOIN persons p ON p.id = pp.person_id
        """)
        return [
            {"id": r[0], "first": r[1], "last": r[2], "badge": r[3], "shop": r[4]}
            for r in self.cursor.fetchall()
        ]

        # --- Login ---
    def _create_login_frame(self):
        f = tk.Frame(self, bg="#001f3f")
        f.pack(fill='both', expand=True)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

        tk.Label(f, text="SQL POLICE DEPARTMENT - MDC LOGIN", bg="#001f3f", fg="white", font=("Times New Roman", 53)).pack(pady=20)

        form = tk.Frame(f, bg="#001f3f")
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form, text="SELECT OFFICER:", bg="#001f3f", fg="white", font=("Times New Roman", 44)).grid(row=0, column=0, sticky='e')
        self.name_var = tk.StringVar()
        names = [f"{o['first']} {o['last']}" for o in self.officers]
        self.officer_cb = ttk.Combobox(form, textvariable=self.name_var, values=names, state='readonly', font=("Times New Roman", 32), width=44)
        self.officer_cb.grid(row=0, column=1, padx=5, pady=5)
        self.officer_cb.bind("<<ComboboxSelected>>", self._on_officer_selected)

        tk.Label(form, text="BADGE NUMBER:", bg="#001f3f", fg="white", font=("Times New Roman", 44)).grid(row=1, column=0, sticky='e')
        self.badge_label = tk.Label(form, text="", bg="#001f3f", fg="white", font=("Times New Roman", 32))
        self.badge_label.grid(row=1, column=1, sticky='w')

        tk.Label(form, text="SHOP NUMBER:", bg="#001f3f", fg="white", font=("Times New Roman", 44)).grid(row=2, column=0, sticky='e')
        self.shop_label = tk.Label(form, text="", bg="#001f3f", fg="white", font=("Times New Roman", 32))
        self.shop_label.grid(row=2, column=1, sticky='w')

        tk.Button(f, text="LOGIN", command=self._handle_login, font=("Times New Roman", 67), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(side="bottom", pady=60)

        self.login_frame = f

    def _on_officer_selected(self, evt):
        idx = self.officer_cb.current()
        if idx >= 0:
            o = self.officers[idx]
            self.badge_label.config(text=o["badge"])
            self.shop_label.config(text=o["shop"])

    def _handle_login(self):
        if not self.name_var.get():
            messagebox.showerror("Error", "Select an officer.")
            return
        idx = [f"{o['first']} {o['last']}" for o in self.officers].index(self.name_var.get())
        self.officer = self.officers[idx]
        self.login_frame.destroy()
        self._create_main_menu()


    # --- Header / Main ---
    def _show_header(self,parent):
        hdr = tk.Frame(parent,bd=1,relief='solid',pady=10, bg="#001f3f"); hdr.pack(fill='x')
        for i in range(3): hdr.columnconfigure(i,weight=1)
        left = tk.Frame(hdr, bg="#001f3f"); left.grid(row=0,column=0,sticky='w',padx=20)
        tk.Label(left,text=f"NAME: {self.officer['first']} {self.officer['last']}",bg="#001f3f", fg="white", font=("Times New Roman",12)).pack(anchor='w')
        tk.Label(left,text=f"BADGE #: {self.officer['badge']}",bg="#001f3f", fg="white", font=("Times New Roman",12)).pack(anchor='w')
        tk.Label(left,text=f"SHOP #: {self.officer['shop']}",bg="#001f3f", fg="white", font=("Times New Roman",12)).pack(anchor='w')
        center = tk.Frame(hdr, bg="#001f3f"); center.grid(row=0,column=1)
        tk.Label(center,text="POLICE MDC",bg="#001f3f", fg="white", font=("Times New Roman",18,'bold')).pack()
        tk.Label(center,text="SQL POLICE DEPARTMENT",bg="#001f3f", fg="white", font=("Times New Roman", 44)).pack()
        tk.Label(center,text='"TO PROTECT AND SERVE"',bg="#001f3f", fg="white", font=("Times New Roman",12,'italic')).pack()
        ctrl = tk.Frame(hdr, bg="#001f3f"); ctrl.grid(row=0,column=2,sticky='e',padx=20)
        tk.Button(ctrl, text="LOGOUT", command=self._logout, font=("Times New Roman", 40), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(anchor="e")
    
    def _create_main_menu(self):
        for w in self.winfo_children(): w.destroy()
        mf = tk.Frame(self, bg="#001f3f"); mf.pack(fill='both',expand=True)
        self._show_header(mf)
        content = tk.Frame(mf, bg="#001f3f"); content.pack(fill='both',expand=True)
        for i in (0,1):
            content.rowconfigure(i,weight=1); content.columnconfigure(i,weight=1)
        btn = {"font":("Times New Roman", 64),"width":15,"height":4}
        tk.Button(content, text="PEOPLE", command=self._open_people_menu, font=("Times New Roman", 40), bg="#001f3f", fg="white", bd=0, highlightthickness=0).grid(row=0, column=0, padx=50, pady=50, sticky='nsew')
        tk.Button(content, text="VEHICLES", command=self._open_vehicles_menu, font=("Times New Roman", 40), bg="#001f3f", fg="white", bd=0, highlightthickness=0).grid(row=0, column=1, padx=50, pady=50, sticky='nsew')
        tk.Button(content, text="WEAPONS", command=self._open_items_menu, font=("Times New Roman", 40), bg="#001f3f", fg="white", bd=0, highlightthickness=0).grid(row=1, column=0, padx=50, pady=50, sticky='nsew')
        tk.Button(content, text="CASES", command=self._open_cases_menu, font=("Times New Roman", 40), bg="#001f3f", fg="white", bd=0, highlightthickness=0).grid(row=1, column=1, padx=50, pady=50, sticky='nsew')
        self.menu_frame = mf

    def _back_to_main(self):
        for attr in ('people_frame','vehicles_frame','items_frame'):
            frm = getattr(self,attr,None)
            if frm: frm.destroy()
        self._create_main_menu()

    # --- People ---
    def _open_people_menu(self):
        if hasattr(self, "people_frame") and self.people_frame:
            self.people_frame.destroy()
        self.menu_frame.destroy()
        pf = tk.Frame(self, bg="#001f3f"); pf.pack(fill='both',expand=True)
        self.people_frame = pf
        self._show_header(pf)
        c = tk.Frame(pf, bg="#001f3f"); c.pack(fill='both',expand=True)
        tk.Label(c,text="PEOPLE FUNCTIONS",bg="#001f3f", fg="white", font=("Times New Roman",16,'bold')).pack(pady=10)
        funcs = [
            ("SEARCH CIVILIANSS",   self._search_civilians),
            ("SEARCH CRIMINALS",  self._search_criminals),
            ("SEARCH PERSONNEL",    self._search_personnel),
            ("REPORT MISSING CITIZEN", lambda:self._report_missing_person("Citizen")),
            ("REPORT MISSING CRIMINAL", lambda:self._report_missing_person("Criminal")),
            ("REPORT MISSING PERSONNEL", lambda:self._report_missing_person("Personnel")),
            ("SHOW MISSING",      self._show_missing_people),
        ]
        for txt,cmd in funcs:
            tk.Button(c, text=txt, command=cmd, font=("Times New Roman", 25), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=5)
        tk.Button(c, text="BACK", command=self._back_to_main, font=("Times New Roman", 25), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _search_civilians(self):
        for w in self.winfo_children():
            w.destroy()
        self.people_frame = tk.Frame(self, bg="#001f3f")
        self.people_frame.pack(fill='both', expand=True)
        self._show_header(self.people_frame)

        c = tk.Frame(self.people_frame, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="SEARCH CIVILIANS", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(c, text="NAME OR SURNAME:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(c, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        columns = ("ID", "Name", "Surname", "Place of Work", "Criminal Record")
        tv = ttk.Treeview(c, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor="center")
        tv.pack(fill='both', expand=True, pady=10)

        def do():
            t = f"%{var.get().strip()}%"
            self.cursor.execute(
                """
                SELECT cv.person_id, p.name, p.surname, cv.place_of_work, cv.criminal_record
                FROM civilians cv
                JOIN persons p ON cv.person_id = p.id
                WHERE p.name LIKE %s OR p.surname LIKE %s
                """,
                (t, t)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(c, text="SEARCH", command=do,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=10)

        tk.Button(c, text="BACK", command=self._open_people_menu,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=20)

    def _search_criminals(self):
        for w in self.winfo_children():
            w.destroy()
        self.people_frame = tk.Frame(self, bg="#001f3f")
        self.people_frame.pack(fill='both', expand=True)
        self._show_header(self.people_frame)

        c = tk.Frame(self.people_frame, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="SEARCH CRIMINALS", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(c, text="NAME OR SURNAME:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(c, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        columns = ("ID", "Name", "Surname", "Prison", "Parole Officer", "Status", "Warrants")
        tv = ttk.Treeview(c, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor="center")
        tv.pack(fill='both', expand=True, pady=10)

        def do():
            t = f"%{var.get().strip()}%"
            self.cursor.execute(
                """
                SELECT c.person_id, p.name, p.surname, c.jail_or_prison_name, c.parole_officer_name,
                    c.current_status, c.warrants
                FROM criminals c
                JOIN persons p ON c.person_id = p.id
                WHERE p.name LIKE %s OR p.surname LIKE %s
                """,
                (t, t)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(c, text="SEARCH", command=do, font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=10)
        tk.Button(c, text="BACK", command=self._open_people_menu, font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    
    def _search_personnel(self):
        for w in self.winfo_children():
            w.destroy()
        self.people_frame = tk.Frame(self, bg="#001f3f")
        self.people_frame.pack(fill='both', expand=True)
        self._show_header(self.people_frame)

        c = tk.Frame(self.people_frame, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="SEARCH PERSONNEL", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(c, text="NAME OR SURNAME:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(c, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        columns = ("ID", "Name", "Surname", "Badge Number", "Position", "Division")
        tv = ttk.Treeview(c, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor="center")
        tv.pack(fill='both', expand=True, pady=10)

        def do():
            t = f"%{var.get().strip()}%"
            self.cursor.execute(
                """
                SELECT pp.person_id, p.name, p.surname, pp.badge_number, pp.position, pp.division
                FROM police_personnel pp
                JOIN persons p ON pp.person_id = p.id
                WHERE p.name LIKE %s OR p.surname LIKE %s
                """,
                (t, t)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(c, text="SEARCH", command=do, font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=10)
        tk.Button(c, text="BACK", command=self._open_people_menu, font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _report_missing_person(self, type_):
        for w in self.winfo_children():
            w.destroy()
        self.people_frame = tk.Frame(self, bg="#001f3f")
        f = self.people_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text=f"REPORT MISSING {type_.upper()}", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        # First Name
        tk.Label(c, text="FIRST NAME:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)
        fn = tk.StringVar()
        tk.Entry(c, textvariable=fn, font=("Times New Roman", 24)).pack(pady=5)

        # Last Name
        tk.Label(c, text="LAST NAME:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)
        ln = tk.StringVar()
        tk.Entry(c, textvariable=ln, font=("Times New Roman", 24)).pack(pady=5)

        # Last Known Location
        tk.Label(c, text="LAST KNOWN LOCATION:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)
        location = tk.StringVar()
        tk.Entry(c, textvariable=location, font=("Times New Roman", 24)).pack(pady=5)

        # Evidence
        tk.Label(c, text="EVIDENCE:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)
        evidence = tk.StringVar()
        tk.Entry(c, textvariable=evidence, font=("Times New Roman", 24)).pack(pady=5)

        # Suspects
        tk.Label(c, text="SUSPECTS:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)
        suspects = tk.StringVar()
        tk.Entry(c, textvariable=suspects, font=("Times New Roman", 24)).pack(pady=5)

        def submit():
            first = fn.get().strip()
            last = ln.get().strip()
            loc = location.get().strip()
            evid = evidence.get().strip()
            susp = suspects.get().strip()

            if not all([first, last, loc, evid, susp]):
                messagebox.showerror("Error", "All fields are required.")
                return

            # Lookup person_id from persons table
            self.cursor.execute(
                "SELECT id FROM persons WHERE name = %s AND surname = %s",
                (first, last)
            )
            result = self.cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Person not found.")
                return

            person_id = result[0]
            now = datetime.now().isoformat(" ", "seconds")

            # Insert into missing_persons table
            self.cursor.execute(
                """
                INSERT INTO missing_persons
                (person_id, last_known_location, time_reported_missing, evidence, suspects)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (person_id, loc, now, evid, susp)
            )

            # Remove from original category table
            if type_.lower() == "civilian":
                self.cursor.execute("DELETE FROM civilians WHERE person_id = %s", (person_id,))
            elif type_.lower() == "criminal":
                self.cursor.execute("DELETE FROM criminals WHERE person_id = %s", (person_id,))
            elif type_.lower() == "police":
                self.cursor.execute("DELETE FROM police_personnel WHERE person_id = %s", (person_id,))

            self.conn.commit()
            messagebox.showinfo("Success", f"{type_.capitalize()} reported missing.")
            self._open_people_menu()

        # Buttons
        tk.Button(c, text="REPORT", command=submit, font=("Times New Roman", 24),
                bg="#001f3f", fg="white", bd=0).pack(pady=10)

        tk.Button(c, text="BACK", command=lambda: [self.people_frame.destroy(), self._open_people_menu()],
                font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0).pack(pady=10)

    def _show_missing_people(self): 
        for w in self.winfo_children():
            w.destroy()
        self.people_frame = tk.Frame(self, bg="#001f3f")
        f = self.people_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="MISSING PEOPLE", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        columns = ("ID", "Name", "Surname", "Last Known Location", "Reported Missing", "Evidence", "Suspects")
        tv = ttk.Treeview(c, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor="center")
        tv.pack(fill='both', expand=True, pady=10)

        self.cursor.execute("""
            SELECT m.person_id, p.name, p.surname,
                m.last_known_location, m.time_reported_missing,
                m.evidence, m.suspects
            FROM missing_persons m
            JOIN persons p ON m.person_id = p.id
        """)
        for r in self.cursor.fetchall():
            tv.insert('', 'end', values=r)

        tk.Button(c, text="BACK", command=self._open_people_menu,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=20)


    # --- Vehicles ---
    def _open_vehicles_menu(self):
        self.menu_frame.destroy()
        vf = tk.Frame(self, bg="#001f3f"); vf.pack(fill='both',expand=True)
        self.vehicles_frame = vf
        self._show_header(vf)
        c = tk.Frame(vf, bg="#001f3f"); c.pack(fill='both',expand=True)
        tk.Label(c,text="VEHICLES FUNCTIONS",bg="#001f3f", fg="white", font=("Times New Roman",16,'bold')).pack(pady=10)
        funcs = [
            ("SEARCH VEHICLE",         self._search_vehicle),
            ("SEARCH DRIVER'S LICENSE",self._search_drivers_license),
            ("SEARCH NUMBER PLATES",   self._search_number_plates),
        ]
        for txt,cmd in funcs:
            tk.Button(c, text=txt, command=cmd, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=5)
        tk.Button(c, text="BACK", command=self._back_to_main, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _search_vehicle(self):
        for w in self.winfo_children():
            w.destroy()
        self.vehicles_frame = tk.Frame(self, bg="#001f3f")
        self.vehicles_frame.pack(fill='both', expand=True)
        self._show_header(self.vehicles_frame)

        body = tk.Frame(self.vehicles_frame, bg="#001f3f")
        body.pack(fill='both', expand=True)

        tk.Label(body, text="SEARCH VEHICLES", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(body, text="CATEGORY:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(body, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        table_frame = tk.Frame(body, bg="#001f3f")
        table_frame.pack(fill='both', expand=True)

        xscroll = tk.Scrollbar(table_frame, orient='horizontal')
        yscroll = tk.Scrollbar(table_frame, orient='vertical')
        
        columns = (
            "id", "number_plate", "owner_id", "company_name", "town", "address", "ownership_type",
            "manufacturer", "model", "vehicle_type", "vin_number", "weight", "registration_expiration",
            "insurance_name", "engine_size", "horsepower", "fuel_type", "vehicle_color", "number_of_seats", "model_year"
        )

        tv = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            xscrollcommand=xscroll.set, yscrollcommand=yscroll.set
        )

        xscroll.config(command=tv.xview)
        yscroll.config(command=tv.yview)

        xscroll.pack(side='bottom', fill='x')
        yscroll.pack(side='right', fill='y')
        tv.pack(side='left', fill='both', expand=True)

        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor='center', width=100)

        def do():
            search_val = f"%{var.get().strip()}%"
            self.cursor.execute(
                f"""
                SELECT {', '.join(columns)}
                FROM vehicles
                WHERE vehicle_type LIKE %s
                """,
                (search_val,)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for row in rows:
                tv.insert('', 'end', values=row)

        tk.Button(body, text="SEARCH", command=do,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0).pack(pady=10)

        tk.Button(body, text="BACK", command=lambda: [self.vehicles_frame.destroy(), self._open_vehicles_menu()],
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=20)


    def _search_drivers_license(self):
        for w in self.winfo_children():
            w.destroy()
        self.vehicles_frame = tk.Frame(self, bg="#001f3f")
        self.vehicles_frame.pack(fill='both', expand=True)
        self._show_header(self.vehicles_frame)

        container = tk.Frame(self.vehicles_frame, bg="#001f3f")
        container.pack(fill='both', expand=True)

        tk.Label(container, text="SEARCH DRIVER'S LICENSE", bg="#001f3f", fg="white",
                font=("Times New Roman", 36)).pack(pady=10)

        tk.Label(container, text="LAST NAME:", bg="#001f3f", fg="white",
                font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(container, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        columns = ("ID", "First Name", "Last Name", 
                "Date Created", "Date Expires", "Police Station", 
                "Residence", "Categories")

        tv = ttk.Treeview(container, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, anchor="center")
        tv.pack(fill='both', expand=True, pady=10)

        def do():
            search_val = f"%{var.get().strip()}%"
            self.cursor.execute(
                """
                SELECT dl.id, p.name, p.surname,
                    dl.date_created, dl.date_expires, dl.police_station,
                    dl.place_of_residence, dl.categories
                FROM drivers_license dl
                JOIN persons p ON dl.person_id = p.id
                WHERE p.surname LIKE %s
                """,
                (search_val,)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(container, text="SEARCH", command=do,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=10)

        tk.Button(container, text="BACK",
                command=lambda: [self.vehicles_frame.destroy(), self._open_vehicles_menu()],
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=20)

    def _search_number_plates(self):
        for w in self.winfo_children():
            w.destroy()
        self.vehicles_frame = tk.Frame(self, bg="#001f3f")
        f = self.vehicles_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="SEARCH NUMBER PLATES", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(c, text="PLATE TEXT:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(c, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        tv = ttk.Treeview(c, columns=("ID", "Number Plate", "Vehicle Type"), show="headings")
        for col in ("ID", "Number Plate", "Vehicle Type"):
            tv.heading(col, text=col)
            tv.column(col, anchor='center')
        tv.pack(fill='both', expand=True, pady=10)

        def do():
            t = f"%{var.get().strip()}%"
            self.cursor.execute(
                "SELECT id, number_plate, vehicle_type FROM vehicles WHERE number_plate LIKE %s",
                (t,)
            )
            rows = self.cursor.fetchall()
            tv.delete(*tv.get_children())
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(c, text="SEARCH", command=do,
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=10)

        tk.Button(c, text="BACK",
                command=lambda: [self.vehicles_frame.destroy(), self._open_vehicles_menu()],
                font=("Times New Roman", 24), bg="#001f3f", fg="white",
                bd=0, highlightthickness=0).pack(pady=20)

    # --- WEAPONS ---
    def _open_items_menu(self):
        self.menu_frame.destroy()
        it = tk.Frame(self, bg="#001f3f"); it.pack(fill='both',expand=True)
        self.items_frame = it
        self._show_header(it)
        c = tk.Frame(it, bg="#001f3f"); c.pack(fill='both',expand=True)
        tk.Label(c,text="WEAPONS",bg="#001f3f", fg="white", font=("Times New Roman",36,'bold')).pack(pady=10)
        funcs = [
            ("SEARCH WEAPONS", self._search_items),
            ("SHOW WEAPONS", self._show_items),
        ]
        for txt,cmd in funcs:
            tk.Button(c, text=txt, command=cmd, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=5)
        tk.Button(c, text="BACK", command=self._back_to_main, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _search_items(self):
        for w in self.winfo_children():
            w.destroy()
        self.items_frame = tk.Frame(self, bg="#001f3f")
        self.items_frame.pack(fill='both', expand=True)
        self._show_header(self.items_frame)

        # Style notebook and treeview
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TNotebook", background="#001f3f", borderwidth=0)
        style.configure("TNotebook.Tab", background="#001f3f", foreground="white",
                        font=("Times New Roman", 20), padding=[30, 10], borderwidth=0)
        style.map("TNotebook.Tab",
                background=[("selected", "#001f3f")],
                foreground=[("selected", "white")])

        style.configure("Treeview", background="white", foreground="black", fieldbackground="white",
                        borderwidth=0, relief="flat", rowheight=30, font=("Times New Roman", 16))
        style.configure("Treeview.Heading", background="#001f3f", foreground="white",
                        font=("Times New Roman", 18), borderwidth=0)
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        notebook = ttk.Notebook(self.items_frame)
        notebook.pack(fill='both', expand=True, padx=0, pady=10)

        def make_tab(title, table_name, columns):
            frame = tk.Frame(notebook, bg="#001f3f")
            notebook.add(frame, text=title)

            form = tk.Frame(frame, bg="#001f3f")
            form.pack(pady=10)
            tk.Label(form, text="DESCRIPTION CONTAINS:", bg="#001f3f", fg="white",
                    font=("Times New Roman", 28)).grid(row=0, column=0, sticky='e', padx=5)

            var = tk.StringVar()
            tk.Entry(form, textvariable=var, font=("Times New Roman", 24), width=40).grid(row=0, column=1, padx=5)

            tv = ttk.Treeview(frame, columns=columns, show="headings")
            for col in columns:
                tv.heading(col, text=col)
                # Apply thinner widths to narrow fields
                if col in ("id", "owner_id"):
                    tv.column(col, anchor='center', width=80)
                else:
                    tv.column(col, anchor='center', width=140)
            tv.pack(fill='both', expand=True, pady=15, padx=15)

            def do_search():
                search_val = f"%{var.get().strip()}%"
                self.cursor.execute(f"SELECT {','.join(columns)} FROM {table_name} WHERE description LIKE %s", (search_val,))
                rows = self.cursor.fetchall()
                tv.delete(*tv.get_children())
                for row in rows:
                    tv.insert('', 'end', values=row)

            tk.Button(frame, text="SEARCH", command=do_search,
                    font=("Times New Roman", 36), bg="#001f3f", fg="white",
                    bd=0, highlightthickness=0, activebackground="#001f3f", activeforeground="white").pack(pady=10)

        # Tabs
        make_tab("Weapons", "weapons", [
            "id", "serial_number", "weapon_type", "description", "place_of_purchase",
            "owner_id", "related_to_crime", "crime_location", "time_of_crime",
            "fingerprints_found", "fingerprint_ids"
        ])

        make_tab("Police Weapons", "police_weapons", [
            "id", "serial_number", "weapon_type", "description", "quantity",
            "ammunition", "other_equipment", "weapon_id"
        ])

        # Back button styled same as LOGOUT
        tk.Button(self.items_frame, text="BACK", command=lambda: [self.items_frame.destroy(), self._open_items_menu()],
                font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0,
                activebackground="#001f3f", activeforeground="white").pack(pady=30)


    def _show_items(self):
        for w in self.winfo_children():
            w.destroy()
        self.items_frame = tk.Frame(self, bg="#001f3f")
        f = self.items_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="SELECT ITEM CATEGORY", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        def open_weapons():
            self._show_table(
                "weapons",
                [
                    "id", "serial_number", "weapon_type", "description", "place_of_purchase",
                    "owner_id", "related_to_crime", "crime_location", "time_of_crime",
                    "fingerprints_found", "fingerprint_ids"
                ]
            )

        def open_police_weapons():
            self._show_table(
                "police_weapons",
                [
                    "id", "serial_number", "weapon_type", "description", "quantity",
                    "ammunition", "other_equipment", "weapon_id"
                ]
            )

        # Consistent button design
        for text, cmd in [("WEAPONS", open_weapons), ("POLICE WEAPONS", open_police_weapons)]:
            tk.Button(c, text=text, command=cmd, font=("Times New Roman", 36),
                    bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=10)

        tk.Button(c, text="BACK", command=lambda: [self.items_frame.destroy(), self._open_items_menu()],
                font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=30)


    def _show_table(self, table_name, columns):
        for w in self.winfo_children():
            w.destroy()
        self.items_frame = tk.Frame(self, bg="#001f3f")
        f = self.items_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text=table_name.upper(), bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        # Treeview with consistent style
        tv = ttk.Treeview(c, columns=columns, show="headings")
        for col in columns:
            tv.heading(col, text=col.replace("_", " ").title())
            tv.column(col, anchor='center', width=150)
        tv.pack(fill='both', expand=True, pady=10, padx=30)

        try:
            self.cursor.execute(f"SELECT {','.join(columns)} FROM {table_name}")
            for row in self.cursor.fetchall():
                tv.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        tk.Button(c, text="BACK", command=self._show_items,
                font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=30)

    #Cases
    def _open_cases_menu(self):
        self.menu_frame.destroy()
        cf = tk.Frame(self, bg="#001f3f"); cf.pack(fill='both', expand=True)
        self.cases_frame = cf
        self._show_header(cf)
        c = tk.Frame(cf, bg="#001f3f"); c.pack(fill='both', expand=True)
        tk.Label(c, text="CASES MENU", bg="#001f3f", fg="white", font=("Times New Roman", 16, 'bold')).pack(pady=10)
        funcs = [
            ("OPEN NEW CASE", self._open_new_case),
            ("VIEW CASES", self._view_cases),
            ("CLOSE CASE", self._close_case),
            ("ADD TO CASE", self._add_to_case),
            ("REMOVE FROM CASE", self._remove_from_case)
        ]
        for txt, cmd in funcs:
            tk.Button(c, text=txt, command=cmd, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=5)
        tk.Button(c, text="BACK", command=self._back_to_main, font=("Times New Roman", 36), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _open_new_case(self):
        for w in self.winfo_children():
            w.destroy()
        self.cases_frame = tk.Frame(self, bg="#001f3f")
        f = self.cases_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="OPEN NEW CASE", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        form = tk.Frame(c, bg="#001f3f")
        form.pack(pady=20)

        fields = {
            "ORDER NUMBER": tk.StringVar(),
            "CASE TYPE": tk.StringVar(),
            "LOCATION": tk.StringVar(),
            "VICTIMS": tk.StringVar(),
            "SUSPECTS": tk.StringVar(),
            "EVIDENCE": tk.StringVar(),
            "CURRENT PERSONNEL": tk.StringVar(),
            "CLOSED BY (Officer ID)": tk.StringVar(),
        }

        # Left column (first 4)
        left_fields = list(fields.items())[:4]
        for i, (label, var) in enumerate(left_fields):
            tk.Label(form, text=label + ":", bg="#001f3f", fg="white", font=("Times New Roman", 20)).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            tk.Entry(form, textvariable=var, font=("Times New Roman", 20), width=30).grid(row=i, column=1, padx=10, pady=5)

        # Right column (last 4)
        right_fields = list(fields.items())[4:]
        for i, (label, var) in enumerate(right_fields):
            tk.Label(form, text=label + ":", bg="#001f3f", fg="white", font=("Times New Roman", 20)).grid(row=i, column=2, sticky="e", padx=10, pady=5)
            tk.Entry(form, textvariable=var, font=("Times New Roman", 20), width=30).grid(row=i, column=3, padx=10, pady=5)

        def do():
            data = {k: v.get().strip() for k, v in fields.items()}

            if not data["ORDER NUMBER"] or not data["CASE TYPE"] or not data["LOCATION"]:
                messagebox.showerror("Error", "Order Number, Case Type, and Location are required.")
                return

            try:
                case_date = datetime.now().date()
                self.cursor.execute(
                    """
                    INSERT INTO cases (
                        order_number, case_date, case_type, case_location,
                        victims, suspects, evidence,
                        opened_by, current_personnel, closed_by
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["ORDER NUMBER"],
                        case_date,
                        data["CASE TYPE"],
                        data["LOCATION"],
                        data["VICTIMS"] or None,
                        data["SUSPECTS"] or None,
                        data["EVIDENCE"] or None,
                        self.officer["id"],
                        data["CURRENT PERSONNEL"] or None,
                        data["CLOSED BY (Officer ID)"] or None
                    )
                )
                self.conn.commit()
                messagebox.showinfo("Success", "New case opened.")
                self._view_cases()
            except Exception as e:
                print("Insert Error:", e)
                messagebox.showerror("Database Error", str(e))

        tk.Button(c, text="OPEN CASE", command=do, font=("Times New Roman", 24),
                bg="#001f3f", fg="white", bd=0).pack(pady=20)
        tk.Button(c, text="BACK", command=self._view_cases, font=("Times New Roman", 24),
                bg="#001f3f", fg="white", bd=0).pack()

    def _view_cases(self):
        for w in self.winfo_children():
            w.destroy()
        self.cases_frame = tk.Frame(self, bg="#001f3f")
        f = self.cases_frame
        f.pack(fill='both', expand=True)
        self._show_header(f)

        c = tk.Frame(f, bg="#001f3f")
        c.pack(fill='both', expand=True)

        tk.Label(c, text="VIEW CASES", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(c, text="ORDER # OR TYPE:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        var = tk.StringVar()
        tk.Entry(c, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        columns = ("ID", "Order #", "Type", "Date", "Location", "Victims", "Suspects",
                "Evidence", "Opened By", "Personnel", "Closed By")

        # Scrollable wrapper
        wrapper = tk.Frame(c)
        wrapper.pack(fill='both', expand=True)

        x_scroll = tk.Scrollbar(wrapper, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')

        y_scroll = tk.Scrollbar(wrapper)
        y_scroll.pack(side='right', fill='y')

        tv = ttk.Treeview(wrapper, columns=columns, show="headings", 
                        xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        x_scroll.config(command=tv.xview)
        y_scroll.config(command=tv.yview)

        for h in columns:
            tv.heading(h, text=h)
            tv.column(h, width=150, anchor='center')  # Set reasonable width per column

        tv.pack(fill='both', expand=True)

        def do():
            t = var.get().strip()
            if t:
                like = f"%{t}%"
                self.cursor.execute("""
                    SELECT id, order_number, case_type, case_date, case_location,
                        victims, suspects, evidence, opened_by,
                        current_personnel, closed_by
                    FROM cases
                    WHERE order_number LIKE %s OR case_type LIKE %s
                """, (like, like))
            else:
                self.cursor.execute("""
                    SELECT id, order_number, case_type, case_date, case_location,
                        victims, suspects, evidence, opened_by,
                        current_personnel, closed_by
                    FROM cases
                """)
            rows = self.cursor.fetchall()
            for i in tv.get_children():
                tv.delete(i)
            for r in rows:
                tv.insert('', 'end', values=r)

        tk.Button(c, text="SEARCH", command=do, font=("Times New Roman", 24),
                bg="#001f3f", fg="white", bd=0).pack(pady=10)
        tk.Button(c, text="BACK", command=lambda: [self.cases_frame.destroy(), self._open_cases_menu()],
                font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0).pack(pady=20)

        do()
    
    def _close_case(self):
        for w in self.winfo_children():
            w.destroy()
        self.cases_frame = tk.Frame(self, bg="#001f3f")
        self.cases_frame.pack(fill='both', expand=True)
        self._show_header(self.cases_frame)

        body = tk.Frame(self.cases_frame, bg="#001f3f")
        body.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(body, text="CLOSE CASE", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)
        tk.Label(body, text="CASE ID:", bg="#001f3f", fg="white", font=("Times New Roman", 24)).pack(pady=5)

        cid = tk.StringVar()
        tk.Entry(body, textvariable=cid, font=("Times New Roman", 24)).pack(pady=5)

        def do():
            try:
                case_id = cid.get().strip()
                if not case_id:
                    messagebox.showerror("Error", "Case ID is required")
                    return

                # Update the case record
                self.cursor.execute("""
                    UPDATE cases 
                    SET closed_by = %s 
                    WHERE id = %s
                """, (self.officer["id"], case_id))
                self.conn.commit()

                messagebox.showinfo("Done", f"Case #{case_id} has been closed.")
                self._view_cases()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(body, text="CLOSE CASE", command=do, font=("Times New Roman", 24),
                bg="#001f3f", fg="white", bd=0).pack(pady=10)
        tk.Button(body, text="BACK", command=lambda: [self.cases_frame.destroy(), self._open_cases_menu()], font=("Times New Roman", 24), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)


    def _add_to_case(self):
        for w in self.winfo_children():
            w.destroy()
        self.cases_frame = tk.Frame(self, bg="#001f3f")
        self.cases_frame.pack(fill='both', expand=True)
        self._show_header(self.cases_frame)

        body = tk.Frame(self.cases_frame, bg="#001f3f")
        body.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(body, text="ADD TO CASE", bg="#001f3f", fg="white", font=("Times New Roman", 36)).pack(pady=10)

        fields = {
            "Case ID": tk.StringVar(),
            "Victims": tk.StringVar(),
            "Suspects": tk.StringVar(),
            "Evidence": tk.StringVar(),
            "Current Personnel (comma-separated IDs)": tk.StringVar()
        }

        for label, var in fields.items():
            tk.Label(body, text=label + ":", bg="#001f3f", fg="white", font=("Times New Roman", 18)).pack(pady=5)
            tk.Entry(body, textvariable=var, font=("Times New Roman", 24)).pack(pady=5)

        def do():
            try:
                case_id = fields["Case ID"].get().strip()
                self.cursor.execute("SELECT 1 FROM cases WHERE id=%s", (case_id,))
                if not self.cursor.fetchone():
                    messagebox.showerror("Error", "Case ID does not exist")
                    return

                updates = []
                values = []

                for db_field, var_name in [
                    ("victims", "Victims"),
                    ("suspects", "Suspects"),
                    ("evidence", "Evidence"),
                    ("current_personnel", "Current Personnel (comma-separated IDs)")
                ]:
                    val = fields[var_name].get().strip()
                    if val:
                        updates.append(f"{db_field} = %s")
                        values.append(val)

                if not updates:
                    messagebox.showinfo("No Update", "No data provided to update.")
                    return

                values.append(case_id)
                sql = f"UPDATE cases SET {', '.join(updates)} WHERE id = %s"
                self.cursor.execute(sql, tuple(values))
                self.conn.commit()
                messagebox.showinfo("Success", "Case updated.")
                self._view_cases()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(body, text="UPDATE", command=do, font=("Times New Roman", 18), bg="#001f3f", fg="white", bd=0).pack(pady=10)
        tk.Button(body, text="BACK", command=lambda: [self.cases_frame.destroy(), self._open_cases_menu()], font=("Times New Roman", 18), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)

    def _remove_from_case(self):
        for w in self.winfo_children():
            w.destroy()
        self.cases_frame = tk.Frame(self, bg="#001f3f")
        self.cases_frame.pack(fill='both', expand=True)
        self._show_header(self.cases_frame)

        body = tk.Frame(self.cases_frame, bg="#001f3f")
        body.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(body, text="REMOVE FROM CASE", bg="#001f3f", fg="white",
                font=("Times New Roman", 40, "bold")).pack(pady=20)

        # CASE ID
        tk.Label(body, text="CASE ID:", bg="#001f3f", fg="white", font=("Times New Roman", 28)).pack(pady=5)
        cid = tk.StringVar()
        tk.Entry(body, textvariable=cid, font=("Times New Roman", 28), width=20).pack(pady=10)

        # Checkbox fields
        fields_to_clear = {
            "VICTIMS": tk.BooleanVar(),
            "SUSPECTS": tk.BooleanVar(),
            "EVIDENCE": tk.BooleanVar(),
            "CURRENT PERSONNEL": tk.BooleanVar()
        }

        for label, var in fields_to_clear.items():
            tk.Checkbutton(
                body,
                text=f"CLEAR {label}",
                variable=var,
                bg="#001f3f",
                fg="white",
                font=("Times New Roman", 26),
                selectcolor="#001f3f",
                activebackground="#001f3f",
                activeforeground="white",
                anchor="w",
                width=30,
                padx=10
            ).pack(pady=4)

        # Submit button
        def do():
            case_id = cid.get().strip()
            if not case_id:
                messagebox.showerror("Error", "CASE ID IS REQUIRED")
                return

            self.cursor.execute("SELECT 1 FROM cases WHERE id=%s", (case_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "CASE ID DOES NOT EXIST")
                return

            updates = []
            for field, var in fields_to_clear.items():
                if var.get():
                    db_col = field.lower().replace(" ", "_")
                    updates.append(f"{db_col} = NULL")

            if not updates:
                messagebox.showinfo("NOTICE", "NO FIELDS SELECTED TO CLEAR")
                return

            try:
                sql = f"UPDATE cases SET {', '.join(updates)} WHERE id = %s"
                self.cursor.execute(sql, (case_id,))
                self.conn.commit()
                messagebox.showinfo("SUCCESS", "FIELDS REMOVED FROM CASE")
                self._view_cases()
            except Exception as e:
                messagebox.showerror("DATABASE ERROR", str(e))

        # Buttons
        tk.Button(body, text="REMOVE", command=do, font=("Times New Roman", 28), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack(pady=20)
    	
        tk.Button(body, text="BACK", command=lambda: [self.cases_frame.destroy(), self._open_cases_menu()], font=("Times New Roman", 28), bg="#001f3f", fg="white", bd=0, highlightthickness=0).pack()

 
    def _logout(self):
        for w in self.winfo_children():
            w.destroy()
        self._create_login_frame()

if __name__ == "__main__":
    app = MDCApp()
    app.mainloop()