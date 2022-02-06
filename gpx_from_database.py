

from datetime import timezone,datetime,timedelta

def day_to_timestamp(date):
    start = int(datetime(date.year, date.month, date.day, tzinfo=date.tzinfo).astimezone(timezone.utc).timestamp())
    return (start,start+(60*60*24))


import psycopg2
from psycopg2.extras import RealDictCursor
import gpxpy
import gpxpy.gpx
import os
from settings import DESTINATION_DIR

class core:
    jobs=[]
    @classmethod
    def plan(cls,config):
        cls.config=config

    @classmethod
    def job_export_total(cls,timestamp_start,timestamp_end):
        cls.queue(
            {'query': '''SELECT * from %s WHERE %s>=%s AND %s<=%s %s''' % (
            cls.config['table'],  cls.config['fields']['timestamp'], day_to_timestamp(timestamp_start)[0],
            cls.config['fields']['timestamp'], day_to_timestamp(timestamp_end)[1],
            cls.config['custom_where'] if 'custom_where' in cls.config else ""),
             'filename': "%s-%s.gpx" % (timestamp_start.strftime("%Y%m%d"), timestamp_end.strftime("%Y%m%d"))
             })

    @classmethod
    def job_export_daily(cls,timestamp_start,timestamp_end):
        # split by day (or something else)
        delta = timedelta(days=1)
        start_date = timestamp_start
        while start_date <= timestamp_end:
            cls.queue(
                {'query': '''SELECT * from %s WHERE %s>=%s AND %s<=%s %s''' % (
                    cls.config['table'], cls.config['fields']['timestamp'], day_to_timestamp(start_date)[0],
                    cls.config['fields']['timestamp'], day_to_timestamp(start_date)[1],
                    cls.config['custom_where'] if 'custom_where' in cls.config else ""),
                 'filename': "%s.gpx" % (start_date.strftime("%Y%m%d"))
                 })
            start_date += delta

    @classmethod
    def queue(cls,job):
        core.jobs.append(job)

    @classmethod
    def run(cls):

        # establishing the connection

        if 'postgresql' in cls.config:
            conn = psycopg2.connect(**cls.config['postgresql'])
            conn.autocommit = True
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            print('Please config the database in the settings.py')
            os.abort()

        for job in cls.jobs:

            # Retrieving data
            cursor.execute(job['query'])

            # Fetching 1st row from the table
            result = cursor.fetchall();

            gpx = gpxpy.gpx.GPX()

            # Create first track in our GPX:
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)

            # Create first segment in our GPX track:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

            # Create points:
            for geopos in result:
                print(geopos)
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(geopos["lat"], geopos["lon"], speed=geopos["speed"],
                                                                  time=datetime.utcfromtimestamp(geopos["timestamp"]),
                                                                  elevation=geopos["altitude"]))

            # and write
            with open(os.path.join(DESTINATION_DIR,job['filename']), "w") as f:
                f.write(gpx.to_xml())

        # Commit your changes in the database
        conn.commit()

        # Closing the connection
        conn.close()