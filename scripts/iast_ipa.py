import re
from aksharamukha import transliterate


def transcribe(string):
	string = transliterate.process('IAST', 'Devanagari', string)	
	transText = str()
	string = 'अ' + string
	prevChar = 0
	for charIndex in range(len(string)):
		if (string[charIndex] == '्') or (str(string[charIndex]) in mapping['VOWELS']):
			if not string[charIndex] in {'ः': 'əx', 'ं': 'əm',}:
				try:
					transText = transText[:len(transText)-1]
					if transText[len(transText)-1] == "ə":
						transText = transText[:len(transText)-1]
				except IndexError:
					print("WARNING: You are attempting to transcribe a stand-alone diacritical mark.\n")
			else:
				pass
		if prevChar == 1:	
			flag = 0
			if string[charIndex] in {" ",}:
				if charIndex+1 < len(string):
					flag = 1		
			for label in ['VELAR', 'PALATAL', 'RETROFLEX', 'DENTAL', 'LABIAL', 'ESCAPE']:
				if string[charIndex+flag] in mapping[label]:
					transText = transText[:len(transText)-1]
					transText += str(mapping[label]['NASAL'])
					break
				transText = transText[:len(transText)-1] + "̃"	
		elif prevChar == 2 and False:
			if not string[charIndex] in mapping['VOWELS']:	
				backTrack = charIndex-1
				while (backTrack > 0 and string[backTrack] != "."):
					backTrack -= 1
				syllableBeginning = backTrack
				while backTrack < charIndex and not string[backTrack] in vowels:
					backTrack += 1
				if string[backTrack] in {'ङ', 'ञ', 'ण', 'न', 'म', 'ं'} or string[backTrack] in longVowels:
					pass
				else:
					syllables = transText.split('.')[:len(transText.split('.'))-1]
					lastSyllable = transText.split('.')[len(transText.split('.'))-1]
					transText = ""
					for syllable in syllables:
						transText += str(syllable) + "."
					transText += "ˈ" + str(lastSyllable)
		if not string[charIndex] == '.':
			if (string[charIndex] == 'ं'):
				prevChar = 1
			elif (string[charIndex] == '्'):
				if prevChar != 2: prevChar = 2
				else: prevChar = 4
			else: prevChar = 0	
		transText += str(mapping.get(string[charIndex], string[charIndex]))
	altTransText = '.'
	try:
		vowelB = vowelA = 0
		vowelB = get_next_vowel_index(transText, -1)['index']
		length = lastLength = get_next_vowel_index(transText, -1)['length']
		vowelB += lastLength
		prevSyllBreak = 0
		while vowelA != None and vowelB != None:
			vowelA = get_next_vowel_index(transText, vowelB)['index']
			length = get_next_vowel_index(transText, vowelB)['length']
			clusterComponents = []
			if vowelA == None or vowelB == None:
				break			
			cluster = transText[vowelB: vowelA]
			for charIndex in range(len(cluster)):
				if (len(cluster) == 1) or (not cluster[charIndex] in "'͡ʃʰʱː̪ʒɕʑ"):
					clusterComponents.append(cluster[charIndex])
				else:
					clusterComponents[len(clusterComponents)-1] += cluster[charIndex]
			altTransText += transText[vowelB-lastLength:vowelB]		
			stress_exclude_set = {'ŋ', 'ɲ', '.ɳ', 'n', 'm',}
			if len(clusterComponents) == 1:
				prevSyllBreak = len(altTransText) + int(' ' in clusterComponents)
				if len(altTransText): altTransText += '.' + clusterComponents[0]
				else: altTransText += clusterComponents[0]
			elif len(clusterComponents) == 2:
				if len(altTransText) and clusterComponents[0] not in stress_exclude_set.union({' '}):
					if altTransText[len(altTransText)-1] != '̃' and (lastLength == 1 or altTransText[len(altTransText)-1] == '̩'):
						for i in range(1,10):
							try:
								periodIndex = len(altTransText)-i+altTransText[-i:].index('.')
								altTransText = altTransText[:periodIndex+1] + 'ˈ' + altTransText[periodIndex+1:]
								break
							except ValueError:
								pass
				prevSyllBreak = len(altTransText) + 1 + int(' ' in clusterComponents)
				altTransText += clusterComponents[0] + '.' + clusterComponents[1]
			elif len(clusterComponents) == 3:
				if (clusterComponents[2] in {'j', 'ɹ',}):
					if len(altTransText) and clusterComponents[0] not in stress_exclude_set:
						if altTransText[len(altTransText)-1] != '̃' and (lastLength == 1 or altTransText[len(altTransText)-1] == '̩'):
							for i in range(1,10):
								try:
									periodIndex = len(altTransText)-i+altTransText[-i:].index('.')
									altTransText = altTransText[:periodIndex+1] + 'ˈ' + altTransText[periodIndex+1:]
									break
								except ValueError:
									pass
					prevSyllBreak = len(altTransText) + 1 + int(' ' in clusterComponents)
					altTransText += clusterComponents[0] + '.' + clusterComponents[1] + clusterComponents[2]
				elif (clusterComponents[0] in stops.values()) and (clusterComponents[1] in stops.values()):
					if len(altTransText) and clusterComponents[0] not in stress_exclude_set:
						if altTransText[len(altTransText)-1] != '̃' and (lastLength == 1 or altTransText[len(altTransText)-1] == '̩'):
							for i in range(1,10):
								try:
									periodIndex = len(altTransText)-i+altTransText[-i:].index('.')
									altTransText = altTransText[:periodIndex+1] + 'ˈ' + altTransText[periodIndex+1:]
									break
								except ValueError:
									pass
					prevSyllBreak = len(altTransText) + 1 + int(' ' in clusterComponents)
					altTransText += clusterComponents[0] + '.' + clusterComponents[1] + clusterComponents[2]
				else:
					if len(altTransText) and clusterComponents[0] not in stress_exclude_set:
						if altTransText[len(altTransText)-1] != '̃' and (lastLength == 1 or altTransText[len(altTransText)-1] == '̩'):
							for i in range(1,10):
								try:
									periodIndex = len(altTransText)-i+altTransText[-i:].index('.')
									altTransText = altTransText[:periodIndex+1] + 'ˈ' + altTransText[periodIndex+1:]
									break
								except ValueError:
									pass
					prevSyllBreak = len(altTransText) + 2 + int(' ' in clusterComponents)
					altTransText += clusterComponents[0] + clusterComponents[1] + '.' + clusterComponents[2]				
			else:
				if len(altTransText) and clusterComponents[0] not in stress_exclude_set:
					if altTransText[len(altTransText)-1] != '̃' and (lastLength == 1 or altTransText[len(altTransText)-1] == '̩'):
						for i in range(1,10):
							try:
								periodIndex = len(altTransText)-i+altTransText[-i:].index('.')
								altTransText = altTransText[:periodIndex+1] + 'ˈ' + altTransText[periodIndex+1:]
								break
							except ValueError:
								pass
				for i in range(len(clusterComponents)): altTransText += clusterComponents[i]
			vowelB = vowelA+length
			lastLength = length
		altTransText += transText[vowelB-lastLength:]	
		altTransText = ''.join(altTransText[3:].split('.'))
		return re.sub('ˈ', '', altTransText)
	except Exception as e:
		altTransText = transText[1:]
		altTransText = ''.join(altTransText.split('.'))
		return re.sub('ˈ', '', altTransText)
	

def get_next_vowel_index(ipaString, currentIndex):
	if currentIndex <= 0:
		pass
	for index in range(1+currentIndex,len(ipaString)):
		for iterator in range(5):
			if ipaString[index:index+1+4-iterator] in set(vowels.values()).union({None}) - {'əm', 'əh'}:
				return {'index': index, 'length': 1 + 4 - iterator}
	return {'index': None, 'length': None}

	
def char_in_range(c):
	o = ord(c)
	lower = int('0x900', 16)
	upper = int('0x97f', 16)
	exclude = {'0x900', '0x904', '0x90e', '0x912', '0x929', '0x931', '0x934', '0x93a', '0x93b', '0x93c', '0x946', '0x94e', '0x94f', '0x94a', '0x951', '0x952', '0x953', '0x954', '0x955', '0x956', '0x957', '0x958', '0x959', '0x95a', '0x95b', '0x95c', '0x95d', '0x95e', '0x95f', '0x973', '0x974', '0x975', '0x976', '0x977', '0x978', '0x979', '0x97a', '0x97b', '0x97c', '0x97f', '0x97d', '0x97e', '0x970', '0x971'}
	return c == ' ' or ((o >= lower and o <= upper) and not (hex(o) in exclude))	


mapping = {
	'ॐ': 'oːm',
	'अ': 'ə',
	'आ': 'ɑː', 'ा': 'ɑː',
	'इ': 'i', 'ि': 'i',
	'ई': 'iː', 'ी': 'iː',
	'उ': 'u', 'ु': 'u',
	'ऊ': 'uː', 'ू': 'uː',
	'ऋ': 'ɹ̩', 'ॠ': 'ɹ̩ː', 'ृ': 'ɹ̩', 'ॄ': 'ɹ̩ː',
	'ऌ': 'l̩', 'ॢ': 'l̩', 'ॡ': 'l̩ː', 'ॣ': 'l̩ː',
	'ए': 'eː', 'े': 'eː',
	'ऐ': 'ɑːi', 'ै': 'ɑːi',
	'ओ': 'oː', 'ो': 'oː',
	'अाै': 'ɑːu', 'ाै': 'ɑːu',
	'अं': 'əm', 'ं': 'm',
	'अः': 'əh', 'ः': 'h',
	'VOWELS': {
		'ा': 'ɑː',
		'ि': 'i',	'ी': 'iː',
		'ु': 'u', 'ू': 'uː',
		'ृ': 'ɹ̩', 'ॄ': 'ɹ̩ː', 'ॢ': 'l̩',
		'े': 'eː', 'ै': 'ɑːi',
		'ो': 'oː', 'ाै': 'ɑːu',
		'ः': 'əh', 'ं': 'əm',
	},
	'क': 'kə', 'ख': 'kʰə', 'ग': 'gə', 'घ': 'gʰə', 'ङ': 'ŋə',
	'VELAR': {'क': 'kə', 'ख': 'kʰə', 'ग': 'gə', 'घ': 'gʰə', 'NASAL': 'ŋ',},
	'च': 't͡ɕə', 'छ': 't͡ɕʰə', 'ज': 'd͡ʑə', 'झ': 'd͡ʑʱə', 'ञ': 'ɲə',
	'PALATAL': {'च': 't͡ɕə', 'छ': 't͡ɕʰə', 'ज': 'd͡ʑə', 'झ': 'd͡ʑʱə', 'NASAL': 'ɲ',},
	'ट': 'ʈə', 'ठ': 'ʈʰə', 'ड': 'ɖə', 'ढ': 'ɖʰə', 'ण': 'ɳə',
	'RETROFLEX': {'ट': 'ʈə', 'ठ': 'ʈʰə', 'ड': 'ɖə', 'ढ': 'ɖʰə', 'NASAL': 'ɳ',},
	'त': 't̪ə', 'थ': 't̪ʰə', 'द': 'd̪ə', 'ध': 'd̪ʰə', 'न': 'nə',
	'DENTAL': {'त': 't̪ə', 'थ': 't̪ʰə', 'द': 'd̪ə', 'ध': 'd̪ʰə', 'NASAL': 'n',},
	'प': 'pə', 'फ': 'pʰə', 'ब': 'bə', 'भ': 'bʱə', 'म': 'mə',
	'LABIAL': {'प': 'pə', 'फ': 'pʰə', 'ब': 'bə', 'भ': 'bʱə', 'NASAL': 'm',},
	'य': 'jə', 'र': 'ɹə', 'ल': 'lə', 'व': 'ʋə', 'श': 'ɕə',
	'ष': 'ʂə', 'स': 'sə', 'ह': 'ɦə', 'ळ': 'ɭə',
	'क्ष': 'kʂə', 'ज्ञ': 'd͡ʑɲə', 'त्र': 't̪ɹə',
	'्': '', 'ऽ': '',
	' ': ' ', '\n': '\n', '\t': '\t', '\r': '\n', '.': '.', '।': '।',
	'ESCAPE': {
		'\n': '\n', '\t': '\t', '\r': '\n', '.': '.', '।': '।', 'NASAL': 'm',
		'॥': '॥'
	}
}

vowels = {
	'ा': 'ɑː',
	'ि': 'i',	'ी': 'iː',
	'ु': 'u', 'ू': 'uː',
	'ृ': 'ɹ̩', 'ॄ': 'ɹ̩ː', 'ॢ': 'l̩',
	'े': 'eː', 'ै': 'əi',
	'ो': 'oː', 'ाै': 'əu',
	'ः': 'əh', 'ं': 'əm',
	'ॐ': 'oːm',
	'अ': 'ə',
	'आ': 'ɑː', 'ा': 'ɑː',
	'इ': 'i', 'ि': 'i',
	'ई': 'iː', 'ी': 'iː',
	'उ': 'u', 'ु': 'u',
	'ऊ': 'uː', 'ू': 'uː',
	'ऋ': 'ɹ̩', 'ॠ': 'ɹ̩ː', 'ृ': 'ɹ̩', 'ॄ': 'ɹ̩ː',
	'ऌ': 'l̩', 'ॢ': 'l̩', 'ॡ': 'l̩ː', 'ॣ': 'l̩ː',
	'ए': 'eː', 'े': 'eː',
	'ऐ': 'əi', 'ै': 'əi',
	'ओ': 'oː', 'ो': 'oː',
	'अाै': 'əu', 'ाै': 'əu',
	'अं': 'əm', 'ं': 'əm',
	'अः': 'əx', 'ः': 'əx'
}

longVowels = {
	'ा': 'ɑː', 'ी': 'iː', 'ू': 'uː', 'ॄ': 'ɹ̩ː',
	'े': 'eː', 'ै': 'əi', 'ो': 'oː', 'ाै': 'əu',
	'ः': 'əx', 'ं': 'əm', 'ॣ': 'l̩ː'
}

stops = {
	'क': 'k', 'ख': 'kʰ', 'ग': 'g', 'घ': 'gʰ',
	'च': 't͡ɕ', 'छ': 't͡ɕʰ', 'ज': 'd͡ʑ', 'झ': 'd͡ʑʱ',
	'ट': 'ʈ', 'ठ': 'ʈʰ', 'ड': 'ɖ', 'ढ': 'ɖʰ',
	'त': 't̪', 'थ': 't̪ʰ', 'द': 'd̪', 'ध': 'd̪ʰ',
	'प': 'p', 'फ': 'pʰ', 'ब': 'b', 'भ': 'bʱ'
}

sonority = {
	'k': 1, 't͡ɕ': 1, 'ʈ': 1, 't̪': 1, 'p': 1,
	'kʰ': 2, 't͡ɕʰ': 2, 'ʈʰ': 2, 't̪ʰ': 2, 'pʰ': 2,
	'g': 3, 'd͡ʑ': 3, 'ɖ': 3, 'd̪': 3, 'b': 3,
	'gʰ': 4, 'd͡ʑʱ': 4, 'ɖʰ': 4, 'd̪ʰ': 4, 'bʱ': 4,
	'ŋ': 5, 'ɲ': 5, 'ɳ': 5, 'n': 5, 'm': 5,
	'श': 6, 'ष': 6, 'स': 6, 'ह': 6, 'ळ': 6,
	'य': 7, 'र': 7, 'ल': 7, 'व': 7
}
