#+================================+
#|                                |
#|      Made by: MaxTechnik       |
#|                                |
#+================================+
import craftixtools as ct
import json
def run():
	ct.ok(f"running {__name__}")
SCRUCTURE = {
	"createaddition_liquid_burning": {
		"fluid_input": "",
		"fluid_amount":"1000",
		"time":"200",
		"heat":"0"
	}
}

ct.CreateScructure(SCRUCTURE)
def PlayGround():
	offset:int=120
	ct.Input("fluid_amount",483+offset,190,width=100)
	ct.ItemInput("fluid_input",348+offset,159)
	ct.caption("Fluid:",292+offset,191)
	ct.caption("Amount:",417+offset,190)
	ct.Input("time",483+offset,226,width=100)
	ct.caption("Time:",431+offset,226)
	ct.CheckBox("heat","Super-Heated",290+offset,228,width=100,height=24)
#generator
def Generator(js):
    rec={}
    rec["type"]="createaddition:liquid_burning"
    rec["burnTime"]=int(js.get("time"))
    rec["superheated"]=bool(js.get("heat"))
    rec["input"]={"fluid":js.get("fluid_input"),"amount":int(js.get("fluid_amount"))}
    
    return json.dumps(rec)