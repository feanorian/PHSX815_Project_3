"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 13
Due Date 4/10/2023
This script will determine the maximum likelihood estimate (MLE) for p = the probability of drawing a White/Black marble, determine the confidence interval and uncertainty,
then plot the empirical histogram and best fit, 
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random
import scipy.stats as st 
from scipy.stats import bernoulli


if __name__ == "__main__":

	if '-f' in sys.argv:
		p = sys.argv.index('-f')
		InputFile = sys.argv[p+1]
	if '-t' in sys.argv:
		p = sys.argv.index('-t')
		urn = sys.argv[p+1]
	if '-u' in sys.argv:
		p = sys.argv.index('-u')
		urn_number = sys.argv[p+1]

	InputFiles = InputFile.strip('][').split(', ')

	# contains list of tables
	table_list = []
	for i in range(len(InputFiles)):
		with open(InputFiles[i]) as file:
			table = pd.read_csv(file)
			table.drop(columns=table.columns[0], axis=1, inplace=True)
			table_list.append(table)
			#print(table.head())
		

	table_10 = table_list[0]
	table_100 = table_list[1]
	table_1000 = table_list[2]
	table_10000 = table_list[3]

	# Generate some sample outcome
	#outcome = table[f'Trial {urn}']
	outcome = [table_10, table_100, table_1000, table_10000] 
	# Define the likelihood function for a Bernoulli distribution
	def likelihood(p, outcome):
		return np.prod(bernoulli.pmf(outcome, p))

	# Define a function to maximize the likelihood function
	def maximum_likelihood_estimation(outcome):
		# Initial guess for the probability parameter
		p_init = np.mean(outcome)

		# Use scipy.optimize.minimize to maximize the likelihood function
		from scipy.optimize import minimize
		result = minimize(lambda params: likelihood(params[0], outcome), [p_init], method='L-BFGS-B')
		return result.x
	mle_array_tot = []
	for table in outcome:

		mle_array = []
		# Calculate the maximum likelihood estimate for the sample outcome
	
		for columns in table:
			mle = maximum_likelihood_estimation(table[columns])
			mle_array.append(mle[0])
		mle_array_tot.append(mle_array)
		print(f"Maximum likelihood estimate for p: {np.mean(mle_array)}")
	
		x_95 = np.quantile(mle_array, [.05,.95])
		uncert = round(np.std(mle_array)/np.sqrt(len(mle_array)), 4)
		textstr = '\n'.join((
			rf'.95 CL = {x_95}',
			rf'$\sigma$ ={uncert}'))

		# Plot the likelihood function
		p_values = np.linspace(0, 1, 1000)
		likelihood_values = [likelihood(p, table) for p in p_values]
		plt.plot(p_values, np.log(likelihood_values))
		plt.axvline(np.mean(mle_array), linestyle='--', color='red', label=f'MLE of p = {round(np.mean(mle_array),4)}')
		plt.xlabel('p')
		plt.ylabel('Log-Likelihood')
		plt.annotate(textstr, xy=(0.2, 0.5), xycoords='axes fraction')

		plt.legend()
		plt.savefig(f'mle_urn_{urn_number}_{len(table)}')
		plt.show()

	box = pd.DataFrame(mle_array_tot)
	box = box.T
	box.rename(columns={0: "10", 1: "100", 2: "1000", 3 : "10000"}, inplace = True)
	sns.pointplot(data=box[['10', '100', '1000', '10000']], join=False, ci=95)
	#sns.boxplot(data=box[['10', '100', '1000', '10000']]) #draws boxplot instead
	plt.xlabel('Number of draws')
	plt.ylabel('range of p')
	plt.title(f'95 % C.L. of estimates for p for draw counts')
	#plt.savefig(f'CL_95_Urn_{urn_number}')
	plt.show()


