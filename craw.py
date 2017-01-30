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

#def rank_web_pages(timestamp, url): #random web surfer that pick page randomly
    #all the pages that have some links to a url
    #/outgoinglinks[p]
    #weblink structures is a directed graph
    #how it was ranked
    """
    d = damping constant 0.8
    N = number of pages
    rank(0, url) = 1/N
    rank(t, url) = d* sum of rank(t-1, p) where p in links[url] / outlinks[p]+ ((1-d)/N)
    """
def compute_ranks(graph):
    """
    input url, outlinks
    return dic of url and rankpoints
    """
    d = 0.8 #damping factor
    numloops = 10 #relaxation
    ranks = {}
    npages = len(graph) #N
    
    #initial rank
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(numloops):
        newranks = {}
        for page in graph: #for everypage
            #initialize with a probability of starting random
            newrank = (1-d) / npages
            #update the newrank by adding summation the inlink ranks
            for friend in graph:
                if page in graph[friend]: #if the page is a inlink of a friend
                    newrank += d * (ranks[friend]/len(graph[friend])) #damping factor*friend's initial rank/friend's npages/outlinks
            newranks[page] = newrank 
        ranks = newranks
    return ranks

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

def lookup_best(index, keyword, ranks):
    #finds the page that contains that keyword and return the best in the ranks
    pages = lookup(index, keyword) #pages with the keyword
    if not pages:
        return None

    best_page = pages[0]
    for page in pages:
        if ranks[page]>ranks[best_page]:
            best_page = page
    return best_page

def ordered_search(index, keyword, ranks):
    pages = lookup(index, keyword)
    return quicksort_by_rank(pages, ranks) #sort the pages by ranks descending

def quicksort_by_rank(pages, ranks):
    if not pages or len(pages)<=1: #sorted
        return pages
    pivot = ranks[pages[0]] #pick a comparison point
    left = [] #the smaller
    right = [] #the bigger
    for page in pages[1:]:
        if ranks[page]<=pivot:
            left.append(page)
        else:
            right.append(page)

    return quicksort_by_rank(right, ranks) + [pages[0]] + quicksort_by_rank(left, ranks)

def quicksort(arr):
    if not arr:
        return left, right
    pivot = arr[0]
    left = []
    right = []
    for q in arr:
        if q<pivot:
            left.append(q)
        else:
            right.append(q)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {} #the result
    graph = {} #new page add to graph to create network contains url and pages that link to target

    while tocrawl:
        page = tocrawl.pop() #remove the element O(1)

        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)

            #graph of a page associates with outlinks
            graph[page] = outlinks
            tocrawl = union(tocrawl, outlinks) #avoid duplication and dfs
            crawled.append(page)

    return index, graph

def union(tocrawl, outlinks):
    if outlinks:
        return list(set(tocrawl)|set(outlinks))
    return tocrawl

def get_next_target(page):
    start_link = page.find('<a href=')
    if not start_link:
        return None, 0
    start_quote = page.find('"', start_link) #start from beginning
    end_quote = page.find('"', start_quote + 1) #start searching after the first quote
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
    return collections

