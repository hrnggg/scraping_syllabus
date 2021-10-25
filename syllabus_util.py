# pタグでlistに列挙して取ってくる以外のアイデア
# content_mapの中でtableになっているものについては、
# find(p>b)でテキストがそれに一致するものをとってくると、
# それの隣(next.siblingとか)にあるtableがその内容になっているので、
# あとはtr_list, td_listの一般的な処理でとれる。

import json
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from const import content_map

def parse_p(p):
    texts = []
    if p.find_all('p') != []:
        return ''
    for child in p:
        if type(child) == NavigableString:
            text = child.string.strip()
        elif type(child) == Tag:
            text = child.get_text().strip()
        else:
            continue
        if text != '':
            texts.append(text)

    return '\n'.join(texts)

# for summary, golas, remarks
def parse_others(table, key):
    texts = []
    try:
        p = table.find("p", text=content_map[key])
        # text_list = list(filter(lambda x: x != '', [parse_p(p) for p in ps]))
        for sibl in p.next_siblings:
            # 次のkeyが現れたら終了
            if sibl.get_text() in content_map.values():
                break
            if sibl.name == "p":
                text = sibl.get_text().strip()
                if text != '':
                    texts.append(text)
    except:
        return ''

    return '\n'.join(texts)

def parse_schedule(table):
    result = []    
    try:
        sched_table = table.find("table", class_="show__schedule")
        tr_list = sched_table.find_all("tr", class_=lambda x: x != "show__schedule-th")
    except:
        return []
    for tr in tr_list:
        td_list = tr.find_all("td")
        if len(td_list) == 3:
            td_text_list = []
            for td in td_list:
                # for ch in td:
                #     if type(ch) == NavigableString:
                #         text = ch.string.strip()
                #         # if text != '':
                #         td_text_list.append(text)
                #         break
                td.find("b").decompose()
                td_text_list.append(td.get_text().strip())

            week, contents, assignments = td_text_list
            # week, contents, assignments = [td.find(class_=lambda x: x != "sp_show").get_text().strip() for td in td_list]
            result.append(
                {
                    "week": week,
                    "contents": contents,
                    "assignments": assignments,
                }
            )
    return result  

def parse_evaluation(table):
    result = []
    try:
        eval_table = table.find("table", class_="show__grades")
        tr_list = eval_table.find_all("tr")
    except:
        return []    
    for tr in tr_list:
        td_list = tr.find_all("td")        
        if len(td_list) == 3:
            name, ratio, contents = [td.get_text().strip() for td in td_list]
            result.append(
                {
                    "name": name,
                    "ratio": ratio,
                    "contents": contents,
                }
            )

    return result

def parse_textbook(table):
    result = []
    try:
        p = table.find("p", text=content_map["textbook"])
        text_table = None
        for sibl in p.next_siblings:
            if sibl.name == "table":
                text_table = sibl    

        tr_list = text_table.find_all("tr")
    except:
        return []

    for tr in tr_list:
        td_list = tr.find_all("td")
        tmp = None
        for td in td_list: # カラムが複数ある形式ではなさそうなので一個とればok
            # if type(td) == NavigableString: # テキストにはリンクはなさそうなのでこれでok
            #     text = td.string.strip()
            #     if text != '':
            #         tmp = text
            #         break
            text = td.get_text().strip()
            if text != '':
                tmp = text
                break            
        if tmp == None:
            continue
        result.append(tmp)

    return result

def parse_ref_book(table):
    result = []
    try:
        p = table.find("p", text=content_map["reference_book"])
        ref_book_table = None
        for sibl in p.next_siblings:
            if sibl.name == "table":
                ref_book_table = sibl

        tr_list = ref_book_table.find_all("tr")
    except:
        return []

    for tr in tr_list:
        td_list = tr.find_all("td")
        name = None
        url = None
        for td in td_list: # カラムが複数ある形式ではなさそうなので一個とればok
            # if type(td) == NavigableString: # 一旦、リンクのないものはpass（パターン確認中）
                # td.string.strip()
            if type(td) == Tag:
                link = td.find("form")
                if link != None:
                    name = link.get_text().strip()
                    url = link.get('action')
                    break
        if name == None and url == None:
            continue
        result.append(
            {
                "name": name, 
                "url": url
            }
        )

    return result

def parse_ref_url(table):
    result = []
    try:
        p = table.find("p", text=content_map["reference_url"])
        ref_url_table = None
        for sibl in p.next_siblings:
            if sibl.name == "table":
                ref_url_table = sibl    

        tr_list = ref_url_table.find_all("tr")
    except:
        return []

    for tr in tr_list:
        td_list = tr.find_all("td")
        name = None
        url = None
        for td in td_list: # カラムが複数ある形式ではなさそうなので一個とればok
            # if type(td) == NavigableString: # 説明文みたいなやつはpass
                # td.string.strip()
            if type(td) == Tag:
                link = td.find("a")
                if link != None:
                    name = link.get_text().strip()
                    url = link.get('href')
                    break
        if name == None and url == None:
            continue
        result.append(
            {
                "name": name, 
                "url": url
            }
        )

    return result    

# def scrape_syllabus_with_p(url):
#     res = requests.get(url)
#     res.raise_for_status()  # エラーチェック
#     res.encoding = 'utf-8'

#     soup = BeautifulSoup(res.text, 'html.parser')    
#     table = soup.find("table", class_="show__content")     

#     try: 
#         ps = table.find_all("p")
#     except:
#         return {}
#     text_list = list(filter(lambda x: x != '', [parse_p(p) for p in ps]))

#     result = {}
#     for k in content_map.keys():
#         result[k] = []

#     itr = iter(content_map.keys())
#     k = next(itr)
#     nk = next(itr)
#     tmp = []
#     start_idx = text_list.index(content_map[k]) + 1
#     for i, text in enumerate(text_list[start_idx:]):
#         if text == content_map[nk]:
#             if k == "schedule":
#                 # 第一項（関数の返り値）が空でないならそれがtmpへ代入される
#                 # 空であればtmpの中身は変わらない
#                 tmp = parse_schedule(table) or tmp
#             elif k == "evaluation":
#                 tmp = parse_evaluation(table) or tmp
#             result[k] = tmp
#             tmp = []
#             k = nk
#             try:
#                 nk = next(itr)        
#             except:
#                 result[nk] = text_list[i+1:]
#                 break
#         else:
#             tmp.append(text)

#     for k in content_map.keys():
#         if result.get(k) == None:
#             result[k] = []

#     return result        

def scrape_syllabus(url):
    # init
    result = {}
    for k in content_map.keys():
        result[k] = None

    res = requests.get(url)
    try:
        res.raise_for_status()  # エラーチェック
    except:
        return result
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')
    try:    
        table = soup.find("table", class_="show__content")
    except:
        return result
    
    for k in content_map.keys():
        if k == "schedule":
            result[k] = parse_schedule(table)
        elif k == "evaluation":
            result[k] = parse_evaluation(table)
        elif k == "textbook":
            result[k] = parse_textbook(table)
        elif k == "reference_book":
            result[k] = parse_ref_book(table)
        elif k == "reference_url":
            result[k] = parse_ref_url(table)
        else:
            result[k] = parse_others(table, k)
        

    return result      

def main():
    urls = [
        "https://syllabus.doshisha.ac.jp/html/2021/0101/10101187000.html", # ref_url
        "https://syllabus.doshisha.ac.jp/html/2021/1610/11610121000.html", # text, ref_book
        "https://syllabus.doshisha.ac.jp/html/2021/0270/10270611003.html" # not table
        "https://syllabus.doshisha.ac.jp/html/2021/1502/11502061002.html" # 404 
    ] 
    idx = 3
    url = urls[idx]
    result = scrape_syllabus(url)        
    with open(f"hoge_{idx}.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    main()