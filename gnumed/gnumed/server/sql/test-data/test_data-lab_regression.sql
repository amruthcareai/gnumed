-- Projekt GnuMed
-- test data for regression testing lab import

-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>
-- license: GPL
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/test-data/test_data-lab_regression.sql,v $
-- $Revision: 1.16 $
-- =============================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- =============================================
-- identity
delete from identity where
	gender = 'f'
		and
	cob = 'CA'
		and
	pk in (
		select pk_identity
		from v_basic_person
		where firstnames='Laborata'
				and lastnames='Testwoman'
				and dob='1931-3-22+2:00'
	);

insert into identity (gender, dob, cob, title)
values ('f', '1931-3-22+2:00', 'CA', '');

insert into names (id_identity, active, lastnames, firstnames)
values (currval('identity_pk_seq'), true, 'Testwoman', 'Laborata');


delete from xlnk_identity where xfk_identity = currval('identity_pk_seq');

insert into xlnk_identity (xfk_identity, pupic)
values (currval('identity_pk_seq'), currval('identity_pk_seq'));


-- encounter
insert into clin_encounter (
	fk_patient,
	fk_location,
	fk_provider,
	fk_type,
	description
) values (
	currval('identity_pk_seq'),
	-1,
	(select pk_staff from v_staff where firstnames='Leonard Horatio' and lastnames='McCoy' and dob='1920-1-20+2:00'),
	(select pk from encounter_type where description='chart review'),
	'first for this RFE'
);


-- episode
delete from clin_episode where pk in (
	select pk_episode
	from v_pat_episodes
	where pk_patient = currval('identity_pk_seq')
);

insert into clin_episode (
	description,
	fk_patient,
	is_open
) values (
	'lab import regression test',
	currval('identity_pk_seq'),
	true
);

-- lab request
insert into lab_request (
	fk_encounter,
	fk_episode,
	narrative,
	fk_test_org,
	request_id,
	fk_requestor,
	is_pending,
	request_status
) values (
	currval('clin_encounter_id_seq'),
	currval('clin_episode_pk_seq'),
	'used for anonymized import regression tests',
	(select pk from test_org where internal_name='your own practice'),
	'anon: sample ID',
	(select pk_identity from v_basic_person where firstnames='Leonard Horatio' and lastnames='McCoy' and dob='1920-1-20+2:00'::timestamp),
	true,
	'pending'
);

-- =============================================
-- do simple schema revision tracking
delete from gm_schema_revision where filename like '$RCSfile: test_data-lab_regression.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: test_data-lab_regression.sql,v $', '$Revision: 1.16 $');

-- =============================================
-- $Log: test_data-lab_regression.sql,v $
-- Revision 1.16  2005-03-31 20:09:32  ncq
-- - lab_request not requires non-null status
--
-- Revision 1.15  2005/03/14 14:47:37  ncq
-- - adjust to id_patient -> pk_patient
-- - add family history on Kirk's brother
--
-- Revision 1.14  2005/02/13 15:08:23  ncq
-- - add names of actors and some comments
--
-- Revision 1.13  2005/02/12 13:49:14  ncq
-- - identity.id -> identity.pk
-- - allow NULL for identity.fk_marital_status
-- - subsequent schema changes
--
-- Revision 1.12  2004/12/14 01:44:50  ihaywood
-- gmPsql now supports BEGIN..COMMIT. Note that without a "begin" it reverts
-- to the old one-line-one-transaction mode, so a lone commit is useless
-- (this is the change to test_data-lab_regression)
--
-- Revision 1.11  2004/12/06 21:11:12  ncq
-- - properly insert episode, alas, Psql.py does not support that
--   yet, psql, however, does
--
-- Revision 1.10  2004/11/28 14:38:18  ncq
-- - some more deletes
-- - use new method of episode naming
-- - this actually bootstraps again
--
-- Revision 1.9  2004/11/16 18:59:57  ncq
-- - adjust to episode naming changes
--
-- Revision 1.8  2004/09/17 21:00:18  ncq
-- - IF health issue then MUST have description
--
-- Revision 1.7  2004/09/17 20:18:10  ncq
-- - clin_episode_id_seq -> *_pk_seq
--
-- Revision 1.6  2004/06/26 23:45:51  ncq
-- - cleanup, id_* -> fk/pk_*
--
-- Revision 1.5  2004/06/26 07:33:55  ncq
-- - id_episode -> fk/pk_episode
--
-- Revision 1.4  2004/06/02 13:46:46  ncq
-- - setting default session timezone has incompatible syntax
--   across version range 7.1-7.4, henceforth specify timezone
--   directly in timestamp values, which works
--
-- Revision 1.3  2004/06/02 00:14:47  ncq
-- - add time zone setting
--
-- Revision 1.2  2004/05/30 21:03:29  ncq
-- - encounter_type.id -> encounter_type.pk
--
-- Revision 1.1  2004/05/12 23:54:37  ncq
-- - used for regression testing lab handling
--
