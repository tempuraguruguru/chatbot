#作成者(五十音順)
#21K1123 那須大聖
#21K1127 野本匠馬
#21K0035 深美利光


from chatbotweb.chat_server import ChatServer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import random
import time

#分割ファイル
import professor
import scraping_data
import sort
import yes_or_no

class MyChatClass():
    BOT_NAME = "研究室お助けBOT"
    html = None

    POSITIVE_WORDS = ["はい", "ある", "うん", "あります","思う"]
    NEGATIVE_WORDS = ["いいえ", "ない", "うーん", "ないです","思わない","ありません"]
    QUESTION_VARIATIONS = [
        "{}に興味はありますか？",
        "{}について学びたいですか？",
        "{}に関しての興味はどうですか？",
        "{}は魅力的だと思いますか？"
    ]

    def __init__(self):
        self.analyzer = Analyzer()

        all = scraping_data.main()
        tags = all[0]
        names = all[1]
        self.labs = []#教授のオブジェクトのリスト
        for i in range(len(names)):
            prof = professor.Professor(list(names.values())[i], list(tags.keys())[i], list(tags.values())[i])
            self.labs.append(prof)
        all_majors = []#専門単語のリスト(頻度に対して昇順)
        self.asked = []#既に質問で使った専門単語のリスト
        for prof in self.labs:
            for major in prof.majors:
                all_majors.append(major)#それぞれの教授の専門をall_majorsに格納
        self.all_tags = sort.sort(all_majors)#全ての教授の専門単語を比較し、キーが専門単語、値が出現回数の辞書を作成。その後、出現回数が少ないものからスタックに格納する。
        self.current_word = None

    def ask_question(self):
        while len(self.labs) > 3:
            word = self.all_tags[-1]
            # for prof in self.labs:
            if(any(word in prof.majors for prof in self.labs)):
                self.current_word = word
                return random.choice(MyChatClass.QUESTION_VARIATIONS).format(word)
            #ここに絞り込みと更新がいたよ
        if(len(self.labs) == 0):
            return f"学部にその条件の研究室はありません。"
        elif(len(self.all_tags) == 1):
            return f"あなたにおすすめの研究室は{self.labs[0].name}教授の{self.labs[0].labo}です。"
        else:
            labs_str = ""
            for i in range(len(self.labs)):
                labs_str += f"{self.labs[i].name}教授の{self.labs[0].labo}、"
            labs_str = labs_str[:-1]
            return f"あなたにおすすめの研究室は{labs_str}のいずれかです。"

    def update_labs(self, word, positive_response):
        self.asked.append(word)
        if(positive_response):
            #研究室の絞り込み
            new_labs = []
            for prof in self.labs:
                if(word in prof.majors):
                    new_labs.append(prof)
            self.labs = new_labs
            #質問単語リストの更新
            all_majors = []
            for prof in self.labs:
                for major in prof.majors:
                    all_majors.append(major)
            self.all_tags = sort.sort(all_majors)
        else :
            new_labs = []
            for prof in self.labs:
                if(word not in prof.majors):
                    new_labs.append(prof)
            self.labs = new_labs
            #質問単語リストの更新
            all_majors = []
            for prof in self.labs:
                for major in prof.majors:
                    all_majors.append(major)
            self.all_tags = sort.sort(all_majors)
        self.all_tags = [word for word in self.all_tags if word not in self.asked]
        print(f"研究室の候補数: {len(self.labs)}")
        print()


class UserClass():
    def __init__(self,chat_obj):
        self.chat_obj = chat_obj

    def init_function(self,query_params):
        return self.chat_obj.ask_question()

    def callback_method(self, text, response):
        start = time.time()
        print(f"Received user input: {text}")
        tokens = [token.base_form for token in self.chat_obj.analyzer.analyze(text)]
        print(f"Recognized tokens: {tokens}")
        print(f"Current word before update: {self.chat_obj.current_word}")

        #2023/10/29変更部分
        input = [text]
        #print("開始")
        word_cos_sim = yes_or_no.yes_or_no(input)
        print(f"入力とコサイン類似度: {word_cos_sim}")
        if word_cos_sim:
            self.chat_obj.update_labs(self.chat_obj.current_word, True)
        else:
            self.chat_obj.update_labs(self.chat_obj.current_word, False)
        finish = time.time()
        print(f"実行時間: {finish-start}")

        return self.chat_obj.ask_question(), True

if __name__ == '__main__':
    address = "0.0.0.0"
    port = 31127
    chat_server = ChatServer(MyChatClass,UserClass)
    chat_server.start(address,port)


##改善点
#1.最終的に絞り込んだ研究室が複数のときにそれらを返すelse処理
#2.なんと入力してもpositive or negativeで判別できる関数
#3.一連のフローが終わった後にもう一度始めからやり直せる
#4.文章をベクトル化してコサイン類似度をとったら計算時間がかなり遅くなってしまった。


##発表後
#「はい」と「いいえ」のベクトルは逆ではないから注意
#「はい」と「いいえ」の真ん中あたりの処理をどうにかしたい
#一番初めに聴く単語に依存しているところが多い。「画像処理」と始めに聞けばすぐ終わるのに、遠回りしてしまう。
#中途半端な返答のときの処理
#「いいえ」と返答したときの質問リストが更新されていない。
#スコアをちゃんと導入すれば上手くいくのか？
#「いいえ」と答え続けるとなぜか花泉先生が推薦される。
#出現する単語の意味がわからない。-> スクレイピングや検索をかけてAPIを使用するよりも辞書構造で解決？
#返答の重みづけがあると良い。
#強化学習→評価が必要、またデータも必要