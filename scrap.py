from requests_html import HTMLSession
import csv
import time

s = HTMLSession()
url = 'https://yourwebsite/shop/'

def get_links(url):
    r = s.get(url)
    items = r.html.find('div.product-inner')
    links = []
    for item in items:
        links.append(item.find('a', first=True).attrs['href'])
    return links

def get_productdata(link):
    r = s.get(link)
    title = r.html.find('h2', first=True).full_text
    price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
    img = r.html.find('img', first=True).attrs['src']

    product = {
        'title': title.strip(),
        'price': price.strip(),
        'img': img.strip()


    }
    print(product)
    return product

results = []
links = get_links(url)

for link in links:
    results.append(get_productdata(link))
    time.sleep(1)

with open('version3.csv', 'w', encoding='utf8', newline='') as f:
    fc = csv.DictWriter(f, fieldnames=results[0].keys(),)
    fc.writeheader()
    fc.writerows(results)
