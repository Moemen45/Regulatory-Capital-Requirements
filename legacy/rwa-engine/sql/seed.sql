-- =====================================================================
-- Seed data — reporting date 2026-09-30. All amounts in EUR.
-- Each loan is designed to hit one specific branch of the rules.
-- =====================================================================

-- ---------- Rating -> CQS ----------
INSERT INTO rating_cqs VALUES
 ('AAA',1),('AA+',1),('AA',1),('AA-',1),
 ('A+',2),('A',2),('A-',2),
 ('BBB+',3),('BBB',3),('BBB-',3),
 ('BB+',4),('BB',4),('BB-',4),
 ('B+',5),('B',5),('B-',5),
 ('CCC+',6),('CCC',6),('CCC-',6),('CC',6),('C',6),('D',6);

-- ---------- Risk weights by class and CQS (0 = unrated) ----------
-- Sovereigns (CRE20.7)
INSERT INTO risk_weight VALUES
 ('SOVEREIGN',1,0.00),('SOVEREIGN',2,0.20),('SOVEREIGN',3,0.50),
 ('SOVEREIGN',4,1.00),('SOVEREIGN',5,1.00),('SOVEREIGN',6,1.50),('SOVEREIGN',0,1.00);
-- Institutions, ECRA (CRE20.16). Unrated banks would go to SCRA;
-- simplification here: every unrated bank treated as SCRA Grade B = 75%.
INSERT INTO risk_weight VALUES
 ('INSTITUTION',1,0.20),('INSTITUTION',2,0.30),('INSTITUTION',3,0.50),
 ('INSTITUTION',4,1.00),('INSTITUTION',5,1.00),('INSTITUTION',6,1.50),('INSTITUTION',0,0.75);
-- Corporates (CRE20.42)
INSERT INTO risk_weight VALUES
 ('CORPORATE',1,0.20),('CORPORATE',2,0.50),('CORPORATE',3,0.75),
 ('CORPORATE',4,1.00),('CORPORATE',5,1.50),('CORPORATE',6,1.50),('CORPORATE',0,1.00);
-- SME corporates: rated -> corporate table; unrated -> 85% (CRE20.47)
INSERT INTO risk_weight VALUES
 ('CORPORATE_SME',1,0.20),('CORPORATE_SME',2,0.50),('CORPORATE_SME',3,0.75),
 ('CORPORATE_SME',4,1.00),('CORPORATE_SME',5,1.50),('CORPORATE_SME',6,1.50),('CORPORATE_SME',0,0.85);
-- Retail (CRE20.65-67): regulatory retail 75%, other retail 100%. Ratings not used.
INSERT INTO risk_weight VALUES
 ('RETAIL_REGULATORY',0,0.75),('RETAIL_OTHER',0,1.00);

-- ---------- CCFs (CRE20.94-101, simplified) ----------
INSERT INTO ccf VALUES
 ('NONE',0.00),('COMMITTED',0.40),('UNCONDITIONALLY_CANCELLABLE',0.10);

-- ---------- Residential RE, general, whole-loan approach (CRE20.82) ----------
INSERT INTO rre_ltv_band VALUES
 (0.50,0.20),(0.60,0.25),(0.80,0.30),(0.90,0.40),(1.00,0.50),(999.0,0.70);

-- ---------- Counterparties (fictional) ----------
INSERT INTO counterparty VALUES
 ('C001','Republic of Examplia',      'SOVEREIGN',  'MT','A',    NULL),
 ('C002','Harbour Bank plc',          'INSTITUTION','MT','BBB+', NULL),
 ('C003','Coastal Savings Bank',      'INSTITUTION','MT',NULL,   NULL),
 ('C004','Atlas Logistics Ltd',       'CORPORATE',  'FR','A-',   400000000),
 ('C005','Medina Foods SARL',         'CORPORATE',  'FR',NULL,   30000000),
 ('C006','Nour Textiles',             'CORPORATE',  'TN',NULL,   5000000),
 ('C007','Individual A',              'INDIVIDUAL', 'MT',NULL,   NULL),
 ('C008','Individual B',              'INDIVIDUAL', 'MT',NULL,   NULL),
 ('C009','Individual C',              'INDIVIDUAL', 'MT',NULL,   NULL),
 ('C010','Individual D',              'INDIVIDUAL', 'MT',NULL,   NULL),
 ('C011','Individual E',              'INDIVIDUAL', 'MT',NULL,   NULL),
 ('C012','Borealis Shipping SA',      'CORPORATE',  'LU','BB',   200000000),
 ('C013','Tidewater Retail Group',    'CORPORATE',  'NL','CCC+', 80000000),
 ('C014','Individual F (private bkg)','INDIVIDUAL', 'LU',NULL,   NULL),
 ('C015','Sirocco Ceramics',          'CORPORATE',  'TN',NULL,   10000000);

-- ---------- Loans ----------
-- loan_id, cpty, date, product, ccy, drawn, undrawn, commitment, property_value, dpd, provisions
INSERT INTO loan VALUES
 ('L001','C001','2026-09-30','TERM_LOAN',         'EUR',10000000,      0,'NONE',                       NULL,  0,     0),
 ('L002','C002','2026-09-30','INTERBANK_LOAN',    'EUR', 3000000,      0,'NONE',                       NULL,  0,     0),
 ('L003','C003','2026-09-30','INTERBANK_LOAN',    'EUR', 1000000,      0,'NONE',                       NULL,  0,     0),
 ('L004','C004','2026-09-30','REVOLVING_FACILITY','EUR', 5000000,3000000,'COMMITTED',                  NULL,  0,     0),
 ('L005','C005','2026-09-30','TERM_LOAN',         'EUR', 2500000,      0,'NONE',                       NULL,  0,     0),
 ('L006','C006','2026-09-30','TERM_LOAN',         'EUR',  400000,      0,'NONE',                       NULL,  0,     0),
 ('L007','C006','2026-09-30','OVERDRAFT',         'EUR',   50000, 150000,'UNCONDITIONALLY_CANCELLABLE', NULL,  0,     0),
 ('L008','C007','2026-09-30','MORTGAGE',          'EUR',  180000,      0,'NONE',                     400000,  0,     0),
 ('L009','C008','2026-09-30','MORTGAGE',          'EUR',  255000,      0,'NONE',                     300000,  0,     0),
 ('L010','C009','2026-09-30','CONSUMER_LOAN',     'EUR',   15000,      0,'NONE',                       NULL,  0,     0),
 ('L011','C009','2026-09-30','CREDIT_CARD',       'EUR',    3000,   7000,'UNCONDITIONALLY_CANCELLABLE', NULL,  0,     0),
 ('L012','C010','2026-09-30','PERSONAL_LOAN',     'EUR',   20000,      0,'NONE',                       NULL,120,  2000),
 ('L013','C011','2026-09-30','MORTGAGE',          'EUR',  150000,      0,'NONE',                     140000,200, 30000),
 ('L014','C012','2026-09-30','TERM_LOAN',         'EUR', 4000000,      0,'NONE',                       NULL,  0,     0),
 ('L015','C013','2026-09-30','TERM_LOAN',         'EUR', 1500000,      0,'NONE',                       NULL,  0,     0),
 ('L016','C014','2026-09-30','LOMBARD_LOAN',      'EUR', 1200000,      0,'NONE',                       NULL,  0,     0),
 ('L017','C007','2026-09-30','CONSUMER_LOAN',     'EUR',   20000,      0,'NONE',                       NULL,  0,     0),
 ('L018','C015','2026-09-30','TERM_LOAN',         'EUR',  500000,      0,'NONE',                       NULL, 95,150000);
