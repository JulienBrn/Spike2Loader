from distutils.core import setup
from pathlib import Path

setup(
    name='spike2loader',
    packages=['spike2loader'],
    entry_points={
        'console_scripts': [
            'smrx2python = spike2loader:smrx2python',
        ]
    },
    version='0.5',
    license='MIT',
    description = 'Reads smrx (spike2) files as pandas dataframes',
    description_file = "README.md",
    author="Julien Braine",
    author_email='julienbraine@yahoo.fr',
    url='https://github.com/JulienBrn/Spike2Loader',
    download_url = 'https://github.com/JulienBrn/Spike2Loader.git',
    package_dir={'': 'src'},
    keywords=['python',  'logging'],
    install_requires=['pandas', 'sonpy', "beautifullogger", "tqdm"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown'
)