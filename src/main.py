import shutil


def copy_static_to_public():
    shutil.rmtree('./public', ignore_errors=True)
    shutil.copytree('./static', './public')


def main():
    copy_static_to_public()


if __name__ == '__main__':
    main()
