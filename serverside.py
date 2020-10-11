import binascii
from flask_cors import CORS
from libs import *
from url_rules import *
from libs.parse_args import *



if __name__ == "__main__":
    # execute only if run as a script

    args = sys.argv[1:]
    args = parse_args(args)

    settings = Settings(os.path.dirname(os.path.abspath(__file__)))
    settings.load()

    if settings.get(SETTING_LABELS_DATABASE_HOST) is None:
        db_host = os.environ['MONGODB_HOSTNAME']
        settings[SETTING_LABELS_DATABASE_HOST] = db_host
        settings.save()
    if settings.get(SETTING_LABELS_DATABASE_PORT) is None:
        db_port = 27017
        settings[SETTING_LABELS_DATABASE_PORT] = db_port
        settings.save()
    if settings.get(SETTING_LABELS_DATABASE_NAME) is None:
        db_name = os.environ['MONGODB_DATABASE']
        settings[SETTING_LABELS_DATABASE_NAME] = db_name
        settings.save()
    if settings.get(SETTING_LABELS_COLLECTION) is None:
        db_collection = 'labels'
        settings[SETTING_LABELS_COLLECTION] = db_collection
        settings.save()
    if settings.get(SETTING_MONGODB_PASSWORD) is None:
        db_password = os.environ['MONGODB_PASSWORD']
        settings[SETTING_MONGODB_PASSWORD] = db_password
        settings.save()
    if settings.get(SETTING_MONGODB_USERNAME) is None:
        db_username = os.environ['MONGODB_USERNAME']
        settings[SETTING_MONGODB_USERNAME] = db_username
        settings.save()





    db_conection_dict = {'db_host': settings[SETTING_LABELS_DATABASE_HOST],
                         'db_port': settings[SETTING_LABELS_DATABASE_PORT],
                         'db_name': settings[SETTING_LABELS_DATABASE_NAME],
                         'db_collection': settings[SETTING_LABELS_COLLECTION],
                         'db_password': settings[SETTING_MONGODB_PASSWORD],
                         'db_username': settings[SETTING_MONGODB_USERNAME]}

    app = FlaskExtended(__name__, static_folder='cache')

    try:
        with app.app_context():
            app.db = DatabaseOps(db_conection_dict, './logs/db_errors.log')
            if not app.db.test_db_connection():
                if not args.disable_mongodb:
                    raise Exception('mongodb unavailable')
                else:
                    app.db = None
                    app.disable_mongodb = True
    except Exception as ex:
        ServiceDefs.ReportException('./logs/db_errors.log', ex)
        print('mongodb unavailable')
        quit()

    CORS(app)
    app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))

    tmp_imag_dir = os.path.join(os.getcwd(), 'tmp')
    src_data_dir = os.path.join(os.getcwd(), 'src_data')
    
    app.add_url_rule(rule='/app/', endpoint='url_rule_root', view_func=lambda: url_rule_root(app), methods=['GET'])
    app.add_url_rule(rule='/app/exec', endpoint='url_rule_exec', view_func=lambda: url_rule_exec(app), methods=['GET'])
    app.add_url_rule(rule='/app/images', endpoint='url_rule_image', view_func=lambda: url_rule_image(app), methods=['GET'])
    app.add_url_rule(rule='/app/labels', endpoint='url_rule_labels', view_func=lambda: url_rule_labels(app), methods=['GET', 'POST'])
    app.add_url_rule(rule='/app/imdone', endpoint='url_rule_imdone', view_func=lambda: url_rule_imdone(app), methods=['GET'])

    app.run(host='0.0.0.0', port=args.port)
    