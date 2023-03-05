DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS invoice;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  plan TEXT NOT NULL,
  terms BOOLEAN NOT NULL,
  newsletter BOOLEAN NOT NULL,
  name TEXT,
  surname TEXT,
  phone_no INTEGER,
  company_name TEXT,
  street TEXT,
  house_no INTEGER,
  flat_no INTEGER,
  zip_code INTEGER,
  city TEXT,
  tax_no INTEGER,
  bank_account TEXT

);

CREATE TABLE invoice (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_no TEXT NOT NULL,
  invoice_type TEXT NOT NULL,
  issue_date TEXT NOT NULL,
  issuer_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  issue_city TEXT NOT NULL,
  issuer_tax_no INTEGER NOT NULL,
  item TEXT NOT NULL,
  price_net REAL NOT NULL,
  recipient_tax_no INTEGER NOT NULL,
  sell_date TEXT NOT NULL,
  sum_gross REAL NOT NULL,
  sum_net REAL NOT NULL,
  tax_rate REAL NOT NULL,
  unit TEXT NOT NULL,
  currency TEXT NOT NULL,
  -- contractor_id,
  FOREIGN KEY (issuer_id) REFERENCES user (id)
);
