import requests
import os
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from celery import Celery
from celery.schedules import crontab
     
app = Celery('blogs')

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'blogs.download_blogs', 
        'schedule': crontab(),
    #     'schedule': crontab(minute=0, hour=0)
    #     'schedule': crontab(minute='*/15')
    },
}
 
  
def download_blog_from_xml(dir, url, xmldoc, utf):
    if not os.path.exists(dir):
    		os.makedirs(dir)    
    try:
        output_file = dir
        files = os.listdir(dir)
        if xmldoc:
            var_url = urlopen(url)
            xmldoc = parse(var_url)
            for item in xmldoc.iterfind('channel/item'):
                title = item.findtext('title')
                title = title.replace('?', ' ')
                title = title.replace(':', ' ')
                num = 0        
                for x in files:
                    x = x[:-5]
                    if title == x:
                        num+=1
                    else:
                        num == 0

                if num == 0:
                    date = item.findtext('pubDate')
                    link = item.findtext('link')

                    print(title)
                    print(date)
                    print(link)
                    print()
                    if utf:
                            cache_filename = ''
                            response = requests.get(link)
                            cache_filename = '{}/{}.html'.format(output_file, title)
                            with open(cache_filename, mode='w', encoding='utf-8') as cache:
                                cache.write(response.text)
                    else: 
                            # Fetch header first to get check content type
                            response = requests.head(link)
                            # Content type can contain encoding information after a semi-colon (`;`)
                            content_type = response.headers.get('Content-Type').split(';')[0]

                            if content_type == 'text/html':
                                response = urllib.request.urlopen(link)
                                webContent = response.read()
                                f = open('{}/{}.html'.format(output_file, title), 'wb')
                                f.write(webContent)
                                f.close

        else: 
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features='xml')
            articles = soup.findAll('item')
            for a in articles:
                title = a.find('title').text
                title = title.replace('?', ' ')
                title = title.replace(':', ' ')
                num = 0        
                for x in files:
                    x = x[:-5]
                    if title == x:
                        num+=1
                    else:
                        num == 0

                if num == 0:
                    link = a.find('link').text
                    date = a.find('pubDate').text

                    print(title)
                    print(date)
                    print(link)
                    print()

                    if utf:
                            cache_filename = ''
                            response = requests.get(link)
                            cache_filename = '{}/{}.html'.format(output_file, title)
                            with open(cache_filename, mode='w', encoding='utf-8') as cache:
                                cache.write(response.text)
                    else: 
                            # Fetch header first to get check content type
                            response = requests.head(link)
                            # Content type can contain encoding information after a semi-colon (`;`), which we're not interested in
                            content_type = response.headers.get('Content-Type').split(';')[0]

                            if content_type == 'text/html':
                                response = urllib.request.urlopen(link)
                                webContent = response.read()
                                f = open('{}/{}.html'.format(output_file, title), 'wb')
                                f.write(webContent)
                                f.close            
                
    except Exception as e:
        print('Error. See exception:')
        print(e) 
        
          
@app.blogs         
def download_blogs():

	article ={1:{
		        'title': 'Starting: ThreatPost' ,
		        'dir': r'/home/praneeth/Documents/blog-down/ThreatPost' ,
		        'link': 'https://threatpost.com/feed/',
		        'xmldoc': False,
		        'utf': False,
		        'update': 'Updated: ThreatPost'
		        }, 
		  2: {
		        'title': 'Starting: Zdnet' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Zero Day' ,
		        'link': 'https://www.zdnet.com/blog/rss.xml',
		        'xmldoc': True,
		        'utf': False,
		        'update': 'Updated: Zdnet'
		        },
		  3: {
		        'title': 'Starting: NakedSecurity' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Naked Security' ,
		        'link': 'https://nakedsecurity.sophos.com/feed/',
		        'xmldoc': True,
		        'utf': False,
		        'update': 'Updated: NakedSecurity'
		        },
		  4: {
		        'title': 'Starting: DarkReading' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Dark Reading' ,
		        'link': 'https://www.darkreading.com/rss_simple.asp?f_n=659&f_ln=Threat%20Intelligence',
		        'xmldoc': False,
		        'utf': True,
		        'update': 'Updated: DarkReading'
		        },
		  5: {
		        'title': 'Starting: GrahamCluley' ,
		        'dir': r'/home/praneeth/Documents/blog-down/GrahamCluley' ,
		        'link': 'https://grahamcluley.com/feed/',
		        'xmldoc': False,
		        'utf': True,
		        'update': 'Updated: GrahamCluley'
		        },
		  6: {
		        'title': 'Starting: TechNewsWorld' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Tech News World' ,
		        'link': 'https://www.technewsworld.com/perl/syndication/rssfull.pl?__hstc=67659214.41033b4a8973e2312a56265f9f08be64.1623167946568.1623167946568.1623167946568.1&__hssc=67659214.2.1623167946570&__hsfp=4264810217',
		        'xmldoc': True,
		        'utf': False,
		        'update': 'Updated: TechNewsWorld'
		        },
		  7: {
		        'title': 'Starting: The Hacker News' ,
		        'dir': r'/home/praneeth/Documents/blog-down/The Hacker News' ,
		        'link': 'https://feeds.feedburner.com/TheHackersNews',
		        'xmldoc': True,
		        'utf': False,
		        'update': 'Updated: The Hacker News'
		        },
		  8: {
		        'title': 'Starting: Information Security Buzz' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Information Security Buzz' ,
		        'link': 'https://feeds.feedburner.com/InformationSecurityBuzz',
		        'xmldoc': True,
		        'utf': False,
		        'update': 'Updated: Information Security Buzz'
		        },
		  9: {
		        'title': 'Starting: Krebs on Security' ,
		        'dir': r'/home/praneeth/Documents/blog-down/Krebs on Security' ,
		        'link': 'https://krebsonsecurity.com/feed/',
		        'xmldoc': False,
		        'utf': True,
		        'update': 'Updated: Krebs on Security'
		        }
		 }   
		 
	for i in range(1,10):
		print(article[i]['title']) 
		print()
		download_blog_from_xml(article[i]['dir'], article[i]['link'], article[i]['xmldoc'], article[i]['utf'])
		print(article[i]['update'])
		print()
		 
          
download_blogs()
