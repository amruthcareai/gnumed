-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
drop index if exists dem.idx_trgm_dem_org_desc cascade;
create index idx_trgm_dem_org_desc on dem.org using gin (description pgtrgm.gin_trgm_ops);

-- --------------------------------------------------------------
drop index if exists dem.idx_trgm_dem_org_unit_desc cascade;
create index idx_trgm_dem_org_unit_desc on dem.org_unit using gin (description pgtrgm.gin_trgm_ops);

-- --------------------------------------------------------------
select gm.log_script_insertion('v21-dem-org-trgm_idx.sql', '21.0');
