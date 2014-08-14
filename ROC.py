import numpy as np
import Gnuplot

def readtolist(filename):
	result = []
	with open(filename) as f:
		for line in f:
			result.append(float(line))
	return result

def histtofile(hist, filename):
	with open(filename, 'w') as f:
		for i in range(0, len(hist[0])):
			f.write("{1}\t{0}\n".format(hist[0][i],hist[1][i]))

def plothist(hist):
	result = []
	for i in range(0, len(hist[0])):
		result.append((hist[1][i], hist[0][i]))
	return result

def plothistograms(title, testname, normal, diseased):
	gp = Gnuplot.Gnuplot()
	gp.title(title)
	#gp('set style data linespoints')
	gp('set style data lines')
	gp('set ylabel "Frequency"')
	gp('set xlabel "{0}"'.format(testname))
	normal = Gnuplot.PlotItems.Data(plothist(normal), title="Normal")
	diseased = Gnuplot.PlotItems.Data(plothist(diseased), title="Diseased")
	gp.plot(normal, diseased)

def plotROC(title, plot):
	gp = Gnuplot.Gnuplot()
	gp.title(title)
	#gp('set style data linespoints')
	gp('set style data lines')
	gp('set ylabel "Sensitivity"')
	gp('set xlabel "1-Specificity"')
	#gp('set ztics 1')
	#gp('set view 29,53')
	roc = Gnuplot.PlotItems.Data(plot)
	zero = Gnuplot.PlotItems.Data([(0,0),(1,1)])
	gp.plot(roc,zero)



def getTPRFPR(cutoff, operator, normal, diseased):
	# operator = [<]
	# Positive if value [operator] cutoff == True
	#                         Disease
	#                  Present        Absent
	# Test  Positive    TP              FP
	#       Negetive    FN              TN
	
	TP = 0.0
	FN = 0.0
	for value in diseased:
		if value < cutoff:
			TP += 1.0
		else:
			FN += 1.0
	FP = 0.0
	TN = 0.0
	for value in normal:
		if value < cutoff:
			FP += 1.0
		else:
			TN += 1.0
	TPR = TP / (TP + FN)
	FPR = 1.0 - (TN / (FP  + TN))

	result = (TPR, FPR, cutoff)

	return result

		
	

#normal = readtolist('normal.lst')
mu = 9
sigma = 1
normal = np.random.normal(mu, sigma, 100)

#diseased = readtolist('diseas.lst')
mu = 14
sigma = 3
diseased = np.random.normal(mu, sigma, 100)

normalhist = np.histogram(normal, bins=40, range=(0,30))
diseasedhist = np.histogram(diseased, bins=40, range=(0,30))

plothistograms("","Test", normalhist, diseasedhist)


ROC = []
for i in range(0,30):
	cutoff = 1.0 + (float(i)/30.0 * 30)
	ROC.append(getTPRFPR(float(cutoff),">=", normal, diseased))

plotROC("ROC", ROC)
