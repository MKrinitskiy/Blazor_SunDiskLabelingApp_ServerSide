from flask_cors import CORS
from libs import *
import binascii, logging
from url_rules import *
from flask import g


if __name__ == "__main__":
    # execute only if run as a script

    settings = Settings(os.path.dirname(os.path.abspath(__file__)))
    settings.load()

    if settings.get(SETTING_LABELS_DATABASE_HOST) is None:
        db_host = 'localhost'
        settings[SETTING_LABELS_DATABASE_HOST] = db_host
        settings.save()
    if settings.get(SETTING_LABELS_DATABASE_PORT) is None:
        db_port = 27017
        settings[SETTING_LABELS_DATABASE_PORT] = db_port
        settings.save()
    if settings.get(SETTING_LABELS_DATABASE_NAME) is None:
        db_name = 'SunDiskLabelsDatabase'
        settings[SETTING_LABELS_DATABASE_NAME] = db_name
        settings.save()
    if settings.get(SETTING_LABELS_COLLECTION) is None:
        db_collection = 'labels'
        settings[SETTING_LABELS_COLLECTION] = db_collection
        settings.save()

    db_conection_dict = {'db_host': settings[SETTING_LABELS_DATABASE_HOST],
                         'db_port': settings[SETTING_LABELS_DATABASE_PORT],
                         'db_name': settings[SETTING_LABELS_DATABASE_NAME],
                         'db_collection': settings[SETTING_LABELS_COLLECTION]}

    app = FlaskExtended(__name__, static_folder='cache')

    try:
        with app.app_context():
            app.db = DatabaseOps(db_conection_dict, './logs/db_errors.log')
            if not app.db.test_db_connection():
                raise Exception('mongodb unavailable')
    except Exception as ex:
        ServiceDefs.ReportException('./logs/db_errors.log', ex)
        print('mongodb unavailable')
        quit()

    CORS(app)
    app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))

    tmp_imag_dir = os.path.join(os.getcwd(), 'tmp')
    src_data_dir = os.path.join(os.getcwd(), 'src_data')

    app.add_url_rule(rule='/', endpoint='url_rule_root', view_func=lambda: url_rule_root(app), methods=['GET'])
    app.add_url_rule(rule='/exec', endpoint='url_rule_exec', view_func=lambda: url_rule_exec(app), methods=['GET'])
    app.add_url_rule(rule='/images', endpoint='url_rule_image', view_func=lambda: url_rule_image(app), methods=['GET'])
    app.add_url_rule(rule='/labels', endpoint='url_rule_labels', view_func=lambda: url_rule_labels(app), methods=['GET', 'POST'])
    app.add_url_rule(rule='/imdone', endpoint='url_rule_imdone', view_func=lambda: url_rule_imdone(app), methods=['GET'])

    app.run(host='0.0.0.0', port=2019)