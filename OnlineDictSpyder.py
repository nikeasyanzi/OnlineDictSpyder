



# coding=utf-8
# module need to be install: request, lxml html2text scrapy
#please install twisted (manaually) before install scrapy
#how to intall twisted: get *.whl and command with "pip install yourfilename.whl"
#get Unofficial Windows Binaries for Python Extension Packages from here http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

#for memrise format
from lxml import html
import requests 


# for user to read format
from lxml import etree
import html2text
import scrapy
import re

from multiprocessing.dummy import Pool as ThreadPool 

class onlineDict:
    def __init__(self,inFile,FileNameToSave):
        self.infile=inFile;
        self.setKeyBank();
        self.setFileNameToSave(FileNameToSave);
    def setFileNameToSave(self, FileNameToSave):
        self.FileNameToSave=self.infile+"_"+FileNameToSave+"_explain.txt";
    def set_url(self,url):
        self.url=url;
    def getPageContent(self):
        #print(self.url);
        page = requests.get(self.url);
        #print(page.text);
        #print(page.encoding);
        self.pageContent=page.content;
        return page;
    
    def parseToText(self):
        tree = html.fromstring(self.pageContent);
        explanations = tree.xpath(self.xpath);
        result="";
        for i in explanations:
            result.join(explanations.pop());
        result = ''.join(explanations);
        
        #print(result);
        return result;
    def parseToTextByhtmlToText(self):    
        pageTree = html.fromstring(self.pageContent);
        htmlstr="";

        page=self.getPageContent();
        hxs = scrapy.Selector(page);
        #sample = hxs.xpath("//*[@id='american-english-1-1-1']").extract()[0]
        sample = hxs.xpath("//*[@id='british-1-1-1']").extract()[0]
        
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        result=converter.handle(sample);
        #print(''.join(str(ord(c)) for c in result)); #show in ASCII format
        #print(result);
        return result;
             
    def setKeyBank(self):
        self.keybank = [line.strip() for line in open(infile+'.txt', 'r')];      
    
    def getVacabBank(self):
        return self.keybank;
       
    def writeToFile(self, vocabExplainations):
        target=open("./"+self.FileNameToSave,"w", encoding = 'UTF-8');

        for i in range(len(vocabExplainations)):
            print(i , vocabExplainations[i][0]);
            print(vocabExplainations[i][1]);
            target.write(vocabExplainations[i][0]);
            target.write(";");
            target.write(vocabExplainations[i][1]);
            target.write("\n");
  
        
class CambridgeDict(onlineDict):
    #def
#//*[@id="british-1-1-1"]/div[1]/div[2]/p/b
#//*[@id="british-1-1-1"]/div[1]/*/p/b

#//*[@id="american-english-1-1-1"]/div/div[1]/p/b 
#//*[@id="american-english-1-1-1"]/div/*/p/b
#example
#//*[@id="british-1-1-1"]/div[1]/div[1]/span/div[1]/span  
#//*[@id="british-1-1-1"]/div[1]/div[1]/span/div[2]/span 

#//*[@id="american-english-1-1-1"]/div[1]/div[1]/span/div[2]/span 
#//*[@id="american-english-1-1-1"]/div[1]/*/span

#def & example
#//*[@id="american-english-1-1-1"]/div/div[1]
#//*[@id="british-1-1-1"]/div/div[1]

#//*[@id="american-english-1-1-1"]/div[1]/*
    def __init__(self,inFile,FileNameToSave):
        super().__init__(infile,FileNameToSave);
        self.set_url('http://dictionary.cambridge.org/us/dictionary/english/');
        self.xpathOfDefinition="//*[@id='american-english-1-1-1']/div/*/p/b";
        self.xpathOfExample="//*[@id='american-english-1-1-1']/div[1]/*/span";
        
    def parseDefinitionToText(self):
        tree = html.fromstring(self.pageContent);
        explanations = tree.xpath(self.xpathOfDefinition);
        result=[];
        for i in explanations:
            result.append(i.text);
        print("definition=" );
        print( result);
        
    def parseExampleToText(self):
        tree = html.fromstring(self.pageContent);
        explanations = tree.xpath(self.xpathOfExample);
        result=[];
        '''
        result="";
        for i in explanations:
            result.join(explanations.pop());
        result = ''.join(explanations);
        print(result);
        '''
        for i in explanations:
            result.append(i.text);
        print("example=");
        print(result);        
    def parseToText(self):
        definition=self.parseDefinitionToText();
        examples=self.parseExampleToText();
        
    def set_url(self,vacab):
        self.url='http://dictionary.cambridge.org/us/dictionary/english/' + str(vacab);
    
    def parseToTextByhtmlToText(self):    
        raw_result=super(CambridgeDict,self).parseToTextByhtmlToText();
        result=self.HtmlToTextPostProcessing(raw_result);
        return result;
    
    def HtmlToTextPostProcessing(self,raw_result):
        print("============");
        result=re.sub(r" \*\*\n\n",'\n', str(raw_result));  
        result=re.sub(r" \*\*",'', str(result));        
        result=re.sub(r"\n\n",'\n', str(result));  
        #print(result);
        return result
    def spider(self,vacab): 
        mytext.set_url(vacab);
        mytext.getPageContent();
        print(vacab);
        result=mytext.parseToTextByhtmlToText();
        result=[vacab, result];

        return result;
    
class YahooDict(onlineDict):  
    def __init__(self,inFile,FileNameToSave):
        super().__init__(infile,FileNameToSave);
        self.xpath="//div[@id='main']/div/div/ol/li[2]//text()";
        self.url='https://tw.dictionary.yahoo.com/dictionary?p=';
    def set_url(self,vacab):
        self.url='https://tw.dictionary.yahoo.com/dictionary?p=' + str(vacab)+'&fr2=dict';
    def spider(self,vacab): 
        mytext.set_url(vacab);
        mytext.getPageContent();
        result=mytext.parseToText();
        result=[vacab, result];

        return result;
'''   
def fromYahooDict(vacab):
        qurl = 'https://tw.dictionary.yahoo.com/dictionary?p=' + str(vacab)+'&fr2=dict';
        #print(qurl);
        try:
            page = requests.get(qurl);
        except requestGetError:
            #print(page.status_code);
            print(page.text);
            #print(page.encoding);
        
        tree = html.fromstring(page.content);
        explanations = tree.xpath('//div[@id="main"]/div/div/ol/li[2]//text()');
        result="";
        for i in explanations:
            result.join(explanations.pop());
        result = ''.join(explanations);
        result=[vacab, result];
        #print(result);
        
        #print(result) #Python 3 print syntax
        return result;
'''

def multiprocess(parsefunc,vacabBank):
    # Make the Pool of workers
    pool = ThreadPool(3);

    # Open the urls in their own threads
    # and return the results
    results = pool.map(parsefunc , vacabBank);
    
    #close the pool and wait for the work to finish 
    pool.close();
    pool.join();
    return results;
  
def downloadPronciation():
    urllib.request.urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3");

     
if __name__ == "__main__":
    QueryDict = {
        'yahoo': YahooDict.parseToTextByhtmlToText,
        'cambridge':CambridgeDict.parseToTextByhtmlToText
    }
    infile='cam9';
    mytext=CambridgeDict(infile,'cam');
    vacabBank=mytext.getVacabBank();
    result=multiprocess(mytext.spider,vacabBank);
    mytext.writeToFile(result);
    '''         
    mytext=YahooDict(infile, 'yahoo');
    vacabBank=mytext.getVacabBank();
    result=multiprocess(mytext.spider,vacabBank);
    mytext.writeToFile(result);
    '''

    '''
    unit test
    mytext=YahooDict('https://tw.dictionary.yahoo.com/dictionary?p=');
    mytext.set_url('test');
    mytext.getPageContent();
    mytext.parseToText();
    '''

    
    '''
    mytext=CambridgeDict(infile,'cam');
    mytext.set_url('radically');
    mytext.getPageContent();
    result=mytext.parseToTextByhtmlToText();
    result=['stupid',  result];
    '''

    print(result);
    print("Job done");
        


