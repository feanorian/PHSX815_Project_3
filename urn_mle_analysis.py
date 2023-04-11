"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 13
Due Date 4/10/2023
This script will determine the maximum likelihood estimate (MLE) for p = the probability of drawing a White/Black marble, determine the confidence interval and uncertainty,
then plot the empirical histogram and best fit, 
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random
import scipy.stats as st 

if __name__ == "__main__":

	if '-f1' in sys.argv:
		p = sys.argv.index('-f1')
		InputFile1 = sys.argv[p+1]
	
	if '-f2' in sys.argv:
		p = sys.argv.index('-f2')
		InputFile2 = sys.argv[p+1]
	
	with open(InputFile1) as file1, open(InputFile2) as file2:
		table = pd.read_csv(file1)
		means = pd.read_csv(file2)
		#print(table.head())
		print(means)
	
	# Arrays that store the fractions of White marbles per trial for each urn to be plotted in histogram
	urn1_White = table['Urn1W'] #/ (max(table['Urn1W']) + min(table['Urn1B']))
	urn2_White = table['Urn2W'] #/ (max(table['Urn1W']) + min(table['Urn1B']))
	urn3_White = table['Urn3W'] #/ (max(table['Urn1W']) + min(table['Urn1B']))

	urn1_Black = table['Urn1B'] #/ (max(table['Urn1W']) + min(table['Urn1B']))
	urn2_Black = table['Urn2B'] #/ (max(table['Urn1W']) + min(table['Urn1B']))
	urn3_Black = table['Urn3B'] #/ (max(table['Urn1W']) + min(table['Urn1B']))

	delta = min(urn1_Black) + max(urn1_White)
	# bounds is the number of observations per trial and the domain of the probability
	bounds = [(0, np.mean(urn1_White) + .5 * np.mean(urn1_White)), (0, 1)]

	#distribution to fit to data
	dist = st.binom

	# function calls to minimize the binomial distribution and fit the data
	res_urn1_white = st.fit(dist, urn1_White, bounds)
	res_urn1_black = st.fit(dist, urn1_Black, bounds)

	res_urn2_white = st.fit(dist, urn2_White, bounds)
	res_urn2_black = st.fit(dist, urn2_Black, bounds)

	res_urn3_white = st.fit(dist, urn3_White, bounds)
	res_urn3_black = st.fit(dist, urn3_Black, bounds)

	# Confidence intervals for each color in each urn
	urn1_CI_White = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 1'][0]) 
	urn2_CI_White = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 2'][0]) 
	urn3_CI_White = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 3'][0]) 

	urn1_CI_Black = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 1'][1]) 
	urn2_CI_Black = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 2'][1]) 
	urn3_CI_Black = st.binom.interval(confidence = .95, n=len(urn1_White), p = means['Urn 3'][1]) 

	#print(urn1_CI_White, urn1_CI_Black)
	#print(urn2_CI_White, urn2_CI_Black)
	#print(urn3_CI_White, urn3_CI_Black)

	#print(res_urn1_white.params, res_urn1_black.params)
	#print(res_urn2_white.params, res_urn2_black.params)
	#print(res_urn3_white.params, res_urn3_black.params)




	ax1 = res_urn1_white.plot()
	ax1.legend([f'MLE: p = {round(res_urn1_white.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn1_White)/(len(urn1_White)*np.sqrt(len(urn1_White))), 5)}'])
	#plt.xlabel('p')
	plt.title(f'MLE of p for White Marbles in Urn 1 ({len(urn1_White)} draws)')
	#plt.xlim(urn1_CI_White[0] -.2*urn1_CI_White[0] ,urn1_CI_White[1] +.2*urn1_CI_White[1])
	plt.savefig(f'urn1_White{len(urn1_White)}')
	plt.show()

	ax2 = res_urn2_white.plot()
	ax2.legend([f'MLE: p = {round(res_urn2_white.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn2_White)/(len(urn1_White)*np.sqrt(len(urn1_White))), 5)}'])
	#plt.xlim(urn2_CI_White[0] -.2*urn2_CI_White[0] ,urn2_CI_White[1] +.2*urn2_CI_White[1])
	plt.title(f'MLE of p for White Marbles in Urn 2 ({len(urn1_White)} draws)')
	#plt.xlabel('p')
	plt.savefig(f'urn2_White{len(urn1_White)}')
	plt.show()

	ax3 = res_urn3_white.plot()
	ax3.legend([f'MLE: p = {round(res_urn3_white.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn3_White)/(len(urn1_White)*np.sqrt(len(urn1_White))), 5)}'])
	#plt.xlabel('p')
	plt.title(f'MLE of p for White Marbles in Urn 3 ({len(urn1_White)} draws)')
	#plt.xlim(urn3_CI_White[0] -.2*urn3_CI_White[0] ,urn3_CI_White[1] +.2*urn3_CI_White[1])
	plt.savefig(f'urn3_White{len(urn1_White)}')
	plt.show()

	ax4 = res_urn1_black.plot()
	ax4.legend([f'MLE: p = {round(res_urn1_black.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn1_Black)/(len(urn1_White)*np.sqrt(len(urn1_White))), 5)}'])
	#plt.xlabel('p')
	plt.title(f'MLE of p for Black Marbles in Urn 1 ({len(urn1_White)} draws)')
	#plt.xlim(urn1_CI_Black[0]-.2*urn1_CI_Black[0] ,urn1_CI_Black[1] +.2*urn1_CI_Black[1])
	plt.savefig(f'urn1_Black{len(urn1_White)}')
	plt.show()

	ax5 = res_urn2_black.plot()
	ax5.legend([f'MLE: p = {round(res_urn2_black.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn2_Black)/(len(urn1_White)*np.sqrt(len(urn1_White))), 5)}'])
	#plt.xlabel('p')
	plt.title(f'MLE of p for Black Marbles in Urn 2 ({len(urn1_White)} draws)')
	#plt.xlim(urn2_CI_Black[0]-.2*urn2_CI_Black[0],urn2_CI_Black[1] +.2*urn2_CI_Black[1])
	plt.savefig(f'urn2_Black{len(urn1_White)}')
	plt.show()

	ax6 = res_urn3_black.plot()
	ax6.legend([f'MLE: p = {round(res_urn3_black.params[1], 3)}', r'Data: $\frac{\sigma}{\sqrt{n}}$:' f'{round(np.std(urn3_Black)/(len(urn1_White)*np.sqrt(len(urn1_White))),5)}'])
	#plt.xlabel('p')
	plt.title(f'MLE of p for Black Marbles in Urn 3 ({len(urn1_White)} draws)')
	#plt.xlim(urn3_CI_Black[0]/2 ,urn3_CI_Black[1] +.2[1])
	plt.savefig(f'urn3_Black{len(urn1_White)}')
	plt.show()
