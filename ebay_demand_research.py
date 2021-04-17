from bs4 import BeautifulSoup
import requests
import csv


def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('server responded', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail(soup):
    try:
        title = soup.find('h1', id='itemTitle').text[15:].replace('\xa0', '')
    except:
        title = ''

    try:
        try:
            p = soup.find('span', id='prcIsum').text.strip()
        except:
            p = soup.find('span', id='mm-saleDscPrc').text.strip()

        currency, price = p.split(' ')

    except:
        currency = ''
        price = ''

    data = {'title': title, 'price': price,
            'currency': currency}

    return data


def get_index_data(soup):
    links = soup.find_all('a', class_='s-item__link')
    urls = [link.get('href') for link in links]
    return urls


def write_csv(data, url):
    with open('Ebay_mens_watches.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        row = [data['title'], data['price'],
               data['currency']]
        writer.writerow(row)
        print('done..')


def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1'
    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail(get_page(link))
        print(data)
        write_csv(data, link)


if __name__ == '__main__':
    main()
