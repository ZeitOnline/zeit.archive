from setuptools import setup, find_packages

setup(
    name='zeit.archive',
    version='2.1.dev0',
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
        'zeit.cms>1.52.0',
        'zeit.content.article>=3.0',
        'zeit.content.cp>=0.33.1',
        'zeit.edit',
        ],
    entry_points = """
        [console_scripts]
        archive-index-builder = zeit.archive.worker:build_main
        """
)
