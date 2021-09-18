import scrapy

class PszSpider(scrapy.Spider):
    name = "psz"
    start_urls = [
        # "https://www.nekretnine.rs/stambeni-objekti/kuce/lista/po-stranici",
        # "https://www.nekretnine.rs/stambeni-objekti/stanovi/lista/po-stranici",
        "https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/izdavanje/lista/po-stranici",
        "https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/prodaja/lista/po-stranici",
        "https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici",
        "https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici"
    ]

    def parse(self, response):

        nekretnine_links = response.css('h2.offer-title a::attr(href)')
        yield from response.follow_all(nekretnine_links, self.parse_nekretnina)

        pagination_links = response.css('a.next-article-button::attr(href)')
        yield from response.follow_all(pagination_links, self.parse) 
        # for stan in response.css('div.product-item'):
        #     yield {
        #         'adresa': stan.css('h3.product-title a::text').get()    
        #     }
            
    def parse_nekretnina(self, response):
        #response.xpath('//li[contains(text(), " Transakcija: ")]') 
        tip_nekretnine = response.url.split('/')[-4]
        stanje_nekretnine = '-'
        uknjizenost = 'Ne'
        godina_izgradnje = '-'
        povrsina_zemljista = '-' # samo za kuce
        ukupna_spratnost = '-' 
        broj_kupatila = '1'
      #  broj_soba = '-'
      
        
        for number in range(3,15):
            left =  response.xpath(f'//*[@id="detalji"]/div[1]/ul/li[{number}]/text()').get() if response.xpath(f'//*[@id="detalji"]/div[1]/ul/li[{number}]/text()').get() is not None else '-'
            if left == '-': break
            right = response.xpath(f'//*[@id="detalji"]/div[1]/ul/li[{number}]/strong/text()').get().strip() if response.xpath(f'//*[@id="detalji"]/div[1]/ul/li[{number}]/strong/text()').get() is not None else '-'
            if right == '-': break
            if 'Stanje' in left:
                stanje_nekretnine = right
                break
            elif 'Uknjiženo' in left:
                uknjizenost = right
                break
            elif 'Godina izgradnje' in left:
                godina_izgradnje = right
                break
            # elif 'soba' in left:
            #     broj_soba = right
            #     break
            elif 'Površina' in left:
                povrsina_zemljista = right
                break
            elif 'kupatila' in left:
                broj_kupatila = right
                break
        cena = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[3]/div/h4[1]/text()').get().strip() if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[3]/div/h4[1]/text()').get() is not None else '-'          
        tip_ponude =  response.xpath('//*[@id="detalji"]/div[1]/ul/li[1]/strong/text()').get().strip()
        grad = response.xpath('//*[@id="lokacija"]/div[1]/ul/li[3]/text()').get().strip() if response.xpath('//*[@id="lokacija"]/div[1]/ul/li[3]/text()').get() is not None else '-'
        deo_grada = response.xpath('//*[@id="lokacija"]/div[1]/ul/li[4]/text()').get().split('(')[0] if response.xpath('//*[@id="lokacija"]/div[1]/ul/li[4]/text()').get() is not None else '-'
        kvadratura = response.xpath('//*[@id="detalji"]/div[1]/ul/li[3]/strong/text()').get().split('m')[0].strip() if response.xpath('//*[@id="detalji"]/div[1]/ul/li[3]/strong/text()').get() is not None else '-'
        broj_soba = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[2]/span/text()').get().strip() if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[2]/span/text()').get() is not None else '-'
        grejanje = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[3]/span/text()').get().strip() if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[3]/span/text()').get() is not None else '-'
        parking = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[4]/span/text()').get().strip() if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[4]/span/text()').get() is not None else '-'
        # dodatno
        dodatno = response.xpath('//*[@id="detalji"]/div[2]/ul').get()
        terasa = 'Ne'
        lift = 'Ne'
        podrum = 'Ne'
        if dodatno is not None:
            if (('Terasa' in dodatno) or ('Balkon' in dodatno)):
                terasa = 'Da'
            if 'Lift' in dodatno:
                lift = 'Da'
            if 'Podrum' in dodatno:
                podrum = 'Da'

        if (tip_nekretnine == 'kuce'):
            yield {
                'tip_nekretnine': 'Kuca',
                'tip_ponude':  tip_ponude,
                'cena': cena,
                'grad': grad,
                'deo_grada': deo_grada,
                'kvadratura': kvadratura,
                'godina_izgradnje': godina_izgradnje,
                'povrsina_zemljista': povrsina_zemljista,
                'uknjizenost': uknjizenost,
                'stanje_nekretnine': stanje_nekretnine,
                'broj_kupatila': broj_kupatila,
                'broj_soba': broj_soba,
                'grejanje': grejanje,
                'parking': parking
            }
        elif (tip_nekretnine == 'stanovi'):
            sprat = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[5]/span/text()').get().split('/')[0].strip()  if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[5]/span/text()').get() is not None else '-' # samo za stanove
            ukupna_spratnost = response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[5]/span/text()').get().split('/')[1].strip() if response.xpath('/html/body/div[6]/div[7]/div/div[1]/div[4]/div/ul/li[5]/span/text()').get() is not None else '-' # samo za stanove
            yield {
                'tip_nekretnine': 'Stan',
                'tip_ponude':  tip_ponude,
                'cena': cena,
                'grad': grad,
                'deo_grada': deo_grada,
                'kvadratura': kvadratura,
                'godina_izgradnje': godina_izgradnje,
                'uknjizenost': uknjizenost,
                'stanje_nekretnine': stanje_nekretnine,
                'ukupna_spratnost': ukupna_spratnost,
                'sprat': sprat,
                'broj_kupatila': broj_kupatila,
                'broj_soba': broj_soba,
                'grejanje': grejanje,
                'parking': parking,
                'terasa' : terasa,
                'lift' : lift,
                'podrum' : podrum
            }
        
        