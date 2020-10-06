# import sqlite3
# from .SQLite_queries import *
from .ServiceDefs import *
import datetime
from flask import g
from pymongo import MongoClient
from .constants import *
import json
from libs.interfaces.ExampleLabels import *



class DatabaseOps():


    def __init__(self, db_conection_dict, errors_fname):
        self.db_conection_dict = db_conection_dict
        self.errors_fname = errors_fname
        # self.client = self.client = MongoClient(host = self.db_conection_dict[SETTING_LABELS_DATABASE_HOST],
        #                                         port = int(self.db_conection_dict[SETTING_LABELS_DATABASE_PORT]),
        #                                         serverSelectionTimeoutMS = 2000)
        self.client = MongoClient(
            'mongodb://' + db_conection_dict['db_username'] + ':' + db_conection_dict['db_password'] + '@' +
            db_conection_dict['db_host'] + ':27017/' + db_conection_dict['db_name'], serverSelectionTimeoutMS=2000)
        self.db = self.client[db_conection_dict[SETTING_LABELS_DATABASE_NAME]]
        self.collection = self.db[db_conection_dict[SETTING_LABELS_COLLECTION]]


    def test_db_connection(self):
        try:
            info = self.client.server_info()
            return True
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return False


    def read_example_labels(self, img_basename):
        try:
            found = self.collection.find_one({"strBaseImageFilename": img_basename})
            if found:
                del found['_id']
                return json.dumps(found)
            else:
                return None
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return None


    def insert_example_labels(self, example_labels):
        try:
            example_id = self.collection.insert_one(example_labels).inserted_id
            return example_id
        except Exception as ex:
            ServiceDefs.ReportException(self.errors_fname, ex)
            return False


    def remove_label(self, label_uid):
        raise NotImplementedError()
        # try:
        #     with sqlite3.connect(self.db_fname, isolation_level=None) as conn:
        #         c = conn.cursor()
        #         rows_affected = 0
        #         for t in REMOVE_LABEL_QUERY_TEXTS:
        #             q_result = c.execute(t % label_uid)
        #             rows_affected += q_result.rowcount
        #         conn.commit()
        #         return rows_affected if rows_affected > 0 else True
        # except Exception as ex:
        #     ServiceDefs.ReportException(self.errors_fname, ex)
        #     return False


    def update_label(self, label):
        raise NotImplementedError()
        # try:
        #     with sqlite3.connect(self.db_fname) as conn:
        #         c = conn.cursor()
        #         q_result = c.execute(
        #                 UPDATE_LABEL_DATA_QUERY_TEXT % (datetime.datetime.strftime(label.dt, DATETIME_FORMAT_STRING),
        #                                                 label.name,
        #                                                 '%.14f' % label.pts['pt0']['lon'],
        #                                                 '%.14f' % label.pts['pt0']['lat'],
        #                                                 '%.14f' % label.pts['pt1']['lon'],
        #                                                 '%.14f' % label.pts['pt1']['lat'],
        #                                                 '%.14f' % label.pts['pt2']['lon'],
        #                                                 '%.14f' % label.pts['pt2']['lat'],
        #                                                 label.uid))
        #         rows_affected = q_result.rowcount
        #         conn.commit()
        #         return rows_affected if rows_affected > 0 else True
        # except Exception as ex:
        #     ServiceDefs.ReportException(self.errors_fname, ex,
        #                                 sqlite_query=UPDATE_LABEL_DATA_QUERY_TEXT % (
        #                                         datetime.datetime.strftime(label.dt, DATETIME_FORMAT_STRING),
        #                                         label.name,
        #                                         '%.14f' % label.pts['pt0']['lon'],
        #                                         '%.14f' % label.pts['pt0']['lat'],
        #                                         '%.14f' % label.pts['pt1']['lon'],
        #                                         '%.14f' % label.pts['pt1']['lat'],
        #                                         '%.14f' % label.pts['pt2']['lon'],
        #                                         '%.14f' % label.pts['pt2']['lat'],
        #                                         label.uid))
        #     return False
