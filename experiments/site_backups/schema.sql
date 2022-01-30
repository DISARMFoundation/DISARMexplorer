-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS phase;
-- DROP TABLE IF EXISTS tactic;
-- DROP TABLE IF EXISTS framework;
-- DROP TABLE IF EXISTS task;
-- DROP TABLE IF EXISTS technique;
-- DROP TABLE IF EXISTS counter;
-- DROP TABLE IF EXISTS sector;
-- DROP TABLE IF EXISTS metatechnique;
-- DROP TABLE IF EXISTS reference;
-- DROP TABLE IF EXISTS dataset;
-- DROP TABLE IF EXISTS actor_type;
-- DROP TABLE IF EXISTS incident;
-- DROP TABLE IF EXISTS response_type;
-- DROP TABLE IF EXISTS playbook;
-- DROP TABLE IF EXISTS techniques_counters;


CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS phase (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  rank INTEGER NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tactic (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  phase_id TEXT NOT NULL,
  rank INTEGER NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (phase_id) REFERENCES phase (disarm_id)
);

CREATE TABLE IF NOT EXISTS framework (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (phase_id) REFERENCES phase (disarm_id),
  FOREIGN KEY (framework_id) REFERENCES framework (disarm_id)
);

CREATE TABLE IF NOT EXISTS technique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (tactic_id) REFERENCES tactic (disarm_id)
);

CREATE TABLE IF NOT EXISTS counter (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  metatechnique_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (metatechnique_id) REFERENCES metatechnique (disarm_id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (disarm_id)
);

CREATE TABLE IF NOT EXISTS detection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (tactic_id) REFERENCES tactic (disarm_id)
);

/* CREATE TABLE IF NOT EXISTS sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

CREATE TABLE IF NOT EXISTS metatechnique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

/* CREATE TABLE IF NOT EXISTS reference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actor_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  sector_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector (disarm_id),
  FOREIGN KEY (framework_id) REFERENCES framework (disarm_id)
);

CREATE TABLE IF NOT EXISTS incident (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  incident_type TEXT NOT NULL,
  year_started INTEGER NOT NULL,
  countries TEXT NOT NULL,
  found_via TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS response_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS playbook (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  summary TEXT NOT NULL
);
*/

CREATE TABLE IF NOT EXISTS counter_tactic (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  counter_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  main_tactic TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (counter_id) REFERENCES counter (disarm_id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (disarm_id)
);


CREATE TABLE IF NOT EXISTS counter_technique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  counter_id TEXT NOT NULL,
  technique_id TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (counter_id) REFERENCES counter (disarm_id),
  FOREIGN KEY (technique_id) REFERENCES technique (disarm_id)
);





