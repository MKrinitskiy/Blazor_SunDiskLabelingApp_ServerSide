
CREATE_TRACKS_TABLE_QUERY_TEXT = '''CREATE TABLE tracks (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, ''' + \
                                 '''                     start_dt TEXT, ''' + \
                                 '''                     end_dt TEXT, ''' + \
                                 '''                     track_uid TEXT NOT NULL UNIQUE, ''' + \
                                 '''                     human_readable_name TEXT NOT NULL)'''


CREATE_LABELS_TABLE_QUERY_TEXT = '''CREATE TABLE labels (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, ''' + \
                                 '''               label_uid TEXT NOT NULL UNIQUE, ''' + \
                                 '''               dt TEXT NOT NULL, ''' + \
                                 '''               sourcedata_fname TEXT NOT NULL)'''



CREATE_TRACK_LABELS_QUERY_TEXT = '''CREATE TABLE track_labels (label_id INTEGER NOT NULL, ''' + \
                                 '''                           track_id INTEGER NOT NULL)'''


INSERT_TRACK_QUERY_TEXT = '''INSERT OR IGNORE INTO tracks (track_uid, human_readable_name) ''' + \
                          '''                      VALUES ("%s", "%s")'''



INSERT_LABEL_QUERY_TEXT = '''INSERT OR IGNORE INTO labels (label_uid, dt, name, lon0, lat0, lon1, lat1, lon2, lat2, sourcedata_fname) ''' + \
                          '''                      VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'''


INSERT_TRACK_LABEL_QUERY_TEXT = '''INSERT INTO track_labels (label_id, track_id) ''' + \
                                '''     SELECT labs.id AS label_id, trks.id AS track_id FROM labels labs JOIN tracks trks ''' + \
                                '''     WHERE labs.label_uid = "%s" ''' + \
                                '''     AND trks.track_uid = "%s"'''

UPDATE_TRACK_START_DT_QUERY_TEXT = '''UPDATE tracks SET start_dt = strftime("%%Y-%%m-%%dT%%H:%%M:%%S", (SELECT min(d1.dt) as dt_min FROM ''' + \
                                   '''    (SELECT datetime(dt) as dt FROM track_labels WHERE track_labels.track_id IN ''' + \
                                   '''        (SELECT id FROM tracks WHERE tracks.track_uid = "%s")''' + \
                                   '''    ) AS d1)) WHERE tracks.track_uid = "%s"'''

UPDATE_TRACK_END_DT_QUERY_TEXT = '''UPDATE tracks SET end_dt = strftime("%%Y-%%m-%%dT%%H:%%M:%%S", (SELECT max(d1.dt) as dt_max FROM ''' + \
                                 '''    (SELECT datetime(dt) as dt FROM track_labels WHERE track_labels.track_id IN ''' + \
                                 '''        (SELECT id FROM tracks WHERE tracks.track_uid = "%s")''' + \
                                 '''    ) AS d1)) WHERE tracks.track_uid = "%s"'''

DELETE_LABELS_OF_TRACK_QUERY_TEXT = '''DELETE FROM track_labels WHERE track_labels.track_id IN (SELECT id FROM tracks tr WHERE tr.track_uid = "%s")'''

SELECT_LABELS_OF_TRACK_QUERY_TEXT = '''SELECT labs.* FROM track_labels trlabs ''' + \
                                    '''     INNER JOIN tracks tr ON tr.id = trlabs.track_id ''' + \
                                    '''     INNER JOIN labels labs ON labs.id = trlabs.label_id ''' + \
                                    '''     WHERE tr.track_uid = "%s" ''' + \
                                    '''     ORDER BY labs.dt'''

DELETE_TRACK_QUERY_TEXT = '''DELETE FROM tracks WHERE tracks.track_uid = "%s"'''

SELECT_TRACK_QUERY_TEXT = '''SELECT lab.label_uid from track_labels lab ''' + \
                          ''' INNER JOIN tracks tr ON tr.id = lab.track_id ''' + \
                          ''' WHERE tr.track_uid = "%s" '''

SELECT_TRACKS_QUERY_TEXT = '''SELECT tr.track_uid, lab.label_uid from track_labels lab ''' + \
                           ''' INNER JOIN tracks tr ON tr.id = lab.track_id ''' + \
                           ''' ORDER BY tr.track_uid '''

TEST_SQLITE_DB_CONNECTION_QUERY_TEXT = '''SELECT * FROM labels labs ''' + \
                                       '''ORDER BY RANDOM() LIMIT 1'''


SELECT_TRACKS_BY_LABEL_UIDS_QUERY_TEXT = '''SELECT tr.track_uid, tr.human_readable_name, labs.* FROM track_labels trlabs ''' + \
                                         '''    INNER JOIN tracks tr ON tr.id = trlabs.track_id ''' + \
                                         '''    INNER JOIN labels labs ON labs.id = trlabs.label_id ''' + \
                                         '''    WHERE tr.id IN (    SELECT DISTINCT trlabs1.track_id FROM track_labels trlabs1 ''' + \
                                         '''                        INNER JOIN tracks tr1 ON tr1.id = trlabs1.track_id ''' + \
                                         '''                        INNER JOIN labels labs1 ON labs1.id = trlabs1.label_id ''' + \
                                         '''                        WHERE labs1.label_uid IN (%s)) ''' + \
                                         '''    ORDER BY tr.track_uid, labs.dt'''


SELECT_TRACKS_BY_DATETIME_RANGE_QUERY_TEXT = '''SELECT tr.track_uid, tr.human_readable_name, labs.* FROM track_labels trlabs ''' + \
                                             '''    INNER JOIN tracks tr ON tr.id = trlabs.track_id ''' + \
                                             '''    INNER JOIN labels labs ON labs.id = trlabs.label_id ''' + \
                                             '''    WHERE tr.id IN (''' + \
                                             '''                    SELECT DISTINCT trlabs1.track_id FROM track_labels trlabs1 ''' + \
                                             '''                    INNER JOIN tracks tr1 ON tr1.id = trlabs1.track_id''' + \
                                             '''                    INNER JOIN labels labs1 ON labs1.id = trlabs1.label_id ''' + \
                                             '''                    WHERE labs1.dt BETWEEN "%s" AND "%s")''' + \
                                             '''    ORDER BY tr.track_uid, labs.dt'''

SELECT_LABELS_BY_SOURCEDATA_BASENAME = '''SELECT * FROM labels WHERE labels.sourcedata_fname = "%s"'''


REMOVE_LABEL_QUERY_TEXTS = ['''DELETE FROM track_labels WHERE track_labels.label_id IN (SELECT id FROM labels WHERE labels.label_uid = "%s")''',
                            '''DELETE FROM labels WHERE labels.label_uid = "%s"''']


UPDATE_LABEL_DATA_QUERY_TEXT = '''UPDATE labels SET dt="%s", name="%s", lon0="%s", lat0="%s", lon1="%s", lat1="%s", lon2="%s", lat2="%s" ''' + \
                               '''  WHERE label_uid = "%s"'''


DATETIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'
DATETIME_HUMAN_READABLE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'