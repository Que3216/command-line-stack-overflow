from lxml import html
from termcolor import colored
import requests
import json
import sys
import urllib

def main():
  if len(sys.argv) == 1:
    print 'Searches stack overflow for a given query and displays the first result'
    print ''
    print 'Usage: ' + colored('so <your-search-terms>', 'yellow')
    print ''
    print 'For example, try: ' + colored('so python foldr', 'yellow')
    return

  searchTerm = ' '.join(['site:stackoverflow.com/questions'] + sys.argv[1:])
  searchUrl = 'google.com/search?' + urllib.urlencode({'q': searchTerm})

  print 'Searching for \'' + searchTerm + '\'... ( ' + searchUrl + ' )'

  searchResults = search_google(searchTerm)

  for result in searchResults:
    url = result['url']
    answers = get_stack_overflow_answers(url)
    if len(answers) > 0:
      print ''
      print colored(with_underline("Answer from " + url), 'yellow')
      print add_colors_to_html(answers[0])
      return
    else:
      print url + " has no answers"

def search_google(query):
  response = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0', params={'q': query})
  parsedResponse = json.loads(response.content)['responseData']
  return parsedResponse['results']

def get_stack_overflow_answers(url):
  stackoverflowResponse = requests.get(url)
  tree = html.fromstring(stackoverflowResponse.text)
  return tree.xpath('//div[@id="answers"]//div[@itemtype="http://schema.org/Answer"]//div[@class="post-text"]')

def with_underline(text):
  return text + '\n' + ('_' * len(text))

def tab_in(text):
  return '  ' + '\n  '.join(text.splitlines())

def add_colors_to_html(element):
  text = ''
  for child in element:
    if child.tag == 'pre':
      text += '\n' + colored(tab_in(child.text_content()), 'white') + '\n'
    else:
      text += '\n' + child.text_content() + '\n'
  return text

if __name__ == "__main__":
  main()
