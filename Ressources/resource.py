from os import getcwd


def get_resource(name_resource):
    """
    Return the complete path of the desired element in the resource directory
    :param name_resource: file to get
    :return: absolute path to the file
    """
    return getcwd() + name_resource
