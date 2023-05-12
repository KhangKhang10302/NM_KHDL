import scrapy
import json

class collect_player_info(scrapy.Spider):
    name='players_info'
    def __init__(self):
        try:
            with open('D:/KHDL/fifa_crawler/fifa_crawler/dataset/players_urls.json') as f:
                self.players = json.load(f)
            self.player_count = 1

        except IOError:
            print("File not found")


    def start_requests(self):
        urls = ['https://sofifa.com/player/231747?units=mks']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        id = response.xpath("//li[9]/text()").extract()
        if id == []:
            id = response.xpath("//li[8]/text()").get()
        else:
            id = id[0]
        name = response.xpath("//div[1]//div//h1/text()").get()
        primary_position = response.xpath("//div[3]//div//div[1]//ul//li[1]//span/text()").get()
        positions = response.xpath('//div[@class="info"]//span/text()').extract()
        # #-----------------------------
        player_info = response.xpath("//div//div[@class='meta ellipsis']/text()").extract()
        player_info = [info for info in player_info if info != ' ']
        str = player_info[0].split()
        age = str[0].replace('y.o.', '')
        month = str[1].replace('(', '')
        day = (str[2].replace(',', ''))
        year = (str[3].replace(')', ''))
        height = int(str[4].replace('cm', ''))
        weight = int(str[5].replace('kg', ''))
        str = ""
        str = year + '/' + month + '/' + day
        # #-----------------------------
        OP = response.xpath("//div[@class='block-quarter']//div//span[1]/text()").re(r'[\w ]+')
        Overall_Rating = int(OP[0])
        Potential = int(OP[1])

        Value = response.xpath("//div[2]//div[1]//section//div[3]//div/text()").get()
        Wage = response.xpath("//div[2]//div[1]//section//div[4]//div/text()").get()
        Preferred_Foot = response.xpath("//div[2]//div//ul//li[1]/text()").get()
        Weak_Foot = int(response.xpath("//div[2]//div//ul//li[2]/text()").get())
        Skill_Moves = int(response.xpath("//div[2]//div//ul//li[3]/text()").get())
        International_Reputation = int(response.xpath("//div[2]//div//ul//li[4]/text()").get())
        Work_Rate = response.xpath("//div[2]//div//ul//li[5]//span/text()").get()
        Body_Type = response.xpath("//div[2]//div//ul//li[6]//span/text()").get()
        Real_Face = response.xpath("//div[2]//div//ul//li[7]//span/text()").get()
        Release_Clause = response.xpath("//div[2]//div//ul//li[8]//span/text()").extract()
        # # #-----------------------------
        team1 = response.xpath("//div[2]//div[4]//div//h5//a/text()").get()
        team2 = int(response.xpath("//div[4]//div//ul//li[1]//span/text()").get())
        team3 = response.xpath("//div[5]//div//h5//a/text()")
        team4 = int(response.xpath("//div[5]//div//ul//li[1]//span/text()").get())
        if team3 == []:
            teams = {team1:team2}
        else:
            teams = {team1:team2, team3.get():team4}
        # #-----------------------------
        at1 = response.xpath("//div[2]//div[3]//div//ul//li//span/text()").extract()
        attacking = {}
        ii = 0
        while(ii <= len(at1)-1):
            if at1[ii+1][0] == '+' or at1[ii+1][0] == '-':
                attacking.update( {at1[ii+2].replace(' ', ''):int(at1[ii])} )
                ii += 3
            else:
                attacking.update( {at1[ii+1].replace(' ', ''):int(at1[ii])} )
                ii += 2

        sk = response.xpath("//div[2]//div[4]//div//ul//li//span/text()").extract()
        skill = {}
        ii = 2
        while(ii <= len(sk)-1):
            if sk[ii+1][0] == '+' or sk[ii+1][0] == '-':
                skill.update( {sk[ii+2].replace(' ', ''):int(sk[ii])} )
                ii += 3
            else:
                skill.update( {sk[ii+1].replace(' ', ''):int(sk[ii])} )
                ii += 2
        
        mo = response.xpath("//div[2]//div[5]//div//ul//li//span/text()").extract()
        if team3 == []:
            ii = 0
        else:
            ii = 2

        movement = {}
        while(ii <= len(mo)-1):
            if mo[ii+1][0] == '+' or mo[ii+1][0] == '-':
                movement.update( {mo[ii+2].replace(' ', ''):int(mo[ii])} )
                ii += 3
            else:
                movement.update( {mo[ii+1].replace(' ', ''):int(mo[ii])} )
                ii += 2

        po = response.xpath("//div[6]//div//ul//li//span/text()").extract()
        power = {}
        ii = 0
        while(ii <= len(po)-1):
            if po[ii+1][0] == '+' or po[ii+1][0] == '-':
                power.update( {po[ii+2].replace(' ', ''):int(po[ii])} )
                ii += 3
            else:
                power.update( {po[ii+1].replace(' ', ''):int(po[ii])} )
                ii += 2

        men = response.xpath("//div[7]//div//ul//li//span/text()").extract()
        mentality = {}
        ii = 0
        while(ii <= len(men)-1):
            if men[ii+1][0] == '+' or men[ii+1][0] == '-':
                mentality.update( {men[ii+2].replace(' ', ''):int(men[ii])} )
                ii += 3
            else:
                mentality.update( {men[ii+1].replace(' ', ''):int(men[ii])} )
                ii += 2

        de = response.xpath("//div[8]//div//ul//li//span/text()").extract()
        defending = {}
        ii = 0
        while(ii <= len(de)-1):
            if de[ii+1][0] == '+' or de[ii+1][0] == '-':
                defending.update( {de[ii+2].replace(' ', ''):int(de[ii])} )
                ii += 3
            else:
                defending.update( {de[ii+1].replace(' ', ''):int(de[ii])} )
                ii += 2

        go = response.xpath("//div[9]//div//ul//li//span/text()").extract()
        goalkeeping = {}
        ii = 0
        while(ii <= len(go)-1):
            if go[ii+1][0] == '+' or go[ii+1][0] == '-':
                goalkeeping.update( {go[ii+2].replace(' ', ''):int(go[ii])} )
                ii += 3
            else:
                goalkeeping.update( {go[ii+1].replace(' ', ''):int(go[ii])} )
                ii += 2

        # #-----------------------------
        player_traits = response.xpath("//div[10]//div//ul//li//span/text()").extract()
        player_specialities = response.xpath("//div[3]//div//ul//li//a/text()").extract()
        if Release_Clause != []:
            yield {
                'id': id,
                'name': name,
                'primary_position': primary_position,
                'positions': positions,
                'age': age,
                'birth_date': str, 
                'height': height,
                'weight': weight,
                'Overall Rating': Overall_Rating,
                'Potential': Potential,
                'Value': Value,
                'Wage': Wage,
                'Preferred Foot': Preferred_Foot,
                'Weak Foot': Weak_Foot,
                'Skill Moves': Skill_Moves,
                'International Reputation': International_Reputation,
                'Work Rate': Work_Rate,
                'Body Type': Body_Type,
                'Real Face': Real_Face,
                'Release Clause': Release_Clause[0],
                'teams': teams,
                'attacking': attacking,
                'skill': skill,
                'movement': movement,
                'power': power,
                'mentality': mentality,
                'defending': defending,
                'goalkeeping':goalkeeping,
                'player_traits': player_traits,
                'player_specialities': player_specialities,
        }
        else:
            yield {
                'id': id,
                'name': name,
                'primary_position': primary_position,
                'positions': positions,
                'age': age,
                'birth_date': str, 
                'height': height,
                'weight': weight,
                'Overall Rating': Overall_Rating,
                'Potential': Potential,
                'Value': Value,
                'Wage': Wage,
                'Preferred Foot': Preferred_Foot,
                'Weak Foot': Weak_Foot,
                'Skill Moves': Skill_Moves,
                'International Reputation': International_Reputation,
                'Work Rate': Work_Rate,
                'Body Type': Body_Type,
                'Real Face': Real_Face,
                'teams': teams,
                'attacking': attacking,
                'skill': skill,
                'movement': movement,
                'power': power,
                'mentality': mentality,
                'defending': defending,
                'goalkeeping':goalkeeping,
                'player_traits': player_traits,
                'player_specialities': player_specialities,
            }
        if self.player_count < len(self.players):
            next_page_url = 'https://sofifa.com' + self.players[self.player_count]['player_url'] + '?units=mks'
            self.player_count += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse) 
    