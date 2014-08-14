import numpy as np
import Gnuplot


class DataSet:
	def __init__(self, filename):
		self.condition = []
		self.outcome   = []
				
		if filename == "TEST":
			samplesize = 200
			mu = 13
			sigma = 5
			outcomePositive = list(np.random.normal(mu, sigma, samplesize/2))
			mu = 10
			sigma = 4
			outcomeNegetive = list(np.random.normal(mu, sigma, samplesize/2))
			outcomePositive.extend(outcomeNegetive)
			self.outcome = outcomePositive
			self.condition = [1] * (samplesize/2) + [0] * (samplesize/2)
			self.current = 0
			self.high = len(self.condition) - 1
			return
			
		with open(filename) as f:
			for line in f:
				line = str.split(line.strip(), ",", 1)
				self.condition.append(float(line[0]))
				self.outcome.append(float(line[1]))

		self.current = 0
		self.high = len(self.condition) - 1


	def __iter__(self):
		self.current = 0
		return self

	
	def next(self):
		if self.current > self.high:
			raise StopIteration
		else:
			i = self.current
			self.current += 1
			return (self.condition[i], self.outcome[i])




class ClassificationRule:
	def __init__(self, condition, parameter):
		self.condition = condition
		self.parameter = parameter


	def positive(self, value):
		if self.condition == "gt":
			if value > self.parameter:
				return True
		elif self.condition == "lt":
			if value < self.parameter:
				return True
		elif self.condition == "gte":
			if value >= self.parameter:
				return True
		else:
			if value <= self.parameter:
				return True
		return False




class TwoByTwoTable:
	def __init__(self, dataset):
		self.dataset = dataset
		self.TP = 0.0
		self.FP = 0.0
		self.FN = 0.0
		self.TN = 0.0


	def classify(self, classificationrule):
		self.TP = 0.0
		self.FP = 0.0
		self.FN = 0.0
		self.TN = 0.0
		for item in self.dataset:
			condition, outcome = item
			outcomePositive = classificationrule.positive(outcome)
			if condition == 1.0:
				if outcomePositive:
					self.TP += 1
				else:
					self.FN += 1
			else:
				if outcomePositive:
					self.FP += 1
				else:
					self.TN += 1

	
	def TPR(self):
		return self.TP / (self.TP + self.FN)


	def FPR(self):
		return 1.0 - (self.TN / (self.FP  + self.TN))


	def display(self):
		print "                            Condition"
		print "                   Positive             Negetive"
		print "                  -----------------------------"
		print "         Positive |  {0}                 {1}".format(self.TP, self.FP)
		print "  Test            |"
		print "         Negetive |  {0}                 {1}".format(self.FN, self.TN)





class Histogram:
	def __init__(self, dataset):
		self.dataset = dataset


	def generate(self, bins, range):
		self.conditionPositive = []
		self.conditionNegetive = []
		for item in self.dataset:
			condition, outcome = item
			if condition == 1.0:
				self.conditionPositive.append(outcome)
			else:
				self.conditionNegetive.append(outcome)
		self.conditionPositiveHist = np.histogram(self.conditionPositive, bins, range)
		self.conditionNegetiveHist = np.histogram(self.conditionNegetive, bins, range)


	def _histToPlot(self, hist):
		result = []
		for i in range(0, len(hist[0])):
			x = (hist[1][i] + hist[1][i+1])/2.0
			y = hist[0][i]
			result.append((hist[1][i], hist[0][i]))
		return result


	def display(self):
		gp = Gnuplot.Gnuplot()
		gp.title("Histogram")
		gp('set style data linespoints')
		#gp('set style data lines')
		gp('set xlabel "Test Outcome"')
		gp('set ylabel "Frequency"')
		conditionPositivePlot = Gnuplot.PlotItems.Data(
				self._histToPlot(self.conditionPositiveHist), title="ConditionPositive")
		conditionNegetivePlot = Gnuplot.PlotItems.Data(
				self._histToPlot(self.conditionNegetiveHist), title="ConditionNegetive")
		gp.plot(conditionPositivePlot, conditionNegetivePlot)




class ROC:
	def __init__(self, dataset):
		self.dataset = dataset
		self.twobytwotable = TwoByTwoTable(self.dataset)
		self.plot = []


	def generate(self, condition, steps, range):
		step = float(range[1]-range[0])/float(steps)
		parameter = float(range[0])
		while parameter < (range[1] + step):
			self.twobytwotable.classify(ClassificationRule(condition, parameter))
			point = (self.twobytwotable.FPR(), self.twobytwotable.TPR())
			self.plot.append(point)
			parameter += step


	def display(self):
		gp = Gnuplot.Gnuplot()
		gp.title("ROC Curve")
		gp('set size square')
		gp('set style data linespoints')
		#gp('set style data lines')
		gp('set xrange [0:1]')
		gp('set yrange [0:1]')
		gp('set xtics 0.1')
		gp('set ytics 0.1')
		gp('set xlabel "FPR"')
		gp('set ylabel "TPR"')
		roccurve = Gnuplot.PlotItems.Data(self.plot)
		normal = Gnuplot.PlotItems.Data([(0,0),(1,1)])
		gp.plot(roccurve, normal)

		
		

#data = DataSet("data.csv")
data = DataSet("TEST")
result = TwoByTwoTable(data)
result.classify(ClassificationRule("gt", 15.0))

hist = Histogram(data)
hist.generate(60.0, (0.0,30.0))
hist.display()

rok = ROC(data)
rok.generate("gt", 30, (0, 30))
rok.display()

