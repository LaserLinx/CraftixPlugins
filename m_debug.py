from core import DataAPI

def on_mouse_move(event):
	global m_debug
	if m_debug:
		print(f"Mouse position: x={event.x}, y={event.y}")

def update():
	try:
		frame.bind("<Motion>", on_mouse_move)
	except:
		pass

m_debug = False

RUN_DIALOG_NAME = "Toogle m Debug"
def runDialog():
	global m_debug
	if m_debug:
		m_debug = False
		print("[info]: m debug off")
	else:
		print("[info]: m debug on")
		m_debug = True
def run():
	global frame
	frame = DataAPI.root
	print("[m debug]: m Debug Now running!")

