from flask_cors import CORS
from libs import *
import binascii, logging
from url_rules import *
from flask import g


if __name__ == "__main__":
    # execute only if run as a script

    settings = Settings(os.path.dirname(os.path.abspath(__file__)))
    settings.load()
    if settings.get(SETTING_TRACKS_DATABASE_FNAME) is None:
        db_fname = './db/tracks.db'
        if DatabaseOps.create_tracks_db(db_fname, './logs/errors.log'):
            settings[SETTING_TRACKS_DATABASE_FNAME] = db_fname
            settings.save()
        else:
            raise Exception("unable to create tracks database. Cannot proceed.")

    app = FlaskExtended(__name__, static_folder='cache')
    CORS(app)
    app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
    # file_handler = logging.FileHandler('./logs/app.log')

    tmp_imag_dir = os.path.join(os.getcwd(), 'tmp')
    src_data_dir = os.path.join(os.getcwd(), 'src_data')

    app.add_url_rule(rule='/', endpoint='url_rule_root', view_func=lambda: url_rule_root(app), methods=['GET'])
    app.add_url_rule(rule='/exec', endpoint='url_rule_exec', view_func=lambda: url_rule_exec(app), methods=['GET'])
    app.add_url_rule(rule='/images', endpoint='url_rule_image', view_func=lambda: url_rule_image(app), methods=['GET'])
    app.add_url_rule(rule='/labels', endpoint='url_rule_labels', view_func=lambda: url_rule_labels(app), methods=['GET', 'POST'])
    app.add_url_rule(rule='/imdone', endpoint='url_rule_imdone', view_func=lambda: url_rule_imdone(app), methods=['GET'])

    try:
        g.db = DatabaseOps(settings[SETTING_TRACKS_DATABASE_FNAME], './logs/errors.log')
    except Exception as ex:
        ServiceDefs.ReportException('./logs/errors.log', ex)

    app.run(host='0.0.0.0', port=2019)