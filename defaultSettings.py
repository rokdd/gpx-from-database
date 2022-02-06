# rename this file to settings.py
CONFIG=dict(
	{
		'postgresql':{
			'user':'',
			'password':'',
			'host':'localhost',
			'port':'5432',
			'database':'nxcloud'
		},
		# for nextcloud db: your db, schema=publoc and table=oc_phonetrack_points
		'table':'<db>.<schema>.<table>',
        'fields':{
		'timestamp':'timestamp',
	    'lat':'lat',
	    'lon':'lon',
		'elevation':'altitude',
		'speed':'speed',
		},

    }
)