import requests
import re
from bs4 import BeautifulSoup

class BingSearch:

    def __init__(self, query):
        self.query = query
    
    def get_results(self, num, max_lines):
        
        self.num = num
        self.max_lines = max_lines
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        
        try:
            bing_url = "https://www.bing.com/search?&q=" + self.query.lower()
            result = requests.get(url=bing_url, headers=headers)
            soup = BeautifulSoup(result.text, 'html.parser')
            a_tags = soup.find_all('a', {"class": "b_widePag sb_bp"})
            a_pages = [bing_url] + ["https://www.bing.com" + a['href'] for a in a_tags]
            pg_url_list = []
            content_list = []

            for pg in a_pages:
                res = requests.get(url=pg, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                a_url_tags = soup.find_all('a', {"class": "tilk"})
                a_url_tags = [a['href'] for a in a_url_tags]
                for u in a_url_tags:
                    pg_url_list.append(u)
            i = 0
            for url_ in a_url_tags:
                content_list.append(self.get_content(url_, self.max_lines))
                if i == self.num:
                    break
                i = i + 1

            return content_list
        
        except Exception as e:
            return str(e)
    
    def get_content(self, url, max_lines):
        
        self.url = url    
        self.max_lines = max_lines
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        
        try:
            u_dict = {}
            r = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            p_tags = soup.find_all('p')
            p_text = []
            for p in p_tags:
                if len(p.text) > 20:
                    p_text.append(p.text)
            
            u_dict['url'] = self.url
            u_dict['title'] = soup.title.text
            u_dict['content'] = ('.').join(p_text[:self.max_lines])

            return u_dict
        
        except Exception as e:
            return str(e)
