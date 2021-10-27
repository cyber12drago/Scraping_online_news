import scrapy
import datetime
from tribunnews.items import TribunnewsItem

class Covid19Spider(scrapy.Spider):
    name = 'covid-19'
    allowed_domains = ['tribunnews.com']
    start_urls = ['https://www.tribunnews.com/tag/covid-19?page=1']


    def parse(self, response):
       	
        pages = response.xpath('//*[@class="ptb15"]')

        for page in pages:
            links = page.xpath('.//a/@href').extract_first()+"?page=all"
            absolute_next_url = response.urljoin(links)
            yield scrapy.Request(absolute_next_url, callback=self.parse_artikel,  )
            
        cek_len= 45-len(response.url)

        if(int(response.url[cek_len:])+1<=575):
        	next_page_url = response.url[0:cek_len] + str(int(response.url[cek_len:]) +1)
        	absolute_next_page_url= response.urljoin(next_page_url)
        	yield scrapy.Request(absolute_next_page_url)
        else:
        	sys.exit()
        

    def parse_artikel(self, response):

        items = TribunnewsItem()
        title = response.xpath('//*[@class="f50 black2 f400 crimson"]/text()').extract_first()
        time = response.xpath('//*[@class="mt10"]/time/text()').extract_first()
        content_array = response.xpath('//*[@class="side-article txt-article"]/p/text()').extract()
        img_link=  response.xpath('//*[@class="imgfull"]/@src').extract_first()

        if(int(time.split()[1])<10):
        	day="0"+time.split()[1]
        else:
        	day=time.split()[1]

        if(time.split()[2]=="Mei"):
        	month_name="May"
        elif(time.split()[2]=="Agustus"):
        	month_name= "Aug"
        elif(time.split()[2]=="Oktober"):
        	month_name= "Oct"
        elif(time.split()[2]=="Desember"):
        	month_name= "Dec"
        else:
        	month_name= time.split()[2][:3]

        datetime_object = datetime.datetime.strptime(month_name, "%b")
        month_number = datetime_object.month

        if(month_number<10):
        	month="0"+ str(month_number)
        else:
        	month= str(month_number)
        	
        date = time.split()[3]+"-"+month+"-"+day
        content=""
        for i in range(len(content_array)):
        	content += content_array[i]+' '

        print(content)
        tag_array = response.xpath('//*[@class="tagcloud3"]/a/text()').extract()
        tag=""
        for i in range(len(tag_array)):
        	if(i!=len(tag_array)-1):
        		tag += tag_array[i]+', '
        	else:
        		tag += tag_array[i]


        items['link'] = response.url
        items['title'] = title
        items['date'] = date
        items['content'] = content
        items['tag'] = tag
        items['source'] = "tribunnews"
        items['img_link'] = img_link
        yield items
        return
        