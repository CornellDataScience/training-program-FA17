from bs4 import BeautifulSoup
import requests

# Crawling http://www.datasciencecentral.com

ROOT = "http://www.datasciencecentral.com"

def crawl_site(n_articles=1000):
  """
  Crawls DataScienceCentral for a set of n articles.
  Returns a list of HTML documents.
  """
  articles = {}
  
  def dfs(url):
    if len(articles.keys()) > n_articles:
      return
    if url in articles:
      return
    soup = BeautifulSoup(
      requests.get(url)._content, 
      "lxml"
    )
    if url != ROOT:
      articles[url] = " ".join([div.text for div in soup.find_all("div", {"class": "postbody"})])
    post_links = [a for a in soup.find_all("a") if "href" in a.attrs and "profiles/blogs" in a["href"]]
    addrs = set([a["href"] for a in post_links])
    for addr in addrs:
      if addr[0] == "/":
        dfs("{}/{}".format(ROOT, addr))
      elif ROOT.replace("http://www.", "") in addr:
        dfs(addr)
      
  dfs(ROOT)
  return articles
  
articles = crawl_site()
f = open("articles.txt", "a")
for url in articles:
  article = articles[url]
  print "Writing {} to file".format(url)
  f.write(article.encode("utf8").replace("\n", " ") + "\n")
f.close()
