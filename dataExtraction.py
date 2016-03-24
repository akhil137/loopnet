import pandas as pd
import json

data = []
with open('loopnet-forlease.json') as f:
    for line in f:
        data.append(json.loads(line))

#run these three times to really get rid of error entries
#why?? not sure

error_exists=True
while error_exists:
	error_exists=False
	for a in data:
		if 'error' in a.keys():
			data.remove(a)
			error_exists = True

		

#Turn into a data frame
df=pd.DataFrame.from_dict(data,orient='columns')

#df.shape=(7198,39)
#list col names for reference
#df.columns.values
#------
# array([u'Building_Class', u'Building_Size', u'City', u'Country', u'County',
#        u'Date_Created_', u'FIPS_CO', u'Full_Address',
#        u'Gross_Leasable_Area', u'Last_Updated_', u'Listing_ID_',
#        u'Lot_Size', u'Max_Contiguous', u'Min_Divisible', u'NNN_Expenses',
#        u'POINT', u'Property_Sub_type', u'Property_Use_Type',
#        u'Rental_Rate', u'SHAPE', u'State', u'Total_Space_Available',
#        u'Url', u'Year_Built', u'Zipcode', u'Zoning_Description', u'_id',
#        u'batch-name', u'brokers', u'city-state', u'county-reconciled',
#        u'error', u'full-address', u'geocoded', u'place-reconciled',
#        u'raw-filename', u'raw-object-id', u'source',
#        u'spaces-available-info', u'ts-download'], dtype=object)
#------

#to determine useful (i.e. not mostly NaN) columns, count nans
df.isnull().sum()
# Building_Class           4730*
# Building_Size            1751
# City                     7198
# Country                  7198
# County                   7198
# Date_Created_               0
# FIPS_CO                  7198
# Full_Address             7198
# Gross_Leasable_Area      5657
# Last_Updated_               0
# Listing_ID_                 0
# Lot_Size                 4003
# Max_Contiguous           4421
# Min_Divisible            4023
# NNN_Expenses             6896
# POINT                    7198
# Property_Sub_type           0
# Property_Use_Type        7198
# Rental_Rate              2638
# SHAPE                    7198
# State                    7198
# Total_Space_Available     605*
# Url                         0
# Year_Built               4781*
# Zipcode                  7198
# Zoning_Description       5374*
# _id                         0
# batch-name                  0
# brokers                     0 ??? perhaps broker name could be useful!
# city-state                  0***
# county-reconciled           0
# full-address                0
# geocoded                    0
# place-reconciled            0
# raw-filename                0
# raw-object-id            7198
# source                      0
# spaces-available-info       0***
# ts-download                 0



#sub_df=pd.DataFrame.from_dict(df['spaces-available-info'].to_dict(),orient='columns')
#keys are row number; values are list of dictionaries
tmp=df['spaces-available-info'].to_dict()

#ammend the full-address and 
space_info_list=[]
for k,v in tmp.iteritems():
	tmp_df=pd.DataFrame(v)
	tmp_df['full-address']=df['full-address'][k]
	tmp_df['city']=df['city-state'][k].split(',')[0]
	tmp_df['zipcode']=df['city-state'][k].split(',')[1].split(' ')[2]
	tmp_df['Building_Class']=df['Building_Class'][k]
	tmp_df['Year_Built']=df['Year_Built'][k]
	tmp_df['Total_Space_Available']=df['Total_Space_Available'][k]

	space_info_list.append(tmp_df)

#concatenate to a single large data frame
spaces_df=pd.concat(space_info_list)
#shape - (15682, 18)
#potentially useful features in spaces data
# Clear_Ceiling_Height    14886
# Date_Available          15682
# Lease_Term              12327
# Lease_Type               1575**
# Lot_Size                15530
# Lot_Type                15530
# Max_Contiguous          13348
# Min_Divisible           13886
# NNN_Expenses            15682
# No_Parking_Spaces       11630
# Rental_Rate              6025!!!!Note about 30% of spaces missing rental rate!!!
# Space_Available           152**
# Space_Type                152**
# Sublease                14735
# city                        0**
# full-address                0
# space-label                 0
# zipcode                     0**

#There are many empty (nan) fields, but here are informative ones
#Categorical 
spaces_df['Space_Type'].value_counts()
# Office Building               6428
# Strip Center                  1221
# Medical Office                1119
# Neighborhood Center           1119
# Street Retail                  986
# Retail (Other)                 837
# Creative/Loft                  618
# Warehouse                      529
# Flex Space                     469
# Community Center               378
# Restaurant                     367
# Free Standing Bldg             275
# Executive Suite                244
# Office-R&D                     138
# Manufacturing                  133
# Power Center                    93
# Distribution Warehouse          89
# Vehicle Related                 72
# Retail Pad                      65
# Specialty Center                62
# Office Showroom                 62
# R&D                             59
# Special Purpose (Other)         49
# Anchor                          38
# Regional Center/Mall            25
# Refrigerated/Cold Storage       20
# Super Regional Center           17
# Truck Terminal/Hub/Transit       5
# Outlet Center                    4
# Retail-Pad (land)                3
# Institutional/Governmental       3
# Theme/Festival Center            2
# Retail (land)                    1
spaces_df['Lease_Type'].value_counts()
# NNN                 5455
# Full Service        5214
# Modified Gross      2756
# Industrial Gross     461
# Other                154
# Modified Net          67
spaces_df['city'].value_counts()
# 90010    881
# 92660    259
# 92618    204
# 90045    198
# 90015    189
# 92705    170
# 91101    160
# 90025    157
# 91355    150
# 90013    149
# 91367    148
# 91436    142
# 91356    140
# 90301    131
# 90014    130
# ...
# 90002         1
# 92702         1
# 91207         1
# 90293         1
# 90720-2205    1
# 92845         1
# 92647-2422    1
# 93543         1
# 90077         1
# 92843-1743    1
# 91406-4206    1
# 928041        1
# 92707-5745    1
# 92804-3006    1
# 92843-1602    1
# Length: 370, dtype: int64
spaces_df['zipcode'].value_counts()
# Los Angeles       3707
# Irvine             489
# Pasadena           402
# Long Beach         395
# Santa Ana          371
# Anaheim            343
# Torrance           309
# Newport Beach      309
# Woodland Hills     249
# Glendale           230
# Beverly Hills      221
# Santa Monica       213
# Orange             211
# Encino             208
# Lancaster          196
# ...
# Dove Canyon             3
# La Canada Flintridge    3
# Marina Del Rey          2
# Highland Park           2
# Arleta                  2
# Playa Vista             2
# Anaheim Hills           1
# Balboa Island           1
# Littlerock              1
# Villa Park              1
# Playa del Rey           1
# Westchester             1
# Eagle Rock              1
# Lennox                  1
# West Adams              1
# Length: 176, dtype: int64