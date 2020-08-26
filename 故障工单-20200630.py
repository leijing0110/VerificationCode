# 集中派单  机器上运行的
from selenium import webdriver  #pip install selenium 
import os
import time
import re

class VerificationCode:
    def __init__(self):
        #引入chromedriver.exe
        chromedriver = "C:\\Users\jiedan\\AppData\Local\\Google\\Chrome\\Application\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        self.driver = browser
        self.find_element = self.driver.find_element_by_css_selector
        
    def get_pictures(self):
        self.driver.get('http://119.39.227.99:9189/EOMSCU/login.jsp')  # 打开登陆页面
        time.sleep(5)
        self.driver.find_element_by_id("userId").send_keys("dw_leiting")
        self.driver.find_element_by_id("passId").send_keys("cz@123456")
        img = self.find_element('#mpanel1 > div > div.verify-code')  # 验证码
        time.sleep(2)
        verycode_text = img.text
        self.driver.find_element_by_xpath('//*[@id="mpanel1"]/div/div[2]/div/input').send_keys(verycode_text)
        time.sleep(2)
        self.driver.find_element_by_id("submitButton").click()
        time.sleep(10)
    
        links_len_str  = self.driver.find_element_by_css_selector('#backlog').text#工单数量
        if len(links_len_str) == 0:#未获取到工单数量
            self.driver.quit()
        time.sleep(10)
        
        #点击代办工单
        self.driver.find_element_by_xpath('//*[@id="bodybody"]/div/aside/section/ul/li[1]/ul/li[2]/a').click()
        time.sleep(5)

        self.driver.switch_to_frame('mainFrame')#跳转至待处理工单
        self.driver.maximize_window() #窗口最大化
        print (time.strftime("%Y-%m-%d %H:%M:%S")) #输出时间
        print (links_len_str) #输出工单数量
        time.sleep(5)
        

        links_len = int(links_len_str)
        if links_len == 0:#工单数量为 0
            self.driver.quit()
        else:
            #testlen2 = self.driver.find_element_by_xpath('/html/body/section/div/div[2]/div[4]/div[1]/span[1]').text
            testlen2 = self.driver.find_element_by_css_selector('body > section > div > div.fixed-table-container > div.fixed-table-pagination > div.pull-left.pagination-detail > span.pagination-info').text
            if testlen2 == '没有找到匹配的记录':
                print('工单数量为：0')
                links_len = 0
                self.driver.quit()
            else:
                # \d+ 匹配字符串中的数字部分，返回列表
                #num = re.findall('\d+',testlen2)
                #links_len = int(num[0])
                resultnumber = re.search('\d+',testlen2)
                if resultnumber == None:
                    self.driver.quit()
                else:
                    links_len = int(resultnumber.group(0))
                    print('工单数量是：',links_len)
                    

        time.sleep(10)
        if links_len == 1:
            link_text =  self.driver.find_element_by_xpath('//*[@id="reportTable"]/tbody/tr/td[8]/a').text
            if link_text == '签收':
                self.driver.find_element_by_xpath('//*[@id="reportTable"]/tbody/tr/td[8]/a').click()#签收
                time.sleep(2)
                self.driver.switch_to_frame('layui-layer-iframe1')
                #self.driver.maximize_window() #窗口最大化
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id="theForm"]/nav/input[1]').click()#点击提交按钮
                time.sleep(2)
                self.driver.quit()
            else:
                self.driver.quit()
        else:#工单数 非 0，非1
            for index in range(links_len):
                if index ==51:#只处理50条工单，后面的工单不处理了
                    break
                #testxpath = str(index+1)
                testindex = index%10
                testxpath = str(testindex+1)
            
                link_text =  self.driver.find_element_by_xpath('//*[@id="reportTable"]/tbody/tr['+testxpath+']/td[8]/a').text
                if link_text == '签收':
                    self.driver.find_element_by_xpath('//*[@id="reportTable"]/tbody/tr['+testxpath+']/td[8]/a').click()#签收
                    time.sleep(2)
                    self.driver.switch_to_frame('layui-layer-iframe1')#弹窗的iframe
                    #self.driver.maximize_window() #窗口最大化
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="theForm"]/nav/input[1]').click()#点击提交按钮
                    time.sleep(2)
                    time.sleep(10)
                    self.driver.switch_to_frame('mainFrame')
                    time.sleep(2)
                    #跳转到对应的页
                    if index >= 10:
                        pagenum = int(index/10)+1#页码
                        testxpath2 = str(pagenum+2)#当前页的xpathid
                        self.driver.find_element_by_xpath('/html/body/section/div/div[2]/div[4]/div[2]/ul/li['+testxpath2+']/a').click()
                            
                #else:
                    #self.driver.quit()
                if testindex == 9 and links_len%10!=0:
                    #跳转到下1页
                    pagenum2 = int(index/10)+1#页码
                    testxpath3 = str(pagenum2+3)#下1页的xpathid
                    self.driver.find_element_by_xpath('/html/body/section/div/div[2]/div[4]/div[2]/ul/li['+testxpath3+']/a').click()

        
        time.sleep(2)
        self.driver.quit()
                
                

if __name__ == '__main__':
    a = VerificationCode()
    a.get_pictures()