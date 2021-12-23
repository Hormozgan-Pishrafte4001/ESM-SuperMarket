from tkinter import Tk, Button, Label, Entry, Frame, Toplevel, Text, Menu, StringVar
from tkinter.ttk import Treeview


class UserPanel(Tk):
    def __init__(self, total_sell, callback1, callback2, callback3):
        """
        :param total_sell: Total  sell amount
        :param callback1: Returns List of Genses
        :param callback2: Creates new Gens, parameters: name, price, info
        :param callback3: Sells a Gens, parameters: _id, amount
        """
        super(UserPanel, self).__init__()
        self.total_sell = total_sell
        self.callback3 = callback3
        self.callback2 = callback2
        self.callback1 = callback1
        self.list_gens = None
        self.title("Esmail Market")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        mother = Frame(self)
        mother.grid(row=1, column=1)
        self.label_total = Label(mother, text=f"Total Sell: {total_sell}")
        self.label_total.grid(row=1, column=1, pady=10)
        Button(mother, text="New Gens", command=self.new_gens).grid(row=3, column=1, pady=10)
        self.tree = Treeview(mother, columns=["name", "amount", "price"], show="headings")
        self.tree.grid(row=2, column=1, pady=5)
        self.tree.heading("name", text="name")
        self.tree.heading("amount", text="amount")
        self.tree.heading("price", text="price")
        self.tree.column("amount", width=100)
        self.tree.column("price", width=100)
        self.tree.bind("<Button-3>", self.right_click)
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="sell", command=self.sell)
        self.menu.add_command(label="buy", command=self.buy)
        self.menu.add_command(label="view", command=self.view)
        self.menu.add_command(label="edit", command=self.edit)
        self.right_clicked_item = None
        self.load_gens()

    def right_click(self, event):
        x = event.x
        y = event.y
        item = self.tree.identify_row(y)
        if item:
            self.right_clicked_item = item
            self.menu.post(self.tree.winfo_rootx() + x, self.tree.winfo_rooty() + y)

    def sell(self):
        gens = self.list_gens[int(self.right_clicked_item)]
        in_panel = NumericInputPanel(self, "Input", f"How Many To Sell {gens.name}:")
        in_panel.wait_window()
        if in_panel.ans:
            amount = in_panel.ans
            self.callback3(gens.id, amount)
            self.load_gens()
            self.total_sell += amount * gens.price
            self.label_total.config(text=f"Total Sell: {self.total_sell}")

    def buy(self):
        gens = self.list_gens[int(self.right_clicked_item)]
        in_panel = NumericInputPanel(self, "Input", f"How Many To Buy {gens.name}:")
        in_panel.wait_window()
        if in_panel.ans:
            amount = in_panel.ans
            gens.buy(amount)
            self.load_gens()

    def view(self):
        gens = self.list_gens[int(self.right_clicked_item)]
        GensViewPanel(self, gens)

    def edit(self):
        gens = self.list_gens[int(self.right_clicked_item)]
        GensViewPanel(self, gens, editable=True).wait_window()
        self.load_gens()

    def load_gens(self):
        for i in range(len(self.tree.get_children(""))):
            self.tree.delete(str(i))
        self.list_gens = self.callback1()
        for index, gens in enumerate(self.list_gens):
            self.tree.insert("", "end", str(index), values=(gens.name, gens.amount, gens.price))

    def new_gens(self):
        NewGensPanel(self, self.callback2).wait_window()
        self.load_gens()


class NewGensPanel(Toplevel):
    def __init__(self, master, callback):
        # callback1: calls it whenever user presses ok with name, price, info
        super(NewGensPanel, self).__init__(master)
        self.callback = callback
        self.geometry("400x300")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        mother = Frame(self)
        mother.grid(row=1, column=1)
        frame1 = Frame(mother)
        frame1.grid(row=1, column=1)
        Label(frame1, text="Name:").grid(row=1, column=1)
        Label(frame1, text="Price:").grid(row=2, column=1)
        self.ent_name = Entry(frame1)
        self.ent_name.grid(row=1, column=2, pady=5)
        self.ent_price = Entry(frame1)
        self.ent_price.grid(row=2, column=2, pady=5)
        Label(mother, text="Info:").grid(row=2, column=1, pady=5, sticky="w")
        self.txt_info = Text(mother, width=30, height=4)
        self.txt_info.grid(row=3, column=1, pady=5)
        Button(mother, text="OK", command=self.ok).grid(row=4, column=1, pady=5)
        self.err_message = Label(mother)

    def ok(self):
        name = self.ent_name.get()
        price = self.ent_price.get()
        if price.isnumeric():
            price = int(price)
        else:
            self.err_message.config(text="Price is not integer.")
            self.err_message.grid(row=5, column=1)
            return
        info = self.txt_info.get("0.0", "end")
        self.callback(name, price, info)
        self.destroy()


class NumericInputPanel(Toplevel):
    def __init__(self, master, title, message):
        super(NumericInputPanel, self).__init__(master)
        self.title(title)
        Label(self, text=message).grid(row=1, column=1, pady=10, padx=5)
        self.ent = Entry(self)
        self.ent.grid(row=2, column=1, pady=5, padx=5)
        Button(self, text="OK", command=self.ok).grid(row=3, column=1, pady=5, padx=5)
        self.err_message = Label(self)
        self.ans = None

    def ok(self):
        inp = self.ent.get()
        if inp.isnumeric():
            self.ans = int(inp)
            self.destroy()
        else:
            self.err_message.grid(row=4, column=1, pady=5, padx=5)
            self.err_message.config(text="You should enter numeric input.", fg="red")


class GensViewPanel(Toplevel):
    def __init__(self, master, gens, editable=False):
        super(GensViewPanel, self).__init__(master)
        self.gens = gens
        self.title("Gens Info")
        frame1 = Frame(self)
        frame1.grid(row=1, column=1, pady=5, padx=5)
        Label(frame1, text="Name:").grid(row=1, column=1)
        text_var = StringVar(self, gens.name)
        if editable:
            self.ent = Entry(frame1, textvariable=text_var)
        else:
            self.ent = Entry(frame1, state="disabled", textvariable=text_var)
        self.ent.grid(row=1, column=2, padx=5)
        Label(self, text=f"ID: {gens.id}").grid(row=2, column=1, padx=5, pady=5)
        Label(self, text=f"Amount: {gens.amount}").grid(row=3, column=1, pady=5, padx=5)
        Label(self, text="Info:").grid(row=5, column=1, pady=5, padx=5)
        frame2 = Frame(self)
        frame2.grid(row=4, column=1, pady=5, padx=5)
        Label(frame2, text="Price:").grid(row=1, column=1)
        text_var2 = StringVar(self, gens.price)
        if editable:
            self.ent_price = Entry(frame2, textvariable=text_var2)
        else:
            self.ent_price = Entry(frame2, state="disabled", textvariable=text_var2)
        self.ent_price.grid(row=1, column=2, padx=5)
        self.txt = Text(self, width=30, height=4)
        self.txt.insert("end", gens.info)
        self.txt.grid(row=6, column=1, pady=5, padx=5)
        if not editable:
            self.txt.config(state="disabled")
        if editable:
            Button(self, text="OK", command=self.ok).grid(row=7, column=1)

    def ok(self):
        self.gens.edit(self.ent.get(), int(self.ent_price.get()), self.txt.get("0.0", "end"))
        self.destroy()
