import requests
import urllib.request


class ApiError(object, Exception):
    pass


def get_category(category):
    category_url = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:' + category + '&cmlimit=max&format=json'
    resp = requests.get(category_url)
    if resp.status_code != 200:
        raise ApiError("Get category error " + str(resp.status_code))

    # print(resp.json())
    # return list(map(lambda x: x['pageid'], resp.json()['query']['categorymembers']))
    return [x['pageid'] for x in resp.json()['query']['categorymembers']]


def get_single_urls_part(pageids):
    # print(pageids)
    ids = '|'.join(map(str, pageids))
    article_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=info&pageids=' + str(
        ids) + '&inprop=url&format=json'
    resp = requests.get(article_url)
    if resp.status_code != 200:
        raise ApiError("Get page urls error " + str(resp.status_code))
    if 'query' not in resp.json().keys():
        return []
    print(resp.json())
    pages = resp.json()['query']['pages']
    # print(x[1]['fullurl'] for x in pages.items())
    return [x[1]['fullurl'] for x in pages.items()]


def get_urls(pageids):
    res = []
    i = 0
    while i * 49 + 49 < len(pageids):
        res += get_single_urls_part(pageids[(i * 49): (i * 49 + 49)])
        i += 1
    return res + get_single_urls_part(pageids[i*49:])


def download_pages(urls, folder=None):
    for url in urls:
        page = urllib.request.urlopen(url).read()
        file_name = ((folder + '/') if folder is not None else '') + url.split('/')[-1]
        print(file_name)
        with open(file_name, 'wb+') as file:
            file.write(page)


if __name__ == '__main__':
    category = 'Electronics'
    pageids = get_category(category)
    # print(pageids)
    urls = get_urls(pageids)
    # print(urls)
    download_pages(urls, 'wiki')
