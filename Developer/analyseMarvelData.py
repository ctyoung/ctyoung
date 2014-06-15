# simple analysis of stream from Datasift

from fileHelpers import fileRead

def analyseStream():
	''' analyse stream data collected 
		- basic analysis, with some simple stats printed '''
		
	marvelChars = fileRead('marvelChars')
	twitterMentions = fileRead('twitterUsefulData')
	
	counts={}
	sentiments={}
	
	# get most frequent mention
	for char in marvelChars:
		for line in twitterMentions:
			try:
				if str(char).lower() in line.values()[0]['text'].lower():
					if char in counts.keys():
						counts[char] +=1
					else:
						counts[char] = 1
					# get sentiments - adding sentiment values to get combined score
					if 'sentiment' in line.values()[0]:
						if char in sentiments.keys():
							sentiments[char] += line.values()[0]['sentiment']
						else:
							sentiments[char] = line.values()[0]['sentiment']
			except:
				#TODO skipping character not in ascii - fix!
				break
				
	sortedCounts = sorted(counts.items(), key=lambda x: x[1])
	print 'Most mentioned 3 characters:', sortedCounts[-3:] 
	
	sortedSentiments = sorted(sentiments.items(), key=lambda x: x[1])
	print 'Most liked 3 characters', sortedSentiments[-3:]
	print 'Least liked 3 characters', sortedSentiments[:2]
	
	print 'Total mentions for', len(marvelChars), 'characters searched:', len(twitterMentions)
	
analyseStream()