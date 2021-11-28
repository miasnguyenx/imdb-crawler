from bs4 import BeautifulSoup
import requests

class Imdb_crawler:
    def crawl(self):
        print("How many movies: ")
        limit = int(input())
        genres = ("action", "comedy", "mystery", "sci_fi", "adventure",
                  "fantasy", "horror", "animation", "drama", "thriller")
        iteration = 1
        count = 0
        while count < limit:
            for genre in genres:
                if count > limit:
                    break
                soup = self.get_webpage(genre, iteration)
                if soup == None:
                    continue
                data = self.get_movie_data(soup)
                print(data)
            iteration += 1

    def get_movie_data(self, soup):
        data = []
        while tr_next:
            td = tr_next.contents[5]
            name = self.get_movie_name(td)
            year = self.get_movie_year(td)
            movie_id = self.get_movie_id(td)
            rating = self.get_movie_rating(td)
            users = self.get_movie_users(td)
            summary = self.get_movie_summary(td)
            genre = self.get_movie_genre(td)
            tr_next = tr_next.next_sibling.next_sibling
            data.append({'title': name, 'year': year, 'movie_id': movie_id,
                        'rating': rating, 'users': users, 'summary': summary, 'genre': genre})
        return data
   
    def get_webpage(self, genre, iteration):
        try:
            url = "http://www.imdb.com/search/title?at=0&genres="+genre+"&sort=moviemeter,asc&start="+str(iteration*50+1)+"&title_type=feature"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        except:
            print("COuld not open Url: ", self.url)


crawler = Imdb_crawler()
crawler.crawl()
