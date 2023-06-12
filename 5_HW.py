import logging
import aiohttp
import asyncio
import platform
import sys
from datetime import datetime, timedelta

async def request(url):

    async with aiohttp.ClientSession() as session:
        try: 
            async with session.get(url) as response:
                if response.status == 200:
                    resp = await response.json()
                    return(resp)
                logging.error(f"Error status{response.status}for {url}")
        except aiohttp.ClientConnectionError as error:
            logging.error(f"Error{error}")
        return(None)


async def get_exchange(days):
    dates = date_list(days)
    r = []
    for i in dates:    
        result = await request('https://api.privatbank.ua/p24api/exchange_rates?date='+i)
        res = {}
        currency = result.get('exchangeRate')
        for c in currency:
            if c.get("currency") == "EUR" or c.get("currency") == "USD":
                res.update({c.get("currency"): {"sale": c.get(
                    "saleRateNB"), "purchase": c.get("purchaseRateNB")}})
        r.append({i:res})
        
    return(r)
            

def date_list(date):
    date_list = []
    for i in range(int(date)):
        current_date = datetime.now().date()
        new_date = str(current_date - timedelta(days=i))
        day_date = ".".join(new_date.split("-")[::-1])
        date_list.append(day_date)
    return(date_list)


if __name__ == "__main__":
    date = sys.argv[1]
    if int(date) > 10:
        print("Please, enter the number less then 10")
    else:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(get_exchange(date))
        print(r)
