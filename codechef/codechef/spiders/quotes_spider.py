import scrapy
from ..items import CodechefItem
class QuoteSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = ['http://quotes.toscrape.com/']
	def parse(self, response):
		items = CodechefItem()
		div = response.css('div.quote')
		for quot in div:
			title = quot.css('span.text::text').extract()
			author = quot.css('.author::text').extract()
			tag = quot.css('.tag::text').extract()
			items['title'] = title
			items['author'] = author
			items['tag'] = tag
			yield items
		next_page = response.css("li.next a::attr(href)").get()
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)
