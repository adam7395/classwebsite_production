#class/views.py
from django.shortcuts import render
from announcements.models import Announcement
from urllib import request, parse
from bs4 import BeautifulSoup as BS

import re
from datetime import date, timedelta
import datetime

def index(request):

    #get the announcements
    announce_list = Announcement.objects.order_by('-date')
    print(len(announce_list))

    if request.method == 'POST':
        title = request.POST['title']
        announcement = request.POST['announcement']
        if isinstance( title, str) and isinstance(announcement, str) and len(title) < 100:
            announcement = Announcement.objects.create( title=title, message=announcement)


    announce_list = Announcement.objects.order_by('-date')
    print(len(announce_list))

    return render( request, 'class/index.html', context={"announcements": announce_list})




def about(request):
    return render( request, 'class/about.html')


def jobsearch(request):

    cb_list = []
    search_terms = []
    #li_list = []
    cl_list = []

    if request.POST:
        keywords, city, since = make_queries( request.POST)
        search_terms = [request.POST['keywords'], request.POST['city'], request.POST['fromage']]


        try:
            cb_list = scrape_career_builder( keywords, city, since)
        except:
            cb_list = []
        


        cl_list = scrape_craigslist( city, since )



    else:
        pass

    return render(request, 'class/jobs.html', {'search_terms': search_terms,  'cb_list': cb_list, 'cl_list': cl_list})

################################################################################
################################################################################
#                                                                              #
#                               internal functions
#                                                                              #
################################################################################
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"


def make_queries( query_dict ):

    #potential keys on the list
    keys = ['keywords', 'city', 'sci', 'hea', 'mnu', 'fromage']

    #parse the keywords
    try:
        keywords = query_dict['keywords']
    except:
        pass
    try:
        city = query_dict['city']
    except:
        pass
    try:
        since = query_dict['fromage']
        since = verify_since(since)
    except:
        since = verify_since()
    return keywords, city, since
    mylist = scrape_career_builder( keywords, city, since)



def scrape_career_builder( query, city, fromage):

    #parse, format, an
    query = query.lower().split()
    query = '-'.join(query)

    city = city.lower().split()
    city = '-'.join(city)

    #build the url-now parse the page
    base_url = 'http://www.careerbuilder.com/jobs-{0}-in-{1}?&posted={2}'.format( query, city, fromage)

    #scrape from the page
    req = request.Request( base_url, headers=headers)
    html = request.urlopen(req).read()
    soup = BS(html, 'html.parser')


    titles = []
    links =  []

    jobs = soup.find_all("h2", attrs={'class': 'job-title'})

    for job in jobs:
        try:
            link = job.find('a')
            link = 'http://www.careerbuilder.com/' + link['href']

            title = job.text
            titles.append(title)
            links.append(link)
        except:
            continue

    return [(t, l) for t, l in zip(titles, links)]


'''
Javascript rendered page
'''
def scrape_linkedin( query, city, fromage):

    #parse, format, an
    query = query.lower().split()
    query = '%20'.join(query)
    query.replace(',', '%2C')

    city = city.lower().split()
    city = '%20'.join(city)
    city.replace(',', '%2C')

    #build the url-now parse the page
    base_url = 'https://www.linkedin.com/jobs/search?keywords={0}&location={1}'.format( query, city)
    print(base_url)

    #scrape from the page
    req = request.Request( base_url, headers=headers)
    html = request.urlopen(req).read()
    soup = BS(html, 'html.parser')



    titles = []
    links =  []
    posted = []

    divs = soup.find_all("div")
    print(len(divs))

    for div in divs:

        link = job.find('a', attrs={"class": "job-title-link"})['href']
        print(len(link))
        print(link)

        '''
        title = job.text
        titles.append(title)
        links.append(link)
        '''


    return [(t, l) for t, l in zip(titles, links)]




















def scrape_indeed( query="software tester", city="san diego", since="7" ):

    query = query.lower().split()
    city = city.lower().split()


    #query = r'jobs?q=' + '+'.join(query) #Glue together job key words
    #city = r'&l=' + '+'.join(city) + '%2C+CA'
    #since = r'&fromage=' + since
    query = '+'.join(query)
    city = '+'.join(city)
    base_url = 'http://www.indeed.com/'
    base_url += 'jobs?as_and={0}&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l={1}'.format(query, city)
    base_url += '&fromage={0}&limit=50&sort=&psf=advsrch'.format(since)

    #scrape from the page
    req = request.Request( base_url, headers=headers)
    html = request.urlopen(req).read()
    soup = BS(html, 'lxml')




#scrape craigslist using search terms passed in
def scrape_craigslist( city, fromage ):

    queries = ['sof', 'web', 'sci', 'hea', 'mnu']
    city = city.lower().split()
    city = ''.join(city)

    jobs = []


    for query in queries:

        #open jobs page of craigslist category
        base_url = 'https://' + city + '.craigslist.org/'
        listview_url = base_url + 'search/' + query
        req = request.Request( listview_url, headers=headers)
        html = request.urlopen(req).read()
        soup = BS(html, 'html.parser')

        #find all jobs on a the list
        listitems = soup.findAll( 'li', attrs={"class":"result-row"} )
        print(len(listitems))
        for item in listitems:
            att = item.find('a', attrs={'class':'result-title hdrlnk'})
            link = base_url + att['href']
            title = att.text
            pdate = item.find('time')['datetime']

            pdate = list(map(int, pdate.split()[0].split('-')))
            today = date.today()
            post = date( *pdate )
            n = (today - post).days

            #set threshold for how many days of jobs to print
            if n > int(fromage):
                continue

            job = (title, link, query)
            jobs.append(job)

    return jobs

#make sure since is a number
def verify_since(since=7):
    try:
        i = int(since)
    except:
        i = 7
    return str(i)
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
