# coding=gbk
from scrapy.spiders import Spider  
from scrapy.selector import Selector  
import scrapy
#from scrapy import log  
  
from appstore.items import appstoreItem  
  
  
class appstoreSpider(Spider):  
   
    name = "appstore"  
    #allowed_domains = ["www.apple.com"]#���������ʵֻ����Ϊһ�����ƣ��ǵ���ȡ�Ĺ��������е�url������������¡�Ҳ����û��������ơ�������ǰ���ע�͵���
    start_urls = [  
        "http://ourex.lib.sjtu.edu.cn/primo_library/libweb/action/search.do?dscnt=0&dstmp=1462803572893&searchField=callnumber&fn=BrowseRedirect&vid=chinese&searchTxt="  
    ]  #���ǿ�ʼ����ҳ��ַ������ͼ���˼Դ����µİ�����������
    
    #���ǵ������е�㸴�ƣ������漰����һҳ��ת�����⣬Ȼ��Ϊ�˻�ȡÿ����Ŀ����Ϣ����Ҫ���ȥ���ӣ���������һ������ÿ����������ù��ܾͺ�������ء�
  	#����֮ǰ����������˵һ��֩����߼��ɡ�
  	#ÿ��֩�붼��һ������Ȼ���Բ�ֹһ��start_url��������һ����֩�룬֩��ͻ�����������ڣ�Ȼ����һ����ҳ
  	#���ǰ������ҳ�����һ��html�ļ��Ϳ����ˡ�����ļ��أ��ᱻĬ�ϴ���prase������Ҳ�����������������
    def parse(self, response): #�����spider����Ĭ�ϵķ�����������һ����д��response�����Ǹ�html�ļ�Ŷ��
  
        sel = Selector(response)#��html���ļ���ת������һ��Selector��ѡ����������Ŷ���������ĺô��ǣ����Խ���xpath����css��
        #sel��һ��ѡ����Ŷ�����Ǿͺܷ���ʹ��xpathȥ��ȡһЩ���ݡ���ʱ���أ����ǻ�ȡ�Ļ���һ������list����Ϊ���·������Ҳ����кܶಢ�У�ͬһ��level����Ŀ����       
        sites = sel.xpath('//*[@id="exlidBrowseResultsEnteries"]/tbody/tr/td/a/@href').extract()  
        #�����أ����ǰ����List��һ����������������أ��ͻ�ȡ��ĳһҳ25���������Ŷ�������û����xpath������Ŷ��
        #����xpath��ȥ��֮ǰ��һƪ���¿�һ�°�http://blog.csdn.net/qtlyx/article/details/51036437
        for siteUrl in sites:  
            siteUrl = "http://ourex.lib.sjtu.edu.cn/primo_library/libweb/action/"+siteUrl
            #��ȡ���鱾����ô���أ���Ȼ�ǵ��ȥ�����������yield�ˡ�yield��ʲô�أ���ʱ��������return�Ϳ����ˣ��Ժ�д������˵��һ������return������
            #siteUrl��ÿ�����Ӧ������Ŷ�����Ա���ȡһ�������Ӿͻ�ִ��һ�����������䣬���������һ��callback
            #��������˼�أ����ǣ���Requestһ��siteUrl������ӣ���Request�Ľ�������������� parse_dir_contents �������
            #���ֵ�ĳ�����鷢�����������������ĺ��������ǽ����ص��������������ڼ����������档
            #��Request��ʲô��?�������ɵ���һ�����ӻ�õ�html�ļ��ɡ�Ȼ��ȥ��һ��parse_dir_contents�����ɡ�
            yield scrapy.Request(siteUrl, callback=self.parse_dir_contents)
        
        #������ÿһ�����Ŀ¼�������ӽ����ص�����֮�����ǵ�Ŀ�ľ����Զ���ȡ��һҳ�������ˡ�
        #�ⲿ�ֿɱ�����򵥣�ͬѧ���Լ�����ҳ��xpath��һ�°ɡ�
        #next page  
        urls = sel.xpath('id("resultsNavNoIddown")/a/@href').extract()
        for url in urls:
            #print url
            url = "http://ourex.lib.sjtu.edu.cn/primo_library/libweb/action/" + url
            #print url
            yield scrapy.Request(url, callback=self.parse)
            
    #����һ���ص���������Ĳ����ˣ�������ص��������棬�ֻص���һ������û��������һ�ָо���û���ȥһ��ҳ�棬
    #�Ͷ�һ���ص���������ʵ���������ġ��м�������Ǿͻ��ж��ٸ��ص�������        
    def parse_dir_contents(self, response):
        sel = Selector(response)
        inUrls = sel.xpath('//*[@id="exlidResult0-LocationsTab"]/a/@href').extract()
        for url in inUrls:
            url = "http://ourex.lib.sjtu.edu.cn/primo_library/libweb/action/" + url
            print "test url"+url
            yield scrapy.Request(url, callback=self.parse_req)
    
    def parse_req(self, response):   
        sel = Selector(response)
    		#sites = sel.xpath('id('locationsTable0')/x:tbody/x:tr[3]/x:td/x:ul/x:li[2]')
        #for site in sel:
        item = appstoreItem() 
        status = sel.xpath('//*[@id="locationsTable0"]//tr[3]/td/ul/li[2]/text()').extract()
        #status = sel.xpath('//*[@id="exlidResult-1-TabContent"]/div[2]/div/span[1]/span/text()').extract()
        print "lyx status is" + str(status)
        name = sel.xpath('//*[@id="resultsListNoId"]/div[1]/div[1]/div/h1/text()').extract() 
            
        item['status'] = [t.encode('utf-8') for t in status]  
        item['name'] = [l.encode('utf-8') for l in name]  
            
        yield item
   
  
        #log.msg("Append done.",level='INFO')  
        #return items  
        