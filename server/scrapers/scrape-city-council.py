import requests
from bs4 import BeautifulSoup

ROOT_URL = 'http://dallascityhall.com/'
URL = 'http://dallascityhall.com/government/Pages/city-council.aspx'


r = requests.get(URL)
r.raise_for_status()    # Throw an exception if there's an error in the GET request

soup = BeautifulSoup(r.text, 'html.parser')

member_blocks = soup.select('#memberBlocks')

for member_block in member_blocks:
    link = [(ROOT_URL + a['href']) for a in member_block.find_all('a', href=True)][0]
    district_num = member_block.select_one('span').text.strip().rsplit(' ', 1)[1]
    district_num = district_num.replace(u'\u200b', '')
    district_num = int(district_num)
    council_member_name = member_block.select_one('h2')
