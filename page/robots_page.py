import requests
import sys
import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from page.dev_script_page import *

# app = QApplication()
# trans = QTranslator()
# trans.load('dev_script_page')
# app.installTranslator(trans)


# def robots_page_ui(self):
#     self.robots_table.setRowCount(10)

online_list = []

filename = 'data.json'


def robots_page_refresh_data(api_url,hmp,self):
    print('robots_page--robots_page_refresh_data')

    #讀資料
    with open(filename,"r") as f_obj:
        #讀取資料
        data = json.load(f_obj)

    headers = {
        'Authorization': 'token ' + hmp,
    }


    try:
        response = requests.get(api_url, headers=headers)
    except (requests.ConnectionError, requests.Timeout,KeyError) as e:
        if 'port=443' in str(e):
            self.log_bar.setText(self.tr('連接hamibot失敗，請檢查網路'))
            return 


    response_json = requests_states(self,response)
    print(response_json)

    if response_json == False:
        return

    #記錄線上嘅機械人
    online_list = []

    #獲取機械人數量同item項目
    count = response_json['count']
    items = response_json['items']

    #根據機械人數量而增加個table行位
    self.robots_table.setRowCount(count)
    
    for i in range(count):
        #獲取item項目入面嘅資料
        id = items[i]['_id']
        online_states = items[i]['online']
        tags = ''
        tags_text = items[i]['tags']
        brand = items[i]['brand']
        model = items[i]['model']
        name = items[i]['name']


        if len(tags_text) == 0:
            tags = ""
        else:
            for tags_i in range(len(tags_text)):
                tags = tags + tags_text[tags_i] + " "

        if (online_states == True):
            online = QTableWidgetItem(self.tr("在線"))
            online.setForeground(Qt.green)
            #將在線嘅機械人紀錄
            online_list.append({'id':id, 'name':name, 'tags':tags_text})
        else:
            online = QTableWidgetItem(self.tr("離線"))
            online.setForeground(Qt.red)

        #在線離線戈行置中
        online.setTextAlignment(Qt.AlignCenter)

        #寫table每格嘅資料
        self.robots_table.setItem(i,0,QTableWidgetItem(id))
        self.robots_table.setItem(i,1,QTableWidgetItem(name))
        self.robots_table.setItem(i,2,QTableWidgetItem(brand +" "+ model))
        self.robots_table.setItem(i,3,online)
        self.robots_table.setItem(i,4,QTableWidgetItem(str(tags)))

        #第一次迴圈先清空
        if i == 0:
            data['robots_list'] = []

        data['robots_list'].append({"id":id,"name":name,"brand":brand +" "+ model,"online":online_states,"tag":tags}) 
            

    with open(filename,'w') as f_obj:
        json.dump(data,f_obj)

    #在上面獲取完機械人之後，將在線嘅機械人更新到開發腳本頁面嘅機械人combobox
    dev_script_page_online_robots_list(online_list,self)


    if response.status_code == 200:
        self.log_bar.setText(self.tr('已刷新機械人'))

    print('response_json:'+str(response.json()))
    print('online_list:'+str(online_list))


def requests_states(self,response):
    try:
        response_json = response.json()
        message = response_json['message']
        #message == '当前配额不足，前往控制台获取更多 https://hamibot.com/account/quotas'
        if response.status_code == 429:
            self.log_bar.setText(self.tr('當前配額不足，前往控制台獲取更多')+' https://hamibot.com/account/quotas')
            return False
        #{'code': 1040, 'message': '令牌无效', 'documentation_url': 'https://docs.hamibot.com/rest/overview'}
        #message == '令牌无效'
        elif response.status_code == 401:
            self.log_bar.setText(self.tr('令牌無效'))
            return False
        #status_code 422
        elif response.json()['message'] == '配置格式有误':
            self.log_bar.setText(self.tr('config.json配置格式有誤，請檢查腳本寫法'))
            return False
        else:
            self.log_bar.setText(self.tr('未知錯誤--')+message)
            return False
    except (KeyError,json.decoder.JSONDecodeError) as e:
        if 'message' in str(e):
            return response_json
        elif 'Errno Expecting value' in str(e):
            return True
        else:
            self.log_bar.setText(self.tr('未知錯誤--')+str(e))
            return False


