"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 13
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


if __name__ == "__main__":


	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s [-t -n]" % sys.argv[0])
		print
		sys.exit(1)
	if '-t' in sys.argv:
		p = sys.argv.index('-t')
		trials = int(sys.argv[p+1])
	else:
		trials = 100
	if '-n' in sys.argv:
		p = sys.argv.index('-n')
		N_marbles_sample = int(sys.argv[p+1])
	else:
		N_marbles_sample = 100
	

	np.random.seed(677)

	#Number of urns
	n_urns = 3
	# Number of Marbles per urn
	N_marbles_urn = 10000
	# constructs an urn  passing the number of rolls and the probability. Here, the number of marbles is set to N = 100000
	
	# alpha to generate dispersion of propbabilities
	alpha = [1,1]

	occurences_list = []
	
	# outcomes of each urn as strings
	outcomes_list = []
	
	# outcomes of each urn as ints
	outcomes_int = []
	

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
	def Category(trials, prob):
		x = np.random.multinomial(trials, prob, 1)
		return x



	# function that takes the urns stored in outcomes_list and samples N_picks for N_Trials each
	def color_samples(N_Trials, N_picks):
		
			

		urn_samples = []
		for urn in outcomes_list:
			sublist = []
			for _ in range(N_Trials):
				urnH0_draws = random.sample(urn,N_picks)
				sublist.append(urnH0_draws)
			urn_samples.append(sublist)
			
		# store the draws as color data
		urnh0_draws_colors = []
		# converts the draws from urnH0_draws into colors
		for urn in urn_samples:
			colors = []
			for trial in urn:
				color = []
				for i in range(len(trial)):
					if trial[i] == '1':
						color.append('White')
					else:
						color.append('Black')
				colors.append(color)
			urnh0_draws_colors.append(colors)
		return urnh0_draws_colors

	# function to obtain the ratios/numbers of white and black marbles per trial per urn
	def counts(urn_samp):
		white_urn_counts = []
		black_urn_counts = [] 
		for urn in urn_samp:
			white_count = []
			black_count = []
			for trial in urn:
				w_count = trial.count('White')
				white_count.append(w_count)
				b_count = trial.count('Black')
				black_count.append(b_count)
			white_urn_counts.append(white_count)
			black_urn_counts.append(black_count)
		return [white_urn_counts, black_urn_counts]

	occurences_list = []
	# outcomes of each urn as strings
	outcomes_list = []
	
	# outcomes of each urn as ints
	outcomes_int = []
	
	
	print(urns)
	# constructs an urn  passing the number of rolls and the probability. Here, the number of marbles is set to N = 100000
	for urn in urns:
		occurences = Category(N_marbles_urn, urn)[0]
		occurences_list.append(occurences)
	for urn in occurences_list:
		outcome = []
		for i in range(len(urn)):
			outcome += str(i+1)*urn[i]
			
		outcomes_list.append(outcome)


	#function call to begin sampling with 30 Trials and 1000 marbles per urn
	urn_samp = color_samples(trials, N_marbles_sample)
	
	# function call to obtain the fractio of white marbles in the trials
	urns_combined = counts(urn_samp)
	white = urns_combined[0]
	black = urns_combined[1]
	

	# Arrays that store the fractions of White marbles per trial for each urn to be plotted in histogram
	urn1_White = white[0]
	urn2_White = white[1]
	urn3_White = white[2]

	urn1_Black = black[0]
	urn2_Black = black[1]
	urn3_Black = black[2]

	# stores data in a dictionary and converts to a DataFrame to write to a .csv file
	urns_dic = {'Urn1W': urn1_White, 
		'Urn1B': urn1_Black, 
		'Urn2W': urn2_White, 
		'Urn2B': urn2_Black,
		'Urn3W': urn3_White, 
		'Urn3B': urn3_Black}
	
	urn_df = pd.DataFrame(urns_dic)
	urn_df.to_csv(f'urn_data_mle_{trials}.csv')
	if haveUrns == False:
		urns_frac_dic = {'Urn 1':urns[0], 'Urn 2':urns[1], 'Urn 3': urns[2]}
		urns_frac_df = pd.DataFrame(urns_frac_dic)
		urns_frac_df.to_csv('urn_data_mle_frac.csv')

	# plots histograms for every urn. Uncomment plt.savefig() to save image
	sns.histplot(urn1_White, element="step",fill = True, color = 'salmon', bins='auto', label='Urn 1')
	sns.histplot(urn2_White, element="step",fill = True, color = 'violet', bins='auto', label='Urn 2', alpha = .25)
	sns.histplot(urn3_White, element="step",fill = True, color = 'aqua', bins='auto', label='Urn 3')
	plt.legend(loc='center')
	plt.title(f'white/total per urn for {len(urn1_White)} trials per urn')  
	plt.xlabel('White/Total')
	#plt.savefig(f'white_urns{trials}', dpi= 700)
	plt.show()
	

	sns.histplot(urn1_Black, element="step",fill = True, color = 'salmon', bins='auto', label='Urn 1')
	sns.histplot(urn2_Black, element="step",fill = True, color = 'violet', bins='auto', label='Urn 2', alpha = .25)
	sns.histplot(urn3_Black, element="step",fill = True, color = 'aqua', bins='auto', label='Urn 3')
	plt.legend(loc='center')
	plt.title(f'Black/total per urn for {len(urn1_Black)} trials per urn')  
	plt.xlabel('Black/Total')
	#plt.savefig(f'black_urns{trials}', dpi=700)
	plt.show()

