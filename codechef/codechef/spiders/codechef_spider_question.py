import scrapy
class CodechefSpider(scrapy.Spider):
	name = 'codechef'
	url_base = 'https://www.codechef.com/'
	url_chlng = 'MAY20B/'
	url_status = "status/"
	url_prblm = "CORUS"
	url_ac = "?sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO"
	url = url_base+url_chlng+url_status+url_prblm+url_ac
	start_urls = [url]
	def parse(self, response):
		table = response.css('.dataTable tbody tr')
		for tr in table:
			user = tr.css('td[width="144"] a span[class!="rating"]::text').get()
			score = tr.css('td.centered span::text').get()
			rating = tr.css('td[width="144"] a span[class="rating"]::text').get()
			if user is None:
				user = tr.css('td[width="144"] a::text').get()
				rating = "unrated"
			if score=='100':
				yield {"user: ": user, "rating: ": rating, "score: ": score}
		next_page = response.css('table[align="center"] td[align="right"] a.active::attr(href)').get()
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)
