"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 3
Due Date 4/10/2023
This code generates samples from 3 urns with White and Black marbles where the user defines the number sample for each trial and the number of trials. 
This data is written to a file and which another script, 'urn_mle_analysis' will determine the maximum likelihood estimate (MLE) for p = the probability 
of drawing a White/Black marble
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random
from scipy.stats import bernoulli

if __name__ == "__main__":


	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s [-t -n]" % sys.argv[0])
		print
		sys.exit(1)
	if '-t' in sys.argv:
		p = sys.argv.index('-t')
		trials = int(sys.argv[p+1])
	else:
		trials = 10
	if '-n' in sys.argv:
		p = sys.argv.index('-n')
		N_marbles_sample = int(sys.argv[p+1])
	else:
		N_marbles_sample = 100

	np.random.seed(677)

	#Number of urns
	n_urns = 3
	# Number of trials
	trials = 10
	
	# constructs an urn  passing the number of rolls and the probability. Here, the number of marbles is set to N = 100000
	
	# alpha to generate dispersion of propbabilities
	alpha = [1,1]


	# Urns generated with different ratios
	InputFile = 'urn_data_mle_frac.csv'
	haveUrns = True
	if haveUrns == True:
		with open(InputFile) as file:
			means = pd.read_csv(file,usecols=[1,2,3])
			#print(means)
		means1 = means['Urn 1'].values.tolist()
		means2 = means['Urn 2'].values.tolist()
		means3 = means['Urn 3'].values.tolist()
		urns = [means1, means2, means3]
	else:
		urns = np.random.dirichlet(alpha, n_urns)

	# Function that constructs an urn  passing the number of trials and probability array for the urn. 
	def bern(p, n):
		x = bernoulli.rvs(p, size=n)
		return x

	urn_data = []
	for urn in urns:
		urn_test = []
		for _ in range(trials):
			urn_trials = bern(urn[0],N_marbles_sample)
			urn_test.append(urn_trials) 
		urn_data.append(urn_test)


	#urns_dic = {'Urn 1': urn_data[0], 'Urn 2': urn_data[1], 'Urn 3': urn_data[2]}
	
	urn_1_dic = {f'Trial {i+1}': urn_data[0][i] for i in range(len(urn_data[0]))}
	urn_1_df = pd.DataFrame(urn_1_dic)

	urn_2_dic = {f'Trial {i+1}': urn_data[1][i] for i in range(len(urn_data[1]))}
	urn_2_df = pd.DataFrame(urn_2_dic)

	urn_3_dic = {f'Trial {i+1}': urn_data[1][i] for i in range(len(urn_data[2]))}
	urn_3_df = pd.DataFrame(urn_3_dic)

	urn_array = [urn_1_df, urn_2_df, urn_3_df]

	for i in range(len(urn_array)):
		urn_array[i].to_csv(f'urn_{i+1}_data_mle_{N_marbles_sample}.csv')
'''
	urn_df = pd.DataFrame(urns_dic)
	urn_df.to_csv(f'urn_data_mle_{N_marbles_sample}.csv')
	if haveUrns == False:
		urns_frac_dic = {'Urn 1':urns[0], 'Urn 2':urns[1], 'Urn 3': urns[2]}
		urns_frac_df = pd.DataFrame(urns_frac_dic)
		urns_frac_df.to_csv('urn_data_mle_frac.csv')
	

	sns.histplot(urn1_Black, element="step",fill = True, color = 'salmon', bins='auto', label='Urn 1')
	sns.histplot(urn2_Black, element="step",fill = True, color = 'violet', bins='auto', label='Urn 2', alpha = .25)
	sns.histplot(urn3_Black, element="step",fill = True, color = 'aqua', bins='auto', label='Urn 3')
	plt.legend(loc='center')
	plt.title(f'Black/total per urn for {len(urn1_Black)} trials per urn')  
	plt.xlabel('Black/Total')
	#plt.savefig(f'black_urns{trials}', dpi=700)
	plt.show()

