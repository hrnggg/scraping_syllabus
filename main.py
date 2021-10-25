import re
import os
import time
# from os import wait
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import sys
from const import (
    years, 
    periods,
    TOP_PAGE_URL, 
    degree_map, 
    major_map, 
    day_map    
)
from syllabus_util import scrape_syllabus
from selenium_wrapper import (
    init_driver, 
    set_wait, 
    select_by_value_with_wait, 
    click_btn_with_wait
)

out_dir = "./syllabuses"

@dataclass
class JsonArgs:
    year: str
    degree: str
    major: str

def make_json(td_list, json_args):
    # get_text()でbrタグが消去されてしまうので事前に改行コードへ変換しておく
    for tmp in td_list[3].select('br'):
        tmp.replace_with('\n')
    code, degree, name, instructors, place, num_credits, day_and_class_period, _  = [td.get_text().strip() for td in td_list]
    instructors = instructors.split('\n')

    if name.startswith("○"):
        period = "春"
        name = name[1:]
    elif name.startswith("△"):
        period = "秋"
        name = name[1:]
    else:
        period = None

    url = td_list[2].find('a').get('href') # relative link
    url = TOP_PAGE_URL + url[2:]    
    syllabus_contents = scrape_syllabus(url)
    # 2021年度以外は曜日、開講講時は記載なし
    if day_and_class_period == '':
        day, class_period = None, None
    else:
        # 実験の授業などで曜日と講時が複数並んでいるものについては、最初のものだけをとってくる
        tmp = day_and_class_period.split('\t')[0].strip().split()
        # インターネット講義 or 現地
        if len(tmp) == 2:
            day, class_period = tmp
        else:
            day = tmp[0]
            class_period = None

    return {
        "code": code,
        "year": json_args.year,
        "preiod": period,
        "degree": degree,
        "major": json_args.major,
        "name": name,
        "url": url,
        "instructors": instructors,
        "place": place,
        "num_credits": num_credits,
        "day": day,
        "class_period": class_period,
        "syllabus_contents": syllabus_contents,
    }

def run_scraping(driver, wait, json_args):
    result = []
    while True:
        # シラバス一覧の取得
        html = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        try:
            table = soup.find("table", class_="result__table")        
            tr_list = table.find_all("tr") # シラバス一覧
            if len(tr_list) == 0:
                return []
        except:
            return []        
        
        for tr in tr_list:
            # tr: 授業レコード
            # [授業コード, 課程, 授業名, 担当者, 校地, 単位数, 曜日/講時, _]            
            td_list = tr.find_all("td") 
            if len(td_list) == 8:
                result.append(make_json(td_list, json_args))

        # 次のページのリンクの取得
        # あれば遷移、なければ終了
        try:
            next_page_link = wait.until(lambda d: d.find_element(By.XPATH, "//input[@value=\"次結果一覧/Next\"]"))                        
        except:
            print(f"{json_args.year}/{json_args.degree}/{json_args.major} finish.")
            break            

        # Footerとリンクが被ってクリックできないのを防ぐため
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
        next_page_link.click()

    return result

def main(argv):
    if len(argv) != 2:
        exit(1)        

    opts = Options()    
    opts.headless = False # Falseでブラウザ起動
    driver = init_driver(opts)
    wait = set_wait(driver, 20)

    driver.get(TOP_PAGE_URL)

    # 開講年度
    year = sys.argv[1]
    select_by_value_with_wait(year, wait, lambda d: d.find_element(by=By.NAME, value="select_bussinessyear"))    
    for degree_key in degree_map.keys():
        # 課程
        print(f"\n{degree_map[degree_key]}")
        select_by_value_with_wait(degree_key, wait, lambda d: d.find_element(by=By.NAME, value="courseid"))
        for major_key in major_map.keys():
            # 学部・研究科
            print(major_map[major_key])
            select_by_value_with_wait(major_key, wait, lambda d: d.find_element(by=By.NAME, value="subjectcd"))
            # dropdown = driver.find_element(by=By.NAME, value="subjectcd")            
            # try:
            #     select = Select(dropdown)
            #     select.select_by_value(major_key)
            #     print(driver.current_url)
            # except:
            #     msg = f"error.\n{driver.current_url}\n{type(dropdown)}\n{dropdown.is_enabled()}\n{dropdown.is_selected()}\n{dropdown.text}\n{dropdown}"
            #     raise Exception(msg)

            # 検索ボタンクリック
            click_btn_with_wait(wait, lambda d: d.find_element(by=By.XPATH, value="//input[@value=\"検索/Search\"]"))

            json_args = JsonArgs(year, degree_map[degree_key], major_map[major_key])
            # 検索結果のhtmlページ内のスクレイピング            
            result = run_scraping(driver, wait, json_args)
            if result != []:
                dirname = f"{out_dir}/{year}"
                if not os.path.exists(dirname):
                    os.makedirs(dirname, exist_ok=True)
                filename = f"{year}_{degree_map[degree_key]}_{major_map[major_key]}.json"
                with open(f"{dirname}/{filename}", "w") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)

            driver.get(TOP_PAGE_URL)
            select_by_value_with_wait(year, wait, lambda d: d.find_element(by=By.NAME, value="select_bussinessyear"))    
            select_by_value_with_wait(degree_key, wait, lambda d: d.find_element(by=By.NAME, value="courseid"))

if __name__ == "__main__":
    main(sys.argv)