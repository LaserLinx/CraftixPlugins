import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"distillation": {
		"ia": "1000",
		"i": "",
		"time": "200",
		"hate": "none",
		"r": [{"item": "", "count": "1000", "chance": "100"}]
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.ItemInput("i",372,13)
	ct.Input("ia",548,14,width=80)
	ct.caption("Amount:",478,15)
	ct.caption("Fluid:",326,48)
	ct.Input("time",548,50,width=80)
	ct.caption("ProcessTime: ",440,46)
	ct.OptionMenu("hate",['none', 'heated', 'superheated'],739,18,width=80,height=28)
	ct.caption("Heat Level:",646,18)
	ct.ResultsInput("r",291,115)


def Generator(js):
	rec = {}
	rec["type"]="createdieselgenerators:distillation"
	rec["ingredients"] = [{"fluid": str(js.get("i")),"amount": int(js.get("ia"))}]
	rec["heatRequirement"]=str(js.get("hate"))
	rec["processingTime"]=int(js.get("time"))
	rec["results"]=[]
	for item in js.get("r"):
		rec["results"].append({"fluid":str(item.get("item")),"amount":int(item.get("count"))})
	print(rec)
	return json.dumps(rec)



