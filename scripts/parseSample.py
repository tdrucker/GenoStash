import argparse
import sys
import json

intro = """
This is the hackathon script to make FormatData from a VCF
"""

footer = """
Example usage: $ 
"""
parser = argparse.ArgumentParser(description=intro, epilog=footer, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i','--input', help='The multi-sample VCF file', default=".", required=True)
args = vars(parser.parse_args())

def getID(line):
	return line[0] + "_" + line[1] + "_" + line[3] + "_" + line[4]

def getSamples(headerline):
	samples = []
	tokens = headerline.split("\t")
	#print tokens
	count = 0
	for token in tokens:
		count = count + 1
		if ( count > 9 ):
			samples.append(token.replace('\n', ''))
			return samples

def jsonize(token, format, id, sample):
	formattokens = format.split(":")
	sampletokens = token.split(":")
	if len(formattokens) != len(sampletokens):
		print json.dumps({"GT" : "./.", "vID" : id, "sID" : sample})
	else:
		attr = {}
		for i in range(0,len(formattokens)) :
			attr[formattokens[i]] = sampletokens[i]
		attr["vID"] = id
		attr["sID"]=sample
		print json.dumps(attr)

vcf = args['input']
samples = []

file = open(vcf, 'r')
for line in file:
	if line.startswith("##"):
		 x = 1 #do nothing, just the VCF metadata
	elif line.startswith("#"):
		#the regular header line, get the samples
		samples = getSamples(line)
		#print samples
	else: #data line
		#print line
		tokens = line.split()
		id = getID(tokens)
		format = tokens[8]
		#print id
		count = 0
		for token in tokens:
			if count > 8:
				#print samples
				jsonize(token, format, id, samples[0])
			count = count + 1
		break

