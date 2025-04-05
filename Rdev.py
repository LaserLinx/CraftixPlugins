import craftixtools as ct
import customtkinter as ctk
import tkinter as tk
from PIL import Image,ImageTk
import json
import os
import easygui
from core.ui import colorschem
outline_collor = colorschem.outline_collor
dark_bg_color = colorschem.dark_bg_color
light_bg_color = colorschem.light_bg_color
I_slot00=ImageTk.PhotoImage(Image.open("assets/textures/slot00.png").resize((54,54),resample=0))


def run():
	ct.ok(f"running {__name__}")


def auto_close(event):
	"""Automaticky uzavírá závorky a uvozovky v CTkTextbox."""
	textbox = event.widget
	text = event.char
		
	pairs = {"(": ")", "[": "]", "{": "}", "\"": "\"", "'": "'"}
		
	if text in pairs:
		textbox.insert("insert", pairs[text])
		textbox.mark_set("insert", "insert-1c")

class TextBoxCommander:
	def __init__(self, textbox: ctk.CTkTextbox):
		self.textbox = textbox
		self.textbox.bind("<Control-f>", self.open_search)
		self.textbox.bind("<KeyRelease>", lambda e: self.apply_highlights())
		self.keywords = {}
		
	def open_search(self, event=None):
		search_window = ctk.CTkToplevel()
		search_window.title("Find")
		search_window.geometry("250x100")
		
		ctk.CTkLabel(search_window, text="Find:").pack(pady=5)
		search_entry = ctk.CTkEntry(search_window)
		search_entry.pack(pady=5)
		
		def update_highlight(event=None):
			self.highlight_search(search_entry.get(), "#FFFF00")
		
		search_entry.bind("<KeyRelease>", update_highlight)
		search_entry.bind("<Return>", lambda e: search_window.destroy())
		search_entry.bind("<Escape>", lambda e: search_window.destroy())
		search_entry.bind("<Control-a>", lambda e: search_entry.select_range(0, ctk.END))
		search_entry.focus_set()
		
	def highlight_search(self, keyword, color):
		self.textbox.tag_remove("search", "1.0", ctk.END)
		if not keyword:
			return
		
		start = "1.0"
		while True:
			start = self.textbox.search(keyword, start, stopindex=ctk.END, nocase=True)
			if not start:
				break
			end = f"{start}+{len(keyword)}c"
			self.textbox.tag_add("search", start, end)
			self.textbox.tag_config("search", background=color)
			start = end
		
	def add_mark_keywords(self, color: str, words: list):
		self.keywords[color] = words
		self.apply_highlights()
		
	def apply_highlights(self, event=None):
		for tag in self.textbox.tag_names():
			if not str(tag) == "json_error":
				self.textbox.tag_remove(tag, "1.0", ctk.END)
		
		for color, words in self.keywords.items():
			for word in words:
				start = "1.0"
				while True:
					start = self.textbox.search(word, start, stopindex=ctk.END, nocase=True)
					if not start:
						break
					end = f"{start}+{len(word)}c"
					self.textbox.tag_add(word, start, end)
					self.textbox.tag_config(word, foreground=color)
					start = end

class ElementEditor:
	def __init__(self, element, editable_attributes, callback):
		self.element = element
		self.callback = callback
		self.editable_attributes = editable_attributes
		self.entries = {}
		
	def open_editor(self, event):
		self.root = ctk.CTkToplevel()
		self.root.title("Element Editor")

		for i, attr in enumerate(self.editable_attributes):
			ctk.CTkLabel(self.root, text=attr).grid(row=i, column=0, padx=5, pady=5)
			entry = ctk.CTkEntry(self.root,width=1500)
			entry.grid(row=i, column=1, padx=5, pady=5)
			entry.insert(0, str(getattr(self.element, attr, "")))
			self.entries[attr] = entry
		
		ctk.CTkButton(self.root, text="Apply", command=self.apply_changes).grid(row=len(self.editable_attributes), column=0, columnspan=2, pady=10)
		
	def apply_changes(self):
		for attr, entry in self.entries.items():
			setattr(self.element, attr, entry.get())
		self.element.update()
		self.callback()
		self.root.destroy()

class DragMode:
	def __init__(self, widget):
		self.widget = widget
		widget.bind("<Button-1>", self.drag_start)
		widget.bind("<B1-Motion>", self.drag_move)
	def drag_start(self, event):
		self.widget.startX = event.x
		self.widget.startY = event.y
	def drag_move(self, event):
		x = self.widget.winfo_x() - self.widget.startX + event.x
		y = self.widget.winfo_y() - self.widget.startY + event.y
		self.widget.place(x=x, y=y)

def GetPlayground():
	return root

class caption(ctk.CTkLabel):
	def __init__(self,text,x,y, width = 0, height = 28):
		super().__init__(master=GetPlayground(), width=width, height=height,text=text)
		self.x = x
		self.y= y
		self.text = text
		self.place(x=self.x,y=self.y)
		DragMode(self)
		self.editor = ElementEditor(self, ["text"],lambda: self.update_text(self.text))
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_text(self,text):
		self.configure(text=text)
		self.text=text

class ItemInput(tk.Button):
	def __init__(self, id,x,y):
		super().__init__(master = GetPlayground(),highlightbackground=outline_collor,highlightcolor=outline_collor,background=light_bg_color,image=I_slot00,borderwidth=0,highlightthickness=1)
		self.id = id
		self.x = x
		self.y = y
		self.place(x=self.x,y=self.y)
		DragMode(self)
		self.editor = ElementEditor(self, ["id"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		pass
		
	
class Input(ctk.CTkEntry):
	def __init__(self,id,x,y,width=160):
		super().__init__(master=GetPlayground(),width=width)
		self.id = id
		self.x = x
		self.y = y
		self.width = width
		self.place(x=self.x,y=self.y)
		self.configure(state="disabled")
		DragMode(self)
		self.editor = ElementEditor(self,["id","width"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		self.configure(width=self.width)
		

class OptionMenu(ctk.CTkOptionMenu):
	def __init__(self,id,options,x,y,width = 140, height = 28):
		super().__init__(master = GetPlayground(), width = width, height = height,values=options)
		self.options = options
		self.x = x
		self.y = y
		self.id = id
		self.width = width
		self.height = height
		self.place(x=self.x,y=self.y)
		self.configure(state="disabled")
		DragMode(self)
		self.editor = ElementEditor(self,["id","options","width","height"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		self.configure(width=self.width,height=self.height,values=self.options)

class CheckBox(ctk.CTkCheckBox):
	def __init__(self, id,text,x,y, width = 100, height = 24):
		super().__init__(master=GetPlayground(), width=width, height=height,text=text,onvalue="1",offvalue="0")
		self.id = id
		self.x = x
		self.y = y
		self.text = text
		self.width = width
		self.height = height
		self.var = ctk.StringVar(value="0")
		self.configure(variable=self.var)
		self.place(x=self.x,y=self.y)
		self.configure(state="disabled")
		DragMode(self)
		self.editor = ElementEditor(self,["id","text","width","height"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		self.configure(width=self.width,height=self.height,text=self.text)

class Switch(ctk.CTkSwitch):
	def __init__(self, id,text,x,y, width = 100, height = 24):
		super().__init__(master=GetPlayground(), width=width, height=height,text=text,onvalue="1",offvalue="0")
		self.id = id
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.var = ctk.StringVar(value="0")
		self.configure(variable=self.var)
		self.place(x=self.x,y=self.y)
		self.configure(state="disabled")
		DragMode(self)
		self.editor = ElementEditor(self,["id","text","width","height"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		self.configure(width=self.width,height=self.height,text=self.text)

class Slider(ctk.CTkSlider):
	def __init__(self,id,min,max,x,y,width = 200, height = 20,orientation = "horizontal"):
		super().__init__(master = GetPlayground(), width = width, height = height,from_=min,to=max,orientation=orientation)
		self.x = x
		self.y = y
		self.max=max
		self.min=min
		self.width = width
		self.height = height
		self.orientation = orientation
		self.id = id
		self.place(x=self.x,y=self.y)
		self.configure(state="disabled")
		DragMode(self)
		self.editor = ElementEditor(self,["id","min","max","width","height","orientation"],self.update_parms)
		self.bind("<Double-Button-1>", self.editor.open_editor)
	def update_parms(self):
		self.configure(width = self.width, height = self.height,from_=self.min,to=self.max,orientation=self.orientation)



class InfinytyItemInput(ctk.CTkFrame):  # Hlavní rám
	def __init__(self, id, x, y):
		super().__init__(master=GetPlayground(),bg_color="#0000ff")  
		self.place(x=x, y=y)
		DragMode(self)
		self.editor = ElementEditor(self,["id"],lambda: None)
		self.bind("<Double-Button-1>", self.editor.open_editor)
		self.parent_frame = ctk.CTkFrame(self)  # Vnější rám
		self.parent_frame.pack(fill="both", expand=True, padx=5, pady=5)

		self.scrollable_frame = ctk.CTkScrollableFrame(self.parent_frame,border_width=0,width=255)  # ScrollableFrame
		self.scrollable_frame.pack(fill="both", expand=True)

		self.id = id
		self.update_fn()

	def add(self):
		pass


	def update_fn(self):
		for element in self.scrollable_frame.winfo_children():
			element.destroy()

		self.results = [{"item": "","item":""}]
		
		self.loop = 0

		for res in self.results:
			frame = ctk.CTkFrame(self.scrollable_frame)  # Vkládání do scrollable_frame
			frame.pack(fill="x", side="top", pady=5, padx=5)

			slot = tk.Button(
				frame, image=I_slot00, borderwidth=0, highlightthickness=1, 
				highlightbackground=outline_collor, highlightcolor=outline_collor, 
				background=light_bg_color
			)
			slot.pack(side="left", padx=5, pady=5)
			slot.config(command=lambda b=slot, l=self.loop: self.update_slot(b, l))

			slot.config(image=I_slot00)
			slot.image = I_slot00

			del_button = ctk.CTkButton(frame, text="Delete", command=lambda r=res: self.delete(r))
			del_button.pack(side="left", pady=5, padx=5)

			self.loop += 1
		
		self.add_button = ctk.CTkButton(self.scrollable_frame, text="Add", command=self.add)
		self.add_button.pack(side="top", fill="x", padx=5, pady=5)

	def delete(self, r):
		pass


class ResultsInput(ctk.CTkFrame):  # Hlavní rám
	def __init__(self, id, x, y):
		super().__init__(master=GetPlayground(),bg_color="#ff0000")  
		self.place(x=x, y=y)
		DragMode(self)
		self.editor = ElementEditor(self,["id"],lambda: None)
		self.bind("<Double-Button-1>", self.editor.open_editor)
		
		self.parent_frame = ctk.CTkFrame(self)  # Vnější rám
		self.parent_frame.pack(fill="both", expand=True, padx=5, pady=5)

		self.scrollable_frame = ctk.CTkScrollableFrame(self.parent_frame,border_width=0,width=650)  # ScrollableFrame
		self.scrollable_frame.pack(fill="both", expand=True)
		self.id = id
		self.update_fn()

	def update_fn(self):
		for element in self.scrollable_frame.winfo_children():
			element.destroy()

		self.results = {"count": "1", "chance": "100", "item": ""}
		
		self.loop = 0

		for res in self.results:
			frame = ctk.CTkFrame(self.scrollable_frame)  # Vkládání do scrollable_frame
			frame.pack(fill="x", side="top", pady=5, padx=5)

			slot = tk.Button(
				frame, image=I_slot00, borderwidth=0, highlightthickness=1, 
				highlightbackground=outline_collor, highlightcolor=outline_collor, 
				background=light_bg_color
			)
			slot.pack(side="left", padx=5, pady=5)

			l1 = ctk.CTkLabel(frame,text="Count: ")
			l1.pack(side="left",pady=5,padx=2)
			i1 = ctk.CTkEntry(frame)
			i1.pack(side="left",pady=5,padx=2)
			l2 = ctk.CTkLabel(frame,text="Chance: ")
			l2.pack(side="left",pady=5,padx=2)
			i2 = ctk.CTkEntry(frame)
			i2.pack(side="left",pady=5,padx=2)
			try:
				i1.delete(0,ctk.END)
				i1.insert(0,res.get("count"))
				i1.configure(state="disabled")
			except:
				pass
			try:
				i2.delete(0,ctk.END)
				i2.insert(0,res.get("chance"))
				i2.configure(state="disabled")
			except:
				pass

			del_button = ctk.CTkButton(frame, text="Delete")
			del_button.pack(side="left", pady=5, padx=5)

			self.loop += 1
		
		self.add_button = ctk.CTkButton(self.scrollable_frame, text="Add")
		self.add_button.pack(side="top", fill="x", padx=5, pady=5)



def export():
	
	script = "import craftixtools as ct\nimport json\ndef run():\n\tct.ok(f\"running {__name__}\")"
	script = script + f"\nSCRUCTURE = {scructure_textbox.get(1.0,ctk.END)}"
	script = script + "\nct.CreateScructure(SCRUCTURE)\ndef PlayGround():"

	for widget in root.winfo_children():
		if isinstance(widget,caption):
			script = script + f"\n\tct.caption(\"{widget.text}\",{int(widget.winfo_x())},{int(widget.winfo_y())})"
		elif isinstance(widget,ItemInput):
			script = script + f"\n\tct.ItemInput(\"{widget.id}\",{int(widget.winfo_x())},{int(widget.winfo_y())})"
		elif isinstance(widget,Input):
			script = script + f"\n\tct.Input(\"{widget.id}\",{int(widget.winfo_x())},{int(widget.winfo_y())},width={int(widget.width)})"
		elif isinstance(widget,OptionMenu):
			script = script + f"\n\tct.OptionMenu(\"{widget.id}\",{str(widget.options)},{int(widget.winfo_x())},{int(widget.winfo_y())},width={int(widget.width)},height={int(widget.height)})"
		elif isinstance(widget,CheckBox):
			script = script + f"\n\tct.CheckBox(\"{widget.id}\",\"{widget.text}\",{int(widget.winfo_x())},{int(widget.winfo_y())},width={int(widget.width)},height={int(widget.height)})"
		elif isinstance(widget,Switch):
			script = script + f"\n\tct.Switch(\"{widget.id}\",{widget.text},{int(widget.winfo_x())},{int(widget.winfo_y())},width={int(widget.width)},height={int(widget.height)})"
		elif isinstance(widget,Slider):
			script = script + f"\n\tct.Slider(\"{widget.id}\",{int(widget.min)},{int(widget.max)},{int(widget.winfo_x())},{int(widget.winfo_y())},width={int(widget.width)},height={int(widget.height)},orientation={widget.orientation})"
		elif isinstance(widget,ResultsInput):
			script = script + f"\n\tct.ResultsInput(\"{widget.id}\",{int(widget.winfo_x())},{int(widget.winfo_y())})"
		elif isinstance(widget,InfinytyItemInput):
			script = script + f"\n\tct.InfinytyItemInput(\"{widget.id}\",{int(widget.winfo_x())},{int(widget.winfo_y())})"
	
	script = script + "\n"
	script = script + str(generator_textbox.get(1.0,ctk.END))
	name = easygui.enterbox("Write Name",default="exemple.py")
	name = f"{name}.py"
	with open(os.path.join("plugins",name),"w") as f:
		f.write(script)


RUN_DIALOG_NAME = "Rdev setup"
def runDialog():
	global scructure_textbox,generator_textbox
	root_top = ctk.CTkToplevel()
	root_top.geometry("1000x600")


	def check_json_syntax(event=None):
		content = scructure_textbox.get("1.0", "end-1c")
		try:
			json.loads(content)
			scructure_textbox.tag_remove("json_error", "1.0", "end")
		except json.JSONDecodeError as e:
			line, column = e.lineno, e.colno
			start_index = f"{line}.0"
			end_index = f"{line}.end"
			scructure_textbox.tag_add("json_error", start_index, end_index)
			scructure_textbox.tag_config("json_error", background="red", foreground="white")

	buttons_frame = ctk.CTkFrame(root_top)
	buttons_frame.place(x=1,y=1)
	ctk.CTkButton(buttons_frame, text="Caption", command=lambda: caption("exemple text",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="ItemInput", command=lambda: ItemInput("0",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="Input", command=lambda: Input("0",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="OptionMenu", command=lambda: OptionMenu("0",["exemple 1","exemple 2","exemple 3"],500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="Check Box", command=lambda: CheckBox("0","exemple CheckBox",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="Switch", command=lambda: Switch("0","exemple Switch",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="Slider", command=lambda: Slider("0",0,100,500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="ResultInput", command=lambda: ResultsInput("0",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="InfinytyItemInput", command=lambda: InfinytyItemInput("0",500,300)).pack(pady=1)
	ctk.CTkButton(buttons_frame, text="Export", command=lambda: export()).pack()

	scructure_frame=ctk.CTkFrame(root_top,height=598,width=400)
	scructure_frame.place(x=150,y=1)
	scructure_textbox=ctk.CTkTextbox(scructure_frame,height=598,width=400)
	scructure_textbox.pack(side="bottom",fill="both")
	scructure_textbox.configure(tabs=("4m",))
	scructure_textbox.bind("<KeyPress>",auto_close)
	scructure_textbox.bind("<KeyRelease>",check_json_syntax)
	scructure_textbox.insert(1.0,json.dumps({"exemple": {"exemple_id": ""}},indent="\t"))
	scructure_editor_commander = TextBoxCommander(scructure_textbox)
	scructure_editor_commander.add_mark_keywords("#C061CB",["{","}"])
	scructure_editor_commander.add_mark_keywords("##F8E45C",["(",")"])
	scructure_editor_commander.add_mark_keywords("#3584E4",["[","]"])
	scructure_editor_commander.add_mark_keywords("#ED333B",["\"","\"","'","'"])
	scructure_editor_commander.add_mark_keywords("#8FF0A4",["0","1","2","3","4","5","6","7","8","9"])
	generator_frame=ctk.CTkFrame(root_top,height=598,width=400)
	generator_frame.place(x=555,y=1)
	generator_textbox=ctk.CTkTextbox(generator_frame,height=598,width=400)
	generator_textbox.pack(side="bottom",fill="both")
	generator_textbox.configure(tabs=("4m",))
	generator_textbox.bind("<KeyPress>",auto_close)
	
root = None
TAB_NAME = "Rdev"
def Tab(master):
	global root
	root = master


