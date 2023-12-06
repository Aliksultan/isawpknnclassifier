import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import csv


def get_source_html(url):
    s = Service(executable_path=r'C:\Users\aliko\PycharmProjects\pythonProject\chromedriver-win64\chromedriver.exe')
    options = Options()
    options.add_experimental_option(
        'prefs',
        {
            'profile.managed_default_content_settings.javascript': 2,
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.mixed_script': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'profile.managed_default_content_settings.stylesheets': 2
        }
    )
    driver = webdriver.Chrome(service=s, options= options)

    try:
        driver.maximize_window()
        driver.get(url)
        time.sleep(3)

        with open("top30.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        print("[INFO] Main page saved")

        get_urls(file_path=r"C:\Users\aliko\PycharmProjects\pythonProject\top30.html")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_stats(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
    stats = []
    print("[INFO]Saving the players stats:")
    count = 1
    for url in urls_list:
        s = Service(executable_path=r'C:\Users\aliko\PycharmProjects\pythonProject\chromedriver-win64\chromedriver.exe')
        options = Options()
        options.add_experimental_option(
            'prefs',
            {
                'profile.managed_default_content_settings.javascript': 2,
                'profile.managed_default_content_settings.images': 2,
                'profile.managed_default_content_settings.mixed_script': 2,
                'profile.managed_default_content_settings.media_stream': 2,
                'profile.managed_default_content_settings.stylesheets': 2
            }
        )
        driver = webdriver.Chrome(service=s, options=options)

        player_name = url.split('/')[7].split('?')[0]
        print(count, "/63  Current Player: ", player_name)
        count += 1

        driver.get(url)
        time.sleep(1)

        try:
            stat_dict = {}
            soup = BeautifulSoup(driver.page_source, "lxml")
            statistics = soup.find("div", class_="statistics")
            stats_rows = statistics.find_all("div", class_="stats-row")
            for stats_row in stats_rows:
                spans = stats_row.find_all("span")
                stat_dict[spans[0].get_text()] = spans[-1].get_text()
        except Exception as ex:
            stat_dict = None

        stats.append(stat_dict)

    # keys = stats[0].keys()
    with open('allStats.txt', 'w', newline='') as file:
        json.dump(stats, file)


def get_urls(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    players_td = soup.find_all("td", class_="playerCol")

    urls = []
    for player in players_td:
        player_url = player.find("a").get("href")
        player_url = player_url[14:]
        urls.append("https://www.hltv.org/stats/players/individual" + player_url)

    with open("playerLinks.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")
    print("[INFO] Player URLs successfully collected")


def main():
    get_source_html("https://www.hltv.org/stats/players?startDate=2023-06-03&endDate=2023-12-03&rankingFilter=Top30")
    get_stats(file_path=r"C:\Users\aliko\PycharmProjects\pythonProject\playerLinks.txt")


if __name__ == "__main__":
    main()
