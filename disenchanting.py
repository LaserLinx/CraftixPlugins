import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"disenchanting": {
		"i": "",
		"o": "",
		"xp": "100"
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	ct.ItemInput("o",553,134)
	ct.ItemInput("i",553,65)
	ct.Input("xp",721,97,width=80)
	ct.caption("XP Revard:",632,98)
	ct.caption("Input: ",507,103)
	ct.caption("Result: ",493,166)


def Generator(js):
	rec = {}
	rec["type"]="create_enchantment_industry:disenchanting"
	rec["ingredients"] = []
	if str(js.get("i")).startswith("tag:"):
		rec["ingredients"].append({"tag": str(js.get("i")).replace("tag:","")})
	else:
		rec["ingredients"].append({"item": str(js.get("i"))})
	if str(js.get("o")) == "":
		rec["results"] = [{"fluid": "create_enchantment_industry:experience","amount": int(js.get("xp"))}]
	else:	
		rec["results"] = [{"item": str(js.get("o"))},{"fluid": "create_enchantment_industry:experience","amount": int(js.get("xp"))}]
	return json.dumps(rec)


