import scrapy
from scrapy.crawler import CrawlerProcess



class Nderf(scrapy.Spider):
    name = "nderf_spider"
    start_urls = ['https://www.nderf.org/Archives/archivelist.htm']


    def parse(self, response):
        for archive in response.xpath("//a[contains(@href, '/Archives/')]/@href").getall():
            yield scrapy.Request(url=archive, callback=self.parse_archive)


    def parse_archive(self, response):
        for experience in response.xpath("//a[contains(@href, '/Experiences/')]/@href").getall():
            yield scrapy.Request(url=experience, callback=self.parse_experience)


    def parse_experience(self, response):
        item = {
            "Source": response.url,
            "Name": response.xpath("//h1/strong/text()").get(),
            "NDE type": response.xpath("//ul[@class='hr_list d_inline_m breadcrumbs']/li[2]/a/text()").get(),
            "ID": response.xpath("//ul[@class='hr_list d_inline_m breadcrumbs']/li[3]/a/text()").get(),
            "Story": " ".join(response.xpath("//section[@class='section_offset']//text()").getall()).strip().lower()
        }
        item['Story'] = item['Story'].split("background information:")[0] \
            .replace("\r",'') \
            .replace('\n','') \
            .replace("\t",' ') \
            .replace("  ",' ') \
            .strip() if item['Story'] else item['Story']
        return item



crawler = CrawlerProcess(settings={
    "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "DOWNLOAD_DELAY": 0.5,
    "FEEDS": {"archives.json":{"format": "json", 'encoding': 'utf8'}}
})
crawler.crawl(Nderf)
crawler.start()