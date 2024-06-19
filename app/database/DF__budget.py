import pandas as pd

### 2. Бюджет Outsource
outsourceBudg = pd.DataFrame(
    [
        {'Currency':'uzs','Company name':'UNGM-DR', 'SoW':'Rotating Services','Contract':'UZGTL-CON-2262','opex':'-','working capital':'+','capex':'-','Sum':1320000000, 'Jan':110000000, 'Feb':110000000, 'Mar':110000000, 'Apr':110000000, 'May':110000000, 'Jun':110000000, 'Jul':110000000, 'Aug':110000000, 'Sep':110000000, 'Oct':110000000, 'Nov':110000000, 'Dec':110000000},
        {'Currency':'uzs','Company name':'UZPROMARM', 'SoW':'Valve repair Services','Contract':'UZGTL-CON-2677','opex':'-','working capital':'+','capex':'-','Sum':400000000, 'Jan':0, 'Feb':0, 'Mar':100000000, 'Apr':0, 'May':0, 'Jun':100000000, 'Jul':0, 'Aug':0, 'Sep':100000000, 'Oct':0, 'Nov':0, 'Dec':100000000},
        {'Currency':'uzs','Company name':'Uzbekximmash', 'SoW':'Rotating Services','Contract':'UZGTL-CON-2487','opex':'-','working capital':'+','capex':'-','Sum':600000000, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':200000000, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':200000000, 'Nov':0, 'Dec':200000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'Mechanical services','Contract':'UZGTL-CON-23-904','opex':'-','working capital':'+','capex':'-','Sum':1500000000, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':600000000, 'May':0, 'Jun':0, 'Jul':0, 'Aug':300000000, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':600000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'Scaffolding','Contract':'UZGTL-CON-23-984','opex':'-','working capital':'+','capex':'-','Sum':1800000000, 'Jan':250000000, 'Feb':250000000, 'Mar':200000000, 'Apr':100000000, 'May':100000000, 'Jun':100000000, 'Jul':100000000, 'Aug':100000000, 'Sep':100000000, 'Oct':200000000, 'Nov':100000000, 'Dec':200000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'Insulation ','Contract':'UZGTL-CON-23-985','opex':'-','working capital':'+','capex':'-','Sum':1900000000, 'Jan':250000000, 'Feb':250000000, 'Mar':100000000, 'Apr':100000000, 'May':100000000, 'Jun':100000000, 'Jul':100000000, 'Aug':100000000, 'Sep':100000000, 'Oct':100000000, 'Nov':300000000, 'Dec':300000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'Welding & painting','Contract':'UZGTL-CON-23-182','opex':'-','working capital':'+','capex':'-','Sum':3600000000, 'Jan':300000000, 'Feb':300000000, 'Mar':300000000, 'Apr':300000000, 'May':300000000, 'Jun':300000000, 'Jul':300000000, 'Aug':300000000, 'Sep':300000000, 'Oct':300000000, 'Nov':300000000, 'Dec':300000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'HVAC','Contract':'UZGTL-CON-23-826','opex':'+','working capital':'-','capex':'-','Sum':4800000000, 'Jan':400000000, 'Feb':400000000, 'Mar':400000000, 'Apr':400000000, 'May':400000000, 'Jun':400000000, 'Jul':400000000, 'Aug':400000000, 'Sep':400000000, 'Oct':400000000, 'Nov':400000000, 'Dec':400000000},
        {'Currency':'uzs','Company name':'Maxsusenergogaz', 'SoW':'FGS','Contract':'UZGTL-CON-23-093','opex':'+','working capital':'-','capex':'-','Sum':3480000000, 'Jan':290000000, 'Feb':290000000, 'Mar':290000000, 'Apr':290000000, 'May':290000000, 'Jun':290000000, 'Jul':290000000, 'Aug':290000000, 'Sep':290000000, 'Oct':290000000, 'Nov':290000000, 'Dec':290000000},
        {'Currency':'uzs','Company name':'SGCC', 'SoW':'Additional Services','Contract':'UZGTL-CON-2988','opex':'-','working capital':'+','capex':'-','Sum':600000000, 'Jan':50000000, 'Feb':50000000, 'Mar':50000000, 'Apr':50000000, 'May':50000000, 'Jun':50000000, 'Jul':50000000, 'Aug':50000000, 'Sep':50000000, 'Oct':50000000, 'Nov':50000000, 'Dec':50000000},
        {'Currency':'uzs','Company name':'Jet Washing equipment', 'SoW':'Additional Services','Contract':'?','opex':'-','working capital':'+','capex':'-','Sum':100000000, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':50000000, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':50000000},
        {'Currency':'uzs','Company name':'Oil analysis', 'SoW':'Additional Services','Contract':'??','opex':'+','working capital':'-','capex':'-','Sum':800000000, 'Jan':200000000, 'Feb':0, 'Mar':0, 'Apr':200000000, 'May':0, 'Jun':0, 'Jul':200000000, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':200000000, 'Dec':0},
        {'Currency':'usd','Company name':'Team industrial services', 'SoW':'Static services','Contract':'UZGTL-CON-2751','opex':'-','working capital':'+','capex':'-','Sum':500000, 'Jan':0, 'Feb':0, 'Mar':125000, 'Apr':0, 'May':0, 'Jun':125000, 'Jul':0, 'Aug':0, 'Sep':125000, 'Oct':0, 'Nov':0, 'Dec':125000},
        {'Currency':'usd','Company name':'HIMA', 'SoW':'Instrumentation Services','Contract':'UZGTL-CON-2250','opex':'+','working capital':'-','capex':'-','Sum':144374, 'Jan':144374, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Mitsubishi', 'SoW':'Rotating Services','Contract':'UZGTL-CON-2019','opex':'-','working capital':'+','capex':'-','Sum':200000, 'Jan':0, 'Feb':0, 'Mar':100000, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':100000, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Siemens', 'SoW':'Rotating Services','Contract':'???','opex':'-','working capital':'+','capex':'-','Sum':200000, 'Jan':0, 'Feb':0, 'Mar':100000, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':100000, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'ABB Service', 'SoW':'Electrical Services','Contract':'UZGTL-CON-24-006','opex':'+','working capital':'-','capex':'-','Sum':50000, 'Jan':50000, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Siemens', 'SoW':'VSD repair service','Contract':'????','opex':'+','working capital':'-','capex':'-','Sum':50000, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':50000, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'NDE Inspection services', 'SoW':'Additional Services','Contract':'?????','opex':'-','working capital':'+','capex':'-','Sum':200000, 'Jan':0, 'Feb':0, 'Mar':100000, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':100000, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Doosan', 'SoW':'PAUT for LTFT reactors','Contract':'??????','opex':'-','working capital':'-','capex':'+','Sum':200000, 'Jan':0, 'Feb':0, 'Mar':100000, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':100000, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Sasol', 'SoW':'License fee','Contract':'???????','opex':'+','working capital':'-','capex':'-','Sum':25197561, 'Jan':17197561, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':8000000, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Sasol', 'SoW':'Licensor service','Contract':'????????','opex':'+','working capital':'-','capex':'-','Sum':697846, 'Jan':0, 'Feb':697846, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'ESA(Sasol, HTAS, Chevron)', 'SoW':'ESA/TSA','Contract':'UZGTL-CON-0026','opex':'+','working capital':'-','capex':'-','Sum':7165848, 'Jan':597154, 'Feb':597154, 'Mar':597154, 'Apr':597154, 'May':597154, 'Jun':597154, 'Jul':597154, 'Aug':597154, 'Sep':597154, 'Oct':597154, 'Nov':597154, 'Dec':597154},
        {'Currency':'usd','Company name':'Emerson', 'SoW':'Vendor commissioning services','Contract':'UZGTL-CON-2142','opex':'-','working capital':'-','capex':'+','Sum':63661, 'Jan':63661, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Maintenance Experts', 'SoW':'CMMS','Contract':'UZGTL-CON-23-433','opex':'+','working capital':'-','capex':'-','Sum':73027, 'Jan':6085, 'Feb':6085, 'Mar':6085, 'Apr':6085, 'May':6085, 'Jun':6085, 'Jul':6085, 'Aug':6085, 'Sep':6085, 'Oct':6085, 'Nov':6085, 'Dec':6085},
        {'Currency':'usd','Company name':'Nol-Tec Systems', 'SoW':'Vendor commissioning services','Contract':'UZGTL-CON-1799','opex':'-','working capital':'-','capex':'+','Sum':43000, 'Jan':43000, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'GE Oil and Gas', 'SoW':'Vendor commissioning services','Contract':'UZGTL-CON-1790','opex':'-','working capital':'-','capex':'+','Sum':415896, 'Jan':415896, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'usd','Company name':'Severn Glocon', 'SoW':'Instrumentation Services','Contract':'UZGTL-CON-2599','opex':'-','working capital':'+','capex':'-','Sum':300000, 'Jan':0, 'Feb':100000, 'Mar':0, 'Apr':0, 'May':0, 'Jun':100000, 'Jul':0, 'Aug':0, 'Sep':100000, 'Oct':0, 'Nov':0, 'Dec':0},
    
    
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':20900000000, 'Jan':1850000000, 'Feb':1650000000, 'Mar':1550000000, 'Apr':2400000000, 'May':1350000000, 'Jun':1450000000, 'Jul':1550000000, 'Aug':1650000000, 'Sep':1450000000, 'Oct':1650000000, 'Nov':1750000000, 'Dec':2600000000},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':1672000, 'Jan':148000, 'Feb':132000, 'Mar':124000, 'Apr':192000, 'May':108000, 'Jun':116000, 'Jul':124000, 'Aug':132000, 'Sep':116000, 'Oct':132000, 'Nov':140000, 'Dec':208000},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':35501213, 'Jan':18517731, 'Feb':1401085, 'Mar':1128239, 'Apr':603239, 'May':603239, 'Jun':828239, 'Jul':603239, 'Aug':8753239, 'Sep':1128239, 'Oct':603239, 'Nov':603239, 'Dec':728239},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':37173213, 'Jan':18665731, 'Feb':1533085, 'Mar':1252239, 'Apr':795239, 'May':711239, 'Jun':944239, 'Jul':727239, 'Aug':8885239, 'Sep':1244239, 'Oct':735239, 'Nov':743239, 'Dec':936239},
    ]
)



### 2. Бюджет RMPD
rmpdBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':11489985, 'Jan':957499, 'Feb':957499, 'Mar':957499, 'Apr':957499, 'May':957499, 'Jun':957499, 'Jul':957499, 'Aug':957499, 'Sep':957499, 'Oct':957499, 'Nov':957499, 'Dec':957499},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':11489985, 'Jan':957499, 'Feb':957499, 'Mar':957499, 'Apr':957499, 'May':957499, 'Jun':957499, 'Jul':957499, 'Aug':957499, 'Sep':957499, 'Oct':957499, 'Nov':957499, 'Dec':957499},
    ]
)



### 3. Бюджет CofE
cofeBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':2325230, 'Jan':193770, 'Feb':193770, 'Mar':193770, 'Apr':193770, 'May':193770, 'Jun':193770, 'Jul':193770, 'Aug':193770, 'Sep':193770, 'Oct':193770, 'Nov':193770, 'Dec':193770},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':2325230, 'Jan':193770, 'Feb':193770, 'Mar':193770, 'Apr':193770, 'May':193770, 'Jun':193770, 'Jul':193770, 'Aug':193770, 'Sep':193770, 'Oct':193770, 'Nov':193770, 'Dec':193770},
    ]
)



### 4. Бюджет TAR
tarBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':19000000, 'Jan':1583333, 'Feb':1583333, 'Mar':1583333, 'Apr':1583333, 'May':1583333, 'Jun':1583333, 'Jul':1583333, 'Aug':1583333, 'Sep':1583333, 'Oct':1583333, 'Nov':1583333, 'Dec':1583333},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':19000000, 'Jan':1583333, 'Feb':1583333, 'Mar':1583333, 'Apr':1583333, 'May':1583333, 'Jun':1583333, 'Jul':1583333, 'Aug':1583333, 'Sep':1583333, 'Oct':1583333, 'Nov':1583333, 'Dec':1583333},
    ]
)



### 5. Бюджет MTK
mtkBudg = pd.DataFrame(
    [
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in uzs','opex':'','working capital':'','capex':'','Sum':924000000, 'Jan':77000000, 'Feb':77000000, 'Mar':77000000, 'Apr':77000000, 'May':77000000, 'Jun':77000000, 'Jul':77000000, 'Aug':77000000, 'Sep':77000000, 'Oct':77000000, 'Nov':77000000, 'Dec':77000000},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary local contracts in usd','opex':'','working capital':'','capex':'','Sum':73920, 'Jan':6160, 'Feb':6160, 'Mar':6160, 'Apr':6160, 'May':6160, 'Jun':6160, 'Jul':6160, 'Aug':6160, 'Sep':6160, 'Oct':6160, 'Nov':6160, 'Dec':6160},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary foreign contracts in usd','opex':'','working capital':'','capex':'','Sum':0, 'Jan':0, 'Feb':0, 'Mar':0, 'Apr':0, 'May':0, 'Jun':0, 'Jul':0, 'Aug':0, 'Sep':0, 'Oct':0, 'Nov':0, 'Dec':0},
        {'Currency':'','Company name':'', 'SoW':'','Contract':'Summary all contracts in usd','opex':'','working capital':'','capex':'','Sum':73920, 'Jan':6160, 'Feb':6160, 'Mar':6160, 'Apr':6160, 'May':6160, 'Jun':6160, 'Jul':6160, 'Aug':6160, 'Sep':6160, 'Oct':6160, 'Nov':6160, 'Dec':6160},
    ]
)