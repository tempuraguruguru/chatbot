from transformers import BertJapaneseTokenizer, BertModel
import torch
import torch.nn.functional as F
import pandas as pd

class SentenceBertJapanese:
    def __init__(self, model_name_or_path, device = None):
        self.tokenizer = BertJapaneseTokenizer.from_pretrained(model_name_or_path)
        self.model = BertModel.from_pretrained(model_name_or_path)
        self.model.eval()

        if(device is None):
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        self.model.to(device)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min = 1e-9)

    @torch.no_grad()
    def encode(self, sentences, batch_size = 8):
        all_embeddings = []
        iterator = range(0, len(sentences), batch_size)
        for batch_idx in iterator:
            batch = sentences[batch_idx: batch_idx + batch_size]
            encoded_input = self.tokenizer.batch_encode_plus(batch, padding = "longest", truncation = True, return_tensors = "pt").to(self.device)
            model_output = self.model(**encoded_input)
            sentence_embeddings = self._mean_pooling(model_output, encoded_input["attention_mask"]).to('cpu')
            all_embeddings.extend(sentence_embeddings)
        return torch.stack(all_embeddings)


# sim = F.cosine_similarity(vecs[0], vecs).tolist()
# pd.DataFrame({'文章': input_docs, '類似度': sim})
#上記2つのコードでは引数の次元が違う(多い？)とかなんやで使用できない。
#したがって、下記にコサイン類似度を計算する関数を自作した。

import math

def normalize(X):#正規化
    norm = Norm(X)
    if(norm == 0):
        return X
    return [x/norm for x in X]

def Norm(X):#ノルム計算
    total = 0
    for x in X:
        total += x*x
    return math.sqrt(total)

def DotProduct(X, Y):#内積計算
    total = 0
    if(len(X) == len(Y)):
        for i in range(len(X)):
            total += X[i]*Y[i]
    else:
        return 0
    return total

def cos_sim(X, Y):#コサイン類似度計算
    X = normalize(X)
    Y = normalize(Y)
    return DotProduct(X, Y) / (Norm(X) * Norm(Y))



#継承する関数--------------------------------------------------
positive = ['はい', 'ある', 'うん', 'あります','思う']
negative = ['いいえ', 'ない', 'ないです', '思わない','ありません']

model = SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens-v2")#既存の日本語学習モデルを読み込み

vecs_p = model.encode(positive, batch_size=12)
vecs_n = model.encode(negative, batch_size=12)

def yes_or_no(text):
    vec = model.encode(text, batch_size=12)#文章をベクトル化
    for i in range(len(positive)):
        if(0.7 < math.floor(cos_sim(vec[0], vecs_p[i]).item()*10**6)/(10**6) <= 1.0):
            print("ポジティブ返答")
            return True
    for i in range(len(negative)):
        print(f"n_{i}: {math.floor(cos_sim(vec[0], vecs_n[i]).item()*10**6)/(10**6)}")
        if(0.7 < math.floor(cos_sim(vec[0], vecs_n[i]).item()*10**6)/(10**6) <= 1):
            print("ネガティブ返答")
            return False
    print("あなたの答えは中途半端すぎた")


#テスト----------------------------------------------------------
text2 = ["あります"]
vec2 = model.encode(text2, batch_size=12)
# print(type(vec2[0]))
# print(normalize(vec2[0]))
# print(type(cos_sim(vec2[0], vecs_n[0]).item()))
# print(f"コサイン類似度: {cos_sim(vec2[0], vecs_n[0])}")


##改善点---------------------------------------------------------
#コサイン類似度をとったときに計算が積み重なって誤差が起きてしまう。
#negativeのときのコサイン類似度で類似度を求めているのに比べる範囲を-1~-0.7にしていた。