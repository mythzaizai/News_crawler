from os import link
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
 

def save_to_html(path_name, content):           #save page

    content = str(content)
    with open(path_name, 'w', encoding='UTF-8') as f:
        f.write(content)
    
    print("[info] save to html...")



def crawler(target_url, domain, news_count):
    print("[info] start to crawl web... ")


    #[connect to web]
    hdr = {'User-Agent': 'Mozilla/5.0'}         #avoid web 403
    r = requests.get(target_url, headers=hdr)   #response code
    print("[info] {}".format(r))
    soup = BeautifulSoup(r.text, "lxml")

    save_to_html("./output_data/home_page.html", soup.prettify())


    #[start parse html]
    newsList_tag = soup.select(".js-article-item a")
    skip_btn = 0


    for tag_a in newsList_tag:

        if skip_btn == 0:                       #skip the same link
            skip_btn = 1
            continue
        else:
            skip_btn = 0

        try:
            news_link = tag_a["href"]

            if news_link == "/news/commodities-news/zelenskiy-expects-more-weapons-as-battle-for-ukraines-east-rages-2833068":  #remove daliy news
                continue

            if news_link[-8:] == "comments":    #remove comments
                continue

            link_type = news_link.split("/")    #select news
            if link_type[1] != "news":
                continue
            else:
                news_count += 1

            #[connect to subweb]
            news_link = domain + news_link
            print("[info] connect to \"{}\"".format(news_link))
            
            news_r = requests.get(news_link, headers=hdr)   #response code
            print("[info] {}".format(news_r))
            news_soup = BeautifulSoup(news_r.text, "lxml")

            # save_to_html("./output_data/news_page.html", news_soup.prettify())

            #[start parse sub_html]
            news_title = news_soup.h1.text
            news_content = news_soup.select(".WYSIWYG p")
            news_date = news_soup.select(".contentSectionDetails > span")[0].text

            #[save to txt]
            print("[info] save news...")

            news_path = "./output_data/news_{}.txt".format(news_count)

            with open(news_path, 'w', encoding='UTF-8') as f:
                f.write("Title: {}".format(str(news_title)))
                f.write("\nDate: {}".format(str(news_date)))
                f.write("\n\n\n")
                for p in news_content:
                    f.write(str(p.text))
                    f.write("\n\n")


        except:
            continue


        time.sleep(1)

    return news_count




if __name__ == "__main__":

    target_url = "https://www.investing.com/commodities/crude-oil-news"
    domain = "https://www.investing.com/"

    news_count =0
    for i in range(1,54):

        fnt_target_url = "{}/{}".format(target_url,i)   #page

        news_count = crawler(fnt_target_url, domain, news_count)




