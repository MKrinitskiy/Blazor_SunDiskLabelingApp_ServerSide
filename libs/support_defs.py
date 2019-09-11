import os
import pathlib
import traceback
import fnmatch
import sys
import datetime
import json
import numbers


def DoesPathExistAndIsDirectory(pathStr):
    if os.path.exists(pathStr) and os.path.isdir(pathStr):
        return True
    else:
        return False


def DoesPathExistAndIsFile(pathStr):
    if os.path.exists(pathStr) and os.path.isfile(pathStr):
        return True
    else:
        return False


def EnsureDirectoryExists(pathStr):
    if not DoesPathExistAndIsDirectory(pathStr):
        try:
            pathlib.Path(pathStr).mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            err_fname = './errors.log'
            exc_type, exc_value, exc_traceback = sys.exc_info()
            with open(err_fname, 'a') as errf:
                traceback.print_tb(exc_traceback, limit=None, file=errf)
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=errf)
            print(str(ex))
            print('the directory you are trying to place a file to doesn\'t exist and cannot be created:\n%s' % pathStr)
            raise FileNotFoundError('the directory you are trying to place a file to doesn\'t exist and cannot be created:')



def find_files(directory, pattern, maxdepth=None):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                filename = filename.replace('\\\\', os.sep)
                if maxdepth is None:
                    yield filename
                else:
                    if filename.count(os.sep)-directory.count(os.sep) <= maxdepth:
                        yield filename


def find_directories(directory, pattern=None, maxdepth=None):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if pattern is None:
                retname = os.path.join(root, d, '')
                yield retname
            elif fnmatch.fnmatch(d, pattern):
                retname = os.path.join(root, d, '')
                retname = retname.replace('\\\\', os.sep)
                if maxdepth is None:
                    yield retname
                else:
                    if retname.count(os.sep)-directory.count(os.sep) <= maxdepth:
                        yield retname



def enum(sequential, **named):
    # enums = dict(zip(sequential, [str(x) for x in  range(len(sequential))]), **named)
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)



def ReportException(err_fname, ex):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    with open(err_fname, 'a') as errf:
        errf.write('================ ' + str(datetime.datetime.now()) + ' ================\n')
        traceback.print_tb(exc_traceback, limit=None, file=errf)
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=errf)
        errf.write('\n\n\n')




def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))



def ToJSON(x):
    return json.dumps(x, default=object_convertion_rules)

def object_convertion_rules(x):
    if type(x) is str:
        return x
    if type(x) in [float, int]:
        return str(x)
    elif isinstance(x, numbers.Number):
        return str(x)
    else:
        return x.__dict__