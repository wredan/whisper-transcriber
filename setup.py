from setuptools import setup, find_packages

setup(
    name='whisper-transcriber',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai-whisper>=20230314', 
        'halo>=0.0.31   ', 
        'coloredlogs>=15.0.1',
    ],
    entry_points={
        'console_scripts': [
            'whisper-transcriber=transcriber.whisper_transcriber:main',
        ],
    },
)
