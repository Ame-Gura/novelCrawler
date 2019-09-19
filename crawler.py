from bs4 import BeautifulSoup
import requests
import pickle

class Chapter:
    def __init__(self, h1, h2, p):
        self.h1 = h1
        self.h2 = h2
        self.p = p
    def getDic(self):
        return {'h1': self.h1, 'h2': self.h2, 'p': self.p}

def getLinkList():

    #get link list
    html = requests.get('https://blastron01.tumblr.com/honzuki-contents')
    html.encoding = 'UTF-8'
    soup = BeautifulSoup(html.text, 'lxml')

    contents = soup.select('#blog > div > div:nth-child(6) > ul')

    contentsList = [content.contents[0].get('href') for content in contents[0].contents]
    return contentsList

def getContentsFromblastronBlog(link):

    html = requests.get(link)
    html.encoding = 'UTF-8'
    soup = BeautifulSoup(html.text, 'lxml')
    postText = soup.select_one('#blog > div')
    h1 = postText.find('h1').text
    try:
        h2 = postText.find('h2').text
    except AttributeError:
        h2 = postText.find_all('h1')[1].text
        print(link)
        print(h2)
    pragraphList = postText.find_all('p')
    p = [pragraph.text for pragraph in pragraphList]
    del p[-1]
    chapter = Chapter(h1,h2,p)
    return chapter


if __name__ == '__main__':
    linkList = getLinkList()
    print('got linkList')
    chapters = []
    for link in linkList:
        chapters.append(getContentsFromblastronBlog(link).getDic())
    print('got chapters')
    with open('chapters', 'wb') as f:
        pickle.dump(chapters, f)
    pass



