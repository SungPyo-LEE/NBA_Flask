from urllib.request import urlopen
from bs4 import BeautifulSoup


html=urlopen("https://www.cbssports.com/nba/injuries/")

page=html.read() #이제 이놈을 soup를 이용하여 파싱해라.
soup =BeautifulSoup(page,'html.parser')
children_node=list(soup.children)
text=soup.find_all('div',"Page-colMain")

whole_t_name=text[0].find_all('span',"TeamName")
whole_p_name=text[0].find_all('span',"CellPlayerName--short")