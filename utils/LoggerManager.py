import os
from datetime import datetime
from colorama import Fore, Style, Back



class C_Logger:
    __current_date = datetime.now().date()
    __current_dir = ''

    def __init__(self):
        self.__current_dir = 'logs'
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

    def __checkData(self):
        if datetime.now().date() != self.__current_date:
            self.__init__()

    def info(self, msg: str, tag: str = None):
        '''
        Usado para informações do correto funcionamento do sistema com linguagem descritiva.
        '''
        self.__checkData()

        now = datetime.now().time()
        os.chdir(self.__current_dir)
        _name = (self.info.__name__).upper()
        if tag:
            log_msg = f'{_name.upper()}[{tag}]:\t{now} - {msg}\n'
        else:
            log_msg = f'{_name.upper()}:\t{now} - {msg}\n'
        with open(f"{_name}.txt", "a") as f:
            f.write(log_msg)
        if tag:
            print_msg = f'{Fore.BLUE}{_name.upper()}[{tag}]:\t{
                Style.RESET_ALL}{now} - {msg}'
        else:
            print_msg = f'{Fore.BLUE}{_name.upper()}:\t{Style.RESET_ALL}{
                now} - {msg}'
        print(print_msg)
        os.chdir('../../../../')

    def status(self, msg: str, tag: str = None):
        pass
        '''
        Usado para informações do passo a passo do sistema com linguagem de objetos.
        '''
        self.__checkData()

        now = datetime.now().time()
        os.chdir(self.__current_dir)
        _name = (self.status.__name__).upper()
        if tag:
            log_msg = f'{_name.upper()}[{tag}]:\t{now} - {msg}\n'
        else:
            log_msg = f'{_name.upper()}:\t{now} - {msg}\n'
        with open(f"{_name}.txt", "a") as f:
            f.write(log_msg)
        # if tag:
        #     print_msg = f'{Fore.BLACK}{Back.GREEN}{_name.upper()}[{tag}]:\t{
        #         Style.RESET_ALL}{now} - {msg}'
        # else:
        #     print_msg = f'{Fore.BLACK}{Back.GREEN}{_name.upper()}:\t{Style.RESET_ALL}{
        #         now} - {msg}'
        # print(print_msg)
        os.chdir('../../../../')

    def danger(self, msg: str, tag: str = None):
        '''
        Usado para informações de Risco
        '''
        self.__checkData()

        now = datetime.now().time()
        os.chdir(self.__current_dir)
        _name = (self.danger.__name__).upper()
        if tag:
            log_msg = f'{_name.upper()}[{tag}]:\t{now} - {msg}\n'
        else:
            log_msg = f'{_name.upper()}:\t{now} - {msg}\n'
        with open(f"{_name}.txt", "a") as f:
            f.write(log_msg)
        if tag:
            print_msg = f'{Fore.RED}{Back.YELLOW}{Style.BRIGHT}{_name.upper()}[{tag}]:\t{
                Style.RESET_ALL}{now} - {msg}'
        else:
            print_msg = f'{Fore.RED}{Back.YELLOW}{Style.BRIGHT}{_name.upper()}:\t{Style.RESET_ALL}{
                now} - {msg}'
        print(print_msg)
        os.chdir('../../../../')



Logger = C_Logger()
