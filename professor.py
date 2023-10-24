import sort

class Professor:
    def __init__(self, name, labo, major):#majorはリスト
        self.labo = labo
        self.name = name
        self.majors = sort.sort(major)
        self.score = 0
    
    def get_name(self):#本名
        return self.name

    def get_labo(self):#研究室名
        return self.labo
    
    def get_majors(self):#関連ワード
        return self.majors

    def get_score(self):#スコア
        return self.score



#辞書を受け取ってクラスにするよ
#professor = Professor(dic2[i].value, dic1[i].key, dic1[i].value)
