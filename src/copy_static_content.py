import shutil


def copy_static_content():
    shutil.rmtree('./public', ignore_errors=True)
    shutil.copytree('./static', './public')
