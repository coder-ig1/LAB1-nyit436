#build web scraper using beautiful soup and requests
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def main():
    get_all_bio_urls()
    get_all_bios()
    get_all_courses()
def get_all_bio_urls():
    #url to scrape
    target = "https://www.newschool.edu/parsons665/FacultyList/"
    page = requests.get(target)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open("bio_urls.txt", "w") as bio_urls:
        a = soup.find_all("a", class_="a-contentBlock__link")
        print(a)
        for link in a:
            if link.get('href') != None:
                bio_urls.write("https://www.newschool.edu" + link.get('href') + "\n")
                
def get_all_bios():
    with open("bio_urls.txt", "r") as bio_urls:
        with open("bios.txt", "w") as bios:
            for url in bio_urls:
                #remove line brake at the end 
                url = url[:-1]
                page = requests.get(url)

                soup = BeautifulSoup(page.content, 'html.parser')
                
                main_div = soup.find("div", class_="o-primaryContent")
                for child in main_div.children:
                    if child.name == "p":
                        bios.write(child.text + "\n")
                    if child.name == "h3":
                        if "Degrees Held" in child.text:
                            bios.write("\n"*3)
                            break
def get_all_courses():
    with open("bio_urls.txt", "r") as bio_urls:
        with open("courses_taught.txt", "w") as courses:
            for url in bio_urls:
                url = url[:-1]
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                div = soup.find("div", class_="o-primaryContent")
                main_div = div.parent

                is_courses = False
                for child in main_div.children:
                    if child.name == "h3" and "Future Courses" in child.text:
                        is_courses = True
                    elif child.name == "p" and is_courses:
                        courses.write(child.text + "\n")
                    elif child.name == "h3" and is_courses:
                            break


main()
""" #make request to url
page = requests.get(target)
#print(page.status_code)
#print(page.content)
#parse html
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
#find all divs with class view-row
divs = soup.find("a", title="Go to last page")
print(divs.parent)

#loop through divs
last_page = divs['href']
print (last_page)
#use regex to pull out the number ^[0-9]*$
last_page_num = re.findall('\d+', last_page)
print(last_page_num)
#convert to int
last_page_num = int(last_page_num[0])
print(last_page_num)
#define function hi which takes no input and prints hi
def hi():
    print("hi") """