years = ["2021", "2020", "2019", "2018", "2017"]
periods = ["1", "2", "3", "4", "5", "6", "7"] # 開講講時

TOP_PAGE_URL = "https://syllabus.doshisha.ac.jp"

degree_map = {
    # "-1": "（指定なし / Not specified）", # value=""
    # "1": "学部 / Faculty",
    # "3": "大学院 / Graduate schools",
    # "D": "一貫制大学院 / Consistent graduate schools",
    # "P": "専門職大学院 / Professional graduate schools",
    # "9": "その他（CGE生・日文生) / Others(CGE Students・Nichibun-sei)",
    "1": "学部",
    "3": "大学院",
    "D": "一貫制大学院",
    "P": "専門職大学院",
    "9": "その他（CGE生・日文生)",
}

major_map = {
    # "-1": "（指定なし / Not specified）",
    "1": "神学部・神学研究科",
    # "1_1": "　/School of Theology・Graduate School of Theology",
    "2": "文学部・文学研究科",
    # "2_1": "　/Faculty of Letters・Graduate School of Letters",
    "3": "社会学部・社会学研究科",
    # "3_1": "　/Faculty of Social Studies・Graduate School of Social Studies",
    "4": "法学部・法学研究科",
    # "4_1": "　/Faculty of Law・Graduate School of Law",
    "5": "経済学部・経済学研究科",
    # "5_1": "　/Faculty of Economics・Graduate School of Economics",
    "6": "商学部・商学研究科",
    # "6_1": "　/Faculty of Commerce・Graduate School of Commerce",
    "8": "政策学部・総合政策科学研究科",
    # "8_1": "　/Faculty of Policy Studies・Graduate School of Policy and Management",
    "9": "文化情報学部・文化情報学研究科",
    # "9_1": "　/Faculty of Culture and Information Science・Graduate School of Culture and Information Science",
    "7": "理工学部･理工学研究科（工学研究科）",
    # "7_1": "　/Faculty of Science and Engineering・Graduate School of Science and Engineering",
    "10": "生命医科学部・生命医科学研究科",
    # "10_1": "　/Faculty of Life and Medical Science・Graduate School of Life and Medical Science",
    "11": "スポーツ健康科学部・スポーツ健康科学研究科",
    # "11_1": "　/Faculty of Health and Sports Science・Graduate School of Health and Sports Science",
    "12": "心理学部・心理学研究科",
    # "12_1": "　/Faculty of Psychology・Graduate School of Psychology",
    "13": "グローバル・コミュニケーション学部",
    # "13_1": "　/Faculty of Global Communications",
    "19": "グローバル地域文化学部",
    # "19_1": "　/Faculty of Global and Regional Studies",
    "113": "グローバル･スタディーズ研究科",
    # "113_1": "　/Graduate School of Global Studies",
    "112": "アメリカ研究科",
    # "112_1": "　/Graduate School of American Studies",
    "117": "脳科学研究科",
    # "117_1": "　/Graduate School of Brain Science",
    "115": "司法研究科",
    # "115_1": "　/Law School",
    "116": "ビジネス研究科",
    # "116_1": "　/Graduate School of Business",
    "17": "日本語・日本文化教育科目",
    # "17_1": "　/Japanese Language and Culture subjects",
    "119": "グローバル教育プログラム科目",
    # "119_1": "　/Subject of Global Education Program",
    "14": "国際教育インスティテュート",
    # "14_1": "　/The Institute for the Liberal Arts",
    "15": "全学共通教養教育科目（外国語教育科目）",
    # "15_1": "　/Subject of foreign language",
    "16": "全学共通教養教育科目（保健体育科目）",
    # "16_1": "　/Subject of Health and Physical",
    "18": "全学共通教養教育科目（外国語教育科目・保健体育科目以外）",
    # "18_1": "　/Subject of General and Liberal Education",
    "118": "高等研究教育院設置科目（ALA科目群、GRM科目、Comm5.0科目）",
    # "118_1": "　/Institute for Advanced Research and Education（ALA, GRM, Comm5.0）",
    "20": "免許資格課程科目",
    # "20_1": "　/License and Qualification Subjects"
}

day_map = {
    # "-1": "",
    "月": "月曜日/Monday",
    "火": "火曜日/Tuesday",
    "水": "水曜日/Wednesday",
    "木": "木曜日/Thursday",
    "金": "金曜日/Friday",
    "土": "土曜日/Saturday",
    "日": "日曜日/Sunday",
    "集中": "集中/Intensive",
    "インターネット": "インターネット/Internet"
}

# syllabus contents
content_map = {
    "summary": "＜概要/Course Content Summary＞", 
    "goals": "＜到達目標/Goals,Aims＞",
    "schedule": "＜授業計画/Schedule＞", # table
    "evaluation": "＜成績評価基準/Evaluation Criteria＞", # table
    "textbook": "＜テキスト/Textbook＞", # table  
    "reference_book": "＜参考文献/Reference Book＞", # table
    "reference_url": "＜参照ＵＲＬ/URL＞", # table
    "remarks": "＜備考/Remarks＞",
}