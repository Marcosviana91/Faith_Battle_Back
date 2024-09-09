from colorama import Fore, Back, Style


class C_Print:
    # Usado para eventuais problemas
    def danger(self, msg):
        '''
        Usado para eventuais problemas
        '''
        print(Fore.RED + Back.YELLOW + Style.BRIGHT +
              "DEV DANGER:\t" + Style.RESET_ALL + msg)

    # Usado para informações do correto funcionamento do sistema
    def info(self, msg):
        '''
        Usado para informações do correto funcionamento do sistema
        '''
        print(Fore.BLUE + "DEV INFO:\t" + Style.RESET_ALL + msg)

    # Usado para informações de passo a passo do sistema
    def status(self, msg):
        '''
        Usado para informações de passo a passo do sistema
        '''
        print(f'{Fore.BLACK}{Back.GREEN}DEV STATUS:\t{
              Style.RESET_ALL}{msg}')


consolePrint = C_Print()
