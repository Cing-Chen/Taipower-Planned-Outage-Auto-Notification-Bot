import logging
import requests
import datetime
import re

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def get_contents(parameters):
    logger.info('Start to get contents...')

    html = requests.get(parameters['url'])
    soup = BeautifulSoup(html.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'PowerCutTable'})

    datas = []

    for table in tables:
        date = table.get('id')

        if int(date) < int(str(datetime.date.today()).replace('-', '')):
            continue

        data = {}
        data['date'] = date

        trs = table.find_all('tr')
        announcements = []

        for trs_counter, tr in enumerate(trs):
            if trs_counter == 0:
                continue

            tds = tr.find_all('td')

            for br in tds[1].find_all('br'):
                br.replace_with('<SEP>')

            items_str = tds[1].get_text().replace('，', '')
            items = items_str.split('<SEP>')
            announcements_items_str = items_str.split('<SEP><SEP>')

            for announcement_index, announcement_items_str in \
                    enumerate(announcements_items_str):
                announcement_items = announcement_items_str.split('<SEP>')

                if announcement_index == 0:
                    announcement_items = announcement_items[1:]

                announcement = {}

                try:
                    announcement['time_range'] = tds[0].get_text()[2:]
                except:
                    logger.error(
                        'The format of time_range has some problems...')
                    raise Exception(
                        'The format of time_range has some problems.')

                try:
                    announcement['reason'] = items[0]
                    announcement['administrative_region'] = \
                        announcement_items[0]
                except:
                    logger.error('The format of item has some problems...')
                    raise Exception('The format of item has some problems.')

                roads = []

                for announcement_items_counter, item in enumerate \
                        (announcement_items):
                    # Ignore reason and administrative region block
                    if announcement_items_counter < 2:
                        continue
                    elif announcement_items_counter == \
                            len(announcement_items) - 1:
                        # Remove '等' char
                        item = item[:-1]

                    house_numbers = item.split('、')

                    road = {}
                    road['house_numbers'] = house_numbers

                    roads.append(road)

                announcement['roads'] = roads

                announcements.append(announcement)

        data['announcements'] = announcements

        datas.append(data)

    logger.info('Get contents successfully...')

    return datas


def check_contents(parameters):
    logger.info('Start to check contents...')

    datas = get_contents(parameters)

    results = []

    for data in datas:
        for announcement in data['announcements']:
            if parameters['administrative_region'] == announcement['administrative_region']:
                for road in announcement['roads']:
                    for index, house_number in enumerate(road['house_numbers']):
                        if index == 0 and re.match(parameters['full_road_regex'], house_number) == None:
                            break

                        if re.search(parameters['house_number_regex'], house_number) != None:
                            results.append(
                                {
                                    'date': data['date'],
                                    'time_range': announcement['time_range'],
                                    'reason': announcement['reason']
                                }
                            )

    logger.info('Check contents successfully...')

    return results