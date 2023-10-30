# The below code is Python class called `BingSearch` that allows you to perform a Bing search and retrieve the search results.
import requests
import re
from bs4 import BeautifulSoup

# The BingSearch class is used to perform searches on the Bing search engine.
class BingSearch:

    def __init__(self, query):
        self.query = query
    
    def get_results(self, num, max_lines):
        """
        The `get_results` function retrieves search results from Bing based on a given query and returns
        the content of the web pages up to a specified maximum number of lines.
        
        :param num: The `num` parameter specifies the number of search results to retrieve. It
        determines how many search results will be fetched and returned in the `content_list`
        :param max_lines: The `max_lines` parameter specifies the maximum number of lines of content to
        retrieve from each URL
        :return: a list of content.
        """
        
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
        """
        The `get_content` function takes a URL and a maximum number of lines as input, retrieves the
        content from the URL, and returns a dictionary containing the URL, title, and a truncated
        version of the content.
        
        :param url: The URL of the webpage you want to scrape the content from
        :param max_lines: The `max_lines` parameter is the maximum number of lines of content that you
        want to retrieve from the webpage
        :return: a dictionary `u_dict` containing the URL, title, and content of the webpage. If there
        is an exception, it will return the error message as a string.
        """
        
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
