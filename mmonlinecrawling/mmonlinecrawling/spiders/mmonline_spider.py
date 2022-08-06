import scrapy
import pandas as pd

last_item = ''
class mmSpider(scrapy.Spider):
    name = "mmonline"

    def start_requests(self):
        urls = [
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/thuc-pham-tuoi-song/','https://online.mmvietnam.com/danh-muc/mm-hiep-phu/do-an-che-bien/','https://online.mmvietnam.com/danh-muc/mm-hiep-phu/bo-trung-sua/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/thuc-pham-dong-lanh/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/dau-an-gia-vi-nuoc-cham/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/do-uong-cac-loai/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/do-hop-do-kho/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/banh-keo-cac-loai/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/cham-soc-ca-nhan/',
            'https://online.mmvietnam.com/danh-muc/mm-hiep-phu/ve-sinh-nha-cua/']
            
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        meta = {}
        curr_url = response.request.url
        meta['curr_url'] = curr_url
        items = response.xpath("//div[@class='products products-grid']/div[@class='row']/div/div[@class='product-block block-grid mm']")
        product_list = []
        meta = response.meta
        retries = meta.get('MISSING_RATINGS_RETRY_COUNT', 0)
        if retries < 5:
            throw_on_failure = True
        else:
            throw_on_failure = False
        try:
            for item in items:
                product_id = item.xpath("@data-product-id").get()
                product_name = item.xpath(".//h3/a/text()").get()
                display_price = item.xpath(".//div[@class='display-price']/span/bdi/text()").get()
                regular_price = item.xpath(".//div[@class='regular-price']/del/span/bdi/text()").get()
                currency = item.xpath(".//div[@class='display-price']/span/bdi/span/text()").get()
                uom = item.xpath(".//div[@class='display-price']/span/text()").get()
                item_link = item.xpath(".//h3/a/@href").get()
                item_imge_link  = item.xpath(".//div/figure[@class='image']/a/img/@data-src").get()
                product_list.append([product_id,product_name,display_price,regular_price,currency,uom,item_link,item_imge_link])
            next_page_url = response.xpath("//a[@class='next page-numbers']/@href").get()
            
            if next_page_url.split('/')[-2]=='2':
                df = pd.DataFrame(product_list,columns=['product_id','product_name','display_price','regular_price','currency','uom','item_link','item_imge_link'])
                df.to_csv('mm_data.csv',encoding='utf-8-sig')
            else:
                df = pd.DataFrame(product_list,columns=['product_id','product_name','display_price','regular_price','currency','uom','item_link','item_imge_link'])
                df.to_csv('mm_data.csv',mode='a',header=False,encoding='utf-8-sig')
            if next_page_url != None:
                yield scrapy.Request(next_page_url, callback=self.parse, meta = meta)
        except:
            next_page_url ="http://"+'/'.join(curr_url.split('//')[-1].split('/')[:-3])+"/page/"+str(int(curr_url.split('/')[-2])+1)+"/"
            yield scrapy.Request(next_page_url, callback=self.parse, meta=meta, dont_filter=True)