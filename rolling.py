import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"rolling": {
		"i": "",
		"r": "",
		"c": "1"
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.caption("Input:",396,134)
	ct.caption("Result: ",391,190)
	ct.ItemInput("r",444,158)
	ct.ItemInput("i",444,97)
	ct.caption("Count: ",509,195)
	ct.Input("c",560,195,width=80)

def Generator(js):
	rec = {}
	rec["type"] = "createaddition:rolling"
	rec["result"] = {"item": str(js.get("r")),"count": int(js.get("c"))}
	if str(js.get("i")).startswith("tag:"):
		rec["input"] = {"tag": str(js.get("i")).replace("tag:","")}
	else:
		rec["input"] = {"item": str(js.get("i"))}
	return json.dumps(rec)

