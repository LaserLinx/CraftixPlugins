import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
structure = {
	"ars_nouveau_apparatus": {
		"keepNbtOfReagent": "0",
		"cost": "0",
		"reagent": "",
		"output": "",
		"count": "1"
	}
}


for i in range(0,48):
	structure["ars_nouveau_apparatus"][i] = ""
SCRUCTURE = structure

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.CheckBox("keepNbtOfReagent","Keep NBT",172,19,width=100,height=24)
	ct.Input("cost",395,17,width=70)
	ct.caption("Source Cost: ",296,17)
	ct.caption("Count: ",395+80,17)
	ct.Input("count",530,17,width=70)
	ct.caption("Input: ",169,52)
	ct.ItemInput("reagent",218,58)
	ct.ItemInput("output",218,121)
	ct.caption("Result: ",163,118)
	index = 0
	for row in range(6):
		for col in range(8):
			x = 300 + col * 55
			y = 50 + row * 55
			ct.ItemInput(f"{index}", x, y)
			index += 1
#generator

def Generator(js):
	rec = {}
	rec["type"] = "ars_nouveau:enchanting_apparatus"
	try:
		rec["keepNbtOfReagent"] = (js.get("keepNbtOfReagent") == "1")
	except:
		rec["keepNbtOfReagent"] = True
	try:
		rec["sourceCost"] = int(js.get("cost"))
	except:
		rec["sourceCost"] = 0
	try:
		if str(js.get("reagent")).startswith("tag:"):
			rec["reagent"] = [{"tag": str(js.get("reagent")).replace("tag:","")}]
		else:
			rec["reagent"] = [{"item": str(js.get("reagent"))}]
	except:
		rec["reagent"] = [{"item": "minecraft:dirt"}]
	rec["output"] = {"item": str(js.get("output")),"count": int(js.get("count"))}
	rec["pedestalItems"] = []
	for i in range(0,48):
		if str(js.get(str(i))) != "":
			if str(js.get(str(i))).startswith("tag:"):
				rec["pedestalItems"].append({"tag": str(js.get(str(i))).replace("tag:","")})
			else:
				rec["pedestalItems"].append({"item": str(js.get(str(i)))})
	return json.dumps(rec)
