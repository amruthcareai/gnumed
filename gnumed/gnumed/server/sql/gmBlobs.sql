-- blob tables for GNUmed

-- license: GPL
-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>

-- $Revision: 1.8 $ $Date: 2002-04-13 14:41:57 $ $Author: ncq $

-- =============================================
CREATE TABLE "doc_type" (
    "id" serial primary key,
    "name" character varying(40)
);

INSERT INTO doc_type(id, name) values(1,'discharge summary internal');
INSERT INTO doc_type(id, name) values(2,'discharge summary surgical');
INSERT INTO doc_type(id, name) values(3,'discharge summary psychiatric');
INSERT INTO doc_type(id, name) values(4,'discharge summary neurological');
INSERT INTO doc_type(id, name) values(4,'discharge summary orthopaedic');
INSERT INTO doc_type(id, name) values(5,'discharge summary other');

INSERT INTO doc_type(id, name) values(6,'referral report internal');
INSERT INTO doc_type(id, name) values(6,'referral report surgical');
INSERT INTO doc_type(id, name) values(6,'referral report ENT');
INSERT INTO doc_type(id, name) values(6,'referral report eye');
INSERT INTO doc_type(id, name) values(6,'referral report urology');
INSERT INTO doc_type(id, name) values(6,'referral report orthopaedic');
INSERT INTO doc_type(id, name) values(6,'referral report neuro');
INSERT INTO doc_type(id, name) values(6,'referral report radiology');
INSERT INTO doc_type(id, name) values(6,'referral report other');

-- add any number of types here, this is just to give you an idea

-- =============================================
CREATE TABLE "doc_med" (
    "id" serial primary key,
    "patient_id" integer references identity not null,
    "type" integer references doc_type(id) not null,
    "comment" character varying(60) not null,
    "date" character varying(20) not null,
    "ext_ref" character varying (40) not null
);

COMMENT ON TABLE "doc_med" IS 'a medical document object possibly containing several data objects such as several pages of a paper document';
COMMENT ON COLUMN doc_med.type IS 'semantic type of document (not type of file or mime type), such as "referral letter", "discharge summary", etc.';
COMMENT ON COLUMN doc_med.comment IS 'additional short comment such as "abdominal", "ward 3, Dr. Stein", etc.';
COMMENT ON COLUMN doc_med.date IS 'date of document content creation (such as exam date), NOT date of document creation or date of import; may be imprecise such as "7/99"';
COMMENT ON COLUMN doc_med.ext_ref IS 'external reference string of physical document, original paper copy can be found with this';

-- =============================================
CREATE TABLE "doc_med_external_ref" (
    doc_id int references doc_med(id),
    refcounter int default 0
);

-- =============================================
CREATE TABLE "doc_obj" (
    "doc_id" integer references doc_med(id),
    "comment" character varying(30),
    "data" bytea
);

COMMENT ON TABLE "doc_obj" IS 'several of these may form a medical document such as multiple scanned pages/images';
COMMENT ON COLUMN doc_obj.comment IS 'optional tiny comment for this object, such as "page 1"';

-- =============================================
CREATE TABLE "doc_desc" (
    "doc_id" integer references doc_med(id),
    "text" text
);

COMMENT ON TABLE "doc_desc" is 'A textual description of the content such as a result summary. Several of these may belong to one document object.';

-- =============================================

-- questions:
--  - do we need doc_desc linkeable to doc_obj, too ?
--  - do we need a "source" field in doc_desc so we can distinguish between "that's what the OCR software understood from this referral letter scan" vs "that's what the cardiologist thinks of this ECG"
--  - how do we protect documents from being accessed by unauthorized users ?
--    - on access search for the oid in gmCrypto tables for a matching key/PW hash record ??
--  - should (potentially large) binary objects be moved to audit tables ?!?

-- notes:
-- - as this uses BYTEA for storing binary data we have the following limitations
--   - needs postgres >= 7.1
--   - needs proper escaping of NUL, \ and ' (should go away once postgres 7.3 arrives)
--   - has a 1 GB limit for data objects
-- - we explicitely don't store MIME types etc. as selecting an appropriate viewer is a runtime issue
