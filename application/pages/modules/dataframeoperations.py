'''
Takes a dataframe as input, purpose is to apply operations on a copy of the dataframe
usefull to plot things easily.

Also allows to change the dataframe format such as indexing time or adding data

Every operation has it's 'time_' equivalent, only means that it regoups data and applies
the operations on the group

Available functions:
> Mean
> Percent change
> Median
> Sum
> variance
> Standart deviation
> Maximum
> Minimum
> Moving Average

'''


import pandas as pd
import numpy as np
import sys
import math


class dfOperations(object):
	'''Dataframe operations
	Stores the data'''
	'''______________________________________________Class Attributes______________________________________________'''
	
	def __init__(self, file):
		def timecolumn(df):
			try:
				df["Time"] = pd.to_datetime(df.Time)
			except:
				pass
		
		self.file = file
		self.data = pd.read_csv(file)
		self.len_file = len(self.data.index)
		
		timecolumn(self.data)

		'''Operation History to reduce the number of variables'''
		self.previous_operation = None
		self.last_operation = None

		'''Checks if Time is index when we add data'''
		self.index = True

	def __str__(self):
		return '<dfHandler | File: {} | File Dataframe Size: {}>'.format(self.file, self.len_file)

	def __len__(self):
		return self.len_file

	'''______________________________________________Managing f°______________________________________________'''
	def index_time(self):
		self.data.index = self.data.Time
		return self.data.drop(["Time"], axis=1, inplace=True)

	def add_data(self, data):
		'''Appends data to the current dataframe'''
		def time_rec(df):
			'''cheking if the current data frame has the Time column as index'''
			if self.data.index.dtype == 'datetime64[ns]':
				try:
					df.Time = pd.to_datetime(df.Time)
					df.index = df.Time
					df.drop(["Time"], axis=1, inplace=True)
				except:
					pass
				self.index = False
			return df
		
		if not isinstance(data, dict):
			sys.exit('\ndfHandler | DataError: Data should be a dict')
		
		new_data = time_rec(pd.DataFrame(data=data))

		self.data = pd.concat([self.data, new_data], copy=False, ignore_index=self.index)
		return self.data

	def history(self):
		self.previous_operation = self.last_operation

	'''______________________________________________Time Operations f°______________________________________________'''
	'''Executes fonctions on every value depending on sample'''
	
	def time_mean(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).mean().dropna(axis=0, how='any') 
		return self.last_operation

	def time_percent(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).median().pct_change().dropna(axis=0, how='any') 
		return self.last_operation

	def time_median(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).median().dropna(axis=0, how='any')
		return self.last_operation

	def time_sum(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).sum()
		self.last_operation = self.last_operation[self.last_operation != 0].dropna(axis=0, how='any')
		return self.last_operation

	def time_variance(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).var().dropna(axis=0, how='any')
		return self.last_operation

	def time_stdv(self, freq, column):
		self.history()
		recov_data = self.data.resample(freq).var().dropna(axis=0, how='any')
		new_data = [math.sqrt(i) for i in recov_data[column]]
		recov_data[column] = pd.DataFrame({'New':new_data})['New'].values
		self.last_operation = recov_data
		return self.last_operation

	def time_max(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).max().dropna(axis=0, how='any')
		return self.last_operation
	
	def time_min(self, freq):
		self.history()
		self.last_operation = self.data.resample(freq).min().dropna(axis=0, how='any')
		return self.last_operation

	def time_movave(self, freq, column, axe=1):
		self.history()
		recov_data = self.data.resample(freq).median()
		liste = list(recov_data[column])
		if axe == 1:
			result = [(liste[i-1]+liste[i]+liste[i+1])/3 if i-1 >= 0 and i+1<len(liste) else np.nan for i in range(len(liste))]
			'''
			> Same as

			for i in range(len(liste)):
				if i-1 >= 0 and i+1<len(liste):
					value = (liste[i-1]+liste[i]+liste[i+1])/3
				else:
					value = np.nan
				result.append(value)
			'''
		else:
			result = [(liste[i-2]/2+liste[i-1]+liste[i]+liste[i+1]+liste[i+2]/2)/4 if i-2 >= 0 and i+2<len(liste) else np.nan for i in range(len(liste))]
			'''
			> Same as

			for i in range(len(liste)):
				if i-2 >= 0 and i+2<len(liste):
					value = (liste[i-2]/2+liste[i-1]+liste[i]+liste[i+1]+liste[i+2]/2)/4
				else:
					value = np.nan
				result.append(value)
			'''

		recov_data['Price'] = pd.DataFrame({'New':result})['New'].values
		self.last_operation = recov_data
		return self.last_operation

	'''______________________________________________Operations f°______________________________________________'''
	'''Executes fonctions on a column in the dataframe'''

	def mean(self, column):
		self.history()
		self.last_operation = self.data[column].mean() 
		return self.last_operation

	def percent(self, column):
		self.history()
		recov_data = self.data.copy(deep=True)
		recov_data=recov_data[[column]]*100
		self.last_operation = recov_data.pct_change()
		return self.last_operation

	def median(self, column):
		self.history()
		self.last_operation = self.data[column].median()
		return self.last_operation
	
	def sum(self, column):
		self.history()
		self.last_operation = self.data[column].sum()
		return self.last_operation

	def variance(self, column):
		self.history()
		self.last_operation = self.data[column].var()
		return self.last_operation

	def standart_dev(self, column):
		self.history()
		self.last_operation = math.sqrt(self.data[column].var())
		return self.last_operation

	def min(self, column):
		self.history()
		self.last_operation = self.data[column].min()
		return self.last_operation

	def max(self, column):
		self.history()
		self.last_operation = self.data[column].max()
		return self.last_operation

	def moving_average(self, column):
		self.history()
		recov_data = self.data.copy(deep=True)
		liste = list(recov_data[column])
		#if len(liste)%2 != 0:
		result = [(liste[i-1]+liste[i]+liste[i+1])/3 if i-1 >= 0 and i+1<len(liste) else np.nan for i in range(len(liste))]
		'''
			> Same as

			for i in range(len(liste)):
				if i-1 >= 0 and i+1<len(liste):
					value = (liste[i-1]+liste[i]+liste[i+1])/3
				else:
					value = np.nan
				result.append(value)
		
		#else:
		#	result = [(liste[i-2]/2+liste[i-1]+liste[i]+liste[i+1]+liste[i+2]/2)/4 if i-2 >= 0 and i+2<len(liste) else np.nan for i in range(len(liste))]
		
			> Same as

			for i in range(len(liste)):
				if i-2 >= 0 and i+2<len(liste):
					value = (liste[i-2]/2+liste[i-1]+liste[i]+liste[i+1]+liste[i+2]/2)/4
				else:
					value = np.nan
				result.append(value)
		'''

		recov_data['Price'] = pd.DataFrame({'New':result})['New'].values
		self.last_operation = recov_data
		return self.last_operation



