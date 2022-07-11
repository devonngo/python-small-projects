import requests
from bs4 import BeautifulSoup
import smtplib
import os

# web scraper setup
http_header = {
    "User-Agent": "",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

URL = "https://a.co/d/0Ws5Wro"
response = requests.get(url=URL, headers=http_header).text

soup = BeautifulSoup(response, "html.parser")

# get item name
product_name = soup.find(name="span", id="productTitle", class_="product-title-word-break").get_text().lstrip().split(",")[0]


# get price from amazon page
price = soup.find(name="span", class_="a-offscreen").get_text()
price_currency = soup.find(name="span", class_="a-price-symbol").get_text()
price_float = float(price.replace(price_currency, ''))
price_target = 100

# email setup
smtp_server = "smtp.mail.yahoo.com"

my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

subject = "Amazon Low Price Alert"
message = f"{product_name} is now {price}\n{URL}"
#
if price_float < price_target:
    with smtplib.SMTP(smtp_server, 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="test@email.com",
            msg=f"Subject: {subject}\n\n{message}"
        )
