"""
Extracting a list of all the links in the webpage

get_all_links
Input - a webpage,
Output - a list of links

index structure [keywordlist,urllist]
"""

"""
def popularity(timestep, person): #relaxation - start with a guess while not done
    if timestep==0:
        return 1
    score = 0
    for f in friends(p):
        score = score+popularity(timestep-1, person)
        return score
"""

def rank_web_pages(timestamp, url): #random web surfer that pick page randomly
    #all the pages that have some links to a url
    #/outgoinglinks[p]
    #weblink structures is a directed graph

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index: #storing urls
        index[keyword].append(url)
    else:
        #if not found add a new entry
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword] #return urls that contains the keyword
    return None

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {} #the result
    graph = {} #new page add to graph to create network contains url and pages that link to target

    while tocrawl:
        page = tocreawl.pop() #remove the element O(1)
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)

            #graph of a page associates with outlinks
            graph[page] = outlinks

            union(tocrawl, outlinks) #avoid duplication and dfs
            crawled.append(page)
    return index, graph


def get_next_target(page):
    start_link = page.find('<a href=')
    if not start_link:
        return None, 0
    start_quote = page.find('"', start_link) #start from beginning
    endquote = page.find('"', startquote + 1) #start searching after the first quote
    url = page[start_quote+1: end_quote] #everything in the quotation mark
    return url, end_quote

def get_all_links(page):
    collections = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            collections.append(url)
            page = page[endpos:] #next chunk
        else:
            break #no more urls
    print collections

