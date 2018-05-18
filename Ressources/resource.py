from os.path import dirname


def get_path_resource(name_resource):
    """
    Return the complete path of the desired element in the resource directory
    :param name_resource: file to get
    :return: absolute path to the file
    """
    return dirname(__file__) + '\\' + name_resource
