import tkinter as tk
from tkinter import scrolledtext
import json
from helpers import services


def update():
	try:
		data = services.crafting
		text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		text_box.delete(0.0,tk.END)
		text_box.insert(tk.END, json.dumps(data, indent=4))
	except:
		pass


RUN_DIALOG_NAME = "BJ Debug"
def runDialog():
	global root,text_box
	root = tk.Toplevel()
	root.title("BJ Debug")
	root.geometry("600x500")
	root.configure(bg='#222222')
	try:
		data = services.crafting
		text_box = scrolledtext.ScrolledText(root, bg='#333333', fg='#eeeeee', insertbackground='#eeeeee', highlightbackground='#00cccc', highlightcolor='#00cccc', wrap=tk.WORD)
		text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		text_box.insert(tk.END, json.dumps(data, indent=4))
	except:
		pass
	root.mainloop()

def run():
	print("[BJson Debug]: BetterJson Debug Now running!")

