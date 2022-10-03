import schedule
import time
import logging

from initialize import global_initialize, local_initialize
from crawler import check_contents
from mail import send_mail


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

fh = logging.FileHandler('/root/TPOAN/TPOAN.log', mode='a',encoding='UTF-8')
# fh = logging.FileHandler('TPOAN.log', mode='a',encoding='UTF-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.addHandler(fh)


def main(start_check=False):
    logger.info('Execution condition has been reached...')
    logger.info('Start to run program...')

    global_parameters, users = global_initialize()

    for user in users:
        local_parameters = local_initialize(global_parameters, user)
        results = check_contents(local_parameters)

        if (user['admin'] == 'False' and (len(results) == 0 or start_check == True)):
            continue

        send_mail(local_parameters, results, start_check)

    global_parameters['smtp_server'].quit()


if __name__ == '__main__':
    main(start_check=True)
    
    schedule.every().day.at('05:00').do(main)

    while True:
        schedule.run_pending()

        logger.info('Wait for next execution...')
        time.sleep(60)