"""
Checa dividendos no meusdividendos.com
"""
import requests
from bs4 import BeautifulSoup


#empresas = ['ABEV','AZUL','B3SA','BBAS','BBDC','BBDC','BBSE','BRAP','BRDT','BRFS','BRKM','BRML','BTOW','CCRO','CIEL','CMIG','CSAN','CSNA','CVCB','CYRE','ECOR','EGIE','ELET','ELET','EMBR','ENBR','EQTL','FLRY','GGBR','GOAU','GOLL','HYPE','IGTA','IRBR','ITSA','ITUB','JBSS','KLBN','KROT','LAME','LREN','MGLU','MRFG','MRVE','MULT','NATU','PCAR','PETR','PETR','QUAL','RADL','RAIL','RENT','SANB','SBSP','SMLS','SUZB','TAEE','TIMP','UGPA','USIM','VALE','VIVT','VVAR','WEGE','YDUQ']

empresas = ['ITUB']


boas = {}

print "Iterando"
for emp in empresas:
    print emp

    url = 'https://www.meusdividendos.com/empresa/%s' % (emp)

    response = requests.get(url)

    if response.status_code != 200:
        print "Erro response code: %d" % (response.status_code)

    soup = BeautifulSoup(response.content)

    #conteudo = response.content()
    #dividendo = response.html.find('.list-group-item', first=True)
    dy = float(soup.select_one("li.list-group-item > div > label > span").string)
    dy = dy * 100

    if dy > 7:
        boas_conteudo = soup.findAll("li", {"class": "list-group-item"})
        boas[emp] = {'dy':dy, 'conteudo':boas_conteudo}




print "BOAS:"
for boa in boas:
    print "<h1>" + boa + "</h1>"
    print "<ul>"
    for li in boas[boa]['conteudo']:
        print li
    print "</ul>"


print "\n\n\n BOAS DY:"
for boa in boas:
    print boa + ": " + str(boas[boa]['dy']) + "%"
