import sqlite3
from .SQLite_queries import *
from .ServiceDefs import *
import datetime
from flask import g


class DatabaseOps():


    def __init__(self, db_fname, errors_fname):
        self.db_fname = db_fname
        self.errors_fname = errors_fname
        assert self.test_db_connection(), 'database connection failed. could not proceed\ndb_fname=%s' % self.db_fname


    def test_db_connection(self):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                c.execute(TEST_SQLITE_DB_CONNECTION_QUERY_TEXT)
                res = c.fetchall()
            return True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return False


    @classmethod
    def create_tracks_db(cls, db_fname, errors_fname):
        try:
            with sqlite3.connect(db_fname) as conn:
                c = conn.cursor()
                c.execute(CREATE_TRACKS_TABLE_QUERY_TEXT)
                c.execute(CREATE_LABELS_TABLE_QUERY_TEXT)
                c.execute(CREATE_TRACK_LABELS_QUERY_TEXT)
                conn.commit()
            return True
        except Exception as ex:
            ServiceDefs.ReportException(errors_fname, ex)
            print("Tracks database was not created.")
            return False


    def read_track(self, track_uid):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(SELECT_TRACK_QUERY_TEXT % track_uid)
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def read_tracks(self):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(SELECT_TRACKS_QUERY_TEXT)
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def read_tracks_by_label_uids(self, labels_uids):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                labels_uid_list = ",".join(['\"' + uid + '\"' for uid in labels_uids])
                q_result = c.execute(SELECT_TRACKS_BY_LABEL_UIDS_QUERY_TEXT % labels_uid_list)
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def read_tracks_by_datetime(self, dt):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                dt_start = dt + datetime.timedelta(minutes=-30)
                dt_end = dt + datetime.timedelta(minutes=30)
                q_result = c.execute(
                        SELECT_TRACKS_BY_DATETIME_RANGE_QUERY_TEXT % (
                        datetime.datetime.strftime(dt_start, DATETIME_FORMAT_STRING),
                        datetime.datetime.strftime(dt_end, DATETIME_FORMAT_STRING)))
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex,
                                        sqlite_query=SELECT_TRACKS_BY_DATETIME_RANGE_QUERY_TEXT % (
                                                datetime.datetime.strftime(dt_start, DATETIME_FORMAT_STRING),
                                                datetime.datetime.strftime(dt_end, DATETIME_FORMAT_STRING)))
            return None


    def read_track_labels_by_track_uid(self, track_uid):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(SELECT_LABELS_OF_TRACK_QUERY_TEXT % track_uid)
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def read_labels_by_sourcedata_basename(self, sourcedata_basename):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(SELECT_LABELS_BY_SOURCEDATA_BASENAME % sourcedata_basename)
                res_data = c.fetchall()
            return res_data
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def insert_label_data(self, label):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(INSERT_LABEL_QUERY_TEXT % (label.uid,
                                                                datetime.datetime.strftime(label.dt, DATETIME_FORMAT_STRING),
                                                                label.name,
                                                                '%.14f' % label.pts['pt0']['lon'],
                                                                '%.14f' % label.pts['pt0']['lat'],
                                                                '%.14f' % label.pts['pt1']['lon'],
                                                                '%.14f' % label.pts['pt1']['lat'],
                                                                '%.14f' % label.pts['pt2']['lon'],
                                                                '%.14f' % label.pts['pt2']['lat'],
                                                                label.sourcedata_fname))
                rows_affected = q_result.rowcount
                conn.commit()
                return rows_affected if rows_affected > 0 else True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            # raise ex
            return False
        return


    def insert_track_data(self, track):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(INSERT_TRACK_QUERY_TEXT % (track.uid, track.human_readable_name))
                rows_affected = q_result.rowcount
                conn.commit()
                return rows_affected if rows_affected > 0 else True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return False


    def insert_track_label_entry(self, track, label):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(INSERT_TRACK_LABEL_QUERY_TEXT % (label.uid, track.uid))
                rows_affected = q_result.rowcount
                # q_result_2 = c.execute(UPDATE_TRACK_START_DT_QUERY_TEXT)
                # q_result_3 = c.execute(UPDATE_TRACK_END_DT_QUERY_TEXT)
                conn.commit()
                return True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex,
                                        sqlite_query_1=INSERT_TRACK_LABEL_QUERY_TEXT % (label.uid, track.uid))
            return False


    def remove_label(self, label_uid):
        try:
            with sqlite3.connect(self.db_fname, isolation_level=None) as conn:
                c = conn.cursor()
                rows_affected = 0
                for t in REMOVE_LABEL_QUERY_TEXTS:
                    q_result = c.execute(t % label_uid)
                    rows_affected += q_result.rowcount
                conn.commit()
                return rows_affected if rows_affected > 0 else True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return False


    def update_label(self, label):
        try:
            with sqlite3.connect(self.db_fname) as conn:
                c = conn.cursor()
                q_result = c.execute(
                        UPDATE_LABEL_DATA_QUERY_TEXT % (datetime.datetime.strftime(label.dt, DATETIME_FORMAT_STRING),
                                                        label.name,
                                                        '%.14f' % label.pts['pt0']['lon'],
                                                        '%.14f' % label.pts['pt0']['lat'],
                                                        '%.14f' % label.pts['pt1']['lon'],
                                                        '%.14f' % label.pts['pt1']['lat'],
                                                        '%.14f' % label.pts['pt2']['lon'],
                                                        '%.14f' % label.pts['pt2']['lat'],
                                                        label.uid))
                rows_affected = q_result.rowcount
                conn.commit()
                return rows_affected if rows_affected > 0 else True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex,
                                        sqlite_query=UPDATE_LABEL_DATA_QUERY_TEXT % (
                                                datetime.datetime.strftime(label.dt, DATETIME_FORMAT_STRING),
                                                label.name,
                                                '%.14f' % label.pts['pt0']['lon'],
                                                '%.14f' % label.pts['pt0']['lat'],
                                                '%.14f' % label.pts['pt1']['lon'],
                                                '%.14f' % label.pts['pt1']['lat'],
                                                '%.14f' % label.pts['pt2']['lon'],
                                                '%.14f' % label.pts['pt2']['lat'],
                                                label.uid))
            return False
