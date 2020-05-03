import os
import pathlib
import traceback
import fnmatch
import sys
import datetime
import json
import numbers


class ServiceDefs():

    @classmethod
    def DoesPathExistAndIsDirectory(cls, pathStr):
        if os.path.exists(pathStr) and os.path.isdir(pathStr):
            return True
        else:
            return False


    @classmethod
    def DoesPathExistAndIsFile(cls, pathStr):
        if os.path.exists(pathStr) and os.path.isfile(pathStr):
            return True
        else:
            return False


    @classmethod
    def EnsureDirectoryExists(cls, pathStr):
        if not ServiceDefs.DoesPathExistAndIsDirectory(pathStr):
            try:
                pathlib.Path(pathStr).mkdir(parents=True, exist_ok=True)
            except Exception as ex:
                err_fname = './logs/errors.log'
                exc_type, exc_value, exc_traceback = sys.exc_info()
                with open(err_fname, 'a') as errf:
                    traceback.print_tb(exc_traceback, limit=None, file=errf)
                    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=errf)
                print(str(ex))
                print('the directory you are trying to place a file to doesn\'t exist and cannot be created:\n%s' % pathStr)
                raise FileNotFoundError('the directory you are trying to place a file to doesn\'t exist and cannot be created:')


    @classmethod
    def find_files(cls, directory, pattern, maxdepth=None):
        flist = []
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    filename = filename.replace('\\\\', os.sep)
                    if maxdepth is None:
                        flist.append(filename)
                    else:
                        if filename.count(os.sep)-directory.count(os.sep) <= maxdepth:
                            flist.append(filename)
        return flist


    @classmethod
    def find_directories(cls, directory, pattern=None, maxdepth=None):
        dlist = []
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                if pattern is None:
                    retname = os.path.join(root, d, '')
                    yield retname
                elif fnmatch.fnmatch(d, pattern):
                    retname = os.path.join(root, d, '')
                    retname = retname.replace('\\\\', os.sep)
                    if maxdepth is None:
                        # yield retname
                        dlist.append(retname)
                    else:
                        if retname.count(os.sep)-directory.count(os.sep) <= maxdepth:
                            # yield retname
                            dlist.append(retname)
        return dlist


    @classmethod
    def enum(cls, sequential, **named):
        # enums = dict(zip(sequential, [str(x) for x in  range(len(sequential))]), **named)
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)


    @classmethod
    def ReportException(cls, err_fname, ex, **kwargs):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        with open(err_fname, 'a') as errf:
            errf.write('================ ' + str(datetime.datetime.now()) + ' ================\n')
            traceback.print_tb(exc_traceback, limit=None, file=errf)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=errf)
            if len(kwargs) > 0:
                errf.write('\n')
                for k in kwargs.keys():
                    errf.write('......%s......\n' % k)
                    errf.write('%s' % kwargs[k])
                    errf.write('\n')
            errf.write('\n\n\n')


    @classmethod
    def Log(cls, log_fname, **kwargs):
        with open(log_fname, 'a') as logf:
            logf.write('================ ' + str(datetime.datetime.now()) + ' ================\n')
            if len(kwargs) > 0:
                logf.write('\n')
                for k in kwargs.keys():
                    logf.write('......%s......\n' % k)
                    logf.write('%s' % kwargs[k])
                    logf.write('\n')
            logf.write('\n\n\n')


    @classmethod
    def LogRequest(cls, log_fname, request):
        with open(log_fname, 'a') as logf:
            logf.write('================ ' + str(datetime.datetime.now()) + ' ================\n')
            for k in ['date', 'method', 'scheme', 'path', 'full_path', 'script_root', 'url', 'base_url',
                      'url_root', 'content_encoding', 'content_type', 'mimetype', 'content_length']:
                logf.write('{:<20}   {:<}\n'.format(k, str(getattr(request, k, '---'))))

            logf.write('\nargs: \n')
            for k in request.args.keys():
                logf.write('{:<20}   {:<}\n'.format(k, request.args[k]))
                # logf.write('%s: ' % k)
                # logf.write('%s\n' % request.args[k])

            if 'text/plain' in request.mimetype:
                logf.write('\ndata: \n')
                logf.write(request.data.decode('utf-8'))

            logf.write('\n\n')



    @classmethod
    def urljoin(cls, *args):
        """
        Joins given arguments into an url. Trailing but not leading slashes are
        stripped for each argument.
        """

        return "/".join(map(lambda x: str(x).rstrip('/'), args))


    @classmethod
    def ToJSON(cls, x):
        return json.dumps(x, default=ServiceDefs.object_convertion_rules)


    @classmethod
    def object_convertion_rules(cls, x):
        if type(x) is str:
            return x
        if type(x) in [float, int]:
            return str(x)
        elif isinstance(x, numbers.Number):
            return str(x)
        else:
            return x.__dict__