class VersionNotSupported(Exception):
    def __init__(self):
        Exception.__init__(self, "This version is not supported.")
