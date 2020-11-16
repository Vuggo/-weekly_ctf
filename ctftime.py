import re                                                                                                                                                                                                      
import requests as req                                                                                                                                                                                         
from bs4 import BeautifulSoup                                                                                                                                                                                  
import datetime   

# run every monday: "ctfs this week"
# check what has a start date from now until sunday
# now is datetime.today() yy mm dd,
# saturday is the iterator check to see if 2nd element = 6. yeah
def get_weekly_ctfs(today,sunday,ctf_soup):
    ctfs = "Happy Monday ~ \nHeres your weekly CTF list!\n"
    ctfs += '-------------------------------\n'
    for ctf_row in ctf_soup: 
        ctf,date = tuple(ctf_row.find_all('td', limit=2))
    
        start,end = tuple(date.text.split('—'))
        start_day,start_month = tuple(start.strip().split('.',1)[0].split())
        end_day,end_month = tuple(end.strip().split('.',1)[0].split())
        start_month, end_month = months[start_month], months[end_month]
        
        start_date = datetime.date(today.year,start_month, int(start_day))
        if start_date < sunday:
            ctfs += f'{ctf.text}: {start_month}/{start_day} - {end_month}/{end_day}\n'
            
    ctfs += '-------------------------------\n'
    return ctfs

months = {

    "Jan":1,
    "Feb":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "Aug":8,
    "Sept":9,
    "Oct":10,
    "Nov":11,
    "Dec":12
    
}

today = datetime.date.today()
sunday = today + datetime.timedelta(days = 6)

ctf_url = 'https://ctftime.org/event/list/upcoming?online=-1&format=0&restrictions=0&upcoming=true'
webhook_url = 'your discord webhook url'
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"}
r = req.get(ctf_url,headers=headers).text

soup = BeautifulSoup(r, "html5lib")
content = get_weekly_ctfs(today, sunday, soup.find_all('tr')[1:])

req.post(webhook_url, data = {"content":content})
