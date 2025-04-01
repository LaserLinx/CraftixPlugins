import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
structure = {
	"ars_nouveau_imbuement": {
		"cost": "0",
		"reagent": "",
		"output": "",
		"count": "1"
	}
}


for i in range(0,8):
	structure["ars_nouveau_imbuement"][i] = ""
SCRUCTURE = structure

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.Input("cost",369,17,width=70)
	ct.caption("Source Cost: ",270,17)
	ct.caption("Count: ",449,17)
	ct.Input("count",504,17,width=70)
	ct.caption("Input: ",269,58)
	ct.ItemInput("reagent",318,58)
	ct.ItemInput("output",318,113)
	ct.caption("Result: ",263,113)
	index = 0
	for row in range(2):
		for col in range(4):
			x = 400 + col * 55
			y = 58 + row * 55
			ct.ItemInput(f"{index}", x, y)
			index += 1
#generator

def Generator(js):
	rec = {}
	rec["type"] = "ars_nouveau:imbuement"
	try:
		rec["source"] = int(js.get("cost"))
	except:
		rec["source"] = 1
	try:
		if str(js.get("reagent")).startswith("tag:"):
			rec["input"] = {"tag": str(js.get("reagent")).replace("tag:","")}
		else:
			rec["input"] = {"item": str(js.get("reagent"))}
	except:
		rec["input"] = {"item": "minecraft:dirt"}
	rec["output"] = str(js.get("output"))
	rec["count"]= int(js.get("count"))
	rec["pedestalItems"] = []
	for i in range(0,8):
		if str(js.get(str(i))) != "":
			if str(js.get(str(i))).startswith("tag:"):
				rec["pedestalItems"].append({"item": {"tag": str(js.get(str(i))).replace("tag:","")}})
			else:
				rec["pedestalItems"].append({"item": {"item": str(js.get(str(i)))}})
	return json.dumps(rec)
