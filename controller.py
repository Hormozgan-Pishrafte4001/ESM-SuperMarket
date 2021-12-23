# t.me/ClassMa_py
from model import Core
from view import UserPanel
from pickle import load, dump as save
from os.path import exists


if exists("data.bin"):
    with open("data.bin", "rb") as file:
        core = load(file)
else:
    core = Core()

panel = UserPanel(
    total_sell=core.total_sell,
    callback1=core.get_gens,
    callback2=core.add_gens,
    callback3=core.sell
)
panel.mainloop()
with open("data.bin", "wb") as file:
    save(core, file)
