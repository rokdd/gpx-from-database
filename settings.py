from baseSettings import *

CONFIG={
	'table':'<yourdb>.public.oc_phonetrack_points',
        'fields':{
		'timestamp':'timestamp',
	    'lat':'lat',
	    'lon':'lon',
		'elevation':'altitude',
		'speed':'speed',
		},
    }


CONFIG['postgresql']=dict(database="<yourdb>", user='<your db user>', password='', host='localhost', port='5432')
