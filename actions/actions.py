# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import random
import requests
import json
# 加入文字分析模組&外部搜尋模組
from . import TextAnalyze
from .OuterSearch import outerSearch
# 摘要
from . import StackData

# head_url = 'http://soselab.asuscomm.com:55001/api/'
# head_url='http://localhost:55001/api/'
head_url = 'https://soselab.asuscomm.com:55002/api/'
"""
#共同討論
class ask_return_and_reward(Action):
    def name(self) -> Text:
        return "ask_return_and_reward"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        #拿到replier_id, room_id
        replier_id_room_id = tracker.get_slot("replier_id").split(',')
        replier_id = replier_id_room_id[1]
        room_id = replier_id_room_id[2]
        print("replier_id: "+replier_id)
        print("room_id: "+room_id)
        #拿到tags
        response = requests.post(head_url+'query_chat_tag', json={'_id':room_id})
        tags = json.loads(response.text)
        print("tags: ")
        print(tags)
        #為回答者加積分
        requests.post(head_url+'update_user_score', json={'_id':replier_id, 'tag':tags, 'score':3})
        
        reply="請問你願意回報此問題嗎？（僅限提問者回覆）"
        dispatcher.utter_message(text=reply)
        return []
        
#錯誤訊息解答
class error_message_search(Action):
    def name(self) -> Text:
        return "error_message_search"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        function = tracker.get_slot("function")
        print("pl(programming language):"+tracker.get_slot("pl"))
        os = tracker.get_slot("os")[0:-13]
        pl = tracker.get_slot("pl")[0:-13]
        print("pl(programming language):"+pl)
        error_message_search_time = int(tracker.get_slot("error_message_search_time"))
        #拿到所需訊息及最後一句使用者輸入
        question_or_error_message = tracker.get_slot("error_message_question")
        print(question_or_error_message)
        #question_or_error_message = question_or_error_message.split(',',1)[1]
        qkey = question_or_error_message.split(' ')
        qkey.append(os)
        qkey.append(pl)
            
        #外部搜尋結果（URL）
        resultpage = outerSearch(qkey, 10, error_message_search_time)
            
        stack_items = [StackData(url) for url in resultpage]
        result_title = []
#        for i in resultpage:
        for items in stack_items:
        #showData回傳的資料即是傳送到前端的json格式
            display = items.showData()
            result_title.append(display['question']['title'])
#            result_title.append(i)
    
        reply = "謝謝您的等待，以下為搜尋結果的資料摘要："
        for i in range(0, len(resultpage)):
            reply += ("<br>" + str(i+1) + ".<a href=\"" + resultpage[i] + "\">"+ result_title[i] + "</a>")
        reply += "<br>點選摘要連結可顯示內容。<br><br>希望有幫到你，歡迎下次光臨！透過左邊目錄查看更多功能。"

        #reply += "<a href=\"#\" onclick=\"summary('all')\">點我查看所有答案排名</a>"
        dispatcher.utter_message(text=reply)
        return [SlotSet("error_message_search_time", float(error_message_search_time+1))]
        
#共同討論：是否匿名
class popover_return_incognito(Action):
    def name(self) -> Text:
        return "popover_return_incognito"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
#        affirm = ["好", "是", "匿名", "我要匿名"]
        deny = ["不", "否", "no", "別"]
        incognito = tracker.get_slot("whether_incognito").split(',',1)[1]
        reply = "popover,是"
        for i in deny:
            if i in incognito:
                reply = "popover,否"
        dispatcher.utter_message(text=reply)
        return []
     
#共同討論：討論標籤
class received_discuss_tags(Action):
    def name(self) -> Text:
        return "received_discuss_tags"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        print("received_discuss_tags")
        selected_tags_id = tracker.get_slot("discuss_tags").split('：',1)[1]
        selected_tags_id = selected_tags_id.replace(" ", "")
        selected_tags_array = selected_tags_id.split(',')
        selected_tags_name=""
        for i in selected_tags_array:
            r = requests.get(url = head_url+'query_tag_name', params = {'tag_id':i})
            data = r.json()
            tag_name = data['tag_name']
            selected_tags_name += (tag_name+', ')
        selected_tags_name=selected_tags_name[0:-2]
        reply = "接收到了 "+selected_tags_name+" 標籤。請說明你想討論的問題。"
        dispatcher.utter_message(text=reply)
        return []
   
"""
# 將整句話(問題描述、錯誤訊息)填入slot


class FillSlot(Action):
    def name(self) -> Text:
        return "fill_slot"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        function = tracker.get_slot("function")
        os = tracker.get_slot("os")
        pl = tracker.get_slot("pl")
        
        if os is not None and pl is not None:
            if "error message" in function:
                reply = "Please paste your error message here: "
            elif "guiding QA" in function:
                reply = "Please describe your question here: "
            else:
                reply = "no such service :("
        else:
            if "discussion" in function:
                reply = "是否匿名?"
            else:
                if pl is None:
                    reply = "Which programming language are you using?<br>" \
                            "You can change it later by entering 'change language'"
                elif os is None:
                    reply = "Which operating system are you using?" \
                            "<br>You can change it later by entering 'change OS'"
        
        dispatcher.utter_message(text=reply)
        return []


#分析並搜尋並記下使用者輸入及相關關鍵字（第一次搜尋）
class analyze_and_search(Action):
    def name(self) -> Text:
        return "analyze_and_search"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        print('in analyze_and_search')
        function = tracker.get_slot("function")
        print("pl(programming language):"+tracker.get_slot("pl"))
        os = tracker.get_slot("os")
        pl = tracker.get_slot("pl")
        print("pl(programming language):"+pl)
        if "錯誤訊息" in function:
            #拿到所需訊息及最後一句使用者輸入
            question_or_error_message = tracker.latest_message.get('text')

            print("analyze_and_search_錯誤訊息: " + question_or_error_message)
            #question_or_error_message = question_or_error_message.split(',',1)[1]
            qkey = question_or_error_message.split(' ')
            qkey.append(os)
            qkey.append(pl)
            
            print(qkey)
            #外部搜尋結果（URL）
            resultpage = outerSearch(qkey, 10, 0)
            
            stack_items = [StackData(url) for url in resultpage]
            result_title = []
#            for i in resultpage:
            for items in stack_items:
                #showData回傳的資料即是傳送到前端的json格式
                display = items.showData()
                result_title.append(display['question']['title'])
#                result_title.append(i)
    
            reply = "謝謝您的等待，以下為搜尋結果的資料摘要："
            for i in range(0, len(resultpage)):
                reply += ("<br>" + str(i+1) + ".<a href=\"" + resultpage[i] + "\">"+ result_title[i] + "</a>")
            reply += "<br>點選摘要連結可顯示內容。<br><br>是否要繼續搜尋？"

            #reply += "<a href=\"#\" onclick=\"summary('all')\">點我查看所有答案排名</a>"
            dispatcher.utter_message(text=reply)
            return [SlotSet("error_message_search_time", 1)]

        elif "引導式" in function:
            #拿到所需訊息及最後一句使用者輸入
            question_or_error_message = tracker.latest_message.get('text')
            print("analyze_and_search_引導式問答: " + question_or_error_message)
            #---#question_or_error_message = question_or_error_message.split(',',1)[1]
#            if question_or_error_message == "是":
#                question_or_error_message = tracker.get_slot("guided_QA_question").split(',',1)[1]
#            else:
#                question_or_error_message = question_or_error_message.split(',',1)[1]
            
            #宣告文字分析器
            textAnalyzer = TextAnalyze.TextAnalyze()
            #擷取使用者問題的關鍵字
    #        qkey = ['flask']
            qkey = textAnalyzer.contentPreProcess(question_or_error_message)[0]
            #加上作業系統與程式語言作為關鍵字
            qkey.append(os)
            qkey.append(pl)

            #內部搜尋
            print("qkey: ", qkey)
            #---#response = requests.post(head_url+'query_inner_search', json={'keywords':qkey})
    #        print("內部搜尋的結果: ", response.text)
    
            # 慈 START
            #---#objectAllPost = json.loads(response.text)
            #---#if objectAllPost["inner_search_result"] != None:
                #---#postNumber = 1
                #---#reply = "謝謝您的等待，以下為搜尋結果：<br>"
                #---#for i in range(0, len(objectAllPost["inner_search_result"])):
                    #---#postId = objectAllPost["inner_search_result"][i]
                    #---#singlePostResponse = requests.post(head_url+'query_inner_post', json={'_id':postId})
                    # 轉成object
                    #---#objectSinglePost = json.loads(singlePostResponse.text)
        #            print("單篇文章結果: ", objectSinglePost)
                    #---#reply += str(postNumber)
                    #---#reply += '. <a href="#" onclick="clickChatroomInnerSearch(\''
                    #---#reply += objectSinglePost["_id"]
                    #---#reply += '\')">'
                    #---#reply += objectSinglePost["title"]
                    #---#reply += '</a><br>'
                    #---#postNumber += 1
                
        #        print("reply的結果: "+reply);
            #---#else:
                #---#reply = ""
            # 慈 END
            
            #外部搜尋結果（URL）
            resultpage = outerSearch(qkey, 10, 0)
            for url in resultpage:
                print(url)

            #外部搜尋
            #stackoverflow物件
            #---#stack_items = StackData.parseStackData(resultpage)
            ######假資料～～～～～
            
            with open("DATA_test.json", "r", encoding="utf-8") as f:
                stack_items = json.load(f)
                
            raw_data = [" ".join([item['question']['abstract'], " ".join([ans['abstract'] for ans in item['answers']])]) for item in stack_items ]
            #取得block排名
            result = TextAnalyze.blockRanking(stack_items, qkey)
            #print(result)
            for i in stack_items:
                i['question']['abstract'] = str(textAnalyzer.textSummarization(i['question']['abstract']))
                for ans in i['answers']:
                    ans['abstract'] = str(textAnalyzer.textSummarization(ans['abstract']))
                    
            #---#temp_data_id_list = requests.post(head_url + 'insert_cache', json={'data' : stack_items, 'type' : "temp_data"})
            #---#block_rank_id = requests.post(head_url + 'insert_cache', json={'data': result, 'type' : "blocks_rank"})

            #---#print(temp_data_id_list.text)
            #---#print(block_rank_id.text)
            #---#t_data_list = json.loads(temp_data_id_list.text)
            #---#blocks = json.loads(block_rank_id.text)

            #每篇title
            result_title = [item['question']['title'] for item in stack_items]

            reply = "謝謝您的等待，以下為搜尋結果的資料摘要："
            #---#for i in range(0, len(t_data_list)):
                #---#reply += ("<br>" + str(i+1) + ".<a href=\"#\" onclick=\"summary('" + t_data_list[i] + "')\">" + result_title[i] + "</a>")
            #---#reply += "<br>點選摘要連結可顯示內容。<br>"
            #---#reply += "<a href=\"#\" onclick=\"rank('" + blocks[0] + "')\">點我查看所有答案排名</a>"
            reply += "<br><br>是否要繼續搜尋？"
            dispatcher.utter_message(text=reply)
            
    #        dispatcher.utter_message(text="是否繼續搜尋？")
            
            # 慈 START
    #        reply += "<br><br>是否繼續搜尋？"
#dispatcher.utter_message(text=reply)
            # 慈 END

            more_keywords = textAnalyzer.keywordExtraction(raw_data)
            qkey = qkey + more_keywords
            #！！！將關鍵字及更多關鍵字存入slot
            return [SlotSet("keywords", ','.join(qkey))]
            
            
            
#給user選關鍵字


#選擇關鍵字
class select_keyword(Action):
    def name(self) -> Text:
        return "select_keyword"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        #！！！拿到之前存的關鍵字
        print("給使用者選關鍵字了！")
        qkey = tracker.get_slot("keywords")
        print(qkey)
        qkey = qkey.split(',')
        
        #------------test------------#
        #textAnalyzer = TextAnalyze.TextAnalyze()
        #more_keywords = textAnalyzer.keywordExtraction(eval(raw_data))
        #----------------------------#
        
        reply = '新增/刪除用來搜尋的關鍵字<br><div id="keywords'
        #reply += keywordsTime
        reply += '">'
        id = 0
        for i in qkey:
            reply += '<label id="'
            reply += str(id)
            reply += '" class="badge badge-default purpleLabel">'
            reply += i
            reply += '<button class="labelXBtn" onclick="cancleKeyWords(\''
            reply += str(id)
            reply += '\')">x</button></label>'
            id += 1
        reply += '</div><br><input id="addBtn" class="btn btn-primary purpleBtnInChatroom" value="新增" onclick="wantAddKeyWord()"><input id="doneBtn"class="btn btn-primary purpleBtnInChatroom" value="完成" onclick="doneKeyWord()">'
        
        dispatcher.utter_message(text=reply)
        return []
        
        

#拿選好的關鍵字搜尋(繼續搜尋)
class outer_search(Action):
    def name(self) -> Text:
        return "outer_search"
    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        #拿到所需訊息及最後一句使用者輸入
        print("去外部搜尋了！")
        keywords = tracker.latest_message.get('text')
        #keywords = keywords.split(',',1)[1]
        print(keywords)
        
        #宣告文字分析器
        textAnalyzer = TextAnalyze.TextAnalyze()
            
        qkey = keywords.split(',')
        #外部搜尋結果（URL）
        #---#resultpage = outerSearch(qkey, 10, 0)
        #---#for url in resultpage:
        #---#    print(url)
        #外部搜尋
        #stackoverflow物件
        #---#stack_items = StackData.parseStackData(resultpage)
        
        #假資料～～～～～
        with open("DATA_test.json", "r", encoding="utf-8") as f:
            stack_items = json.load(f)
        
        raw_data = [ " ".join([item['question']['abstract'], " ".join([ans['abstract'] for ans in item['answers']])]) for item in stack_items ]
        #取得block排名
        result = TextAnalyze.blockRanking(stack_items, qkey)
        #print(result)
        for i in stack_items:
            i['question']['abstract'] = str(textAnalyzer.textSummarization(i['question']['abstract']))
            for ans in i['answers']:
                ans['abstract'] = str(textAnalyzer.textSummarization(ans['abstract']))
                    
        #---#temp_data_id_list = requests.post(head_url + 'insert_cache', json={'data' : stack_items[0:5], 'type' : "temp_data"}, verify=False)
        #---#block_rank_id = requests.post(head_url + 'insert_cache', json={'data': result, 'type' : "blocks_rank"}, verify=False)
        
        #---#print(temp_data_id_list.text)
        #---#print(block_rank_id.text)
        #---#t_data_list = json.loads(temp_data_id_list.text)
        #---#blocks = json.loads(block_rank_id.text)
        
        #每篇title
        result_title = [item['question']['title'] for item in stack_items]
        result_title = "\n".join(result_title)
        
        reply = "謝謝您的等待，以下為搜尋結果的資料摘要：" + result_title
        #---#for i in range(0, len(t_data_list)):
        #---#    reply += ("<br>" + str(i+1) + ".<a href=\"#\" onclick=\"summary('" + t_data_list[i] + "')\">" + result_title[i] + "</a>")
        #---#reply += "<br>點選摘要連結可顯示內容。<br>"
        #---#reply += "<a href=\"#\" onclick=\"rank('" + blocks[0] + "')\">點我查看所有答案排名</a>"
        #---#reply += "<br><br>是否要繼續搜尋？"
        
        #---#print("繼續搜尋reply：", reply)
        dispatcher.utter_message(text=reply)
        return []
