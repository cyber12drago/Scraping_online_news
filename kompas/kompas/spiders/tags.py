import scrapy
from kompas.items import KompasItem


class TagsSpider(scrapy.Spider):
    name = 'covid-19-desc'
    allowed_domains = ['kompas.com']
    start_urls = ['https://www.kompas.com/tag/Covid-19?sort=desc&page=1']

    def parse(self, response):
       
        pages =response.xpath('//*[@class="article__list clearfix"]')

        for page in pages:
            links = page.xpath('.//*[@class="article__link"]/@href').extract_first()+"?page=all"
            absolute_next_url = response.urljoin(links)
            yield scrapy.Request(absolute_next_url, callback=self.parse_page,)
            

        cek_len= 51-len(response.url)

        if(int(response.url[cek_len:])+1<=500):
            next_page_url = response.url[0:cek_len] + str(int(response.url[cek_len:]) +1)
            absolute_next_page_url= response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)
        else:
            sys.exit()
        
    def parse_page(self, response):

        items = KompasItem()
        judul = response.xpath(
            '//*[@class="read__title"]/text()').extract_first()
        waktu = response.xpath('//*[@class="read__time"]/text()').extract_first().split()[2][:-1]
        artikel = response.xpath('//*[@class="read__content"]')
        konten_array= artikel.xpath('//*/p/text()').extract()[1:-6]
        tag_array = response.xpath('//*[@class="tag__article__item"]/a/text()').extract()
        link = response.url
        gambar_link_array=  response.xpath('//*/div/img/@src').extract()
        
        tahun=waktu[6:10]
        bulan=waktu[3:5]
        hari=waktu[0:2]
        tanggal=tahun+"-"+bulan+"-"+hari

        gambar_link=""
        for img in gambar_link_array:
            if("/crops/" in img):
                gambar_link= img
                break;

        konten=""
        for i in range(len(konten_array)):
            for j in konten_array[i].split():
                konten += j+' '

        tag=""
        for i in range(len(tag_array)):
            if(i!=len(tag_array)-1):
                tag += tag_array[i]+', '
            else:
                tag += tag_array[i]

        items['link'] = link
        items['title'] = judul
        items['date'] = tanggal
        items['content'] = konten
        items['tag'] = tag
        items['source'] = "kompas"
        items['img_link'] = gambar_link

        yield items
        return
        