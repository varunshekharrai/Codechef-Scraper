import scrapy
import json
class CodechefSpider(scrapy.Spider):
	name = 'codechef_challenge'
	url_base = 'https://www.codechef.com/'
	url_chlng = 'MAY20B/'
	url = url_base+url_chlng
	start_urls = [url]
	headers = {
		"Host": "www.codechef.com",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"x-csrf-token": "b31e4ff3a11ede401a4f4c2f98c6c79c",
		"X-Requested-With": "XMLHttpRequest",
		"DNT": "1",
		"Connection": "keep-alive",
		"Referer": "https://www.codechef.com/MAY20B?order=desc&sortBy=successful_submissions",
		"Cookie": "AWSALB=RGAPB33B6yspV6dwEhULg+2uLqzSWb8aIR4wDzUdXPQJGKgeQrMDeA0at7f37+pSLsNUItT/rYzcC072Ze0Z7y40xr6Cd8zapIKRBgqLFeyTxLPfE/LqU38qLJuN; AWSALBCORS=RGAPB33B6yspV6dwEhULg+2uLqzSWb8aIR4wDzUdXPQJGKgeQrMDeA0at7f37+pSLsNUItT/rYzcC072Ze0Z7y40xr6Cd8zapIKRBgqLFeyTxLPfE/LqU38qLJuN; SESS93b6022d778ee317bf48f7dbffe03173=6f926f110eecb4c5bc0a05f29107564f; _gcl_au=1.1.787182149.1588752206; mtc_id=2049030; mtc_sid=moonfbacewtnkgkol5do8k8; mautic_device_id=moonfbacewtnkgkol5do8k8; poll_time=1588753901733; __asc=f0b7ed38171e915dc94a81d7805; __auc=f0b7ed38171e915dc94a81d7805; notification=0; userkey=2e198e92cd752939a9c91aede6b89538",
		"TE": "Trailers"
	}
	list_problem = []
	current_problem = 0
	prblm_id = {}
	page_count = 1
	def parse(self, response):
		url = 'https://www.codechef.com/api/contests/MAY20B?v=1513415675531'
		yield scrapy.Request(url, callback=self.parse_api, headers=self.headers)
	def parse_api(self, response):
		raw_data = response.body
		data = json.loads(raw_data)
		problem = data['problems']
		for x in problem:
			if problem[x]['category_name']=='main' and problem[x]['type']!='2':
				self.list_problem.append(x)
				self.prblm_id[x] = {}
		url_status = "status/"
		url_ac = "?sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO"
		url = self.url_base+self.url_chlng+url_status+self.list_problem[self.current_problem]+url_ac
		self.current_problem += 1
		yield scrapy.Request(url, callback=self.parse_problem)
	def parse_problem(self, response):
		code = response.css('div.content-wrapper h2.color a::text').get()
		table = response.css('.dataTable tbody tr')
		for tr in table:
			user = tr.css('td[width="144"] a span[class!="rating"]::text').get()
			score = tr.css('td.centered span::text').get()
			rating = tr.css('td[width="144"] a span[class="rating"]::text').get()
			if user is None:
				user = tr.css('td[width="144"] a::text').get()
				rating = "unrated"
			if user is None:
				user = response.css('body').extract()
				rating = 'unrated'
				score = '100'
			if score=='100':
				self.prblm_id[code][user] = {"rating: ": rating, "score: ": score}
		next_page = response.css('table[align="center"] td[align="right"] a.active::attr(href)').get()
		if next_page is not None and self.page_count<=2:
			yield response.follow(next_page, callback=self.parse_problem)
			self.page_count += 1
		elif self.current_problem < len(self.list_problem):
			url_status = "status/"
			url_ac = "?sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO"
			url = self.url_base+self.url_chlng+url_status+self.list_problem[self.current_problem]+url_ac
			self.current_problem += 1
			self.page_count = 1
			yield response.follow(url, callback=self.parse_problem)
		elif self.current_problem == len(self.list_problem):
			yield self.prblm_id
