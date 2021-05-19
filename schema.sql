--Apply to Postgres
 DROP TABLE concrete;
 
 CREATE TABLE concrete (
  ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  CEMENT REAL NOT NULL,
  BLAST_FURNACE_SLAG REAL NOT NULL,
  FLY_ASH TEXT(255) REAL NOT NULL,
  WATER TEXT(255) REAL NOT NULL,
  SUPERPLASTICIZER_CODE REAL NOT NULL,
  COARSE_AGGREGATE REAL NOT NULL,
  FINE_AGGREGATE REAL NOT NULL,
  AGE REAL NOT NULL,
  CONCRETE_COMPRESSIVE_STRENGTH REAL NOT NULL,
);