from setuptools import setup, find_packages

setup(
    name='whisper-transcriber',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'openai-whisper>=20231106', 
        'coloredlogs>=15.0.1',
    ],
    entry_points={
        'console_scripts': [
            'whisper-transcriber=whisper_transcriber:main',
        ],
    },
)
