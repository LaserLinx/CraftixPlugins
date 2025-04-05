import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"emptying": {
		"i": "",
		"o": "",
		"oa": "1000",
		"results": [{"item":"","count": 1,"chance": 100}]
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.ResultsInput("results",305,109)
	ct.ItemInput("i",558,45)
	ct.ItemInput("o",755,44)
	ct.Input("oa",896,61,width=80)
	ct.caption("Input: ",507,75)
	ct.caption("Amount: ",827,61)
	ct.caption("Fluid Result",820,10)

def Generator(js):
	rec = {}
	rec["type"]="create:emptying"
	rec["ingredients"] = []
	if str(js.get("i")).startswith("tag:"):
		rec["ingredients"].append({"tag": str(js.get("i")).replace("tag:","")})
	else:
		rec["ingredients"].append({"item": str(js.get("i"))})
	rec["results"] = []
	for item in js.get("results"):
		rec["results"].append({"item":str(item.get("item")),"count": int(item.get("count")),"chance": float(int(item.get("chance"))/100)})
	if str(js.get("o")) != "":
		rec["results"].append({"fluid": str(js.get("o")),"amount": int(js.get("oa"))})
	return json.dumps(rec)

