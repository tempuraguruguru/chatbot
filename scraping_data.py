import requests
from bs4 import BeautifulSoup


def main():
    url = "https://nyushi.hosei.ac.jp/laboratory/faculty/1"
    res = requests.get(url)
    lab_tags = getLabTags(res.text)
    
    #print(lab_tags)

    lab_prof_name = getProfNames(res.text)
    
    #print(lab_prof_name)
    #+a
    return (lab_tags, lab_prof_name)

def getLabTags(res):
    dic = {}
    s = BeautifulSoup(res, "html.parser")
    for a in s.find_all("article"):
        name = a.find("h3").string
        l = []
        for w in a.find_all("li"):
            l.append(w.string)
        
        dic[name] = l
    
    return dic

def getProfNames(res):
    dic = {}
    s = BeautifulSoup(res, "html.parser")
    for a in s.find_all("article"):
        name = a.find("h3").string
        p_tags =  a.find_all("p")
        pre_s = p_tags[1].string
        
        dic[name] = pre_s[pre_s.find("\u2003") + 1:]
    
    return dic



main()