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