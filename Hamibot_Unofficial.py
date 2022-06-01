import sys
import json
import os
import pyperclip

# from PySide2.QtWidgets import *
# from PySide2.QtCore import *
# from PySide2.QtGui import *

from ui.main_ui import Ui_MainWindow
from page.robots_page import *
from page.dev_script_page import *

# import qtmodern.styles
# import qtmodern.windows


#獲取當下系統語言
local_language = QLocale.system().name()

filename = 'data.json'
hamibot_tokens=""
hamibot_api_url = 'https://api.hamibot.com'
hamibot_api_robots = '/v1/robots'
hamibot_api_dev_script = '/v1/devscripts'
hamibot_robotId = " "
hamibot_api_robots_stop_all = '/v1/robots/'+hamibot_robotId+'/stop'
hamibot_scriptId = " "
hamibot_api_dev_script_run_or_stop = '/v1/devscripts/'+hamibot_scriptId+'/run'
hamibot_api_dev_script_edit = '/v1/devscripts/'+hamibot_scriptId+'/files'

#紀錄目前選擇左嘅機械人
hamibot_current_robot = {'id': ' ', 'name': ' ', 'tag': ' '}

# 接收出錯的資訊
sys.stderr = open('errorlog.txt', 'wt',encoding='utf-8')

# 接收到print語句
sys.stdout = open('printlog.txt','wt',encoding='utf-8')


#判斷有無data.json呢個檔，無就寫入空白嘅數據，因無數據情況下面就咁讀資料會error
if not os.path.exists(filename):
	#第一次運行首先創建filename以及創建數據，以免下面讀嘅時侯error
	with open(filename,"w") as f_obj:
		#先寫入各種空白資料
		json.dump({"language":"","current_tab":2,"hamibot_tokens":"",'lower_api_quotas_checked':False,"edit_config_checked":False,"folder_location":"","robots_list":[],"robots_online_list":[],"current_robots":0,"dev_script_list":[]},f_obj)


#讀資料
with open(filename,"r") as f_obj:
    #讀取資料
    data = json.load(f_obj)

class MainWindow(Ui_MainWindow, QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		#只顯示最小化同關閉按鈕，即禁止窗口最大化按钮
		self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
		#禁止拉伸窗口大小
		self.setFixedSize(self.width(),self.height())

		#新增按鈕
		self.refresh_robot = QPushButton(self.tr('刷新機械人'))
		self.refresh_dev_script = QPushButton(self.tr('刷新開發腳本'))

		#為tabwidget添加按鈕
		self.widget = QWidget()
		h_layout = QHBoxLayout(self.widget)
		h_layout.setContentsMargins(0, 0, 0, 0)
		h_layout.addWidget(self.refresh_dev_script)
		h_layout.addWidget(self.refresh_robot)
		self.tabWidget.setCornerWidget(self.widget)

		#當使用左降低配額使用量降低配額使用量，打開頁面時就會加載資料
		if data['lower_api_quotas_checked'] == True:
			#加載機械人list
			self.robots_table.setRowCount(len(data['robots_list']))
			for i in range(len(data['robots_list'])):
				self.robots_table.setItem(i,0,QTableWidgetItem(data['robots_list'][i]['id']))
				self.robots_table.setItem(i,1,QTableWidgetItem(data['robots_list'][i]['name']))
				self.robots_table.setItem(i,2,QTableWidgetItem(data['robots_list'][i]['brand']))
				if data['robots_list'][i]['online'] == True:
					online_states = QTableWidgetItem(self.tr("在線"))
					online_states.setForeground(Qt.green)
				else:
					online_states = QTableWidgetItem(self.tr("離線"))
					online_states.setForeground(Qt.red)
				online_states.setTextAlignment(Qt.AlignCenter)
				self.robots_table.setItem(i,3,online_states)
				self.robots_table.setItem(i,4,QTableWidgetItem(data['robots_list'][i]['tag']))

			#加載online嘅機械人
			for i in range(len(data['robots_online_list'])):
				#第一個係選擇機械人，所以唔理佢
				if i == 0:
					continue
				if data['robots_online_list'][i]['tag'] != ' ':
					self.dev_script_robots_combobox.addItem(QIcon('./pic/tags.png'),data['robots_online_list'][i]['tag'],data['robots_online_list'][i]['id'])
				else:
					self.dev_script_robots_combobox.addItem(data['robots_online_list'][i]['name'],data['robots_online_list'][i]['id'])

			#上次選擇嘅機械人
			self.dev_script_robots_combobox.setCurrentIndex(data['current_robots'])

			#加載開發腳本
			self.dev_script_table.setRowCount(len(data['dev_script_list']))
			for i in range(len(data['dev_script_list'])):
				self.dev_script_table.setItem(i,0,QTableWidgetItem(data['dev_script_list'][i]['id']))
				self.dev_script_table.setItem(i,1,QTableWidgetItem(data['dev_script_list'][i]['name']))


		#判斷打開邊版tabwidget
		self.tabWidget.currentChanged.connect(self.oncurrentChanged)
		#默認打開設定戈版
		self.tabWidget.setCurrentIndex(data['current_tab'])

		#修改folder icon
		self.folder_choose.setPixmap('./pic/folder.png')

		#修改icon
		self.setWindowIcon(QIcon('./pic/icon.ico'))

		#調整robots_table顯示頂部，隱藏側欄，因為好似qt	 designer有BUG整左都無顯示
		self.robots_table.horizontalHeader().setVisible(True)
		self.robots_table.verticalHeader().setVisible(False)
		self.robots_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		#調整robots_table字型，因為好似qt designer有BUG整左都無顯示
		self.robots_table.setFont(QFont("Noto Sans SC Medium",12))
		#調整robots_table，指定欄位個寬
		self.robots_table.setColumnWidth(1,150)
		self.robots_table.setColumnWidth(2,200)
		self.robots_table.setColumnWidth(3,100)
		self.robots_table.setColumnWidth(3,115)

		#調整robots_table顯示頂部，隱藏側欄，因為好似qt designer有BUG整左都無顯示
		self.dev_script_table.horizontalHeader().setVisible(True)
		self.dev_script_table.verticalHeader().setVisible(False)
		#調整robots_table字型，因為好似qt designer有BUG整左都無顯示
		self.dev_script_table.setFont(QFont("Noto Sans SC Medium",12))
		#調整robots_table，指定欄位個寬
		self.dev_script_table.setColumnWidth(0,80)
		self.dev_script_table.setColumnWidth(1,390)

		#將之前已經填過嘅各種資料填番入指定欄位
		self.tokens.setText(data['hamibot_tokens'])
		self.folder_location.setText(data['folder_location'])

		#設定版面↓
		#修改禁得嘅連結
		self.get_tokens_url.setText("<A href='https://hamibot.com/account/tokens'>"+self.tr('（獲取令牌）')+"</a>")
		#記錄tokens變化
		self.tokens.textChanged.connect(self.ontokens_changed)
		
		#根據語言切換番設定個language_switch
		if   data['language'] == 'tc':
			self.language_switch.setCurrentIndex(1)
		elif data['language'] == 'sc':
			self.language_switch.setCurrentIndex(2)
		else:
			self.language_switch.setCurrentIndex(0)

		self.language_switch.currentIndexChanged.connect(self.onlanguage_switch)
		#降低配額使用量判定
		self.lower_api_quotas.clicked.connect(self.onlower_api_quotas_check)
		self.lower_api_quotas.setChecked(data['lower_api_quotas_checked'])
		#設定版面↑

		#當單擊名字欄會自動紀錄ID
		self.dev_script_table.clicked.connect(self.dev_script_table_clicked)
		#當雙擊名字欄會自動複製內容
		self.dev_script_table.doubleClicked.connect(self.dev_script_table_doubleClicked)
		#當點選folder_choose時就會彈出個瀏覽資料夾
		self.folder_choose.mousePressEvent = self.on_openfolder
		#有可能手動變更資料夾
		self.folder_location.textChanged.connect(self.onfolder_location)
		self.dev_script_edit_config.clicked.connect(self.on_dev_script_edit_config_check)
		self.dev_script_edit_config.setChecked(data['edit_config_checked'])
		self.edit_dev_script_button.clicked.connect(self.on_dev_script_edit_button)
		#為刷新按鈕添加功能
		self.refresh_robot.clicked.connect(self.on_refresh_robot_button)
		self.refresh_dev_script.clicked.connect(self.on_refresh_dev_script_button)
		#開發腳本運行按鈕
		self.dev_script_run_button.clicked.connect(self.on_dev_script_run_button)
		#開發腳本停止按鈕
		self.dev_script_stop_button.clicked.connect(self.on_dev_script_stop_button)		
		#停止所有按鈕
		self.dev_script_stopall_button.clicked.connect(self.on_dev_script_stopall_button)
		#當改變機械人人時就會觸發
		self.dev_script_robots_combobox.currentIndexChanged.connect(self.on_dev_script_robots_combobox)
		
		self.translator = QTranslator(app)

	def dev_script_table_clicked(self):
		global hamibot_scriptId, hamibot_api_dev_script_run_or_stop, hamibot_api_dev_script_edit

		#紀錄上次點選嘅腳本id
		hamibot_before_scriptId = hamibot_scriptId
		#獲取點選中嘅腳本ID
		hamibot_scriptId = self.dev_script_table.item(self.dev_script_table.currentRow(),0).text()
		if hamibot_before_scriptId != hamibot_scriptId:
			#獲取腳本ID後修改url
			hamibot_api_dev_script_run_or_stop = hamibot_api_dev_script_run_or_stop.replace(str(hamibot_before_scriptId),str(hamibot_scriptId))
			hamibot_api_dev_script_edit = hamibot_api_dev_script_edit.replace(str(hamibot_before_scriptId),str(hamibot_scriptId))		


	def dev_script_table_doubleClicked(self):
		row = self.dev_script_table.currentIndex().row()
		column = self.dev_script_table.currentIndex().column()
		if column != 0:
			name = self.dev_script_table.item(row,column).text()
			pyperclip.copy(name)
			self.log_bar.setText(self.tr('已複製名字---')+name)

	def on_dev_script_edit_config_check(self,isCheck):
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)
		
		data['edit_config_checked'] = isCheck
		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)


	def oncurrentChanged(self,i):
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)

		#當打開指定頁面button先顯示番，唔同match原因係要python3.10，xp會用唔到
		if i == 1:
			self.refresh_dev_script.setVisible(True)
		else:
			self.refresh_dev_script.setVisible(False)

		#記錄上次打開邊版，下次打番開戈版
		data['current_tab'] = i
		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)


	def ontokens_changed(self, text):
		data['hamibot_tokens'] = text

		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)


	def onlanguage_switch(self,i):	
		if i == 1:
			data['language'] = 'tc'
			self.log_bar.setText('更換語言後請重新打開軟件')
		elif i == 2:
			data['language'] = 'sc'
			self.log_bar.setText('更换语言后请重新打开软件')

		with open(filename,'w') as f_obj:
				json.dump(data,f_obj)

	def onlower_api_quotas_check(self,isChecked):
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)

		data['lower_api_quotas_checked'] = isChecked

		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)



	def on_dev_script_edit_button(self):
		global hamibot_scriptId
		#獲取文件夾位置
		folder_location = self.folder_location.text()
		#獲取當前行數
		current_dev_script_table_choose_row = self.dev_script_table.currentRow()
		dev_script_folder = ''
		#檢查上傳配置文件方塊有無勾選
		edit_config = self.dev_script_edit_config.isChecked()
		hamibot_tokens = self.tokens.text()

		#獲取點選中嘅腳本ID
		# print(current_dev_script_table_choose_name)
		#當上傳時無選資料夾
		if folder_location == '':
			self.log_bar.setText(self.tr('請先選擇資料夾'))
		elif current_dev_script_table_choose_row == -1 or hamibot_scriptId == " ":
			self.log_bar.setText(self.tr('請先選擇腳本'))
		#當選左腳本判斷有無戈個資料夾同文件
		elif current_dev_script_table_choose_row != -1:
			#獲取當前行嘅腳本文件夾
			dev_script_folder = folder_location+'/'+self.dev_script_table.item(current_dev_script_table_choose_row,1).text()

			#判斷有無戈個資料夾
			if not os.path.isdir(dev_script_folder):
				self.log_bar.setText(self.tr('請在此資料夾下創建與腳本名稱相同的資料夾'))
			#判斷資料夾有無index.js
			elif not os.path.isfile(dev_script_folder+'/'+'index.js'):
				self.log_bar.setText(self.tr('請在此資料夾下創建index.js文件，上傳後，原先腳本內容會被取代'))
			#判斷資料夾有無config.json
			elif edit_config == True and not os.path.isfile(dev_script_folder+'/'+'config.json'):
				self.log_bar.setText(self.tr('請在此資料夾下創建config.json文件，上傳後，原先腳本內容會被取代'))
			else:
				# global hamibot_scriptId
				#紀錄上次點選嘅腳本id
				# hamibot_before_scriptId = hamibot_scriptId
				#獲取點選嘅腳本id
				# hamibot_scriptId = self.dev_script_table.item(current_dev_script_table_choose_row,0).text()
				# hamibot_api_dev_script_edit = hamibot_api_dev_script_edit.replace(hamibot_before_scriptId,hamibot_scriptId)
				# print(hamibot_api_dev_script_edit)
				#獲取腳本ID後修改url
				dev_script_edit(self, hamibot_api_url+hamibot_api_dev_script_edit, hamibot_tokens, dev_script_folder, edit_config)
			

	def on_openfolder(self, event):
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)
			
		if event.button() == Qt.LeftButton:
			
			#獲取依家文件夾位置
			before_FileDirectory = self.folder_location.text()
			#選擇目錄，返回選中的路徑
			FileDirectory = QFileDialog.getExistingDirectory(QMainWindow(), self.tr("選擇資料夾")) 

			#如果選擇嘅資料夾同之前唔同
			if before_FileDirectory != FileDirectory:
				before_FileDirectory = FileDirectory
				#將路徑放入edit_link到
				self.folder_location.setText(FileDirectory)
				#增加log_bar提示
				self.log_bar.setText(self.tr('設定資料夾為：')+FileDirectory)
				#修改資料
				data['folder_location'] = FileDirectory
				#儲存資料
				# save_data = data
				with open(filename,'w') as f_obj:
					json.dump(data,f_obj)
			else:
				self.log_bar.setText(self.tr('與之前設定的資料夾相同'))

	def onfolder_location(self,text):
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)

		data['folder_location'] = text
		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)


	def on_dev_script_stop_button(self):
		global hamibot_scriptId, hamibot_api_dev_script_run_or_stop
		#獲取已勾選嘅腳本
		# for line in range(len(dev_script_checkbox)):
		hamibot_tokens = self.tokens.text()
		# #紀錄上次點選嘅腳本id
		# hamibot_before_scriptId = hamibot_scriptId
		#判斷有無選擇腳本同機械人
		if self.dev_script_table.currentRow() != -1 and self.dev_script_robots_combobox.currentIndex() != 0:
			# #獲取點選中嘅腳本ID
			# hamibot_scriptId = self.dev_script_table.item(self.dev_script_table.currentRow(),0).text()
			#獲取腳本ID後修改url
			# hamibot_api_dev_script_run_or_stop = hamibot_api_dev_script_run_or_stop.replace(hamibot_before_scriptId,hamibot_scriptId)
			# print(hamibot_api_dev_script_run_or_stop)
			dev_script_stop(self,hamibot_api_url+hamibot_api_dev_script_run_or_stop,hamibot_tokens,hamibot_current_robot['id'],hamibot_current_robot['name'])
		elif self.dev_script_robots_combobox.currentIndex() == 0:
			self.log_bar.setText(self.tr('請選擇機械人'))
		else:
			self.log_bar.setText(self.tr('請選擇腳本'))

	def on_dev_script_run_button(self):
		print('main--on_dev_script_run_button')

		# global hamibot_scriptId,hamibot_api_dev_script_run_or_stop
		#獲取已勾選嘅腳本
		# for line in range(len(dev_script_checkbox)):
		hamibot_tokens = self.tokens.text()
		#紀錄上次點選嘅腳本id
		# hamibot_before_scriptId = hamibot_scriptId
		#判斷有無選擇腳本同機械人
		if self.dev_script_table.currentRow() != -1 and self.dev_script_robots_combobox.currentIndex() != 0:
			#獲取點選中嘅腳本ID
			# hamibot_scriptId = self.dev_script_table.item(self.dev_script_table.currentRow(),0).text()
			#獲取腳本ID後修改url
			# hamibot_api_dev_script_run_or_stop = hamibot_api_dev_script_run_or_stop.replace(str(hamibot_before_scriptId),str(hamibot_scriptId))
			# print(hamibot_api_dev_script_run_or_stop)
			dev_script_start(self,hamibot_api_url+hamibot_api_dev_script_run_or_stop,hamibot_tokens,hamibot_current_robot['id'],hamibot_current_robot['name'])
		elif self.dev_script_robots_combobox.currentIndex() == 0:
			self.log_bar.setText(self.tr('請選擇機械人'))
		else:
			self.log_bar.setText(self.tr('請選擇腳本'))
		

		
	def on_dev_script_robots_combobox(self,i):
		print('main--on_dev_script_robots_combobox')
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)

		#將變量變成全局變量
		global hamibot_robotId,hamibot_api_robots_stop_all, hamibot_current_robot
		#紀錄上一次選擇嘅機械人
		hamibot_before_robotId = hamibot_robotId
		#獲取依家選擇嘅機械人，並且將id儲入變量到 
		hamibot_robotId = self.dev_script_robots_combobox.currentData()

		#更新停止所有條link，上次選擇嘅機械人取代為依家
		hamibot_api_robots_stop_all = hamibot_api_robots_stop_all.replace(str(hamibot_before_robotId),str(hamibot_robotId))

		#當點選第一個選擇機械人時
		if i == 0:
			self.log_bar.setText(self.tr("請選擇機械人"))
			#如果個機械人有tag就圖示+tag，否則淨係個名	
		elif str(self.dev_script_robots_combobox.itemIcon(i)) != str(QIcon()):
			self.log_bar.setText(self.tr("已選擇機械人：") + "<html><img src='./pic/tags.png'> " + self.dev_script_robots_combobox.currentText() + "</html>")			
		else:
			self.log_bar.setText(self.tr("已選擇機械人：") + self.dev_script_robots_combobox.currentText())

		
		#只要唔係選第一個就會執行
		if i != 0:
			#睇下有無降低配額嘅唔同情況下紀錄依家選擇左嘅機械人id, name, tag
			if self.lower_api_quotas.isChecked() == True:
				#紀錄依家選擇左嘅機械人
				hamibot_current_robot = data['robots_online_list'][i]
				data['current_robots'] = i
				with open(filename,'w') as f_obj:
					json.dump(data,f_obj)
			else:
				hamibot_current_robot = data['robots_online_list'][i]

	def on_dev_script_stopall_button(self):
		print('main--on_dev_script_stopall_button')
		global hamibot_robotId, hamibot_api_robots_stop_all
		#將令牌寫入hamibot_tokens變量
		hamibot_tokens = self.tokens.text()
		#紀錄上一次選擇嘅機械人
		hamibot_before_robotId = hamibot_robotId
		#獲取依家選擇嘅機械人，並且將id儲入變量到 
		hamibot_robotId = self.dev_script_robots_combobox.currentData()
		#更新停止所有條link，上次選擇嘅機械人取代為依家
		hamibot_api_robots_stop_all = hamibot_api_robots_stop_all.replace(str(hamibot_before_robotId),str(hamibot_robotId))
		# print(hamibot_api_robots_stop_all)

		#當唔係第一個選擇(選擇機械人選項)時先會觸發
		if self.dev_script_robots_combobox.currentIndex() != 0:
			dev_script_stop_all(self,hamibot_api_url+hamibot_api_robots_stop_all,hamibot_tokens)
		else:
			self.log_bar.setText(self.tr('請選擇機械人'))
				
				
	def on_refresh_robot_button(self):
		if  self.tokens.text().find('hmp_') == -1:
			self.log_bar.setText(self.tr('請到設定頁完整輸入個人訪問令牌'))
			return
		
		#hamibot_tokens變量
		hamibot_tokens = data['hamibot_tokens']	
		#更新機械人頁面數據
		robots_page_refresh_data(hamibot_api_url+hamibot_api_robots,hamibot_tokens,self)

	def on_refresh_dev_script_button(self):
		if  self.tokens.text().find('hmp_') == -1:
			self.log_bar.setText(self.tr('請到設定頁完整輸入個人訪問令牌'))
		else:
			#hamibot_tokens變量
			hamibot_tokens = data['hamibot_tokens']		
			#更新開發腳本頁面數據
			dev_script_page_refresh_data(hamibot_api_url+hamibot_api_dev_script,hamibot_tokens,self)

	def closeEvent(self,event):#函数名固定不可变
		#讀資料
		with open(filename,"r") as f_obj:
			#讀取資料
			data = json.load(f_obj)

		if data['lower_api_quotas_checked'] == False:
			data['robots_list'] = []
			data['robots_online_list'] = []
			data['dev_script_list'] = []
			
			with open(filename,'w') as f_obj:
       			 json.dump(data,f_obj)
		# reply = QMessageBox.question(self,u'警告',u'确认退出?',QMessageBox.Yes,QMessageBox.No)
        # #QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
		# if reply == QMessageBox.Yes:
		# 	event.accept()#关闭窗口
		# else:
		# 	event.ignore()#忽视点击X事件


if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	trans = QTranslator(app)

	#當第一次使用就會根據系統嘅語言
	if data['language'] == '':
		if  'TW' in local_language or 'HK' in local_language or 'MO' in local_language:
			data['language'] = 'tc'
		elif 'CN'  in local_language:
			data['language'] = 'sc'
		else:
			data['language'] = 'tc'
		
		with open(filename,'w') as f_obj:
			json.dump(data,f_obj)


	trans.load('./language/'+data['language'])
	app.installTranslator(trans)

	mwin = MainWindow()
	# qtmodern.styles.dark(app)
	# win = qtmodern.windows.ModernWindow(mwin)
	mwin.show()

	sys.exit(app.exec_())
