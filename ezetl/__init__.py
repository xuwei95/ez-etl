reader_map = {
    'file:None': 'ezetl.data_models.file_models.BaseFileModel',
    'file:file_table': 'ezetl.data_models.file_models.TableFileModel',
    'mysql:None': 'ezetl.data_models.base_db_sql.BaseDBSqlModel',
    'mysql:sql': 'ezetl.data_models.base_db_sql.BaseDBSqlModel',
    'mysql:mysql_table': 'ezetl.data_models.mysql_table.MysqlTableModel',
    'mysql:mysql_binlog': 'ezetl.data_models.mysql_binlog.MysqlBinlogModel',
    'clickhouse:None': 'ezetl.data_models.clickhouse_table.BaseDBSqlModel',
    'clickhouse:sql': 'ezetl.data_models.base_db_sql.BaseDBSqlModel',
    'clickhouse:clickhouse_table': 'ezetl.data_models.clickhouse_table.CkTableModel',
    'elasticsearch:None': 'ezetl.data_models.elasticsearch_index.EsIndexModel',
    'elasticsearch:elasticsearch_index': 'ezetl.data_models.elasticsearch_index.EsIndexModel',
    'mongodb:None': 'ezetl.data_models.mongo_models.MongoModel',
    'mongodb:mongodb_collection': 'ezetl.data_models.mongo_models.MongoModel',
    'neo4j:None': 'ezetl.data_models.neo4j_models.N4jSqlModel',
    'neo4j:sql': 'ezetl.data_models.neo4j_models.N4jSqlModel',
    'neo4j:neo4j_graph': 'ezetl.data_models.neo4j_models.N4jGraphModel',
    'influxdb:None': 'ezetl.data_models.ixdb_models.InfluxDBSqlModel',
    'influxdb:sql': 'ezetl.data_models.ixdb_models.InfluxDBSqlModel',
    'influxdb:influxdb_table': 'ezetl.data_models.ixdb_models.InfluxDBTableModel',
    'kafka:None': 'ezetl.data_models.kafka_topic.KafkaTopicModel',
    'kafka:kafka_topic': 'ezetl.data_models.kafka_topic.KafkaTopicModel'
}

writer_map = {
    'mysql:mysql_table': 'ezetl.data_models.mysql_table.MysqlTableModel',
    'clickhouse:clickhouse_table': 'ezetl.data_models.clickhouse_table.CkTableModel',
    'elasticsearch:elasticsearch_index': 'ezetl.data_models.elasticsearch_index.EsIndexModel',
    'kafka:kafka_topic': 'ezetl.data_models.kafka_topic.KafkaTopicModel',
    'mongodb:mongodb_collection': 'ezetl.data_models.mongo_models.MongoModel',
    'neo4j:neo4j_graph': 'ezetl.data_models.neo4j_models.N4jGraphModel',
    'influxdb:influxdb_table': 'ezetl.data_models.ixdb_models.InfluxDBTableModel',
}
