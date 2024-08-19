import os
from datetime import datetime
from colorama import Fore, Style


class C_Logger:
    __current_date = datetime.now()
    __current_dir = 'logs'
    def __init__(self):
        date = str(datetime.now().date()).split('-')

        if 'logs' not in os.listdir("."):
            os.mkdir("logs")
        os.chdir('logs')

        for _date in date:
            if f'{_date}' not in os.listdir("."):
                os.mkdir(f'{_date}')
            self.__current_dir += f"/{_date}"
            os.chdir(f'{_date}')
        os.chdir('../../../../')
        print(self.__current_dir)


    def info(self, msg: str, tag: str = None):
        '''
        Usado para informações do correto funcionamento do sistema
        '''
        now = datetime.now().time()
        if now != self.__current_date:
            self.__init__()
        os.chdir(self.__current_dir)
        _name = (self.info.__name__).upper()
        if tag:
            log_msg = f'{_name.upper()}[{tag}]:\t{now} - {msg}\n'
        else:
            log_msg = f'{_name.upper()}:\t{now} - {msg}\n'
        with open(f"{_name}.txt", "a") as f:
            f.write(log_msg)
        if tag:
            print_msg = f'{Fore.BLUE}{_name.upper()}[{tag}]:\t{Style.RESET_ALL}{now} - {msg}\n'
        else:
            print_msg = f'{Fore.BLUE}{_name.upper()}:\t{Style.RESET_ALL}{now} - {msg}\n'
        print(print_msg)
        os.chdir('../../../../')

Logger = C_Logger()
