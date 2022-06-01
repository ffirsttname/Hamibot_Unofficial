import requests
import json
import page.robots_page as robots_page
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

#新增一個list用來紀錄checkbox，用於同時執行多個腳本
# dev_script_checkbox = [] 
global robots_list
filename = 'data.json'
robots_list = [{'id': ' ', 'name': ' ', 'tag': ' '}]


def dev_script_page_refresh_data(api_url,hmp,self):
    print('dev_script_page--dev_script_page_refresh_data')
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
    

    response_json = robots_page.requests_states(self,response)

    if response_json == False:
        return

    #獲取機械人數量同item項目
    count = response_json['count']
    items = response_json['items']

    #根據開發腳本數量而增加個table行位
    self.dev_script_table.setRowCount(count)


    for i in range(count):
        #獲取item項目入面嘅資料
        id = items[i]['_id']
        name = items[i]['name']

        #寫table每格嘅資料
        self.dev_script_table.setItem(i,0,QTableWidgetItem(id))
        self.dev_script_table.setItem(i,1,QTableWidgetItem(name))

        #第一次迴圈先清空
        if i == 0:
          data['dev_script_list'] = []   

        data['dev_script_list'].append({'id': id, 'name': name})

    if response.status_code == 200:
        self.log_bar.setText(self.tr('已刷新開發腳本'))
    with open(filename,'w') as f_obj:
        json.dump(data,f_obj)

    print(response.json())

#將在線嘅機械人寫入list到
def dev_script_page_online_robots_list(online_robot,self):
    print('dev_script_page--dev_script_page_online_robots_list')
    #讀資料
    with open(filename,"r") as f_obj:
        #讀取資料
        data = json.load(f_obj)
    data['robots_online_list'] = []
    #刪除個combobox list，以免多次按刷新時不斷加新數據
    self.dev_script_robots_combobox.clear()
    #新增robots_id，一開始個選項係機械人
    self.dev_script_robots_combobox.addItem(self.tr('選擇機械人'),' ')
    data['robots_online_list'].append({'id':' ', 'name':' ','tag':' '})
    robots_id = [{'id':"", 'name':" "}]

    #將標籤左嘅機械人新增落combobox到
    for i in range(len(online_robot)):
        for j in range(len(online_robot[i]['tags'])):
             self.dev_script_robots_combobox.addItem(QIcon('./pic/tags.png'),online_robot[i]['tags'][j],online_robot[i]['id'])
             robots_id.append({'id':online_robot[i]['id'], 'name':online_robot[i]['name']})
             data['robots_online_list'].append({'id':online_robot[i]['id'], 'name':online_robot[i]['name'],'tag':online_robot[i]['tags'][j]})

    #將在線嘅機械人新增落combobox到，另開一個for係保證係tags後面新增
    for i in range(len(online_robot)):         
        self.dev_script_robots_combobox.addItem(online_robot[i]['name'],online_robot[i]['id'])
        robots_id.append({'id':online_robot[i]['id'], 'name':online_robot[i]['name']})
        data['robots_online_list'].append({'id':online_robot[i]['id'], 'name':online_robot[i]['name'],'tag':' '})

    with open(filename,'w') as f_obj:
        json.dump(data,f_obj)

#上傳腳本按鈕
def dev_script_edit(self,api_url,hmp,folder,config):
    print('dev_script_page--dev_script_edit')

    headers = {
        'Authorization': 'token '+hmp
    }

    if config == True:
        files=[
            ('data',('index.js',open(folder+'/index.js','rb'),'application/javascript')),
            ('data',('config.json',open(folder+'/config.json','rb'),'application/json'))
        ]
    else:
        files=[
            ('data',('index.js',open(folder+'/index.js','rb'),'application/javascript')),
        ]
        
    try:
        response = requests.put(api_url, headers=headers, files=files)
    except (requests.ConnectionError, requests.Timeout,KeyError) as e:
        if 'port=443' in str(e):
            self.log_bar.setText(self.tr('連接hamibot失敗，請檢查網路'))
            return    

    if robots_page.requests_states(self,response) == False:
        return

    if response.status_code == 204:
        self.log_bar.setText(self.tr('已成功修改腳本'))
    else:
        self.log_bar.setText(self.tr('未知錯誤'))



#開始按鈕
def dev_script_start(self,api_url,hmp,robot_id,robot_name):
    print('dev_script_page--dev_script_start')
    headers = {
        'Authorization': 'token ' + hmp,
    }

    json_data = {
        'robots': [
            {
                '_id': robot_id,
                'name': robot_name,
            },
        ],
    }

    try:
      response = requests.post(api_url, headers=headers, json=json_data)
    except (requests.ConnectionError, requests.Timeout,KeyError) as e:
        if 'port=443' in str(e):
            self.log_bar.setText(self.tr('連接hamibot失敗，請檢查網路'))
            return

    if robots_page.requests_states(self,response) == False:
        return

    if response.status_code == 204:
        self.log_bar.setText(self.tr('已運行開發腳本'))
    else:
        self.log_bar.setText(self.tr('未知錯誤'))


#停止按鈕
def dev_script_stop(self,api_url,hmp,robot_id,robot_name):
    print('dev_script_page--dev_cript_stop')
    headers = {
        'Authorization': 'token ' + hmp,
    }

    json_data = {
        'robots': [
            {
                '_id': robot_id,
                'name': robot_name,
            },
        ],
    }

    try:
        response = requests.delete(api_url, headers=headers, json=json_data)
    except (requests.ConnectionError, requests.Timeout,KeyError) as e:
        if 'port=443' in str(e):
            self.log_bar.setText(self.tr('連接hamibot失敗，請檢查網路'))
            return

    if robots_page.requests_states(self,response) == False:
        return

    if response.status_code == 204:
        self.log_bar.setText(self.tr('已停止開發腳本'))
    else:
        self.log_bar.setText(self.tr('未知錯誤'))

#停止所有按鈕
def dev_script_stop_all(self,api_url,hmp):
    print('dev_script_page--dev_cript_stop_all')
    headers = {
        'Authorization': 'token ' + hmp,
    }

    try:
        response = requests.put(api_url, headers=headers)
    except (requests.ConnectionError, requests.Timeout,KeyError) as e:
        if 'port=443' in str(e):
            self.log_bar.setText(self.tr('連接hamibot失敗，請檢查網路'))
            return   
            
    if robots_page.requests_states(self,response) == False:
        return

    if response.status_code == 204:
        self.log_bar.setText(self.tr('已停止所有腳本'))
    else:
        self.log_bar.setText(self.tr('未知錯誤'))
    
