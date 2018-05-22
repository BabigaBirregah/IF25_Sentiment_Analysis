from os.path import dirname


def get_path_profile(name_resource):
    """
    Return the complete path of the desired element in this directory
    :param name_resource: file to get
    :return: absolute path to the file
    """
    return dirname(__file__) + '\\' + name_resource
