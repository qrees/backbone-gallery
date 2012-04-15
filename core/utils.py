import uuid


def gen_uuid():
    return 'uuid+%s' % uuid.uuid4()