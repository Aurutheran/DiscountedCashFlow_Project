#FastAPI Code
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#Finance Code
import finance

app = FastAPI()
res = {}
DCFValue = 0
CurrentValue = 0
MarginOfSafety = 0

app.mount("/static", StaticFiles(directory="static"), name="static") #html_css

templates = Jinja2Templates(directory="html_css") #html_css

@app.get('/')
def render(request: Request):
    #return templates.TemplateResponse("item.html", {"request": request, "DCFValue": 0, "CurrentValue": 0, "MarginOfSafety": 0})
    return templates.TemplateResponse("item.html", {"request": request, "DCFValue": DCFValue, "CurrentValue": CurrentValue, "MarginOfSafety": MarginOfSafety})

@app.post('/')
async def run(request: Request):
    data = await request.form()
    res.update(data)
    print(data)
    ticker = res['ticker']
    year = res['year']
    ror = res['ROR']
    ev_ebidta = res['EV/EBIDTA']
    Terminal_ROR = res['TerminalROR']
    ebidta_gr = res['EBIDTA_GR']
    fcf = res['FCF']

    cfm = finance.DCF(ticker, year)
    cfm.setupDiscount(ror)
    cfm.setEV_EBITDA(ev_ebidta)
    cfm.setupTerminal(Terminal_ROR)
    cfm.setupEBITDA_GR(ebidta_gr)
    cfm.setupFCF_GR(fcf)

    cfm.obtainGrowthMethod()
    cfm.setGrowthAverage()
    cfm.obtainSharePrice()

    DCFValue = round(cfm.Share_Price,2)

    
    return templates.TemplateResponse("item.html", {"request": request, "data": data, "DCFValue": DCFValue, "CurrentValue": CurrentValue, "MarginOfSafety": MarginOfSafety})

@app.get('/getval')
def val():
    return {"results": res}