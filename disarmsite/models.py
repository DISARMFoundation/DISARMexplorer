from sqlalchemy import Column, Integer, String, Text, ForeignKey
from disarmsite.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'


class Phase(Base):
    __tablename__ = 'phase'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    rank = Column(Integer)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, rank=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.rank = rank
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Phase {self.disarm_id!r} {self.name!r}>'


class Tactic(Base):
    __tablename__ = 'tactic'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    phase_id = Column(String(20), ForeignKey('phase.disarm_id'))
    rank = Column(Integer)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, phase_id=None, 
        rank=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.phase_id = phase_id
        self.rank = rank
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Tactic {self.disarm_id!r} {self.name!r}>'


class Framework(Base):
    __tablename__ = 'framework'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Framework {self.disarm_id!r} {self.name!r}>'


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.disarm_id'))
    framework_id = Column(String(20), ForeignKey('framework.disarm_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, tactic_id=None, framework_id=None, 
        name=None, summary=None):
        self.disarm_id = disarm_id
        self.tactic_id = tactic_id
        self.framework_id = framework_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Task {self.disarm_id!r} {self.name!r}>'


class Technique(Base):
    __tablename__ = 'technique'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.disarm_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, tactic_id=None, 
        name=None, summary=None):
        self.disarm_id = disarm_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Technique {self.disarm_id!r} {self.name!r}>'


class Example(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    object_id = Column(String(20))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, object_id=None, 
        name=None, summary=None):
        self.disarm_id = disarm_id
        self.object_id = object_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Example {self.disarm_id!r} {self.name!r}>'


class Playbook(Base):
    __tablename__ = 'playbook'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    object_id = Column(String(20))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, object_id=None, 
        name=None, summary=None):
        self.disarm_id = disarm_id
        self.object_id = object_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Playbook {self.disarm_id!r} {self.name!r}>'


class Counter(Base):
    __tablename__ = 'counter'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    metatechnique_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.disarm_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, metatechnique_id=None, tactic_id=None, 
        name=None, summary=None):
        self.disarm_id = disarm_id
        self.metatechnique_id = metatechnique_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Counter {self.disarm_id!r} {self.name!r}>'


class Resource(Base):
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)
    resource_type = Column(String(200))

    def __init__(self, disarm_id=None, name=None, summary=None, resource_type=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary
        self.resource_type = resource_type

    def __repr__(self):
        return f'<Resource {self.disarm_id!r} {self.name!r}>'


class Responsetype(Base):
    __tablename__ = 'responsetype'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Responsetype {self.disarm_id!r} {self.name!r}>'


class Detection(Base):
    __tablename__ = 'detection'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.disarm_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, tactic_id=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Counter {self.disarm_id!r} {self.name!r}>'


class Metatechnique(Base):
    __tablename__ = 'metatechnique'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, disarm_id=None, name=None, summary=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Metatechnique {self.disarm_id!r} {self.name!r}>'


class CounterTactic(Base):
    __tablename__ = 'counter_tactic'
    id = Column(Integer, primary_key=True)
    counter_id = Column(String(20), ForeignKey('counter.disarm_id'))
    tactic_id = Column(String(20), ForeignKey('tactic.disarm_id'))
    main_tactic = Column(String(3))
    summary = Column(Text)

    def __init__(self, counter_id=None, tactic_id=None, 
        main_tactic=None, summary=None):
        self.counter_id = counter_id
        self.tactic_id = tactic_id
        self.main_tactic = main_tactic
        self.summary = summary

    def __repr__(self):
        return f'<CounterTactic {self.counter_id!r} {self.tactic_id!r}>'


class CounterTechnique(Base):
    __tablename__ = 'counter_technique'
    id = Column(Integer, primary_key=True)
    counter_id = Column(String(20), ForeignKey('counter.disarm_id'))
    technique_id = Column(String(20), ForeignKey('technique.disarm_id'))
    summary = Column(Text)

    def __init__(self, counter_id=None, technique_id=None, summary=None):
        self.counter_id = counter_id
        self.technique_id = technique_id
        self.summary = summary

    def __repr__(self):
        return f'<CounterTechnique {self.counter_id!r} {self.technique_id!r}>'


class DetectionTechnique(Base):
    __tablename__ = 'detection_technique'
    id = Column(Integer, primary_key=True)
    detection_id = Column(String(20), ForeignKey('detection.disarm_id'))
    technique_id = Column(String(20), ForeignKey('technique.disarm_id'))
    summary = Column(Text)

    def __init__(self, detection_id=None, technique_id=None, summary=None):
        self.detection_id = detection_id
        self.technique_id = technique_id
        self.summary = summary

    def __repr__(self):
        return f'<DetectionTechnique {self.detection_id!r} {self.technique_id!r}>'

class IncidentTechnique(Base):
    __tablename__ = 'incident_technique'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    incident_id = Column(String(20), ForeignKey('incident.disarm_id'))
    technique_id = Column(String(20), ForeignKey('technique.disarm_id'))
    summary = Column(Text)

    def __init__(self, name=None, incident_id=None, technique_id=None, summary=None):
        self.name = name
        self.incident_id = incident_id
        self.technique_id = technique_id
        self.summary = summary

    def __repr__(self):
        return f'<IncidentTechnique {self.incident_id!r} {self.technique_id!r}>'


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)
    url = Column(Text)
    sector = Column(String(200))
    primary_role = Column(String(200))
    secondary_role = Column(String(200))
    primary_subject = Column(String(200))
    secondary_subject = Column(String(200))
    volunteers = Column(String(3))
    region = Column(String(200))
    country = Column(String(200))
    twitter_handle = Column(String(200))

    def __init__(self, disarm_id=None, name=None, summary=None, url=None, sector=None, primary_role=None, 
        secondary_role=None, primary_subject=None, secondary_subject=None, volunteers=None, 
        region=None, country=None, twitter_handle=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary
        self.url = url
        self.sector = sector
        self.primary_role = primary_role
        self.secondary_role = secondary_role
        self.primary_subject = primary_subject
        self.secondary_subject = secondary_subject
        self.volunteers = volunteers
        self.region = region
        self.country = country
        self.twitter_handle = twitter_handle

    def __repr__(self):
        return f'<Group {self.disarm_id!r} {self.name!r}>'

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)
    objecttype = Column(String(200))
    year_started = Column(Integer)
    attributions_seen = Column(String(200))
    found_in_country = Column(String(200))

    def __init__(self, disarm_id=None, name=None, summary=None, objecttype=None, year_started=None, 
        attributions_seen=None, found_in_country=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary
        self.objecttype = objecttype
        self.year_started = year_started
        self.attributions_seen = attributions_seen
        self.found_in_country = found_in_country

    def __repr__(self):
        return f'<Incident {self.disarm_id!r} {self.name!r}>'

class Tool(Base):
    __tablename__ = 'tool'
    id = Column(Integer, primary_key=True)
    disarm_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)
    organization = Column(String(200))
    url = Column(Text)
    category = Column(String(200))
    disinformation_use = Column(String(200))
    cogseccollab_use = Column(String(200))
    function = Column(Text)
    code_url = Column(Text)
    artifacts = Column(String(200))
    automation = Column(String(200))
    platform = Column(String(200))
    accessibility = Column(String(200))

    # FIXIT: move from organization to group_id
    def __init__(self, disarm_id=None, name=None, summary=None, organization=None, url=None, 
        category=None, disinformation_use=None, cogseccollab_use=None, function=None, code_url=None, 
        artifacts=None, automation=None, platform=None, accessibility=None):
        self.disarm_id = disarm_id
        self.name = name
        self.summary = summary
        self.organization = organization
        self.url = url
        self.category = category
        self.disinformation_use = disinformation_use
        self.cogseccollab_use = cogseccollab_use
        self.function = function
        self.code_url = code_url
        self.artifacts = artifacts
        self.automation = automation
        self.platform = platform
        self.accessibility = accessibility
 
    def __repr__(self):
        return f'<Tool {self.disarm_id!r} {self.name!r}>'


'''
/* CREATE TABLE IF NOT EXISTS sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

/* CREATE TABLE IF NOT EXISTS reference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

/* CREATE TABLE IF NOT EXISTS dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);*/

/* CREATE TABLE IF NOT EXISTS actor_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  sector_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector (disarm_id),
  FOREIGN KEY (framework_id) REFERENCES framework (disarm_id)
); */

/* CREATE TABLE IF NOT EXISTS response_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disarm_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);*/

/* CREATE TABLE IF NOT EXISTS playbook (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  summary TEXT NOT NULL
);*/
'''
