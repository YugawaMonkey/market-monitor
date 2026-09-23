"""Refresh official statistics embedded in economy.html. Python 3, standard library only.
Run: python update-economy.py (internet required). No credentials required.
"""
import csv, io, json, math, re, sys, zipfile, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
SOURCES = {'policy.zip':'https://data.bis.org/static/bulk/WS_CBPOL_csv_col.zip',
           'cpi.zip':'https://data.bis.org/static/bulk/WS_LONG_CPI_csv_col.zip'}
INDICATORS={'GDP':'NY.GDP.MKTP.CD','GDPYY':'NY.GDP.MKTP.KD.ZG','UNEMP':'SL.UEM.TOTL.ZS','EXPORT':'TX.VAL.MRCH.CD.WT','IMPORT':'TM.VAL.MRCH.CD.WT'}
for key, ind in INDICATORS.items():
    SOURCES[key+'.json']=f'https://api.worldbank.org/v2/country/USA;CHN;EMU;GBR;JPN/indicator/{ind}?format=json&per_page=1000&date=2000:{datetime.now().year}'

def main():
    # --cache is only used to build from already downloaded, unmodified source files.
    cache=Path(sys.argv[2]) if len(sys.argv)==3 and sys.argv[1]=='--cache' else None
    raw={}
    for name,url in SOURCES.items():
        if cache: raw[name]=(cache/name).read_bytes()
        else:
            with urllib.request.urlopen(url,timeout=90) as response: raw[name]=response.read()
    result={'retrieved':datetime.now(timezone.utc).isoformat(timespec='seconds'),'countries':{c:{} for c in ['US','CN','EU','GB','JP']}}
    for filename,metric in [('policy.zip','INTR'),('cpi.zip','CPI')]:
        archive=zipfile.ZipFile(io.BytesIO(raw[filename]))
        records=csv.DictReader(io.TextIOWrapper(archive.open(archive.namelist()[0]),encoding='utf-8-sig'))
        for record in records:
            country={'XM':'EU'}.get(record['REF_AREA'],record['REF_AREA'])
            if country not in result['countries'] or record['FREQ']!='M':continue
            if metric=='CPI' and record['UNIT_MEASURE']!='628':continue
            points=[[date,float(value) if value.strip() and math.isfinite(float(value)) else None] for date,value in record.items() if re.fullmatch(r'\d{4}-\d{2}',date) and date>='2000-01']
            while points and points[-1][1] is None:points.pop()
            result['countries'][country][metric]={'points':points,'definition':record.get('COMPILATION','Index, 2010 = 100'),'source':'BIS','url':SOURCES[filename],'frequency':'月次','unit':'%' if metric=='INTR' else '2010年＝100'}
    wb={}
    for key in INDICATORS:
        payload=json.loads(raw[key+'.json']);assert payload[0]['pages']==1
        wb[key]=payload
    for country,iso in {'US':'USA','CN':'CHN','EU':'EMU','GB':'GBR','JP':'JPN'}.items():
        dest=result['countries'][country]
        for key in ['GDP','GDPYY','UNEMP']:
            points=sorted([[r['date'],r['value']] for r in wb[key][1] if r['countryiso3code']==iso])
            while points and points[-1][1] is None:points.pop()
            dest[key]={'points':points,'source':'World Bank / WDI','url':'https://data.worldbank.org/indicator/'+INDICATORS[key],'frequency':'年次','unit':'米ドル' if key=='GDP' else '%','updated':wb[key][0]['lastupdated']}
            if key=='UNEMP':
                dest[key]['source']='World Bank / WDI・ILO推計'
                assert all(v is None or 0<=v<=100 for _,v in points),'Invalid unemployment rate'
        exp={r['date']:r['value'] for r in wb['EXPORT'][1] if r['countryiso3code']==iso}
        imp={r['date']:r['value'] for r in wb['IMPORT'][1] if r['countryiso3code']==iso}
        points=[[y,exp[y]-imp[y] if exp[y] is not None and imp.get(y) is not None else None] for y in sorted(exp)]
        while points and points[-1][1] is None:points.pop()
        dest['BOT']={'points':points,'source':'World Bank / WDI（商品輸出 − 商品輸入）','url':'https://data.worldbank.org/indicator/TX.VAL.MRCH.CD.WT','frequency':'年次','unit':'米ドル','updated':wb['EXPORT'][0]['lastupdated']}
        for metric,series in dest.items():
            assert len([p for p in series['points'] if p[1] is not None])>=10,(country,metric)
            assert all(p[1] is None or math.isfinite(p[1]) for p in series['points'])
        assert len(dest)==6,country
    target=ROOT/'economy.html';html=target.read_text(encoding='utf-8')
    data=json.dumps(result,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html,n=re.subn(r'/\* ECONOMY_DATA_START \*/[\s\S]*?/\* ECONOMY_DATA_END \*/',lambda m:'/* ECONOMY_DATA_START */\nconst economyData='+data+';\n/* ECONOMY_DATA_END */',html)
    assert n==1,'Data marker missing; HTML left unchanged'
    temp=target.with_suffix('.html.tmp');temp.write_text(html,encoding='utf-8');temp.replace(target)
    print('Updated 30 series from BIS and World Bank:',result['retrieved'])
if __name__=='__main__':main()
