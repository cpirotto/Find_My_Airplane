from bs4 import BeautifulSoup
import requests
from csv import writer

unknown_price = 'Call for Price'

air_man = input("CESSNA, PIPER, or BEECHCRAFT? Answer in ALL CAPS. ")
        air_type = input("What type of PIPER? ARCHER, J, CHEROKEE+PA28, CHEROKEE+PA32, or WARRIOR? ")
if air_man == 'CESSNA':
    air_type = input("What type of CESSNA? 140, 150, 152, 170, 172, 175, 177, or 182? ")
elif air_man == 'PIPER':
    air_type = input("What type of PIPER? ARCHER, J, CHEROKEE+PA28, CHEROKEE+PA32, or WARRIOR? ")
elif air_man == 'BEECHCRAFT':
    air_type = input("What type of BEECHCRAFT? 33+BONANZA, 35+BONANZA, or MUSKETEER? ")
else:
    print('Double check your spelling. ')

url = f"https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make={air_man}&model_group={air_man}+{air_type}+SERIES&s-type=aircraft&s-sort_key=days_since_update&s-sort_order=asc&s-page=1"
page = requests.get(url).text
soup = BeautifulSoup(page, 'lxml')
airplanes = soup.find_all('div', class_='col-xxl-3 col-xl-4 col-lg-6 col-md-6 col-sm-6 col-12')

with open(air_man + air_type + '.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Date', 'Type', 'Price', 'Reg', 'Location', 'Info']
    thewriter.writerow(header)

    result_text = soup.find('div', class_="search_options").text
    result_num = int(str(result_text).split("within")[-2].split("results")[0].split("of")[-1])

    if result_num > 24:
        page_text = soup.find_all(class_="end")
        pages = int(str(page_text).split("page=")[-1].split(">")[-4][:-1])
        for page in range(1, pages + 1):
            url = f"https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make={air_man}&model_group={air_man}+{air_type}+SERIES&s-type=aircraft&s-sort_key=days_since_update&s-sort_order=asc&s-page={page}"
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'lxml')
            airplanes = soup.find_all('div', class_='col-xxl-3 col-xl-4 col-lg-6 col-md-6 col-sm-6 col-12')

            for airplane in airplanes:
                airplane_posted_date = airplane.find('p', class_='last-update').text.replace('Last Update: ', '')
                airplane_name = airplane.find('a', class_='log_listing_click').text.replace('\n', '')
                airplane_price = airplane.find('div', class_='col-lg-6 col-md-6 col-sm-6 col-xs-6 col-6 txt-price').text.replace('\n', '')
                airplane_reg_num = airplane.find('div', class_='col-md-6 col-sm-6 col-xs-6 txt-reg-num').text.replace('Reg#', '').replace('\n', '')
                airplane_location = airplane.find('p', class_='address').text.replace('\n', '')
                airplane_description = airplane.find('p', class_='description').text.replace('More Info', '')
                more_info = airplane.h3.a['href']

                """""

                Code below finds the individual listing ID of each airplane, and writes it into the URL.
                Need to find a way to extract additional information from the link.
                Tested with BS and printing true/false if info was there, but majority is False.
                So even if I could pull the info the majority would be N/A

                id_text = airplane.find('a', class_="log_listing_click")
                id_num = str(id_text).split("data-listing_id=")[1][1:].split('"')[0]
                url_two = f"https://www.trade-a-plane.com/search?s-type=aircraft&listing_id={id_num}"

                """

                if unknown_price not in airplane_price:
                    print(f"Type: {airplane_name.strip()}")
                    print(f"Reg Num: {airplane_reg_num.strip()}")
                    print(f"Price: {airplane_price.strip()}")
                    print(f"Location: {airplane_location.strip()}")
                    print(f"More Info: https://www.trade-a-plane.com{more_info}")
                    print(f"Date Upgrade: {airplane_posted_date}")

                    print('')

                    info = [airplane_posted_date, airplane_name, airplane_price, airplane_reg_num, airplane_location, more_info]
                    thewriter.writerow(info)

    else:
        url = f"https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make={air_man}&model_group={air_man}+{air_type}+SERIES&s-type=aircraft&s-sort_key=days_since_update&s-sort_order=asc"
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        airplanes = soup.find_all('div', class_='col-xxl-3 col-xl-4 col-lg-6 col-md-6 col-sm-6 col-12')

        for airplane in airplanes:
            airplane_posted_date = airplane.find('p', class_='last-update').text.replace('Last Update: ', '')
            airplane_name = airplane.find('a', class_='log_listing_click').text.replace('\n', '')
            airplane_price = airplane.find('div',
                                           class_='col-lg-6 col-md-6 col-sm-6 col-xs-6 col-6 txt-price').text.replace(
                '\n', '')
            airplane_reg_num = airplane.find('div', class_='col-md-6 col-sm-6 col-xs-6 txt-reg-num').text.replace(
                'Reg#', '').replace('\n', '')
            airplane_location = airplane.find('p', class_='address').text.replace('\n', '')
            airplane_description = airplane.find('p', class_='description').text.replace('More Info', '')
            more_info = airplane.h3.a['href']
            if unknown_price not in airplane_price:
                print(f"Type: {airplane_name.strip()}")
                print(f"Reg Num: {airplane_reg_num.strip()}")
                print(f"Price: {airplane_price.strip()}")
                print(f"Location: {airplane_location.strip()}")
                print(f"More Info: https://www.trade-a-plane.com{more_info}")
                print(f"Date Upgrade: {airplane_posted_date}")

                print('')

                info = [airplane_posted_date, airplane_name, airplane_price, airplane_reg_num, airplane_location,
                        more_info]
                thewriter.writerow(info)

print('Search Finished')

"""""

# Things to continue working on:
# 1) Clean up the code. Can the for airplane in airplanes be created as a function?
# 2) Pull additional information: Can I ask the program to open other sites and pull in additional information?
    #Engine Time, Total Time, ADSB, etc.
# 3) Learn how to move the Excel files to a dedicated folder in a different spot on my cpu

"""