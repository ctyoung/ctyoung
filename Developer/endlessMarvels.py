import csv
import datasift
import datetime
from fileHelpers import fileRead, fileWrite
import json
from marvel.marvel import Marvel
import config

# get Datasift client
client = datasift.Client(config.DATASIFT_USERNAME, config.DATASIFT_APIKEY)

def getCharacters(refresh=False):
	''' get list of Marvel characters using their API
		- get from json file if already retrieved
		- or go back to API if not '''
	
	# if refresh is requested, get a new list from the API
	if not refresh:
		try:
			charsList = fileRead('marvelChars')
			print 'Getting characters from file...'
			return charsList
		except:
			# we don't have a file of characters, so carry on and get from the API
			print 'Getting characters from API...'
	
	marvelClient=Marvel(config.PUBLIC_KEY, config.PRIVATE_KEY)
	
	replyOffset = 0

	# get total number of characters first - we need this to work out how many chunks
	# to get from the API as each call has a 100 limit
	chars = marvelClient.get_characters(limit=str(1), offset=replyOffset)
	totalChars = chars.data.total
	print 'Total characters:', totalChars
	
	currentChars = 0
	loopCount = 0
	foundBad = False
	res=[]
	replyLimit = 100
	
	while currentChars < totalChars:
		# adjust last chunk to what's left of the total number of characters
		if totalChars-currentChars < replyLimit:
			replyLimit = totalChars-currentChars
			
		chars = marvelClient.get_characters(limit=replyLimit, offset=currentChars)

		# Check for current Marvel API bug where asking for record 302 returns an error (code 500)
		if chars.code == 500: 
			# If we've isolated the bad record, skip it by moving on the offset
		    if replyLimit == 1: 
		    	foundBad = True
		    	print 'Bad record from Marvel API at', currentChars
		        currentChars+=replyLimit
		    replyLimit = 1 # Go one at a time until we get past the dodgy record
		else:
			res.extend(chars.data.results)
			print 'Records retrieved:', len(res), '...'
			currentChars+=replyLimit
			if foundBad:
				replyLimit = 100 # Reset the reply limit if we set it to 1 above
				foundBad = False		

	print 'Total records retrieved:', len(res)
			
	charsList=[]

	for r in res:
		charsList.append(r.name)
	fileWrite('marvelChars', charsList)
	
	return charsList
	
def saveInteraction(interaction):
	''' save this interaction to a json file '''
	#TODO Twitter only for first draft - expand to other sources
	twitterData = []
	try:
		twitterData.extend(fileRead('twitterInteractions'))
	except:
		# no file, so carry on
		pass
	twitterData.extend([interaction])
	fileWrite('twitterInteractions', twitterData)

def parseInteraction(interaction):
	''' parse interaction and record useful info '''
	
	usefulData={}
	usefulDataList=[]
	thisInteraction={}
	
	thisInteraction['dataSource'] = interaction['interaction']['type']
	
	#Get tweet contents
	if 'retweet' in interaction['twitter']:
		tweet = interaction['twitter']['retweet']
		thisInteraction['retweet'] = True
	else:
		tweet = interaction['twitter']
		thisInteraction['retweet'] = False
	
	# get tweet data
	if 'user' in tweet.keys():
		if 'name' in tweet['user'].keys():
			thisInteraction['name'] = tweet['user']['name']
		if 'location' in tweet['user'].keys():
			thisInteraction['location'] = tweet['user']['location']
		if 'followers_count' in tweet['user'].keys():
			thisInteraction['followers'] = tweet['user']['followers_count']
	
	if 'created_at' in tweet.keys():
		thisInteraction['created_at'] = tweet['created_at']
		
	if 'demographic' in interaction.keys():
		thisInteraction['gender'] = interaction['demographic']['gender']
		
	if 'text' in tweet.keys():
		thisInteraction['text'] = tweet['text']
		
	if 'salience' in interaction.keys():
		thisInteraction['sentiment'] = interaction['salience']['content']['sentiment']
		
	if 'klout' in interaction.keys():
		thisInteraction['Klout score'] = interaction['klout']['score']
		
	if 'links' in interaction.keys():
		thisInteraction['retweet_count'] = interaction['links']['retweet_count']
	
	# give this interaction a key
	usefulData[tweet['id']] = thisInteraction
	
	fileData = []
	try:
		fileData.extend(fileRead('twitterUsefulData'))
	except:
		# no file so carry on
		pass
	fileData.extend([usefulData])
	fileWrite('twitterUsefulData', fileData)
    
# Handler: Message deleted by user
@client.on_delete
def on_delete(interaction):
    print "You must delete this to be compliant with T&Cs: ", interaction
    #TODO Add deletion functionality
 
# Handler: Connection was closed
@client.on_closed
def on_close(wasClean, code, reason):
    print "Stream subscriber shutting down because ", reason
 
# Handler: Picks up any error, warning, information messages from the platform
@client.on_ds_message
def on_ds_message(msg):
    print( 'DS Message %s' % msg)
            
# Handler: Connected to DataSift
@client.on_open
def on_open():
    print "Connected to DataSift"
    @client.subscribe(fltr['hash'])
    def on_interaction(interaction):
        print "Received interaction "
        
        saveInteraction(interaction)
        
        parseInteraction(interaction)

# get Marvel characters
charsList = getCharacters(refresh=False)
characters = ','.join(charsList)

# do some formatting
characters = characters.replace('"','\\"')

# create query
#TODO simple: remove unmatchable strings like "Skullbuster (Cylla Markham)"
#TODO tricker: hone in on Marvel-only mentions, e.g. "Rhino" hits will be mostly unrelated to the Marvel character
csdl = 'interaction.content contains_any "' + characters + '" and language.tag == "en" ' 

# check query is valid
fltr = client.compile(csdl)
		
# Start streaming
client.start_stream_subscriber()


