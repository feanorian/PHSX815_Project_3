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

if __name__ == "__main__":

	if '-f' in sys.argv:
		p = sys.argv.index('-f')
		InputFile = sys.argv[p+1]
	
	with open(InputFile) as file:
		table = pd.read_csv(file)
		print(table.head())

	# Arrays that store the fractions of White marbles per trial for each urn to be plotted in histogram
	urn1_White = table['Urn1W']
	urn2_White = table['Urn2W']
	urn3_White = table['Urn3W']

	urn1_Black = table['Urn1B']
	urn2_Black = table['Urn2B']
	urn3_Black = table['Urn3B']


	# bounds is the number of observations per trial abd the domain of the probability
	bounds = [(0, len(urn1_White) +1), (0, 1)]

	#distribution to fit to data
	dist = st.binom

	# data from urn 1
	data_u1_white = urn1_White
	data_u1_black= urn1_Black

	# data from urn 2
	data_u2_white = urn2_White
	data_u2_black= urn2_Black

	#data from urn 3
	data_u3_white = urn3_White
	data_u3_black= urn3_Black

	# function calls to minimize the binomial distribution and fit the data
	res_urn1_white = st.fit(dist, data_u1_white, bounds)
	res_urn1_black = st.fit(dist, data_u1_black, bounds)

	res_urn2_white = st.fit(dist, data_u2_white, bounds)
	res_urn2_black = st.fit(dist, data_u2_black, bounds)

	res_urn3_white = st.fit(dist, data_u3_white, bounds)
	res_urn3_black = st.fit(dist, data_u3_black, bounds)

	# Confidence intervals for each color in each urn

	urn1_CI_White = st.norm.interval(alpha = .95, loc=np.mean(urn1_White)) #, scale=st.sem(data_u1_white))
	urn2_CI_White = st.norm.interval(alpha = .95, loc=np.mean(urn2_White)) #, scale=st.sem(data_u2_white))
	urn3_CI_White = st.norm.interval(alpha = .95, loc=np.mean(urn3_White)) #, scale=st.sem(data_u3_white))

	urn1_CI_Black = st.norm.interval(alpha = .95, loc=np.mean(urn1_Black)) #, scale=st.sem(data_u1_black))
	urn2_CI_Black = st.norm.interval(alpha = .95, loc=np.mean(urn2_Black)) #, scale=st.sem(data_u2_black))
	urn3_CI_Black = st.norm.interval(alpha = .95, loc=np.mean(urn3_Black)) #, scale=st.sem(data_u3_black))

	print(urn1_CI_White, urn1_CI_Black)
	print(urn2_CI_White, urn2_CI_Black)
	print(urn3_CI_White, urn3_CI_Black)

	#print(res_urn1_white.params, res_urn1_black.params)
	#print(res_urn2_white.params, res_urn2_black.params)
	#print(res_urn3_white.params, res_urn3_black.params)

	ax1 = res_urn1_white.plot()
	ax1.legend([f'MLE: n = {res_urn1_white.params[0]}, p = {round(res_urn1_white.params[1], 3)}', 'Data'])
	#plt.xlabel('p')
	plt.title('Maximim Likelihood Estimation of p for White Marbles in Urn 1')
	plt.xlim(0,len(urn1_White))
	plt.show()

	ax2 = res_urn2_white.plot()
	ax2.legend([f'MLE: n = {res_urn2_white.params[0]},p = {round(res_urn2_white.params[1], 3)}', 'Data'])
	plt.xlim(0,len(urn2_White))
	plt.title('Maximim Likelihood Estimation of p for White Marbles in Urn 2')
	#plt.xlabel('p')
	plt.show()

	ax3 = res_urn3_white.plot()
	ax3.legend([f'MLE: n = {res_urn3_white.params[0]}, p = {round(res_urn3_white.params[1], 3)}', 'Data'])
	#plt.xlabel('p')
	plt.title('Maximim Likelihood Estimation of p for White Marbles in Urn 3')
	plt.xlim(0,len(urn3_White))
	plt.show()

	ax4 = res_urn1_black.plot()
	ax4.legend([f'MLE: n = {res_urn1_black.params[0]}, p = {round(res_urn1_black.params[1], 3)}', 'Data'])
	#plt.xlabel('p')
	plt.title('Maximim Likelihood Estimation of p for Black Marbles in Urn 1')
	plt.xlim(0,len(urn1_Black))
	plt.show()

	ax5 = res_urn2_black.plot()
	ax5.legend([f'MLE: n = {res_urn2_black.params[0]},  p = {round(res_urn2_black.params[1], 3)}', 'Data'])
	#plt.xlabel('p')
	plt.title('Maximim Likelihood Estimation of p for Black Marbles in Urn 2')
	plt.xlim(0,len(urn2_Black))
	plt.show()

	ax6 = res_urn3_black.plot()
	ax6.legend([f'MLE: n = {res_urn3_black.params[0]},  p = {round(res_urn3_black.params[1], 3)}', 'Data'])
	#plt.xlabel('p')
	plt.title('Maximim Likelihood Estimation of p for Black Marbles in Urn 3')
	plt.xlim(0,len(urn3_Black))
	plt.show()
