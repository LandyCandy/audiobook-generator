import requests
from urllib.parse import urlparse
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class RoyalRoadHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.class_name = "chapter-inner chapter-content"
        self.text_under_target_class = []
        self.inside_target_class = False
        
        self.button_name = "btn btn-primary col-xs-12"
        self.next_chapter_link = None

    def handle_starttag(self, tag, attrs):
        # Check if the tag has the desired class
        if any(attr[0] == 'class' and self.button_name in attr[1] for attr in attrs):
            for attr in attrs:
                if attr[0] == 'href':
                    self.next_chapter_link = attr[1]

        if any(attr[0] == 'class' and self.class_name in attr[1] for attr in attrs):
            self.target_tag = tag
            self.inside_target_class = True

    def handle_data(self, data):
        # If inside the target class, append the text
        if self.inside_target_class:
            self.text_under_target_class.append(data)

    def handle_endtag(self, tag):
        # Reset flag when leaving the target class
        if self.inside_target_class and tag == self.target_tag:
            self.inside_target_class = False

def parse_html(url_link, folder_path):
    base_url = 'https://www.royalroad.com'
    # Fetch HTML content
    url = base_url + url_link

    while url:
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.split('/')
        chapter_name = path_segments[-1]
        response = requests.get(url)
        html_content = response.text

        # Parse HTML
        parser = RoyalRoadHTMLParser()
        parser.feed(html_content)

        content = BeautifulSoup(html_content, 'html.parser')
        chapter_text = ""
        for div in content.findAll('div', attrs={'class': "chapter-inner chapter-content"}):
            chapter_text += div.text

        # Return the extracted text
        with open("%s/%s.txt" % (folder_path, chapter_name), 'x+', encoding="utf8") as a:
            a.writelines(chapter_text)

        if parser.next_chapter_link:
            url = base_url + parser.next_chapter_link
        else:
            url = None

if __name__ == "__main__":
    url_link = "/fiction/25225/delve/chapter/368012/001-woodland"
    folder_path = "./Delve"
    parse_html(url_link, folder_path)