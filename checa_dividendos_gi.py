# coding: utf-8

"""
Checa dividendos no guiainvest.com.br
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


def main():
    """Função principal da aplicação.
    """

    import requests
    from bs4 import BeautifulSoup


    # IBOV
    empresas = ['ITSA4'] #['ABEV3','AZUL4','B3SA3','BBAS3','BBDC3','BBDC4','BBSE3','BRAP4','BRDT3','BRFS3','BRKM5','BRML3','BTOW3','CCRO3','CIEL3','CMIG4','CSAN3','CSNA3','CVCB3','CYRE3','ECOR3','EGIE3','ELET3','ELET6','EMBR3','ENBR3','EQTL3','FLRY3','GGBR4','GOAU4','GOLL4','HYPE3','IGTA3','IRBR3','ITSA4','ITUB4','JBSS3','KLBN11','KROT3','LAME4','LREN3','MGLU3','MRFG3','MRVE3','MULT3','NATU3','PCAR4','PETR3','PETR4','QUAL3','RADL3','RAIL3','RENT3','SANB11','SBSP3','SMLS3','SUZB3','TAEE11','TIMP3','UGPA3','USIM5','VALE3','VIVT4','VVAR3','WEGE3','YDUQ3']

    # IDIV
    #empresas = ['ABCB4','ARZZ3','BBSE3','BRAP4','BRKM5','BRSR6','CCRO3','CMIG4','CPLE6','CSMG3','ECOR3','EGIE3','ELET6','ENBR3','EZTC3','FESA4','FLRY3','GRND3','HGTX3','ITSA4','ITUB3','ITUB4','MRVE3','PARD3','PSSA3','QUAL3','SANB11','SAPR11','SLCE3','TAEE11','TIET11','TRPL4','TUPY3','UNIP6','VIVT4','YDUQ3']
    #empresas = ['ITUB4']


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

        trs = div[0].find_all('table', {'class':'tabelaPadrao'})[0]#.find("tbody")
        dy = div[0].find_all('table', {'class':'tabelaPadrao'})[0].find_all("tr")[3].find_all("td")[4].string

        try:
            dy = float(dy.replace(',', '.').replace('%',''))
            print trs
        except:
            print "Erro: %s" % (emp)
            continue

        if dy > 7:
            boas_conteudo = div[0].find_all('table', {'class':'tabelaPadrao'})[0].find_all("tr")[:7]
            boas[emp] = {'dy':dy, 'conteudo':boas_conteudo}


    print "\n\n\n BOAS DY:"
    for boa in boas:
        print boa + ": " + str(boas[boa]['dy']) + "%"


    boas_html = ''
    for boa in boas:
        boas_html += "<h1>" + boa + "</h1>"
        boas_html += "<table>"
        for trs in boas[boa]['conteudo']:
            boas_html += str(trs)
        boas_html += "</table>"

    envia_email(boas_html)

    """
    print "BOAS:"
    for boa in boas:
        print "<h1>" + boa + "</h1>"
        print "<table>"
        for li in boas[boa]['conteudo']:
            print li
        print "</table>"


    """

# Pegar todos os papeis daqui. Vai sumir!
#http://www.bmfbovespa.com.br/pt_br/produtos/indices/acoes-por-indice/

if __name__ == "__main__":
    main()
