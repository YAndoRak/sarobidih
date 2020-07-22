import requests
from bs4 import BeautifulSoup
import time
from youtubesearchpython import SearchVideos




USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def scrape_youtube(search_term):
    assert isinstance(search_term, str), 'Search term must be a string'
    escaped_search_term = search_term.replace(' ', '+')
    search = SearchVideos(escaped_search_term, offset=1, mode="dict", max_results=10)

    return search.result()

def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results,language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3')
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link' : link})
                rank += 1
    return found_results




def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

if __name__ == '__main__':
    data = []
    youtube_data = []

    try:
        results = scrape_youtube('mitonia')
        print(results)
        for result in results['search_result']:
            print('titre = {}'.format(result['title']))
            print('nombre de vue = {}'.format(result['views']))
            print('durée = {}'.format(result['duration']))
            print('chaine = {}'.format(result['channel']))
            print('link = {}'.format(result['link']))
            print('thumbnails = {}'.format(result['thumbnails'][3]))


    except Exception as e:
        print(e)
    finally:
        time.sleep(5)