import logging


logger = logging.getLogger(__name__)


def get_mail(parameters, results, start_check=False):
    logger.info('Start to get mail...')

    mail = {}
    mail['from'] = parameters['bot_email_address']
    mail['to'] = parameters['email_address']

    message = (
        '用戶' + ' ' + parameters['name'] + ' ' + '您好' + '：' + '\n'
        '您的住址' + '「' +
        parameters['administrative_region'] + parameters['full_road'] + parameters['house_number'] + '」'
    )

    if len(results) > 0:
        mail['subject'] = '【即將停電】台電計畫性停電自動通知機器人'
        message += ('近期有以下計畫性停電安排：' + '\n')

        for result_counter, result in enumerate(results):
            try:
                message += (
                    str(result_counter + 1) + '.' + ' ' +
                    '由於' + '「' + result['reason'] + '」' + '，' +
                    '將於' + '「' + 
                    result['date'][:4] + '年' + result['date'][4:6] + '月' + result['date'][6:] + '日' + '的' + result['time_range'].replace(' ', '') + '」' + '實施計畫性停電' + '。' + '\n'
                )
            except:
                logger.error('The format of result has some problems...')
                raise Exception('The format of result has some problems.')
    else:
        mail['subject'] = '【暫無停電】台電計畫性停電自動通知機器人'
        message += ('近期暫無計畫性停電安排。' + '\n')

    message += (
        '若想查看更多詳細資訊，可點選此連結（' + parameters['url'] + '）。' + '\n' + '\n'
    )

    if start_check == True:
        mail['subject'] = '【啟動測試】台電計畫性停電自動通知機器人'
        message = ('此為機器人啟動測試訊息。' + '\n' + '\n')

    message += '台電計畫性停電自動通知機器人'

    mail['message'] = message

    logger.info('Get mail successfully...')

    return mail


def send_mail(parameters, results, start_check=False):
    logger.info('Start to send mail...')

    mail = get_mail(parameters, results, start_check)
    smtp_server = parameters['smtp_server']

    try:
        smtp_server.sendmail(from_addr=mail['from'], to_addrs=mail['to'], msg=('Subject:' + mail['subject'] + '\n' + mail['message']).encode('UTF-8'))
    except:
        logger.error('Send mail unsucessfully...')
        raise Exception('Send mail unsucessfully.')

    logger.info('Send mail successfully...')