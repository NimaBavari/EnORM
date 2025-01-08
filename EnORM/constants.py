"""Contains library-wide constants."""

TYPES = {
    "postgresql": {
        "Integer": "INTEGER",
        "Boolean": "BOOLEAN",
        "Float": "FLOAT",
        "Numeric": "NUMERIC",
        "String": "VARCHAR",
        "Date": "DATE",
        "Time": "TIME",
        "DateTime": "TIMESTAMP",
        "Binary": "BYTEA",
        "Geometry": "GEOMETRY",
        "Interval": "INTERVAL",
        "Serial": "SERIAL",
        "ARRAY": "ARRAY",
        "JSONB": "JSONB",
        "CIDR": "CIDR",
        "MACADDR": "MACADDR",
        "HSTORE": "HSTORE",
    },
    "mysql": {
        "Integer": "INT",
        "Boolean": "TINYINT(1)",
        "Float": "FLOAT",
        "Numeric": "DECIMAL",
        "String": "VARCHAR",
        "Date": "DATE",
        "Time": "TIME",
        "DateTime": "DATETIME",
        "Binary": "BLOB",
        "Geometry": "GEOMETRY",
    },
    "sqlite": {
        "Integer": "INTEGER",
        "Boolean": "INTEGER",
        "Float": "REAL",
        "Numeric": "NUMERIC",
        "String": "TEXT",
        "Date": "DATE",
        "Time": "TIME",
        "DateTime": "DATETIME",
        "Binary": "BLOB",
    },
    "sql_server": {
        "Integer": "INT",
        "Boolean": "BIT",
        "Float": "FLOAT",
        "Numeric": "DECIMAL",
        "String": "VARCHAR",
        "Date": "DATE",
        "Time": "TIME",
        "DateTime": "DATETIME",
        "Binary": "VARBINARY",
        "Geometry": "GEOMETRY",
    },
    "oracle": {
        "Integer": "NUMBER",
        "Boolean": "NUMBER(1)",
        "Float": "NUMBER",
        "Numeric": "NUMBER",
        "String": "VARCHAR2",
        "Date": "DATE",
        "Time": "TIMESTAMP",
        "DateTime": "TIMESTAMP",
        "Binary": "BLOB",
        "Geometry": "SDO_GEOMETRY",
        "Interval": "INTERVAL",
    },
}