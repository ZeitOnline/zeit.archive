from setuptools import setup, find_packages

setup(
    name='zeit.archive',
    version = '0.8.1dev',
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
        'zeit.cms>=1.41.0',
        'zeit.content.article>=2.8.1',
        'zeit.content.cp>=0.33.0',
        ],
    entry_points = """
        [console_scripts]
        archive-index-builder = zeit.archive.worker:build_main
        """
)
