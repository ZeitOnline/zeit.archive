from setuptools import setup, find_packages

setup(
    name='zeit.archive',
    version = '0.8.2',
    author='Dominik Hoppe',
    author_email='dominik.hoppe@zeit.de',
    url='http://trac.gocept.com/zeit',
    description="""\
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages = ['zeit'],
    install_requires=[
        'grokcore.component',
        'setuptools',
        'zeit.cms>=1.41.1',
        'zeit.content.article>=2.8.1',
        'zeit.content.cp>=0.33.1',
        ],
    entry_points = """
        [console_scripts]
        archive-index-builder = zeit.archive.worker:build_main
        """
)
