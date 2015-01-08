from setuptools import setup, find_packages

setup(
    name='zeit.archive',
    version='2.0.2.dev0',
    author='Dominik Hoppe',
    author_email='dominik.hoppe@zeit.de',
    url='http://www.zeit.de/',
    description="Monthly archive centerpages",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    namespace_packages=['zeit'],
    install_requires=[
        'grokcore.component',
        'plone.testing',
        'setuptools',
        'zeit.cms>1.52.0',
        'zeit.content.article>=3.0',
        'zeit.content.cp>=0.33.1',
        'zeit.edit',
    ],
    entry_points="""
        [console_scripts]
        archive-index-builder=zeit.archive.worker:build_main
        """
)
