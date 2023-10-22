import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import re
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import asyncio
import aiohttp
import nest_asyncio
from datetime import datetime


class Scraping():
    def __init__(self):
        self.Site = []
        self.Title = []
        self.Id = []
        self.Manufacturer = []
        self.ManufacturerId = []
        # self.Category1 = []
        # self.Category2 = []
        # self.Category3 = []
        # self.YearOfIntroduction=[]
        # self.BodyMaterial=[]
        # self.DimensionsOfTheDevice=[]
        # self.Weight = []
        # self.Battery=[]
        # self.Os=[]
        # self.Screen_Size=[]
        # self.Screen=[]
        # self.CPU=[]
        # self.RAM=[]
        # self.Storage=[]
        # self.GPU=[]
        self.Minprice = []
        self.Maxprice = []
        self.Other = []
        self.StockStatus = []
        self.PricChart = {'product_id': [], 'meanprice': [], 'lowprice': [], 'date': []}
        self.Stores = {'product_id': [], 'site': [], 'type': [], 'shop_name': [], 'shop_city': [], 'shop_loc': [],
                       'date': [], 'price': []}

    def get_torob_links(self, test, category=99):
        """
        Get a list of torob links.
        Args:
            test (int): The test flag.
            category (int, optional): The category ID. Defaults to 99.
        Returns:
            list: The list of torob links.
        """
        try:
            # Read the torob links from the csv file
            data = pd.read_csv('torob_links.csv')
            tlinks = list(data['link'].values)
        except:
            # If the csv file does not exist or cannot be read, initialize an empty list
            tlinks = []

        # Create a new Chrome driver instance
        driver = Chrome()

        # Open the torob browse page for the specified category
        driver.get(f'https://torob.com/browse/{category}/')

        if test == 0:
            last_height = 0
            while True:
                try:
                    # Scroll the page down by 1000 pixels
                    driver.execute_script(f"window.scrollTo({last_height}, {last_height + 1000});")
                    time.sleep(1)
                    last_height += 1000
                    # Get the current height of the page
                    f = driver.execute_script("return document.body.scrollHeight")
                    if f - last_height < 0:
                        # If the difference between the current height and the last scroll height is negative, stop scrolling
                        break
                except:
                    # If an exception occurs while scrolling, continue to the next iteration
                    continue

        i = 1
        while True:
            try:
                # Get the link element at the specified index
                link = driver.find_element_by_xpath(
                    f'//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[{i}]/a').get_attribute(
                    'href')[:57]
                # Extract the link ID from the link URL
                link = link.split('/')[4]
                if link not in tlinks:
                    # Append the link ID to the list of torob links if it is not already present
                    tlinks.append(link)
                i += 1
            except:
                # If an exception occurs while getting the link, break out of the loop
                break

        # Close the driver
        driver.close()

        # Create a new DataFrame with the torob links
        torob = pd.DataFrame({'link': tlinks})

        # Save the torob links to the csv file
        torob.to_csv('torob_links.csv')

        # Return the list of torob links
        return tlinks

    def get_digikala_links(self, test, categories='notebook-netbook-ultrabook'):
        """
        Retrieves Digikala product links from the specified category.
        Args:
            test (int): Flag to indicate if the function is running in test mode.
            categories (str): The category to retrieve product links from. Default is 'notebook-netbook-ultrabook'.
        Returns:
            List[str]: A list of Digikala product links.
        """
        try:
            # Read existing links from CSV file
            data = pd.read_csv('digi_links.csv')
            tlinks = list(data['link'].values)
        except:
            tlinks = []

        # Initialize session and set headers
        i = 1
        s = requests.Session()
        site = 'https://www.digikala.com/'
        s.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

        # Make initial request to Digikala website
        res = s.get(site)
        res.raise_for_status()

        # Process each page of products
        while True:
            try:
                # Construct URL for API request
                json_url = f'https://api.digikala.com/v1/categories/{categories}/search/?has_selling_stock=1&page={i}&sort=4&seo_url=%2Fnotebook-netbook-ultrabook%2F%3Fhas_selling_stock%3D1%26page%3D1%26sort%3D4'
                res = s.get(json_url)
                res.raise_for_status()
                data = res.json()

                # Check if there are no more products
                if len(data['data']['products']) == 0:
                    break
                else:
                    products = data['data']['products']
                    for p in products:
                        if len(p['default_variant']) > 0:
                            # Extract the link from the product data
                            link = (site + p['url']['uri'])[:47]
                            link = (link.split('/')[5].split('-')[1])
                            if int(link) not in tlinks:
                                tlinks.append(link)

                print(i, end=' ')
                i += 1

                # Break loop if running in test mode
                if test != 0:
                    break
            except:
                continue

        # Save links to CSV file
        torob = pd.DataFrame({'link': tlinks})
        torob.to_csv('digi_links.csv')

        return tlinks

    def to_csv_all_links(self, data=0, name='all_data'):
        """
        Saves links to CSV file.
        :param data: dictionary for data to save
        :param name: name of the file
        :return: a csv file
        """
        # if data == 0: save all atributes of class
        if data == 0:
            d = {
                'Site': self.Site,
                'Title': self.Title,
                'Id': self.Id,
                'Manufacturer': self.Manufacturer,
                'ManufacturerId': self.ManufacturerId,
                'Min_Price': self.Minprice,
                'Max_Price': self.Maxprice,
                'StockStatus': self.StockStatus,
                'Attributes': self.Other,
            }
            # print length of each attribute before converting to dataframe
            for k, v in d.items():
                print(k, ' ', len(v))
            links = pd.DataFrame(d)
        else:
            # if data != 0: save only selected atributes
            links = pd.DataFrame(data)
        return links.to_csv(name + '.csv')

    def get_pricechart_torob(self, urls):
        '''
        get price chart from torob site
        :param urls: id of product
        :return: none just save data in attributes of class
        '''
        urls = urls

        async def get_each_laptop_from_torob0(id, json):
            # save data price chart of class
            labels = json['labels']
            for i in range(len(labels)):
                try:
                    self.PricChart['meanprice'].append(json['dataSets'][0]['entries'][i]['val'])
                except:
                    self.PricChart['meanprice'].append(None)
                try:
                    self.PricChart['lowprice'].append(json['dataSets'][1]['entries'][i]['val'])
                except:
                    self.PricChart['lowprice'].append(None)
                try:
                    self.PricChart['product_id'].append(id)
                except:
                    self.PricChart['product_id'].append(None)
                try:
                    self.PricChart['date'].append(labels[i])
                except:
                    self.PricChart['date'].append(None)

        async def fetch0(session, url):
            '''
            get price chart from torob site
            :param url: id of product
            :return: json data
            '''
            url0 = f'https://api.torob.com/v4/base-product/price-chart/?prk={url}&t=1697519794164&source=next_d'
            semaphore = asyncio.Semaphore(10)
            try:
                async with semaphore:
                    async with session.get(url0, timeout=False) as response:
                        response.raise_for_status()
                        data = await response.json()
                        return data
            except aiohttp.ClientError as e:
                print(f"Aiohttp ClientError while fetching {url}: {e}")
            except Exception as e:
                print(f"Unexpected error while fetching {url}: {e}")

        count = []

        async def scrape_book0(url):
            ''' get price chart from torob site and send data to class
            :param url: id of product
            :return: no
            '''
            async with aiohttp.ClientSession() as session:
                try:
                    json = await fetch0(session, url)
                    res = await get_each_laptop_from_torob0(url, json)
                    print(len(count))
                    count.append(True)
                    return 1
                except Exception as e:
                    print(f"Error while scraping {url}: {e}")
                    return 0

        nest_asyncio.apply()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        batch_size = 10
        for j in range(0, len(urls), batch_size):
            batch = urls[j:j + batch_size]
            results = loop.run_until_complete(asyncio.gather(*(scrape_book0(url) for url in batch)))
        for k, v in self.PricChart.items():
            print(k, len(v))

    def get_data_torob(self, test, category=99):
        async def get_each_laptop_from_torob(id, json):
            try:
                self.Id.append(id)
            except:
                self.Id.append(None)
            try:
                self.Site.append('torob')
            except:
                self.Site.append(None)
            try:
                name = ' '.join(re.findall(r'[a-zA-Z\d]+', json['name1']))
                self.Title.append(name)
            except:
                self.Title.append(None)
            try:
                m = ' '.join(re.findall(r'[a-zA-Z\d]+', json['breadcrumbs'][3]['title']))
                self.Manufacturer.append(m)
            except:
                self.Manufacturer.append(None)
            try:
                self.ManufacturerId.append(json['breadcrumbs'][3]['brand_id'])
            except:
                self.ManufacturerId.append(None)
            # try:
            #     m = ' '.join(re.findall(r'[a-zA-Zآ-ی\d]+', json['breadcrumbs'][1]['title']))
            #     self.Category1.append(m)
            # except:self.Category1.append(None)
            # try:
            #     m = ' '.join(re.findall(r'[a-zA-Zآ-ی\d]+', json['breadcrumbs'][2]['title']))
            #     self.Category2.append(m)
            # except:self.Category2.append(None)
            try:
                if len(json['stock_status']) > 3:
                    m = json['stock_status']
                else:
                    m = 'new'
                self.StockStatus.append(m)
            except:
                self.StockStatus.append(None)
            try:
                m = json['min_price']
                self.Minprice.append(m)
            except:
                self.Minprice.append(None)
            try:
                m = json['max_price']
                self.Maxprice.append(m)
            except:
                self.Maxprice.append(None)
            # YearOfIntroduction=''
            # Category3=''
            # DimensionsOfTheDevice=''
            # Screen_Size=''
            # Screen=''
            # CPU=''
            # RAM=''
            # GPU=''
            # Storage=''
            # BodyMaterial=''
            # Weight=''
            # Battery=''
            # Os=''
            try:
                Other = json['structural_specs']['headers'][0]['specs']
            except:
                Other = None
            # try:
            #     for key,value in  json['structural_specs']['headers'][0]['specs'].items():
            #         if 'سال تولید' in key.lower() or 'year' in key.lower():
            #             YearOfIntroduction+=key+':'+value+' '
            #         elif  'کاربری' in key.lower() or 'user' in key.lower() or 'بندی' in key.lower():
            #             Category3+=key+':'+value+' '
            #         elif 'ابعاد' in key.lower() or 'dimensions' in key.lower():
            #             DimensionsOfTheDevice+=key+':'+value+' '
            #         elif 'screen size' in key.lower() or 'اینچ' in key.lower() or 'inch' in key.lower() or 'سایز صفحه' in key.lower() or ('نمایش' in key.lower() and 'سایز' in key.lower()):
            #             # print(re.findall(r'[\d]+:[\d]+',value))
            #             Screen_Size+=key+':'+value+'\n'
            #         elif 'تصویر' in key.lower() or 'resolution' in key.lower() or 'RGB' in key.lower() or 'نمایشگر' in key.lower():
            #             Screen+=key+':'+value+' '
            #         elif ('cpu' in key.lower() or 'پردازنده' in key.lower() or 'فرکانس' in key.lower() or 'کش' in key.lower() or 'cache' in key.lower() or 'frequency' in key.lower() or 'هسته' in key.lower()) and 'رم' not in key.lower() and 'گرافیک' not in key.lower() and 'ram' not in key.lower():
            #             CPU+=key+':'+value+' '
            #         elif (('ram' in key.lower() or 'رم' in key.lower()) and 'گرافیک' not in key.lower()) and 'کیلوگرم' not in key.lower():
            #             RAM+=key+':'+value+' '
            #         elif 'storage' in key.lower() or 'دیسک سخت' in key.lower() or 'ssd' in key.lower() or 'hdd' in key.lower() or 'هارد دیسک' in key.lower() or 'هارد' in key.lower() or 'حافظه' in key.lower() and 'داخلی' not in key.lower() and 'رم' not in key.lower() and 'ram' not in key.lower():
            #             Storage+=key+':'+value+' '
            #         elif 'گرافیک' in key.lower() or 'directx' in key.lower() or 'gpu' in key.lower() or 'پردازنده گرافیکی' in key.lower():
            #             GPU+=key+':'+value+' '
            #         elif 'بدنه' in key.lower() :
            #             BodyMaterial+=key+':'+value+' '
            #         elif 'وزن' in key.lower() or 'weight' in key.lower() or 'کیلوگرم' in key.lower() or 'kg' in key.lower() or '(کیلوگرم)' in key.lower():
            #             Weight+=value+' '
            #         elif 'باطری' in key.lower() or 'شارژ' in key.lower() or 'آداپتور' in key.lower() or 'adapter' in key.lower() or 'battery' in key.lower():
            #             Battery+=key+':'+value+' '
            #         elif 'سیستم عامل' in key.lower() or 'os' in key.lower():
            #             Os+=key+':'+value
            #         else:
            #             Other+=key+':'+value+' '
            # except:print('aghil '+id)
            # self.YearOfIntroduction.append(YearOfIntroduction)
            # self.Category3.append(Category3)
            # self.DimensionsOfTheDevice.append(DimensionsOfTheDevice)
            # self.Screen_Size.append(Screen_Size)
            # self.Screen.append(Screen)
            # self.CPU.append(CPU)
            # self.RAM.append(RAM)
            # self.GPU.append(GPU)
            # self.Storage.append(Storage)
            # self.BodyMaterial.append(BodyMaterial)
            # self.Weight.append(Weight)
            # self.Battery.append(Battery)
            # self.Os.append(Os)
            self.Other.append(Other)
            types = json['products_info']['tab_title']
            for value in json['products_info']['result']:
                try:
                    product_id = id
                except:
                    product_id = None
                try:
                    site = 'torob'
                except:
                    site = None
                try:
                    type = types
                except:
                    type = None
                try:
                    shop_name = value['shop_name']
                except:
                    shop_name = None
                try:
                    shop_city = value['shop_name2']
                except:
                    shop_city = None
                try:
                    shop_loc = value['page_url']
                except:
                    shop_loc = None
                try:
                    date = datetime.now()
                except:
                    date = datetime.now()
                try:
                    price = value['price']
                except:
                    price = None
                try:
                    active = value['price_text_mode']
                except:
                    active = None
                if active == 'active':
                    self.Stores['product_id'].append(product_id)
                    self.Stores['site'].append(site)
                    self.Stores['type'].append(type)
                    self.Stores['shop_name'].append(shop_name)
                    self.Stores['shop_city'].append(shop_city)
                    self.Stores['shop_loc'].append(shop_loc)
                    self.Stores['date'].append(date)
                    self.Stores['price'].append(price)
            types = json['products_in_store_info']['tab_title']
            for value in json['products_in_store_info']['result']:
                try:
                    product_id = id
                except:
                    product_id = None
                try:
                    site = 'torob'
                except:
                    site = None
                try:
                    type = types
                except:
                    type = None
                try:
                    shop_name = value['shop_name']
                except:
                    shop_name = None
                try:
                    shop_city = value['shop_name2']
                except:
                    shop_city = None
                try:
                    shop_loc = value['address']
                except:
                    shop_loc = None
                try:
                    date = datetime.now()
                except:
                    date = datetime.now()
                try:
                    price = value['price']
                except:
                    price = None
                try:
                    active = value['price_text_mode']
                except:
                    active = None
                self.Stores['product_id'].append(product_id)
                self.Stores['site'].append(site)
                self.Stores['type'].append(type)
                self.Stores['shop_name'].append(shop_name)
                self.Stores['shop_city'].append(shop_city)
                self.Stores['shop_loc'].append(shop_loc)
                self.Stores['date'].append(date)
                self.Stores['price'].append(price)

        urls = self.get_torob_links(test, category)
        self.get_pricechart_torob(urls)
        semaphore = asyncio.Semaphore(10)

        async def fetch(session, url):
            url0 = f'https://api.torob.com/v4/base-product/details-log-click/?source=next_desktop&discover_method=browse&_bt__experiment=&prk={url}&rank=0&search_id=652b7f1166715c27498902de&suid=652b7f1166715c27498902de&max_seller_count=30&deliver_city='
            try:
                async with semaphore:
                    async with session.get(url0, timeout=False) as response:
                        response.raise_for_status()
                        data = await response.json()
                        return data
            except aiohttp.ClientError as e:
                print(f"Aiohttp ClientError while fetching {url}: {e}")
            except Exception as e:
                print(f"Unexpected error while fetching {url}: {e}")

        count = []

        async def scrape_book(url):
            async with aiohttp.ClientSession() as session:
                try:
                    json = await fetch(session, url)
                    res = await get_each_laptop_from_torob(url, json)
                    print(len(count))
                    count.append(True)
                    return 1
                except Exception as e:
                    print(f"Error while scraping {url}: {e}")
                    return 0

        nest_asyncio.apply()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        batch_size = 10
        for j in range(0, len(urls), batch_size):
            batch = urls[j:j + batch_size]
            results = loop.run_until_complete(asyncio.gather(*(scrape_book(url) for url in batch)))

    def get_data_digi(self, test, category='notebook-netbook-ultrabook'):
        async def get_each_laptop_from_digi(id, json):
            try:
                self.Id.append(id)
            except:
                self.Id.append(None)
            try:
                self.Site.append('digi')
            except:
                self.Site.append(None)
            try:
                name = json['data']['product']['title_en']
                self.Title.append(name)
            except:
                self.Title.append(None)
            try:
                m = json['data']['product']['brand']['title_en']
                self.Manufacturer.append(m)
            except:
                self.Manufacturer.append(None)
            try:
                self.ManufacturerId.append((json['data']['product']['brand']['id']))
            except:
                self.ManufacturerId.append(None)
            try:
                if len(json['stock_status']) > 3:
                    m = json['stock_status']
                else:
                    m = 'new'
                self.StockStatus.append(m)
            except:
                self.StockStatus.append('new')
            try:
                m = json['data']['product']['default_variant']['price']['selling_price']
                self.Minprice.append(m)
            except:
                self.Minprice.append(None)
            try:
                m = json['data']['product']['default_variant']['price']['selling_price']
                self.Maxprice.append(m)
            except:
                self.Maxprice.append(None)
            try:
                Other = json['data']['product']['specifications'][0]['attributes']
            except:
                Other = None
            self.Other.append(Other)
            types = 'خرید اینترنتی'
            for value in json['data']['product']['variants']:
                try:
                    product_id = id
                except:
                    product_id = None
                try:
                    site = 'digi'
                except:
                    site = None
                try:
                    type = types
                except:
                    type = None
                try:
                    shop_name = value['seller']['title']
                except:
                    shop_name = None
                try:
                    shop_city = value['shop_name2']
                except:
                    shop_city = None
                try:
                    shop_loc = value['seller']['url']
                except:
                    shop_loc = None
                try:
                    date = datetime.now()
                except:
                    date = datetime.now()
                try:
                    price = value['price']['selling_price']
                except:
                    price = None
                self.Stores['product_id'].append(product_id)
                self.Stores['site'].append(site)
                self.Stores['type'].append(type)
                self.Stores['shop_name'].append(shop_name)
                self.Stores['shop_city'].append(shop_city)
                self.Stores['shop_loc'].append(shop_loc)
                self.Stores['date'].append(date)
                self.Stores['price'].append(price)

        urls = self.get_digikala_links(test, category)
        semaphore = asyncio.Semaphore(10)

        async def fetch(session, url):
            url0 = f'https://api.digikala.com/v1/product/{int(url)}/'
            try:
                async with semaphore:
                    async with session.get(url0, timeout=False) as response:
                        response.raise_for_status()
                        data = await response.json()
                        return data
            except aiohttp.ClientError as e:
                print(f"Aiohttp ClientError while fetching {url}: {e}")
            except Exception as e:
                print(f"Unexpected error while fetching {url}: {e}")

        count = []

        async def scrape_book(url):
            async with aiohttp.ClientSession() as session:
                try:
                    json = await fetch(session, url)
                    res = await get_each_laptop_from_digi(url, json)
                    print(len(count))
                    count.append(True)
                    return 1
                except Exception as e:
                    print(f"Error while scraping {url}: {e}")
                    return 0

        nest_asyncio.apply()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        batch_size = 5
        for j in range(0, len(urls), batch_size):
            batch = urls[j:j + batch_size]
            results = loop.run_until_complete(asyncio.gather(*(scrape_book(url) for url in batch)))

# this is the main of the program
scrap = Scraping()
scrap.get_data_torob(0)
scrap.get_data_digi(0)
scrap.to_csv_all_links(scrap.PricChart, name='pricechart')
scrap.to_csv_all_links(scrap.Stores, name='stores')
scrap.to_csv_all_links()