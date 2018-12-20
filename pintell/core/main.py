from project import Project

# real project
sbb_project = Project('data_example', '/Users/xxx/Projects/SBB', '/Users/xxx/Projects/SBB/data_example.xlsx')
sbb_project._load_units_from_data_path()

# filter some units
#sbb_project.units_stats(units=sbb_project.filter_units(minimum_pages=2000), verbose=True)

# delete content downloaded from units
#sbb_project.delete_downloaded_units(['https://www.db.com'])

'''
# download some parts of websites
units_regex = {
	'https://www.accorhotels.group':['/en/investors']
}
sbb_project.download_units(units_regex)

sbb_project.units_stats(units=sbb_project.filter_units(minimum_pages=10), verbose=True)

# check if changes have been made since last download
sbb_project.get_unit_from_url('https://www.accorhotels.group').download_changed_files('/en/investors', force=True)
'''