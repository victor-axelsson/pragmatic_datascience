import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize
import scipy
import math

def read_data(fname, withHeaders=True):
	with open(fname) as f:
		lines = f.readlines()

	content = [line.strip() for line in lines]

	tmp = []
	for i in range(len(content)):
		pts = content[i].split(";")
		if len(pts) > 0: 
			wasOk = True

			for col in pts:
				if len(col) <= 0: 
					wasOk = False
					break

			if wasOk:
				tmp += [pts]

	content = tmp

	if withHeaders:
		return content[2:], content[:1][0]
	else:
		return content

def parseBool(val):
	if val == "Yes":
		return 1
	else:
		return 0

def parseFloat(val):
	return float(val)

def parseDate(val):
	return int(datetime.datetime.strptime(val, '%Y-%m-%d').timestamp())

def parseInt(val):
	return int(val)

def cosineSimilarity(x, y):
	numerator = np.dot(x, y)

	xNorm = 0
	for xi in x:
		xNorm += math.pow(abs(xi), 2)

	xNorm = math.pow(xNorm, (1 / 2))

	yNorm = 0
	for yi in y:
		yNorm += math.pow(abs(yi), 2)

	yNorm = math.pow(yNorm, (1/2))

	denominator = xNorm * yNorm

	#scipy.spatial.distance.cosine(x, y)

	return numerator / denominator

def jaccardSimilarity(x, y):
	
	m11 = 0
	m10 = 0
	m01 = 0

	for i in range(len(x)):
		if x[i] == 1 and y[i] == 1:
			m11 += 1
		elif x[i] == 1 and y[i] == 0:
			m10 += 1
		elif y[i] == 1 and x[i] == 0:
			m01 += 1

	return m11 / (m10 + m01 + m11)


def reverseRow(row):
	row[3] = 1 - row[3] 
	row[4] = 1 - row[4] 
	row[5] = 1 - row[5] 
	row[6] = 1 - row[6]
	row[8] = 1 - row[8]

	row[10] = 1 - row[10]
	row[11] = 1 - row[11]
	row[12] = 1 - row[12]
	row[13] = 1 - row[13]
	row[14] = 1 - row[14]
	row[15] = 1 - row[15]
	row[16] = 1 - row[16]
	row[17] = 1 - row[17]
	row[18] = 1 - row[18]
	row[19] = 1 - row[19]
	row[20] = 1 - row[20]
	row[21] = 1 - row[21]
	row[22] = 1 - row[22]
	row[23] = 1 - row[23]
	row[24] = 1 - row[24]
	row[25] = 1 - row[25]
	row[26] = 1 - row[26]

	return row

parseDict = {
	'date': parseDate,					#0
	'temperaturemin' : parseFloat,		#1 				used
	'temperaturemax':parseFloat,		#2				used
	'precipitation': parseFloat,		#3  inversed	used
	'snowfall':parseBool,				#4  inversed
	'snowdepth': parseFloat,			#5  inversed
	'avgwindspeed': parseFloat,			#6  inversed
	'fastest2minwinddir': parseInt,		#7
	'fastest2minwindspeed': parseFloat,	#8  inversed
	'fastest5secwinddir': parseInt,		#9
	'fastest5secwindspeed': parseFloat,	#10 inversed
	'fog': parseBool,					#11 inversed	used
	'fogheavy': parseBool,				#12 inversed
	'mist': parseBool,					#13 inversed
	'rain': parseBool,					#14 inversed
	'fogground': parseBool,				#15 inversed
	'ice': parseBool,					#16 inversed
	'glaze': parseBool,					#17 inversed
	'drizzle': parseBool,				#18 inversed
	'snow': parseBool,					#19 inversed
	'freezingrain': parseBool,			#20 inversed
	'smokehaze':parseBool,				#21 inversed
	'thunder': parseBool,				#22 inversed
	'highwind': parseBool,				#23 inversed
	'hail': parseBool,					#24 inversed
	'blowingsnow': parseBool,			#25 inversed
	'dust': parseBool,					#26 inversed
	'freezingfog': parseBool			#27 inversed
}

data, headers = read_data("rdu-weather-history.csv")

for row in data:
	for i in range(0, len(row)):
		if len(row[i]) > 0:
			row[i] = parseDict[headers[i]](row[i])


data = normalize(data, axis=0, norm='max')

print("Find most similar day. [{} rows in total]. Select rowNr:".format(len(data)))
rowNr = int(input())

print(rowNr)
print(data[rowNr])


bestCosineScore = -1
bestCosineIndex = -1
bestJaccardScore = -1
bestJaccardIndex = -1
for i in range(len(data)):

	if i == rowNr:
		continue

	row = data[i]
	cosineScore = cosineSimilarity(row[1:], data[rowNr][1:])
	jaccardScore = jaccardSimilarity(row[12:], data[rowNr][12:])

	if cosineScore > bestCosineScore:
		bestCosineScore = cosineScore
		bestCosineIndex = i

	if jaccardScore > bestJaccardScore:
		bestJaccardScore = jaccardScore
		bestJaccardIndex = i

print("The most similar (cosine) is on row {} with score {}. \n{}".format(bestCosineIndex, bestCosineScore, data[bestCosineIndex]))
print("The most similar (Jaccard) is on row {} with score {}. \n{}".format(bestJaccardIndex, bestJaccardScore, data[bestJaccardIndex]))




