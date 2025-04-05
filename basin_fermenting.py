import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"basin_fermenting": {
		"items": [{"item": ""}],
		"results": [{"item":"","count": 1,"chance": 100}],
		"hate": "none",
		"time": "200",
		"OF0": "",
		"OF1": "",
		"OFA0": "1000",
		"OFA1": "1000",
		"IF0": "",
		"IF1": "",
		"IFA0": "",
		"IFA1": ""
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.InfinytyItemInput("items",300,93)
	ct.ResultsInput("results",301,324)
	ct.Input("time",423,14,width=160)
	ct.caption("ProccessTime:",308,14)
	ct.caption("________________________________________________________",593,291)
	ct.caption("hated: ",366,48)
	ct.OptionMenu("hate",['none', 'heated', 'superheated'],422,49,width=160,height=28)
	ct.ItemInput("OF1",594,247)
	ct.ItemInput("OF0",594,188)
	ct.caption("______________________Fluid Output______________________",594,157)
	ct.caption("Amount:",658,266)
	ct.caption("Amount:",658,207)
	ct.Input("OFA1",726,265,width=80)
	ct.Input("OFA0",725,207,width=80)
	ct.ItemInput("IF1",594,104)
	ct.ItemInput("IF0",594,45)
	ct.caption("_______________________Fluid Input_______________________",594,14)
	ct.Input("IFA1",721,122,width=80)
	ct.Input("IFA0",721,65,width=80)
	ct.caption("Amount:",657,64)
	ct.caption("Amount:",657,123)

def Generator(js):
	rec = {}
	rec["type"] = "createdieselgenerators:basin_fermenting"
	rec["ingredients"] = []
	for item in js.get("items"):
		if str(item.get("item")).startswith("tag:"):
			rec["ingredients"].append({"tag": str(item.get("item")).replace("tag:","")})
		else:
			rec["ingredients"].append({"item": str(item.get("item"))})
	rec["processingTime"] = int(js.get("time"))
	rec["heatRequirement"] = str(js.get("hate"))
	rec["results"] = []
	for item in js.get("results"):
		rec["results"].append({"item": str(item.get("item")),"count": int(item.get("count")),"chance": float(int(item.get("chance"))/100)})
	if js.get("OF0") != "":
		rec["results"].append({"fluid": str(js.get("OF0")),"amount": int(js.get("OFA0"))})
	if js.get("OF1") != "":
		rec["results"].append({"fluid": str(js.get("OF1")),"amount": int(js.get("OFA1"))})

	if js.get("IF0") != "":
		rec["ingredients"].append({"fluid": str(js.get("IF0")),"amount": int(js.get("IFA0"))})
	if js.get("IF1") != "":
		rec["ingredients"].append({"fluid": str(js.get("IF1")),"amount": int(js.get("IFA1"))})
	return json.dumps(rec)
