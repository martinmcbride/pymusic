# Author:  Martin McBride
# Created: 2026-05-15
# Copyright (C) 2026, Martin McBride
# License: MIT

import tempfile


def create_tempfile(suffix : str = ".tmp", delete : bool = False):
    """
    Create a temporary file
    :param suffix: Suffix to be added to filename, default ,tmp
    :param delete: Whether to delete the temporary file when the object goes out fo context
    :return:
        A file object. Use file.name() on teh object to find its name
    """
    return tempfile.NamedTemporaryFile(mode='w+', suffix=suffix, delete=delete)