-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
-- .fk_brand
comment on column clin.vaccine.fk_brand is
	'The brand of this vaccine, can be a fake entry in ref.branded_drug.';

\unset ON_ERROR_STOP
alter table clin.vaccine drop constraint vaccine_fk_brand_fkey cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccine
	add foreign key (fk_brand)
		references ref.branded_drug(pk)
		on update cascade
		on delete restrict;


-- .min_age
\unset ON_ERROR_STOP
alter table clin.vaccine drop constraint vaccine_min_age_check cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccine
	alter column min_age
		drop not null;

alter table clin.vaccine
	add constraint vaccine_sane_min_age
		check (
			(min_age is null)
				or
			(
				((max_age is null) and (min_age < '150 years'::interval))
					or
				((max_age is not null) and (min_age <= max_age))
			)
		);



-- .max_age
\unset ON_ERROR_STOP
alter table clin.vaccine drop constraint vaccine_check cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccine
	alter column max_age
		drop not null;

alter table clin.vaccine
	add constraint vaccine_sane_max_age
		check (
			(max_age is null)
				or
			(max_age < '150 years'::interval)
				or
			(max_age = '5555 years'::interval)
		);

-- --------------------------------------------------------------
-- generic mono-valent vaccines
create or replace function gm.create_generic_monovalent_vaccines()
	returns boolean
	language plpgsql
	as '
DECLARE
	_row record;
	_generic_name text;
	_pk_brand integer;
	_pk_vaccine integer;
BEGIN
	for _row in select * from clin.vacc_indication loop

		_generic_name := _row.description || '' (generic vaccine)'';
		raise notice ''re-creating [%]'', _generic_name;

		-- retrieve or create ref.branded_drug entry for indication
		select pk into _pk_brand from ref.branded_drug
		where
			is_fake is true
				and
			description = _generic_name;

		if FOUND is false then
			insert into ref.branded_drug (
				description,
				preparation,
				is_fake,
				atc_code
			) values (
				_generic_name,
				''vaccine'',		-- this is rather arbitrary
				True,
				coalesce(_row.atcs_mono_indication[1], ''J07'')
			)
			returning pk
			into _pk_brand;
		end if;

		-- retrieve or create clin.vaccine entry for generic brand
		select pk into _pk_vaccine from clin.vaccine
		where fk_brand = _pk_brand;

		if FOUND is false then
			insert into clin.vaccine (
				id_route,
				is_live,
				fk_brand
			) values (
				(select id from clin.vacc_route where abbreviation = ''i.m.''),
				false,
				_pk_brand
			)
			returning pk
			into _pk_vaccine;
		end if;

		-- link indication to vaccine
		delete from clin.lnk_vaccine2inds
		where
			fk_vaccine = _pk_vaccine;

		insert into clin.lnk_vaccine2inds (
			fk_vaccine,
			fk_indication
		) values (
			_pk_vaccine,
			_row.id
		);

	end loop;

	return true;
END;';

select gm.create_generic_monovalent_vaccines();

-- --------------------------------------------------------------
-- improve ATC codes of pre-existing vaccines
update ref.branded_drug set
	atc_code = 'J07AM01'
where
	description = 'Tetasorbat SSW (Tetanus)';

update ref.branded_drug set
	atc_code = 'J07AM51'
where
	description = 'Td-pur (Td)';

update ref.branded_drug set
	atc_code = 'J07BC02'
where
	description = 'Havrix 720 Kinder (HAV)';

update ref.branded_drug set
	atc_code = 'J07BC02'
where
	description = 'Havrix 1440 (HAV)';

update ref.branded_drug set
	atc_code = 'J07BC01'
where
	description = 'HBVAXPRO (HBVAXPRO)';

update ref.branded_drug set
	atc_code = 'J07AL02'
where
	description = 'Prevenar (Prevenar)';

update ref.branded_drug set
	atc_code = 'J07BB01'
where
	description = 'InfectoVac Flu 2003/2004 (Flu 03)';

update ref.branded_drug set
	atc_code = 'J07BB01'
where
	description = 'InfectoVac Flu 2004/2005 (Flu 04)';

update ref.branded_drug set
	atc_code = 'J07AH07'
where
	description = 'NeisVac-C, Meningokokken-C-Konjugat (NeisVac-C)';

update ref.branded_drug set
	atc_code = 'J07AH07'
where
	description = 'Menjugate, Meningokokken-C-Konjugat (Menjugate)';

update ref.branded_drug set
	atc_code = 'J07AH07'
where
	description = 'Meningitec (Meningitec)';

update ref.branded_drug set
	atc_code = 'J07CA02'
where
	description = 'REPEVAX (Repevax)';

update ref.branded_drug set
	atc_code = 'J07CA01'
where
	description = 'REVAXIS (Revaxis)';

update ref.branded_drug set
	atc_code = 'J07BA01'
where
	description = 'FSME-IMMUN 0.25ml Junior (FSME)';

update ref.branded_drug set
	atc_code = 'J07BA01'
where
	description = 'Encepur Kinder (Encepur K)';

update ref.branded_drug set
	atc_code = 'J07BD52'
where
	description = 'PRIORIX (Priorix)';

update ref.branded_drug set
	atc_code = 'J07BD01'
where
	description = 'Masern-Impfstoff Mérieux (Masern)';

update ref.branded_drug set
	atc_code = 'J07CA06'
where
	description = 'INFANRIX-IPV+HIB (Infanrix)';

update ref.branded_drug set
	atc_code = 'J07AG01'
where
	description = 'Act-HiB (HiB)';

update ref.branded_drug set
	atc_code = 'J07CA06'
where
	description = 'PentaVac (PentaVac)';

update ref.branded_drug set
	atc_code = 'J07BF03'
where
	description = 'IPV Mérieux (IPV)';

update ref.branded_drug set
	atc_code = 'J07AP03'
where
	description = 'Typhim Vi (Typhus)';

update ref.branded_drug set
	atc_code = 'J07BC01'
where
	description = 'Hepatitis B (Hep B)';

--update ref.branded_drug set
--	atc_code = 'J07'
--where
--	description = 'diptheria-tetanus-acellular pertussis infant/child formulation (DTPa)';
--
--update ref.branded_drug set
--	atc_code = 'J07'
--where
--	description = 'diptheria-tetanus-acellular pertussis adult/adolescent formulation (dTpa)';

update ref.branded_drug set
	atc_code = 'J07AG01'
where
	description = 'Haemophilius influenzae type b (PRP-OMP)';

update ref.branded_drug set
	atc_code = 'J07AG01'
where
	description = 'Haemophilius influenzae type b(PRP-T) (PRP-T)';

update ref.branded_drug set
	atc_code = 'J07AG01'
where
	description = 'Haemophilius influenzae type b(HbOC) (HbOC)';

update ref.branded_drug set
	atc_code = 'J07BF03'
where
	description = 'inactivated poliomyelitis vaccine (IPV)';

update ref.branded_drug set
	atc_code = 'J07BK01'
where
	description = 'varicella-zoster vaccine (VZV)';

update ref.branded_drug set
	atc_code = 'J07AL02'
where
	description = '7-valent pneumococcal conjugate vaccine (7vPCV)';

update ref.branded_drug set
	atc_code = 'J07AL02'
where
	description = '23-valent pneumococcal polysaccharide vaccine (23vPPV)';

update ref.branded_drug set
	atc_code = 'J07AH07'
where
	description = 'meningococcal C conjugate vaccine (menCCV)';

update ref.branded_drug set
	atc_code = 'J07AM51'
where
	description = 'adult diptheria-tetanus (dT)';

update ref.branded_drug set
	atc_code = 'J07BF02'
where
	description = 'oral poliomyelitis vaccine (OPV)';

update ref.branded_drug set
	atc_code = 'J07BD52'
where
	description = 'measles-mumps-rubella vaccine (MMR)';

update ref.branded_drug set
	atc_code = 'J07BB01'
where
	description = 'influenza vaccine (influenza)';

update ref.branded_drug set
	atc_code = 'J07AM01'
where
	description = 'Tetasorbat (SFCMS) (Tetanus)';

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_vaccines cascade;
\set ON_ERROR_STOP 1

create view clin.v_vaccines as

	select
		clv.pk
			as pk_vaccine,

		rbd.description
			as vaccine,
		rbd.preparation
			as preparation,
		rbd.atc_code
			as atc_code,
		rbd.is_fake
			as is_fake_vaccine,

		cvr.abbreviation
			as route_abbreviation,
		cvr.description
			as route_description,

		clv.is_live,
		clv.min_age,
		clv.max_age,
		clv.comment,

		rbd.external_code,
		rbd.external_code_type,

		clv.id_route
			as pk_route,
		clv.fk_brand
			as pk_brand,

		rbd.fk_data_source
			as pk_data_source

	from
		clin.vaccine clv
			join ref.branded_drug rbd on (clv.fk_brand = rbd.pk)
				join clin.vacc_route cvr on (clv.id_route = cvr.id)

;

comment on view clin.v_vaccines is
	'A list of vaccines.';

grant select on clin.v_vaccines to group "gm-public";

-- --------------------------------------------------------------
select gm.log_script_insertion('$RCSfile: v14-clin-vaccine-dynamic.sql,v $', '$Revision: 1.3 $');
