import os
import subprocess
import sys

import kep


def test_import_from_another_dir():
    """
    Test that package is importable regardless of working directory.

    This is especially important for docs generation.
    Everything should be importable without side-effects.
    """
    # Change to docs directory
    project_dir = os.path.normpath(os.path.join(os.path.dirname(kep.__file__), '..'))
    docs_dir = os.path.join(project_dir, 'docs')
    assert os.path.isdir(docs_dir)
    env = {'PYTHONPATH': project_dir}
    code = 'import kep'
    # Try to import kep from another directory in a separate python process
    returncode = subprocess.call([sys.executable, '-c', code],
                                 cwd=docs_dir, env=env)
    assert returncode == 0, '`{}` failed! ' \
                            'To find out why, try it manually ' \
                            'from another directory.'.format(code)
