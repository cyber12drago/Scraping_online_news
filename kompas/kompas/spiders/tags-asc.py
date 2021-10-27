import scrapy
from kompas.items import KompasItem


class TagsSpider(scrapy.Spider):
    name = 'covid-19-asc'
    allowed_domains = ['kompas.com']
    start_urls = ['https://www.kompas.com/tag/covid-19?sort=asc&page=1']

    def parse(self, response):
       
        pages =response.xpath('//*[@class="article__list clearfix"]')

        for page in pages:
            links = page.xpath('.//*[@class="article__link"]/@href').extract_first()+"?page=all"
            absolute_next_url = response.urljoin(links)
            yield scrapy.Request(absolute_next_url, callback=self.parse_page,)
            

        cek_len= 50-len(response.url)

        if(int(response.url[cek_len:])+1<500):
            next_page_url = response.url[0:cek_len] + str(int(response.url[cek_len:]) +1)
            absolute_next_page_url= response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)
        else:
            sys.exit()
        
        

    def parse_page(self, response):

        items = KompasItem()
        title = response.xpath(
            '//*[@class="read__title"]/text()').extract_first()
        time = response.xpath('//*[@class="read__time"]/text()').extract_first().split()[2][:-1]
        article = response.xpath('//*[@class="read__content"]')
        content_array= article.xpath('//*/p/text()').extract()[1:-6]
        tag_array = response.xpath('//*[@class="tag__article__item"]/a/text()').extract()
        img_link_array=  response.xpath('//*/div/img/@src').extract()
        
        year=time[6:10]
        month=time[3:5]
        day=time[0:2]
        date=year+"-"+month+"-"+day

        img_link=""
        for img in img_link_array:
            if("/crops/" in img):
                img_link= img
                break;

        content=""
        for i in range(len(content_array)):
            for j in content_array[i].split():
                if("," in j[-1:]):
                    content += j[:-1]+" ,"+' '
                elif("." in j[-1:]):
                    content += j[:-1]+" ."+' '
                else:
                    content += j+' '

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
        items['source'] = "kompas"
        items['img_link'] = img_link

        yield items
        return
        