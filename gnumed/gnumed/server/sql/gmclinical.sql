-- Project: GnuMed
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmclinical.sql,v $
-- $Revision: 1.6 $
-- license: GPL
-- author: 

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

create table audit_clinical (
	audit_id serial
);

comment on table audit_clinical is 
'ancestor table for auditing. Marks tables for automatic trigger generation';

create table enum_clinical_encounters(
	id SERIAL primary key,
	description text
)inherits (audit_clinical);


INSERT INTO enum_clinical_encounters (description)
	values ('surgery consultation');
INSERT INTO enum_clinical_encounters (description)
	values ('phone consultation');
INSERT INTO enum_clinical_encounters (description)
	values ('fax consultation');
INSERT INTO enum_clinical_encounters (description)
	values ('home visit');
INSERT INTO enum_clinical_encounters (description)
	values ('nursing home visit');
INSERT INTO enum_clinical_encounters (description)
	values ('repeat script');
INSERT INTO enum_clinical_encounters (description)
	values ('hospital visit');
INSERT INTO enum_clinical_encounters (description)
	values ('video conference');
INSERT INTO enum_clinical_encounters (description)
	values ('proxy encounter');
INSERT INTO enum_clinical_encounters (description)
	values ('emergency encounter');
INSERT INTO enum_clinical_encounters (description)
	values ('other encounter');

COMMENT ON TABLE enum_clinical_encounters is
'these are the types of encounter';


create table clinical_transaction(
	id SERIAL primary key,
	stamp timestamp with time zone,
	id_location int,
	id_doctor int,  
	id_patient int, 
	id_enum_clinical_encounters int REFERENCES enum_clinical_encounters (id)
) inherits (audit_clinical);

COMMENT ON TABLE clinical_transaction is
'unique identifier for clinical encounter';

COMMENT ON COLUMN clinical_transaction.stamp is 
'Date, time and timezone of the transaction.'; 

COMMENT ON COLUMN clinical_transaction.id_location is 
'Location ID, in ?? gmoffice';

COMMENT ON COLUMN clinical_transaction.id_doctor is 
'Doctor''s ID, in ?? gmoffice';

COMMENT ON COLUMN clinical_transaction.id_patient is 
'Patient''s ID, in gmidentity';

create table enum_clinical_history(
	id SERIAL primary key,
	description text
) inherits (audit_clinical);

COMMENT ON TABLE enum_clinical_history is
'types of history taken during a clinical encounter';


INSERT INTO enum_clinical_history (description)
	values ('past');
INSERT INTO enum_clinical_history (description)
	values ('presenting complaint');
INSERT INTO enum_clinical_history (description)
	values ('history of present illness');
INSERT INTO enum_clinical_history (description)
	values ('social');
INSERT INTO enum_clinical_history (description)
	values ('family');
INSERT INTO enum_clinical_history (description)
	values ('immunisation');
INSERT INTO enum_clinical_history (description)
	values ('requests');
INSERT INTO enum_clinical_history (description)
	values ('allergy');
INSERT INTO enum_clinical_history (description)
	values ('drug');
INSERT INTO enum_clinical_history (description)
	values ('sexual');
INSERT INTO enum_clinical_history (description)
	values ('psychiatric');
INSERT INTO enum_clinical_history (description)
	values ('other');

create table enum_info_sources
(
	id serial,
	description varchar (100)
);

comment on table enum_info_sources is
'sources of clinical information: patient, relative, notes, corresondence';

insert into enum_info_sources (description) values ('patient');
insert into enum_info_sources (description) values ('clinician');
insert into enum_info_sources (description) values ('relative');
insert into enum_info_sources (description) values ('carer');
insert into enum_info_sources (description) values ('notes');
insert into enum_info_sources (description) values ('correspondence');

create table clinical_history(
	id SERIAL primary key,
	id_enum_clinical_history int REFERENCES enum_clinical_history (id),
	id_clinical_transaction int  REFERENCES clinical_transaction (id),
	id_info_sources int REFERENCES enum_info_sources (id),
	text text
)inherits (audit_clinical);

COMMENT ON TABLE clinical_history is
'narrative details of history taken during a clinical encounter';

COMMENT ON COLUMN clinical_history.id_enum_clinical_history is
'the type of history taken';

COMMENT ON COLUMN clinical_history.id_clinical_transaction is
'The transaction during which this history was taken';

COMMENT ON COLUMN clinical_history.text is
'The text typed by the doctor';


create table enum_coding_systems (
	id SERIAL primary key,
	description text
)inherits (audit_clinical);


COMMENT ON TABLE enum_coding_systems is
'The various types of coding systems available';

INSERT INTO enum_coding_systems (description)
	values ('general');
INSERT INTO enum_coding_systems (description)
	values ('clinical');
INSERT INTO enum_coding_systems (description)
	values ('diagnosis');
INSERT INTO enum_coding_systems (description)
	values ('therapy');
INSERT INTO enum_coding_systems (description)
	values ('pathology');
INSERT INTO enum_coding_systems (description)
	values ('bureaucratic');
INSERT INTO enum_coding_systems (description)
	values ('ean');
INSERT INTO enum_coding_systems (description)
	values ('other');


create table coding_systems (
	id SERIAL primary key,
	id_enum_coding_systems int REFERENCES enum_coding_systems (id),
	description text,
	version char(6),
	deprecated timestamp
)inherits (audit_clinical);

comment on table coding_systems is
'The coding systems in this database.';

create table clinical_diagnosis (
	id SERIAL primary key,
	id_clinical_transaction int  REFERENCES clinical_transaction (id),
	approximate_start text DEFAULT null,
	code char(16),
	id_coding_systems int REFERENCES coding_systems (id),
	text text
)inherits (audit_clinical);

COMMENT ON TABLE clinical_diagnosis is
'Coded clinical diagnoses assigned to patient, in addition to history';

comment on column clinical_diagnosis.id_clinical_transaction is
'the transaction in which this diagnosis was made.';

comment on column clinical_diagnosis.approximate_start is
'around the time at which this diagnosis was made';

comment on column clinical_diagnosis.code is
'the code';
comment on column clinical_diagnosis.id_coding_systems is
'the coding system used to code the diagnosis';

comment on column clinical_diagnosis.text is
'extra notes on the diagnosis';

create table enum_confidentiality_level (
	id SERIAL primary key,
	description text
)inherits (audit_clinical);

comment on table enum_confidentiality_level is
'Various levels of confidentialoty of a coded diagnosis, such as public, clinical staff, treating docotr, etc.';

INSERT INTO enum_confidentiality_level (description)
	values ('public');
INSERT INTO enum_confidentiality_level (description)
	values ('relatives');
INSERT INTO enum_confidentiality_level (description)
	values ('receptionist');
INSERT INTO enum_confidentiality_level (description)
	values ('clinical staff');
INSERT INTO enum_confidentiality_level (description)
	values ('doctors');
INSERT INTO enum_confidentiality_level (description)
	values ('doctors of practice only');
INSERT INTO enum_confidentiality_level (description)
	values ('treating doctor');

create table clinical_diagnosis_extra (
	id SERIAL primary key,
	id_clinical_diagnosis int REFERENCES clinical_diagnosis (id),
	id_enum_confidentiality_level int REFERENCES enum_confidentiality_level (id)

)inherits (audit_clinical);

comment on table clinical_diagnosis_extra is
'Extra information about a diagnosis, just the confidentiality level at present.';


-- =============================================
-- do simple schema revision tracking
\i gmSchemaRevision.sql
INSERT INTO schema_revision (filename, version) VALUES('$RCSfile: gmclinical.sql,v $', '$Revision: 1.6 $');

-- =============================================
-- $Log: gmclinical.sql,v $
-- Revision 1.6  2002-12-01 13:53:09  ncq
-- - missing ; at end of schema tracking line
--
-- Revision 1.5  2002/11/23 13:18:09  ncq
-- - add "proper" metadata handling and schema revision tracking
--
