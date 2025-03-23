import os
#os.system("pip install pyperclip")
import pyperclip
from helpers import inventory
def copy_to_clipboard(text):
	pyperclip.copy(text)
		
def copy_selected_item():
	item = inventory.get_selected_item()
	print(f"[selected item]: {item}")
	copy_to_clipboard(str(item))


RUN_DIALOG_NAME = "Copy Selected Item"
def runDialog():
	copy_selected_item()
def run():
	print("[Item Copy]: ItemCopy Now running!")
