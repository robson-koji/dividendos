
# coding: utf-8

"""
Checa dividendos no Lopes Filho - Eleven
"""
import requests, re, json
from bs4 import BeautifulSoup


"""
Para testar json
aaa  = "{'asdf':[{'papel':'ABCB4','codigo-yahoo':'','nome-pregao':'ABC BRASIL','nome-pregao-ajustado':'ABC_BRASIL','tipo':'','logo-empresa':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/ABC%20BRASIL.png','logo-empresa-pequeno':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/ABC%20BRASIL.png','pay-out':52.73,'dividendo':5.42,'recomendacao':'Compra','p-vpa':1.11,'p-l':9.72,'roe':13.2,'rl-anual':-0,'pl-ult':3.666,'ebt-12m':-0,'llq-ult':418,'end-oneroso-liquido':'','nivel-corporativo':'N\u00edvel 2','setor':'Bancos','tag-along':'100.0','valor-de-mercado':4.064,'free-float':65.3,'lucratividade':19.2,'volume':17157759,'maxmin':1.0170423309511,'rentabilidade-pl':'','preco-medio':'30','class-var':'l-up'},{'papel':'TIET11','codigo-yahoo':'','nome-pregao':'AES TIETE E','nome-pregao-ajustado':'AES_TIETE_E','tipo':'','logo-empresa':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/AES%20TIETE%20E.png','logo-empresa-pequeno':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/AES%20TIETE%20E.png','pay-out':117.33,'dividendo':7.63,'recomendacao':'Compra','p-vpa':2.91,'p-l':15.39,'roe':18.9,'rl-anual':1923.53,'pl-ult':1523.47,'ebt-12m':3.08,'llq-ult':288,'end-oneroso-liquido':'','nivel-corporativo':'N\u00edvel 2','setor':'Energia El\u00e9trica','tag-along':'100.0','valor-de-mercado':4430.55,'free-float':100,'lucratividade':12.1,'volume':88486426,'maxmin':1.0215231788079,'rentabilidade-pl':'','preco-medio':'','class-var':'l-up'}]}"

aaa = aaa.replace('"', '|')
aaa = aaa.replace('\'', '"')
aaa = aaa.replace('|', '\'')

decoded = json.loads(aaa)
"""



def envia_email(html):
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.header import Header

    smtp = smtplib.SMTP()
    smtp.connect('localhost')

    msgRoot = MIMEMultipart("alternative")
    msgRoot['Subject'] = Header("Dividendos - DY", "utf-8")
    msgRoot['From'] = "robson_scripts@contabo.com"
    msgRoot['To'] = "robson.koji@gmail.com"

    #text = MIMEText(open('template.txt', 'r').read(), "plain", "utf-8")
    #msgRoot.attach(text)
    #html = MIMEText(open('template.html', 'r').read(), "html", "utf-8")

    html_email = MIMEText(html, 'html')

    msgRoot.attach(html_email)
    smtp.sendmail("sf@b3ircalc.online", "robson.koji@gmail.com", msgRoot.as_string())


def get_emp_list():
    url = 'https://ondeinvestir.lopesfilho.com.br/analises/'

    headers = {
    'Host': 'ondeinvestir.lopesfilho.com.br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://ondeinvestir.lopesfilho.com.br/analises/analise-grafica/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8,gl;q=0.7',
    'Cookie': 'PHPSESSID=8esmf1j35cd962abpnqbc8egb1; __utmc=262044560; __utmz=262044560.1567730649.4.3.utmcsr=easynvest.com.br|utmccn=(referral)|utmcmd=referral|utmcct=/configuracoes/onde-investir; ARRAffinity=20420806f3ad350fe8c053c3bb40d8c18df09175f01c05e1925be9c253b42ca7; __utma=262044560.243583620.1565226753.1568257216.1568330069.10; __utmt=1; __utmb=262044560.10.9.1568330266325',
    }


    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print "Erro response code: %d" % (response.status_code)

    soup = BeautifulSoup(response.content)

    window_dados = re.findall( r'(window.dados\s+=\s+)(.*);', str(soup))
    window_dados_list = window_dados[0][1].replace('\'', '"')
    window_dados_json = '{"windows_dados":' + window_dados_list + '}'

    emp_list = json.loads(window_dados_json)

    return emp_list['windows_dados']


emp_list = get_emp_list()

# Vem uma "variavel" com o nome null
null = None

_emp_list_exemplo = [
  {
    "papel": "ABCB4",
    "codigo-yahoo": "",
    "nome-pregao": "ABC BRASIL",
    "nome-pregao-ajustado": "ABC_BRASIL",
    "tipo": "",
    "logo-empresa": "https://ondeinvestireastus.blob.core.windows.net/logotipos/ABC%20BRASIL.png",
    "logo-empresa-pequeno": "https://ondeinvestireastus.blob.core.windows.net/logotipos/ABC%20BRASIL.png",
    "pay-out": 52.73,
    "dividendo": 5.42,
    "recomendacao": "Compra",
    "p-vpa": 1.11,
    "p-l": 9.72,
    "roe": 13.2,
    "rl-anual": 0,
    "pl-ult": 3.666,
    "ebt-12m": 0,
    "llq-ult": 418,
    "end-oneroso-liquido": "",
    "nivel-corporativo": "Nível 2",
    "setor": "Bancos",
    "tag-along": "100.0",
    "valor-de-mercado": 4.064,
    "free-float": 65.3,
    "lucratividade": 19.2,
    "volume": 20944839,
    "maxmin": 1.0260162601626,
    "rentabilidade-pl": "",
    "preco-medio": "30",
    "class-var": "l-up"
  },
  {
    "papel": "TIET11",
    "codigo-yahoo": "",
    "nome-pregao": "AES TIETE E",
    "nome-pregao-ajustado": "AES_TIETE_E",
    "tipo": "",
    "logo-empresa": "https://ondeinvestireastus.blob.core.windows.net/logotipos/AES%20TIETE%20E.png",
    "logo-empresa-pequeno": "https://ondeinvestireastus.blob.core.windows.net/logotipos/AES%20TIETE%20E.png",
    "pay-out": 117.33,
    "dividendo": 7.63,
    "recomendacao": "Compra",
    "p-vpa": 2.91,
    "p-l": 15.39,
    "roe": 18.9,
    "rl-anual": 1923.53,
    "pl-ult": 1523.47,
    "ebt-12m": 3.08,
    "llq-ult": 288,
    "end-oneroso-liquido": "",
    "nivel-corporativo": "Nível 2",
    "setor": "Energia Elétrica",
    "tag-along": "100.0",
    "valor-de-mercado": 4430.55,
    "free-float": 100,
    "lucratividade": 12.1,
    "volume": 8185961,
    "maxmin": 1.015625,
    "rentabilidade-pl": "",
    "preco-medio": "",
    "class-var": "l-up"
  }
]


for emp in emp_list:
    if float(emp['dividendo']) > 7 and emp['recomendacao'] == "Compra":
        print "%s: %f " % (emp['papel'], float(emp['dividendo']))


boas_html = ''
for emp in emp_list:
    if float(emp['dividendo']) > 7 and emp['recomendacao'] == "Compra":
        boas_html += "<h1>" + emp['papel'] + "</h1>"
        boas_html += "<p>" + str(emp['dividendo']) + "</p>"

envia_email(boas_html)
