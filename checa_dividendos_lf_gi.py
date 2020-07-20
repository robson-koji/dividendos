# coding: utf-8

"""
Checa dividendos no Lopes Filho - Eleven
"""
import os, sys
import requests, re, json
from bs4 import BeautifulSoup

this_path = os.path.dirname(os.path.abspath(__file__))
arquivo_saida = this_path + "/saida.html"
arquivo_template = this_path + "/email_template.html"

"""
Para testar json
aaa  = "{'asdf':[{'papel':'ABCB4','codigo-yahoo':'','nome-pregao':'ABC BRASIL','nome-pregao-ajustado':'ABC_BRASIL','tipo':'','logo-empresa':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/ABC%20BRASIL.png','logo-empresa-pequeno':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/ABC%20BRASIL.png','pay-out':52.73,'dividendo':5.42,'recomendacao':'Compra','p-vpa':1.11,'p-l':9.72,'roe':13.2,'rl-anual':-0,'pl-ult':3.666,'ebt-12m':-0,'llq-ult':418,'end-oneroso-liquido':'','nivel-corporativo':'N\u00edvel 2','setor':'Bancos','tag-along':'100.0','valor-de-mercado':4.064,'free-float':65.3,'lucratividade':19.2,'volume':17157759,'maxmin':1.0170423309511,'rentabilidade-pl':'','preco-medio':'30','class-var':'l-up'},{'papel':'TIET11','codigo-yahoo':'','nome-pregao':'AES TIETE E','nome-pregao-ajustado':'AES_TIETE_E','tipo':'','logo-empresa':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/AES%20TIETE%20E.png','logo-empresa-pequeno':'https:\/\/ondeinvestireastus.blob.core.windows.net\/logotipos\/AES%20TIETE%20E.png','pay-out':117.33,'dividendo':7.63,'recomendacao':'Compra','p-vpa':2.91,'p-l':15.39,'roe':18.9,'rl-anual':1923.53,'pl-ult':1523.47,'ebt-12m':3.08,'llq-ult':288,'end-oneroso-liquido':'','nivel-corporativo':'N\u00edvel 2','setor':'Energia El\u00e9trica','tag-along':'100.0','valor-de-mercado':4430.55,'free-float':100,'lucratividade':12.1,'volume':88486426,'maxmin':1.0215231788079,'rentabilidade-pl':'','preco-medio':'','class-var':'l-up'}]}"

aaa = aaa.replace('"', '|')
aaa = aaa.replace('\'', '"')
aaa = aaa.replace('|', '\'')

decoded = json.loads(aaa)
"""



def envia_email():
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
    html = MIMEText(open(arquivo_saida, 'r').read(), "html", "utf-8")
    msgRoot.attach(html)

    smtp.sendmail("sf@b3ircalc.online", "robson.koji@gmail.com", msgRoot.as_string())


def get_emp_lf():
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


def get_emp_gi(empresas):
    """ Navega no GI """

    boas = {}

    print "Iterando"
    for emp in empresas:
        print emp


        url = "https://www.guiainvest.com.br/raiox/default.aspx?sigla=%s" % (emp)
        #url = 'https://www.meusdividendos.com/empresa/%s' % (emp)

        response = requests.get(url)

        if response.status_code != 200:
            print "Erro response code: %d" % (response.status_code)

        soup = BeautifulSoup(response.content, features = "lxml")

        div = soup.select("div#divIndicadores")

        try:
            trs = div[0].find_all('table', {'class':'tabelaPadrao'})[0]#.find("tbody")
            dy = div[0].find_all('table', {'class':'tabelaPadrao'})[0].find_all("tr")[3].find_all("td")[4].string

            try:
                dy = float(dy.replace(',', '.').replace('%',''))
                # print trs
            except:
                print "Erro: %s" % (emp)
                continue

            if dy > 7:
                boas_conteudo = div[0].find_all('table', {'class':'tabelaPadrao'})[0].find_all("tr")[:7]
                boas[emp] = {'dy':dy, 'conteudo':boas_conteudo}
        except Exception as e:
            print e
            pass

    str_email = ''

    print "\n\n\n BOAS DY:"
    for boa in boas:
        print boa + ": " + str(boas[boa]['dy']) + "%"
        str_email += boa + ": " + str(boas[boa]['dy']) + "% \n"


    # Daqui para baixo retorna um html legal.

    boas_html = ''
    for boa in boas:
        boas_html += "<h2>" + boa + "</h2>"
        boas_html += "<table>"
        for trs in boas[boa]['conteudo']:
            try:
                #boas_html += '<tr>'
                #boas_html += unicode(trs).renderContents()
                #boas_html += '</tr>'
                boas_html += unicode(trs)#.renderContents()
            except Exception as e:
                print e
                import pdb; pdb.set_trace()
        boas_html += "</table>"
    return boas_html



def monta_html_email(boas_lf_html, boas_gi_html):
    with open(arquivo_template) as file:
        template = file.read()
        template += "<h1> GI </h1>"
        template += boas_gi_html
        template += "<h1> LF </h1>"
        template += boas_lf_html
        template += '</body></html>'
        with open(arquivo_saida, "w") as file:
            try:
                file.write(template.encode('utf-8'))
                #file.write(template)
            except Exception as e:
                print e
                import pdb; pdb.set_trace()


"""
for emp in emp_list:
    if float(emp['dividendo']) > 7 and emp['recomendacao'] == "Compra":
        print "%s: %f " % (emp['papel'], float(emp['dividendo']))

boas_html = ''
for emp in emp_list:
    if float(emp['dividendo']) > 7 and emp['recomendacao'] == "Compra":
        boas_html += "<h1>" + emp['papel'] + "</h1>"
        boas_html += "<p>" + str(emp['dividendo']) + "</p>"
"""

#"""
emp_list = get_emp_lf()

# Vem uma "variavel" com o nome null
null = None


boas_lf = []
boas_lf_html = ''
for emp in emp_list:
    #if float(emp['dividendo']) > 7 and emp['recomendacao'] == "Compra":
    boas_lf_html += "<p>" + emp['papel'] + ": " + emp['recomendacao'] + "</p>"

#    if emp['recomendacao'] == "Compra":
    boas_lf.append(emp['papel'])


#"""

#boas_lf = ['ITSA4']
#boas_lf_html =  '<p> TESTE </p>'
boas_gi_html = get_emp_gi(boas_lf)


monta_html_email(boas_lf_html, boas_gi_html)
envia_email()
