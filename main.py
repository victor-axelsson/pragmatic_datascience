import datetime
import matplotlib.pyplot as plt

def read_data(fname, withHeaders=True):
	with open(fname) as f:
		lines = f.readlines()

	content = [line.strip() for line in lines]

	tmp = []
	for i in range(len(content)):
		pts = content[i].split(";")
		if len(pts) > 0: 
			tmp += [pts]

	content = tmp

	if withHeaders:
		return content[2:], content[:1][0]
	else:
		return content

data, headers = read_data("rdu-weather-history.csv")

plotData = []
for row in data:
	if len(row[1]) > 0 and len(row[2]) > 0:
		avgTemp = (float(row[1]) + float(row[2])) / 2
		measuringDate = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
		plotData.append({
			'date': measuringDate,
			'temp': avgTemp
		})

sortedByDate = sorted(plotData, key=lambda k: k['date']) 

temperatures = []
dates = []
for day in sortedByDate:
	temperatures.append(day['temp'])
	dates.append(day['date'])

plt.xlabel("Time")
plt.ylabel("Temperature (avg) F")
plt.title("Temperatures")
plt.plot(dates, temperatures, label='Temerature F')
plt.legend()
plt.show()
