from googlesearch import search
import trafilatura
import concurrent.futures

def search_top(keyword):
    results = search(keyword, num_results=1)
    return list(results)

def check_domains(top_website, domains =['twitter.com', 'instagram.com', 'youtube.com', 'linkedin.com']):
    for website in top_website:
        for domain in domains:
            if domain in website:
                return None
    return top_website


def blogtext(url):
    def fetch_and_extract(url):
        downloaded = trafilatura.fetch_url(url)
        result = trafilatura.extract(downloaded, include_comments=False, include_tables=True, no_fallback=True)
        return result

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_and_extract, url)
        try:
            result = future.result(timeout=8)
            return result
        except concurrent.futures.TimeoutError:
            return None


def get_article(keyword):
    url = search_top(keyword)
    filter_url = check_domains(url)
    if filter_url is not None and filter_url != []:
        article = blogtext(filter_url[0])
        if article is not None and article != 'close':
            article= article
        else:
            article = None
    else:
        article = None
    if filter_url is not None and filter_url != []:
        filter_url = filter_url[0]
    else:   
        filter_url = None
    return article , filter_url

def get_competitors_article(url):
    article = blogtext(url)
    if article is not None and article != 'close':
            article= article
    else:
            article = None

    return article , url


if __name__ == '__main__':
    print(blogtext('Video | Automobile Industry in Vijayawada Appeals For Reduction In GST'))







