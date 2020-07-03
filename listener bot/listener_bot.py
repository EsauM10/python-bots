from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def getNumMessages(name):
    return page.find_element_by_xpath(
            '//span[@title="{}"]/ancestor::div[4]/div[2]/div[2]/span[1]/div[2]/span'.format(name))

def getCurrentMessage(name):
    return page.find_element_by_xpath(
            '//span[@title="{}"]/ancestor::div[4]/div[2]/div[1]/span'.format(name)).text


page = webdriver.Chrome(ChromeDriverManager().install())
page.get('https://web.whatsapp.com/')

while True:
    #Aguarda até que o QR-code seja escaneado
    try:
        check_box = page.find_element_by_name('rememberMe')  
        input('Escaneie o QR Code e pressione Enter..\n')
    except NoSuchElementException: #O objeto check-box não foi encontrado
        print('')
        break

print('Carregando conversas...')

was_found = True
last_message = ''
last_number  = ''

while True:
    name = input('\nDigite o nome do Grupo ou exit para sair: ')
    if(name == 'exit'): break
    try:
        #Realiza uma busca do span com o nome do grupo
        page.find_element_by_xpath('//span[@title="{}"]'.format(name))
    except NoSuchElementException:
        print('Grupo/User não encontrado!')
    else:
        print('\nListening on '+name)
        while True:
            try:
                #Obtém o número de mensagens não lidas
                current_number = getNumMessages(name).text

                # Verifica se há novas mensagens
                if(current_number != last_number):
                    current_message = getCurrentMessage(name)
                    message = current_message.split('\n')
                    
                    # Verifica se a mensagem possui o formato Usuario\n:\nMensagem
                    if(len(message)==3): 
                        print(f'>> {message[0]}: {message[2]}')
                last_number = current_number

                was_found = True
            except NoSuchElementException:
                if was_found:
                    was_found = False
                    print('\nAguardando novas mensagens..\n')
            except StaleElementReferenceException:
                pass

page.quit()



