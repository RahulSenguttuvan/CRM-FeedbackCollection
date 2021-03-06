import os
import pickle
import bs4
import requests
import urllib.request as Req
import json

def getHtml(link):
    #todo Get the page from the source
    res=Req.urlopen(link)
    return res.read()



class Downloader():
    def __init__(self,product,name="Default"):
        self.product=product.lower()
        self.link=self.makeLink()
        self.name=name
        return

    def makeLink(self,product):
        #should be derived in derived class
        raise Exception("Needs to be implemented")

    def getPage(self):
        self.content=getHtml(self.link)
        self.soup=bs4.BeautifulSoup(self.content)
        #check for the prodcut exists in the store and the page is the one
        title=self.soup.title.contents[0].lower()
        if(not self.product in title):
            raise Exception("Product not in store or Irrevelant Page Reached")

        return

    def getScore(self):
        #should be implemented in Derived Class
        raise Exception("Needs to be implemented")

    def getReviews(self):
        #should be implemented in derived class
        raise Exception("Needs to be implemented")

    def saveSummary(self,summary):

        #make directory for for the product
        os.makedirs("DATA", exist_ok=True)
        os.makedirs(os.path.join("DATA",self.product),exist_ok=True)
        productDir=os.path.join("DATA",self.product,self.name)
        os.makedirs(productDir,exist_ok=True)

        with open(os.path.join(productDir,"summary.json"),"w") as file:
            json.dump(summary,file)

        return

    def process(self):
        self.getPage()
        summary={}
        summary["score"]=self.getScore()
        summary["reviews"]=self.getReviews()
        self.saveSummary(summary)


def encode(name):
    '''Encode the space characters in the name with %20'''
    s=""
    for n in name:
        if(n==" "):
            s+="%20"
        else:
            s+=n

    return s

class FlipkartDownloader(Downloader):

    def __init__(self,product,name="Flipkart"):
        super().__init__(product,name)

    def makeLink(self):
        #get the search results page
        search_q="https://www.flipkart.com/search?q="+encode(self.product)+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        #get the first product page link
        soup=bs4.BeautifulSoup(getHtml(search_q))
        results=soup.find_all("a",{"class":"_31qSD5"})
        product_q="https://www.flipkart.com"+results[0]["href"]
        return product_q #todo 3 create a link for flipkart

    def prependDomain(self,link):
        return "https://www.flipkart.com"+link

    def getScore(self):
        #todo get Score for Flipkart
        results=self.soup.find_all("div",{"class":"hGSR34 _2beYZw"})
        return results[0].contents[0]


    def getReviews(self):
        #todo get Reviews for Flipkart
        #get all %n review page
        reviewanchor=self.soup.find_all("div",{"class":"swINJg _3nrCtb"})[0].parent
        reviewlink=self.prependDomain(reviewanchor["href"])
        self.reviewsoup=bs4.BeautifulSoup(getHtml(reviewlink))
        #extract reviews from the page
        reviewsdivs=self.reviewsoup.find_all("div",{"class":"qwjRop"})
        reviews=[r.div.div.contents[0] for r in reviewsdivs]
        return reviews


class AmazonDownloader(Downloader):

    def __init__(self, product, name="Amazon"):
        super().__init__(product, name)

    def makeLink(self):
        search_q ="https://www.snapdeal.com/search?clickSrc=top_searches&keyword="+encode(self.product)+"&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy"
        soup = bs4.BeautifulSoup(getHtml(search_q))
        results = soup.find_all("div",{"class":"product-desc-rating "})
       # print(results[0].a["href"])
        product_q=results[0].a["href"]
        return product_q

    def prependDomain(self,link):
        return "https://www.amazon.in"+link

    def getScore(self):
        results=self.soup.find_all("span",{"class":"avrg-rating"})
        return results[0].contents[0]

    def getReviews(self):
        # todo get Reviews for Amazon
        #reviewanchor=self.soup.find_all("span",{"class":"viewMoreLink"}).parent
        #print(reviewanchor)
        #reviewlink=self.prependDomain(reviewanchor["href"])
        #reviewlink = reviewanchor["href"] 
        #self.reviewsoup=bs4.BeautifulSoup(getHtml(reviewlink))
        reviewsdivs=self.soup.find_all("div",{"class":"commentlist first jsUserAction"})
        print(reviewsdivs)
        reviews=[r.p.text for r in reviewsdivs]
        print(reviews)
        return reviews





















