__author__ = 'root'
#coding=utf-8

from extract import extract
import os
import jieba
import math
import codecs

class Chiextration:
    
    # categories = ['健康养生', '军事历史', '时政', '公益', '读书', '电视剧', 'IT互联网', '教育', '艺术', '电影', '动漫', '游戏', '旅游', '美食', '摄影', '萌宠',
    #         '服装美容', '体育', '设计', '综艺', '星座', '音乐', '健身', '财经']
    categories = [u'健康养生', u'军事历史', u'时政', u'公益', u'读书', u'电视剧', u'IT互联网', u'教育', u'艺术', u'电影', u'动漫', u'游戏', u'旅游', u'美食', u'摄影', u'萌宠',
            u'服装美容', u'体育', u'设计', u'综艺', u'星座', u'音乐', u'健身', u'财经']

    def __init__(self, document):
        self.document = {}
        self.document = document
        self.docNum = self.DocNum()
        self.cateinDoc = {}
        self.wordlist = self.Getwordlist()
        for category in Chiextration.categories:
            number = self.CateInDoc(category)
            self.cateinDoc[category] = number

    def WordInDoc(self, word):
        count = 0
        for content in self.document:
            if word in content:
                count += 1
        return count

    def CateInDoc(self, category):
        categories = self.document.values()
        return categories.count(category)

    def DocNum(self):
        return self.document.__len__()

    def WordInCate(self, word, category):
        count = 0
        for doc in self.document:
            if self.document[doc] == category:
                if word in doc:
                    count += 1
        return count

    def CalculateCHI(self, word, category):
        docNum = self.docNum
        wordInDoc = self.WordInDoc(word) #A+B
        wordNotInDoc = docNum - wordInDoc #C+D
        cateIndoc = self.cateinDoc[category] #A+C
        cateNotIndoc = docNum - cateIndoc #B+D
        wordInCate = self.WordInCate(word, category) #A
        wordNotInCate = wordInDoc - wordInCate #B
        cateWithoutWord = cateIndoc - wordInCate #C
        notCateAndWord = wordNotInDoc - wordNotInCate #D
        N = docNum * float(wordInCate*notCateAndWord-wordNotInCate*cateWithoutWord) * (wordInCate*notCateAndWord-wordNotInCate*cateWithoutWord)
        M = (cateIndoc+0.1) * (wordInDoc+0.1) * (cateNotIndoc+0.1) * (wordNotInDoc+0.1)
        chi = float(N) / M
        return chi

    def Getwordlist(self):
        wordlist = []
        for doc in self.document:
            words = doc.split(',')
            for word in words:
                wordlist.append(word)
        return wordlist

    def wordfrequent(self, word, category):
        wordlist = self.wordlist
        cateInDoc = self.CateInDoc(category)
        frequent = float(wordlist.count(word))/(cateInDoc+1)
        return frequent


    def ImproCalculateCHI(self, word, category):
        docNum = self.docNum
        wordInCate = self.WordInCate(word, category) #A
        cateIndoc = self.cateinDoc[category] #A+C
        wordInDoc = self.WordInDoc(word) #A+B
        wordNotInDoc = docNum - wordInDoc #C+D
        cateNotIndoc = docNum - cateIndoc #B+D
        wordNotInCate = wordInDoc - wordInCate #B
        cateWithoutWord = cateIndoc - wordInCate #C
        notCateAndWord = wordNotInDoc - wordNotInCate #D
        wordlist = self.wordlist
        if (wordInCate*notCateAndWord-wordNotInCate*cateWithoutWord) <= 0:
            return 0
        tf = float(wordlist.count(word)) / wordlist.__len__()
        if tf == 0:
            return 0
        idf = math.log(float(self.document.__len__())/(wordInDoc+0.1))
        tfidf = tf * idf
        N = docNum * float(wordInCate*notCateAndWord-wordNotInCate*cateWithoutWord) * (wordInCate*notCateAndWord-wordNotInCate*cateWithoutWord)
        M = (cateIndoc+0.1) * (wordInDoc+0.1) * (cateNotIndoc+0.1) * (wordNotInDoc+0.1)
        chi = float(N) / M
        frequent = self.wordfrequent(word, category)
        chi *= frequent * tfidf
        return chi



def SplitWord(sentences):
    stopwordfile = open('../工具/哈工大停用词表.txt','r')
    data = stopwordfile.readlines()
    stopwords = []
    for word in data:
        stopwords.append(word)
    words = jieba.cut_for_search(sentences)
    wordlist = []
    for word in words:
        wordlist.append(word)
    words =[]
    for word in wordlist:
        if word.__len__() >= 2 and word.encode('utf-8') not in stopwords:
            words.append(word)
    return words


class Feature_selection:
    categories = [u'健康养生', u'军事历史', u'时政', u'公益', u'读书', u'电视剧', u'IT互联网', u'教育', u'艺术', u'电影', u'动漫', u'游戏', u'旅游', u'美食', u'摄影', u'萌宠',
            u'服装美容', u'体育', u'设计', u'综艺', u'星座', u'音乐', u'健身', u'财经']

    def __init__(self):
        self.document = {}
        self.wordDict = []
    # def loadtrainset(self):
    #     for category in Feature_selection.categories:
    #         catePath = '/home/quincy1994/文档/微脉圈/训练集/' + category
    #         catefiles = os.listdir(catePath)
    #         for catefile in catefiles:
    #             data = open(catePath+'/'+catefile).read()
    #             words = SplitWord(data)
    #             for word in words:
    #                 self.wordDict.append(word)
    #             content = ','.join(words)
    #             self.document[content] = category
    #     self.wordDict = set(self.wordDict)

    def loadDoc(self):
        document = {}
        wordDict = []
        f = codecs.open('document.txt', 'rb', 'utf-8')
        data = f.readlines()
        for sentence in data:
            group = sentence.split(':')
            document[group[0]] = group[1].strip('\n')
            wordslist = group[0].split(',')
            for word in wordslist:
                wordDict.append(word)
        self.document = document
        self.wordDict = set(wordDict)


    def fea_selection(self,wordlist):
        newwordlist = []
        # self.loadtrainset()
        self.loadDoc()
        # print('op')
        chi = Chiextration(self.document)
        for word in wordlist:
            for category in Feature_selection.categories:
                result = chi.ImproCalculateCHI(word, category)
                if result > 0.001:
                    print word, category, result
                    newwordlist.append(word)
            print '---------------'

        return newwordlist

if __name__ == '__main__':
    str = u'你好,宠物,姿势,好的'
    wordlist = str.split(',')
    fea_extraction = Feature_selection()
    newwordlist = fea_extraction.fea_selection(wordlist)


