import os
import shutil
from core import db_engine
import easygui
import json
import uuid
import threading
def run():
	print(f"running {__name__}\n waring this plugin can be very dangerous when you don't know what are you doing..")

def rebuild():
	internal_database = db_engine.database_path
	db = easygui.diropenbox()
	r=easygui.ynbox(f"Waring!!!\nThis operation DESTROY selected database ({db}) and rebuild this database to new version and replace curent Craftix3 Database are you for 100% sure Do you want to continue?\n make sure you have backup of this database.\n(after rebuild you must restart the aplication)")
	if r:
		print("Starting Building New Database")
		for file in os.listdir(internal_database):
			try:
				shutil.rmtree(os.path.join(internal_database,file))
			except:
				pass
		img_paths = []
		database_data = {}
		database_data["database"] = []
		database_data["tags"] = []
		database_mods = os.listdir(db)
		print(f"adding: {database_mods}")
		for mod in database_mods:
			if not mod == "tags":
				types = os.listdir(os.path.join(db,mod))
				print(f"adding {types}")
				for tp in types:
					items = os.listdir(os.path.join(db,mod,tp))
					for item in items:
						print(item)
						name = item.replace(".png","")
						print(name)
						img_name = str(uuid.uuid4()) + ".png"
						os.rename(os.path.join(db,mod,tp,item),os.path.join(db,mod,tp,img_name))
						database_data["database"].append({"name": str(name),"png": str(img_name),"mod": str(mod),"type": str(tp)})
						img_paths.append(os.path.join(db,mod,tp,img_name))
						print(img_paths)
					
		with open(os.path.join(internal_database,"config.json"),"w") as f:
			f.write(json.dumps(database_data))
		print("creating images dir")
		os.mkdir(os.path.join(internal_database,"images"))
		print("moving images")
		for img in img_paths:
			print(f"moving {img}")
			try:
				shutil.copy(img,os.path.join(internal_database,"images"))
			except:
				pass
		shutil.rmtree(db)
		print("Rebuild Done!")

RUN_DIALOG_NAME = "Build New Database (o2n)"
def runDialog():
	rebuild()





