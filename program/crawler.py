class Crawler:
   def __init__(self):
      import curses
      screen = curses.initscr()
   def get_input(self):               #from user about search query
      self.input = ''                 # ex:who is George Bush?
      return self.input
   def get_keywords(self, input):     #convert query to important keywords
      self.qtype = ''                 #possible types = [who/whom, what, where, why, when, how, which]
      self.unknown = ''
      return self.keywords            #keywords from input ex: qtype = 'who', unknown = 'George Bush'
   def get_web(self):                 #first google the query
      self.webdata = ['']             #then crawl the search results and get data from each site crawled the returned list of datas from each website
      return self.webdata
   def parse(self, html):             #search for text pertaining to keywords in webpage
      self.relevant = ['']            #text from webpage with the keywords
   def associations(self, qtype):     #given a question returns associated words that usually follow the unknown. ex: 'George Bush is...'
      self.verb_list = ['']
      return associated_verbs
   def process(self, input, qtype):   #process natural language to find the answer to query within the valuable data from the webpages
      self.info                       #search for 'Bush was...' 'Bush is...' 'Bush had...' 'was, 'is', and 'had' are associated with quesion type 'who'
   def output(self, answer):          #displays answer
      self.answer = answer            #answer to question
