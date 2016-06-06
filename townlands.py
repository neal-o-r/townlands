import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


def top10(input_list):
	# makes a dict of strings -> no. of appearances
	# returns the top ten strings

	counter_dict = {}
	
	for word in input_list:
		if word in counter_dict:
			counter_dict[word] += 1
		else:
			counter_dict[word] = 1

	most_common = sorted(counter_dict, key = counter_dict.get, 
                             reverse = True)

	top_10 = []
	for i in range(10):
		word = most_common[i]
		word_tuple = (word, counter_dict[word])
		top_10.append(word_tuple)

	return top_10

def map_county_townlands(county, ireland=False):
	
	import geopandas as gpd
	all_twnlds = gpd.GeoDataFrame.from_file('data/townlands.shp')
	county = all_twnlds[all_twnlds.CO_NAME == county]	

	if ireland:
		counties = gpd.GeoDataFrame.from_file('data/counties.shp')
		counties.plot(colormap='Greens', alpha=0.3)
	
	county.plot(colormap='winter')
	plt.show()

def map_counties(t_df, townland_density=False):

	import geopandas as gpd
	counties = gpd.GeoDataFrame.from_file('data/counties.shp')
	
	if townland_density:
		counties['Density'] = counties.apply( lambda row:
				(t_df.groupby('CO_NAME').CO_NAME.count()[row.NAME_TAG]/row.AREA)*1e6, axis=1)
	
		vmin, vmax = counties.Density.min(), counties.Density.max()

		ax = counties.plot(column='Density', scheme='equal_interval', k=5, colormap='OrRd', alpha=0.5)
		
		fig = ax.get_figure()
		cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
		sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
		# fake up the array of the scalar mappable. Urgh...
		sm._A = []
		fig.colorbar(sm, cax=cax)
		
		plt.figure()
		ax = (counties.sort('NAME_TAG')).Density.plot(kind='bar') 
		ax.axhline(counties.Density.mean(), color='r', linewidth=2, linestyle='--')
		ax.set_ylabel(r'Townlands/km$^2$')
		ax.set_xticklabels(counties.sort('NAME_TAG').NAME_TAG.values)

	else:
		counties.plot(colormap='Greens', alpha=0.3)

	plt.show()



if __name__ == '__main__':

	df = pd.read_csv('townlands-no-geom.csv')
	ga_names = df[df.NAME_GA.notnull()].NAME_GA.values	

	first_words = [i.split(' ')[0] for i in ga_names]
	
	print('The most common first words in Irish are:\n')
	for i in top10(first_words)[:5]:
		print(i[0] + ' appears %d times' %i[1])

	names = df.NAME_TAG.values
	beginnings = []
	for i in range(1,7):
		beginnings.extend(top10([x[:i] for x in names]))

	print('The most common ')

	#map_county_townlands('Galway')
	#map_counties(df, townland_density=True)

