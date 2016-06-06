import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas.plotting import plot_multipolygon
import seaborn as sns; sns.set()


def top5(input_list):
	# makes a dict of strings -> no. of appearances
	# returns the top ten strings and no. of appearances

	counter_dict = {}
	
	for word in input_list:
		if word in counter_dict:
			counter_dict[word] += 1
		else:
			counter_dict[word] = 1

	most_common = sorted(counter_dict, key = counter_dict.get, 
                             reverse = True)

	top_5 = [[],[]]
	for i in range(5):
		word = most_common[i]
		top_5[0].append(word)
		top_5[1].append(counter_dict[word])

	return top_5


def map_county_townlands(county, ireland=False, t_df=None):
	# plots the townlands in a given county,
	# if the ireland keyword is true it adds the 
	# the other counties for context

	all_twnlds = gpd.GeoDataFrame.from_file('data/townlands.shp')
	county = all_twnlds[all_twnlds.CO_NAME == county]	

	if ireland:
		map_counties(t_df)
	
	county.plot(colormap='winter')

def map_counties(t_df, townland_density=False, name=''):


	counties = gpd.GeoDataFrame.from_file('data/counties.shp')
	
	if townland_density:
		counties['Density'] = counties.apply( lambda row:
				(t_df.groupby('CO_NAME').CO_NAME.count()[row.NAME_TAG]/row.AREA)*1e6, axis=1)
		# add a towlands/km^2 column
		counties.Density.iloc[21] = counties.Density.iloc[21]/0.58
		# Kerry has an incomplete survey, so I scale it by the % surveyed.
		# This is obviously a cheat, assuming that the townlands left will have the same average are as those
		# already done, but it's better than leaving it out 	

		# add a colour bar. this is gross.
		vmin, vmax = counties.Density.min(), counties.Density.max()

		ax = counties.plot(column='Density', scheme='equal_interval', 
				k=5, colormap='OrRd', alpha=0.5)
		plt.title(r'Townlands per km$^2$')
		fig = ax.get_figure()
		cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
		sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
		
		sm._A = []
		fig.colorbar(sm, cax=cax)
		
		# also plot a bar chart, with a mean-line
		plt.figure()
		ax = counties.sort('NAME_TAG').set_index('NAME_TAG').Density.plot(kind='bar') 

		ax.axhline(counties.Density.mean(), color='r', linewidth=2, linestyle='--')
		ax.set_ylabel(r'Townlands/km$^2$')

	else: # if the key word isn't set

		# plot counties
		counties.plot(colormap='Greens', alpha=0.3, axes=None)
		
		if len(name) != 0:
			# if a string is given, then add scatter
			# points of townlands starting with that string
		
			name_in = [i.upper().startswith(name.upper()) for i in t_df.NAME_TAG.values] 
			place_w_name = t_df[name_in]
			
			t_df['Name_in'] = [i.upper().startswith(name.upper()) for i in t_df.NAME_TAG.values]			
			print t_df.groupby('CO_NAME').Name_in.sum()

			plt.scatter(place_w_name.LONGITUDE.values, place_w_name.LATITUDE.values, s=3, color='r')
			plt.title('Townlands with names starting with ' + name[0].upper() + name[1:])
			


if __name__ == '__main__':

	df = pd.read_csv('data/townlands-no-geom.csv')
	ga_names = df[df.NAME_GA.notnull()].NAME_GA.values	
	first_words = [i.split(' ')[0] for i in ga_names]
	print('The most common first words in Irish are\n')
	print top5(first_words)	


	print('The most common beginnings to names are:\n')
	print top5([i[:5] for i in df.NAME_TAG.values])	

#	map_county_townlands('Kerry', t_df=df, ireland=True)
	map_counties(df, name='balli')

	plt.show()

