def without_namespace(tag):
    '''

    :param tag:
    :return:
    '''
    return tag if not '{' in tag \
        else tag.split('}')[1]

