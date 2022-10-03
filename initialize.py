import logging
import os
import configparser
import json
import smtplib


logger = logging.getLogger(__name__)


def global_initialize():
    logger.info('Start to initialize global parameters...')

    if not os.path.exists('/root/TPOAN/config.ini'):
    # if not os.path.exists('config.ini'):
        logger.error('Config file does not exixt...')
        raise Exception('Config file does not exixt.')

    config = configparser.ConfigParser()

    try:
        config.read('/root/TPOAN/config.ini', encoding='UTF-8')
        # config.read('config.ini', encoding='UTF-8')
    except:
        logger.error('Read config file unsuccessfully...')
        raise Exception('Read config file unsuccessfully.')

    try:
        bot_email_address = config['INFO']['bot_email_address']
        bot_email_password = config['INFO']['bot_email_password']
    except:
        logger.error('Get values from config file unsuccessfully...')
        raise Exception('Get values from config file unsuccessfully.')

    parameters = {}
    parameters['bot_email_address'] = bot_email_address
    parameters['smtp_server'] = get_smtp_server(bot_email_address, bot_email_password)

    users = []
    
    try:
        with open(file='/root/TPOAN/users.json', mode='r', encoding='UTF-8') as file:
        # with open(file='users.json', mode='r', encoding='UTF-8') as file:
            for user in file:
                users.append(json.loads(user))
    except:
        logger.error('Read users file unsuccessfully...')
        raise Exception('Read users file unsuccessfully.')

    logger.info('Initialize global parameters successfully...')

    return parameters, users


def local_initialize(parameters, user):
    logger.info('Start to initialize local parameters...')

    try:
        parameters['name'] = user['name']
        parameters['url'] = get_url(user['area'])
        parameters['administrative_region'] = user['administrative_region']
        parameters['full_road'] = (user['road'] + user['lane'] + user['alley'])
        parameters['house_number'] = user['house_number']
        parameters['email_address'] = user['email_address']
        parameters['admin'] = user['admin']
    except:
        logger.error('Get values from user unsucessfully...')
        raise Exception('Get values from user unsucessfully.')

    parameters['full_road_regex'] = halfwidth_to_fullwidth(parameters['full_road'])
    parameters['house_number_regex'] = halfwidth_to_fullwidth(parameters['house_number'])

    logger.info('Initialize local parameters successfully...')

    return parameters


def get_smtp_server(email_address, email_password):
    logger.info('Start to get SMTP server...')

    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)

    # Check whether the SMTP server can provide service or not
    response = smtp_server.ehlo()
    status_code = response[0]

    if status_code != 250:
        logger.error('SMTP server can not provide service.')
        raise Exception('SMTP server can not provide service.')

    # Start TLS mode
    response = smtp_server.starttls()
    status_code = response[0]

    if status_code != 220:
        logger.error('Start TLS mode unsucessfully...')
        raise Exception('Start TLS mode unsucessfully.')

    try:
        smtp_server.login(user=email_address, password=email_password)
    except:
        logger.error('Login unsucessfully...')
        raise Exception('Login unsucessfully.')

    logger.info('Get SMTP server successfully...')

    return smtp_server


def get_url(area):
    logger.info('Start to get url...')

    area_table = {
        '南投區': 'https://branch.taipower.com.tw/Content/NoticeBlackout/bulletin.aspx?&SiteID=564732602442427467&MmmID=616371300133037151'
    }

    try:
        url = area_table[area]
    except:
        logger.error('Get url unsucessfully...')
        raise Exception('Get url unsucessfully...')

    logger.info('Get url successfully...')

    return url


def halfwidth_to_fullwidth(string):
    h2f_table = {
        '0': '０',
        '1': '１',
        '2': '２',
        '3': '３',
        '4': '４',
        '5': '５',
        '6': '６',
        '7': '７',
        '8': '８',
        '9': '９'
    }

    for char in h2f_table:
        string = string.replace(char, h2f_table[char])

    return string