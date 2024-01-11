from setuptools import setup, find_packages

version = '1.1.0'

setup(
    name='ez-etl',
    version=version,
    description="ez-etl is an open-source Extract, Transform, load (ETL) library written in Python. Just configure a dict to read data from various data sources. Use code or built-in conversion algorithms to transform the data into the target data format， and write it to the target data source. ",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Xu Wei',
    author_email='1013104194@qq.com',
    license='Apache License 2.0',
    install_requires=[
        "requests>=2.25.1",
        "sshtunnel",
        "python-dateutil",
        "pandas>=1.0.0",
        "openpyxl",
        "xlrd",
        "minio==7.1.1",
        "sqlalchemy>=1.2.0",
        "pymysql",
        "elasticsearch>=7.17.2",
        "redis==4.0.2",
        "kafka-python==2.0.2",
        "mysql-replication==0.27",
        "minio==7.1.1"
    ],
    extras_require={
        'all': [
            "xorbits==0.3.2",
            "pyarrow>=5.0.0",
            "akshare",
            "ccxt",
            "psycopg2-binary",
            "pymssql",
            "cx_oracle",
            "clickhouse-sqlalchemy",
            "thrift",
            "thrift_sasl",
            "pyhive",
            "py2neo",
            "prometheus-api-client",
            "mongoengine",
            "influxdb==5.3.1",
        ],
        'xorbits': [
            "xorbits==0.3.2",
            "pyarrow>=5.0.0"
        ],
    },
    keywords="etl, extract, transform, load, excel, csv, mysql, kafka, elasticsearch, neo4j, influxdb, mongodb, clickhouse",
)