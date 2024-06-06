CREATE TABLE provider
(
    "ProviderKey" serial NOT NULL,
    "FirstName" character varying(200) COLLATE pg_catalog."default",
    "MiddleName" character varying(200) COLLATE pg_catalog."default",
    "LastName" character varying(200) COLLATE pg_catalog."default",
    "NationalProviderIdentifier" character varying(10) COLLATE pg_catalog."default",
    "SubSpecialty" integer,
    "Specialty" character varying(200) COLLATE pg_catalog."default",
    "PrimaryPhone" character varying(20) COLLATE pg_catalog."default",
    "PrimaryFax" character varying(20) COLLATE pg_catalog."default",
    "AddressLine1" character varying(200) COLLATE pg_catalog."default",
    "AddressLine2" character varying(200) COLLATE pg_catalog."default",
    "City" character varying(50) COLLATE pg_catalog."default",
    "State" character varying(2) COLLATE pg_catalog."default",
    "ZipCode" character varying(5) COLLATE pg_catalog."default"
)



--CREATE TEMP TABLE temp_provider AS SELECT * FROM provider LIMIT 0;



COPY provider ("FirstName", "MiddleName", "LastName", "NationalProviderIdentifier", "SubSpecialty", "Specialty", "PrimaryPhone", "PrimaryFax", "AddressLine1", "AddressLine2", "City", "State", "ZipCode")
FROM 'Your CSV File Path'
DELIMITER ','
CSV HEADER;



SELECT COUNT(1)
FROM provider;