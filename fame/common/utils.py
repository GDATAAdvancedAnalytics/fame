import os
import collections
from time import sleep
from uuid import uuid4
from datetime import datetime
from shutil import copyfileobj
from werkzeug.utils import secure_filename

from fame.common.config import fame_config


def is_iterable(element):
    return isinstance(element, collections.Iterable) and not isinstance(element, str)


def iterify(element):
    if is_iterable(element):
        return element
    else:
        return (element,)


def u(string):
    try:
        return str(string)
    except UnicodeDecodeError:
        try:
            return str(string, 'latin-1')
        except UnicodeDecodeError:
            return str(string, errors='replace')


def get_class(module, klass):
    try:
        m = __import__(module)
        for part in module.split('.')[1:]:
            m = getattr(m, part)

        return getattr(m, klass)
    except (ImportError, AttributeError):
        return None


def list_value(list_of_values):
    result = set()

    for value in list_of_values.split(','):
        value = value.strip()
        if value != "":
            result.add(value)

    return list(result)


def ordered_list_value(list_of_values):
    result = []

    for value in list_of_values.split(','):
        value = value.strip()
        result.append(value)

    return result


def unique_for_key(l, key):
    return list({d[key]: d for d in l}.values())


def tempdir(prefix=None):
    if not prefix:
        prefix = fame_config.temp_path

    tempdir = os.path.join(prefix, str(uuid4()).replace('-', ''))

    try:
        os.makedirs(tempdir)
    except OSError:
        pass

    return tempdir


def get_attachment_filename(response):
    content_disposition = response.headers.get("content-disposition")
    filename = content_disposition.split("filename=")[1]
    return filename


def save_response(response):
    tmp = tempdir()
    filename = secure_filename(get_attachment_filename(response))
    filepath = os.path.join(tmp, filename)

    with open(filepath, 'wb') as out:
        copyfileobj(response.raw, out)

    return filepath


def with_timeout(func, timeout, step):
    started_at = datetime.now()

    while started_at + timeout > datetime.now():
        result = func()

        if result:
            return result

        sleep(step)

    return None
