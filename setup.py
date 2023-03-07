from distutils.core import setup


setup(
    name='spike2loader',
    packages=['spike2loader'],
    version='0.1',
    license='MIT',
    description = 'Loads spike2 events to an event_dataframe',
    description_file = "README.md",
    author="Julien Braine",
    author_email='julienbraine@yahoo.fr',
    url='https://github.com/JulienBrn/Spike2Loader',
    download_url = 'https://github.com/JulienBrn/Spike2Loader.git',
    package_dir={'': 'src'},
    keywords=['python',  'logging'],
    install_requires=['pandas', 'sonpy'],
)