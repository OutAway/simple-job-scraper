import requests, re, random, time, math
import os
from bs4 import BeautifulSoup



url='https://rivaambiental.com.br/' 
PATH='text.txt'

def get_domains(url):
  valid_domains=['gmail.com', 'outlook.com', 'bol.com.br','uol.com.br']
  no_ext = re.sub(r'\.com.*', '.com', url)
  no_web= re.sub(r'https://|https://|www|', '', no_ext)
  with_ext=re.sub(r'https://|https://|www|', '', url)
  
  print(f'no_ext={no_ext}')
  print(f'no_web={no_web}')
  valid_domains.append(no_web)
  valid_domains.append(url)
  
  
  if str(url).endswith('/'):
     valid_domains.append(with_ext[:-1])
  else:
     valid_domains.append(with_ext)
  
  print (valid_domains)
  
  
  return valid_domains

def hook(url): 
    
    
    

    

    with requests.session() as session:
        response = session.get(url)
        response = session.get(url, cookies=response.cookies)
        time.sleep(math.sin(random.random()))
        parse=response.content
    
    soup = BeautifulSoup(parse, "html.parser")
    soup = soup.prettify
    DEBUG= 'DEBUG.txt'

    with open(DEBUG, 'w', encoding='utf-8') as file:
        file.write(f'{soup}')
    return soup  

def scrape_email(email_data, valid_domains):
  

  email_pattern = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
  found_emails = email_pattern.findall(str(email_data))
  #print(found_emails)

  filtered_emails = []
  for email in found_emails:
    #print(f'e-mail:{email}')
    for domain in valid_domains:
      #print(f'domain:{domain}')
      if email.endswith(domain):
        filtered_emails.append(email)
        break

  print(f'filtered list:{filtered_emails}')
  return filtered_emails

def scrape_number(soup):
  filtered_numbers=[]
  number_pattern = re.compile(r'[55]{2}([0-9]{11})|(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})')
  found_number = number_pattern.findall(str(soup))
  found_set=set(found_number)
  for number in found_set:
    filtered_numbers.append(number)
    
  print (f'https://wa.me/55{filtered_numbers}')

  
  return filtered_numbers
    
def get_print(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.save_screenshot('/simple-web-scraper/test2.png')
    driver.quit()   


def make_txt(file_path,emails,numbers):
  with open(file_path, 'a') as file_name:
    file_name.write(f"@ emails: {emails} | numbers: {numbers}\n\n")

soup=hook(url)


make_txt(PATH,scrape_email(soup, get_domains(url)),scrape_number(soup))
