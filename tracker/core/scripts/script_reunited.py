import loader
import os
import pandas as pd

if __name__ == '__main__':
	indexes_to_keep = list()
	
	df = loader.get_df_from_excel('/Users/xxx/Projects/SBB/stocksV2_noadidas.xlsx')

	dirs = os.listdir('/Users/xxx/Projects/SBB/scrapping_data_consolidated')

	idx = 0
	for index, rows in df.iterrows():
		for x in dirs:
			print(x)
			if x in rows['Website']:
				print(rows['Website'])
				idx += 1
				indexes_to_keep.append(index)

	print('indexes_to_keep = {}'.format(indexes_to_keep))
	print('len index to keep = {}'.format(len(indexes_to_keep)))

	df_copy = df.copy()

	for index, rows in df.iterrows():
		if index not in indexes_to_keep:
			df_copy.drop(index, axis=0, inplace=True)
	
	df_copy.reset_index(drop=True, inplace=True)
	#df_copy = df_copy.drop(df_copy.columns[0],axis=1)
	print(len(df_copy))
	print(df_copy.tail())

	writer = pd.ExcelWriter('/Users/xxx/Projects/SBB/scrapping_data_consolidated.xlsx')

	df_copy.to_excel(writer, 'Sheet1')
	writer.save()