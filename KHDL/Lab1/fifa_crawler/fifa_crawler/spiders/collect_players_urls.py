import scrapy

class collect_player_url(scrapy.Spider):
    name = 'players_urls'
    def start_requests(self):
        urls = []
        self.count = 0
        urls = ['https://sofifa.com/players?col=oa&sort=desc&offset=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        players = response.xpath("//td[@class='col-avatar']//figure/img")
        for player in players :
            id = player.xpath(".//@id").get()
            player_url = "/player/" + id
            yield {
                'player_url': player_url,
            }
        if self.count < 660 :
            self.count += 60
            next_page_url = 'https://sofifa.com/players?col=oa&sort=desc&offset=' + str(self.count)
            yield scrapy.Request(url=next_page_url, callback=self.parse)