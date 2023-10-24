class MyStack:
    def __init__(self):
        self.stack = []
    
    def in_null(self):
        if(len(self.stack) == 0):
            return True
        
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        result = self.stack[-1]
        del self.stack[-1]
        return result


#sort関数 リストを引数とする。
def sort(text):
    text2 = []
    #人工知能・機械学習のような記号がついているものを分ける
    for word in text:
        if("・" in word):
            word2 = word.split("・")
            for w2 in word2:
                text2.append(w2)
        elif(word == "AI"):
            text2.append("人工知能")
        elif(word == "CG"):
            text2.append("コンピュータグラフィックス")
        elif(word == "HCI"):
            text2.append("ヒューマンコンピュータインタラクション")
        else:
            text2.append(word)
    dic = {}
    for word in text2:
        if(dic == {}):
            dic[word] = 1
        else:
            if(word in dic):
                dic[word] += 1
            else:
                dic[word] = 1
    #出現頻度が少ない単語が先頭にくるように
    dic_sorted = sorted(dic.items(), key = lambda word : word[1])
    sorded = []
    for key in dic_sorted:
        sorded.append(key[0])
    return sorded
    
    #スタックのtopに出現頻度が最も多い単語
    stack = MyStack()
    for key in dic_sorted:
        stack.push(key[0])
    return stack


#リストとして受け取る
# text = ["データベース", "データベース", "人工知能", 
#         "人工知能・機械学習", "人工知能・機械学習",
#         "人工知能", "システム"]

# stack = sort(text)

# while(not stack.in_null()):
#     print(stack.pop())