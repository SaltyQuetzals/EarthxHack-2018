import requests
from bs4 import BeautifulSoup
import sys
import os
import django

ROOT_URL = 'http://dallascityhall.com/'
URL = 'http://dallascityhall.com/government/Pages/city-council.aspx'

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import CouncilMember, District

def follow_url(URL):
    """
    Just a wrapper function that automatically raises
    an error if there's issues requesting.
    """
    r = requests.get(URL)
    r.raise_for_status()
    return r.text


html = follow_url(URL)

soup = BeautifulSoup(html, 'html.parser')

member_blocks = soup.select('#memberBlocks')


for member_block in member_blocks:
    link = [(ROOT_URL + a['href'])
            for a in member_block.find_all('a', href=True)][0]
    district_num = member_block.select_one(
        'span').text.strip().rsplit(' ', 1)[1]
    district_num = district_num.replace(u'\u200b', '')
    district_num = int(district_num)
    council_member_name = member_block.select_one('h2').text

    # Get representatives' contact information
    contact_html = follow_url(link)
    contact_soup = BeautifulSoup(contact_html, 'html.parser')

    # City of Dallas, why is everything labeled as a "phone"?
    primary_contact_email = contact_soup.select_one('.phone').text

    # Link this council member to their respective council
    district = District.objects.get(number=district_num)
    print(district)

    rep = CouncilMember(name=council_member_name, email=primary_contact_email, district=district)
    rep.save()