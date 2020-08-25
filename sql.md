-- ml.rules_of_origin_scheme_memberships definition

-- Drop table

-- DROP TABLE ml.rules_of_origin_scheme_memberships;

CREATE TABLE ml.rules_of_origin_scheme_memberships (
	geographical_area_id varchar(4) NULL,
	geographical_area_sid int4 NULL,
	rules_of_origin_scheme_sid int4 NULL,
	validity_start_date timestamp NULL,
	validity_end_date timestamp NULL
);


-- ml.rules_of_origin_schemes definition

-- Drop table

-- DROP TABLE ml.rules_of_origin_schemes;

CREATE TABLE ml.rules_of_origin_schemes (
	rules_of_origin_scheme_sid serial NOT NULL,
	description varchar(255) NULL,
	abbreviation varchar(100) NULL,
	validity_start_date timestamp NULL,
	validity_end_date timestamp NULL
);

-- ml.roo_row definition

-- Drop table

-- DROP TABLE ml.roo_row;

CREATE TABLE ml.roo_row (
	idx serial NOT NULL,
	heading text NULL,
	description text NULL,
	processing_rule text NULL,
	chapter varchar(2) NULL,
	country varchar(4) NULL,
	"sequence" int4 NULL,
	rules_of_origin_scheme_sid int4 NULL,
	CONSTRAINT roo_row_pk PRIMARY KEY (idx)
);