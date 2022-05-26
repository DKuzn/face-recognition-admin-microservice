from setuptools import setup
from FRAMS import __version__

setup(
    name='FRAMS',
    version=__version__,
    packages=['FRAMS'],
    url='https://github.com/DKuzn/face-recognition-admin-microservice',
    license='GPLv3',
    author='Dmitry Kuznetsov',
    author_email='DKuznetsov2000@outlook.com',
    description='Microservice to fill the databases for face recognition',
    install_requires=['fastapi', 'torch', 'torchvision', 'facenet_pytorch', 'SQLAlchemy', 'psycopg2-binary', 'mysqlclient', 'uvicorn']
)
