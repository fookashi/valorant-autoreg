from random import choices,choice
from time import sleep
import warnings
import string

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import randomname

warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_URL = 'https://auth.riotgames.com/login#client_id=play-valorant-web-prod&nonce=NzcsMTA2LDEwMCwx&prompt=signup&redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in%2F%3Fredirect%3D%2Fdownload%2F&response_type=token%20id_token&scope=account%20openid&state=c2lnbnVw&ui_locales=tr'
DIGITS_LETTERS=string.ascii_letters+string.digits

def generate_name():
    name=randomname.get_name(sep='')
    data=f'{name}'.join((choices(DIGITS_LETTERS,k=2)))
    return data

def update_crx():
    crx_page_url = "https://chrome.google.com/webstore/detail/hektcaptcha-hcaptcha-solv/bpfdbfnkjelhloljelooneehdalcmljb"
    ext_id = crx_page_url.split('/')[-1]
    download_link = f"https://clients2.google.com/service/update2/crx?response=redirect&os=crx&arch=x86-64&nacl_arch=x86-64&prod=chromecrx&prodchannel=unknown&prodversion=88.0.4324.150&acceptformat=crx2,crx3&x=id%3D{ext_id}%26uc"
    with open('solver.crx', 'wb') as file:
        addon_binary = requests.get(download_link).content
        file.write(addon_binary)

class RiotGen():
    def __init__(self):
        update_crx()
        options = webdriver.ChromeOptions()
        options.add_extension('solver.crx')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.headless = False
        self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager(version="114.0.5735.16").install())

    def login(self):
        name = generate_name()
        email = f"{name}@rambler.ru"
        password = ''.join(choices(DIGITS_LETTERS, k=16))
        password=f"{password}{choice(string.ascii_uppercase)}"
        try:
            self.driver.get(BASE_URL)
            sleep(2)
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input', email)
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div[1]/input', '01012000')
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div/input', name)
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input').send_keys(password)
            self.insert_field('/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[3]/div/input', password)
            print('[*] solving the hcaptcha')
            sleep(30)
            if self.driver.current_url == BASE_URL:
                return
            print(f'Account created: {name}:{password}')
            with open('Credentials.txt',mode='a') as f:
                f.write(f'{name}:{password}\n')
        except Exception as e:
            print('Failed to Create Account, reason:', e)

    def insert_field(self, value, arg):
        self.driver.find_element(by=By.XPATH, value=value).send_keys(arg)
        next_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button')
        self.driver.execute_script("arguments[0].click();", next_btn)


rg=RiotGen()
while True:
    rg.login()