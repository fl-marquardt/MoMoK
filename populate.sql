-- Basic data for Moorgrundbuch

-- Clusters
INSERT INTO clusters (name, description) VALUES
('Nordmoor', 'Moorgebiet im Norden'),
('Suedmoor', 'Moorgebiet im Sueden'),
('Ostmoor', 'Moorgebiet im Osten'),
('Westmoor', 'Moorgebiet im Westen'),
('Zentralmoor', 'Zentrales Moorgebiet');

-- Usage types
INSERT INTO usage_types (name, description) VALUES
('Landwirtschaft', 'Landwirtschaftliche Nutzung'),
('Forstwirtschaft', 'Forstwirtschaftliche Nutzung'),
('Naturschutz', 'Naturschutzgebiet'),
('Renaturierung', 'Renaturierungsprojekt'),
('Torfabbau', 'Torfabbaugebiet'),
('Brache', 'Brachflaeche');

-- Hydrological situations
INSERT INTO hydrological_situations (name, description) VALUES
('Nass', 'Dauerhaft nasse Bedingungen'),
('Feucht', 'Feuchte Bedingungen'),
('Wechselfeucht', 'Wechselnd feuchte Bedingungen'),
('Trocken', 'Trockene Bedingungen'),
('Ueberflutet', 'Zeitweise ueberflutet');

-- Soil types
INSERT INTO soil_types (name, description) VALUES
('Hochmoortorf', 'Torf aus Hochmooren'),
('Niedermoortorf', 'Torf aus Niedermooren'),
('Anmoor', 'Anmooriger Boden'),
('Torfmudde', 'Torfmudde'),
('Mineralboden', 'Mineralischer Boden');

-- Vegetation types
INSERT INTO vegetation_types (name, description) VALUES
('Hochmoorvegetation', 'Typische Hochmoorvegetation'),
('Niedermoorvegetation', 'Typische Niedermoorvegetation'),
('Feuchtwiese', 'Feuchtwiese'),
('Erlenbruchwald', 'Erlenbruchwald'),
('Birkenbruchwald', 'Birkenbruchwald'),
('Schilf', 'Schilfbestand');

-- Institutions
INSERT INTO institutions (name, type, address, city, postal_code, country, phone, email, website) VALUES
('Universitaet Hamburg', 'University', 'Mittelweg 177', 'Hamburg', '20148', 'Deutschland', '+49 40 42838-0', 'info@uni-hamburg.de', 'www.uni-hamburg.de'),
('Landesamt fuer Umwelt Brandenburg', 'Government Agency', 'Seeburger Chaussee 2', 'Potsdam', '14476', 'Deutschland', '+49 33201 442-0', 'info@lfu.brandenburg.de', 'www.lfu.brandenburg.de'),
('NABU Deutschland', 'NGO', 'Charitestrasse 3', 'Berlin', '10117', 'Deutschland', '+49 30 284984-0', 'info@nabu.de', 'www.nabu.de'),
('Thuenen-Institut', 'Research Institute', 'Bundesallee 50', 'Braunschweig', '38116', 'Deutschland', '+49 531 596-0', 'info@thuenen.de', 'www.thuenen.de'); 