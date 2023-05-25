DROP TABLE protocols;
DROP TABLE sigProp;
DROP TABLE testParameters;
DROP TABLE impedanceCoordinates;
DROP TABLE inputs;
DROP TABLE test;
DROP TABLE person;
DROP TABLE progress;

CREATE TABLE test (
    testId INT NOT NULL,
    testName VARCHAR(10),
    PRIMARY KEY (testId)
);

CREATE TABLE protocols (
    protocolId INT NOT NULL,
    fileName VARCHAR(35),
    testId INT NOT NULL,
    PRIMARY KEY (protocolId),
    FOREIGN KEY (testId) REFERENCES test(testId)
);

CREATE TABLE sigProp (
    sigId INT NOT NULL,
    freq INT NOT NULL,
    amp FLOAT(5) NOT NULL,
    testId INT NOT NULL,
    PRIMARY KEY (sigId),
    FOREIGN KEY (testId) REFERENCES test(testId)
);

CREATE TABLE inputs (
    testId INT NOT NULL,
    inputId INT NOT NULL,
    bip bit(1),
    inputName VARCHAR(5),
    PRIMARY KEY (inputId),
    FOREIGN KEY (testId) REFERENCES test(testId)
);

CREATE TABLE impedanceCoordinates (
    inputId INT NOT NULL,
    x1 INT NOT NULL,
    y1 INT NOT NULL,
    x2 INT NOT NULL,
    y2 INT NOT NULL,
    PRIMARY KEY (inputId),
    FOREIGN KEY (inputId) REFERENCES inputs(inputId)
);

CREATE TABLE testParameters (
    testId int not null,
    oxy bit(1),
    bodypos bit(1),
    impRef bit(1),
    impAct bit(1),
    sig bit(1),
    sigBip bit(1),
    press bit(1),
    flash bit(1),
    button bit(1),
    cb bit(1),
    PRIMARY KEY (testId),
    FOREIGN KEY (testId) REFERENCES test(testId)
);

CREATE TABLE person(
    personID int,
    name VARCHAR(15),
    PRIMARY KEY (personID)
);

CREATE TABLE progress(
	serialNumber VARCHAR(10),
    -- 0 means not done yet, 1 means in progress, 2 means test succeeded, 3 means test didn't succeed
    oxysig INT NOT NULL,
    oxy INT NOT NULL,
    bodypos INT NOT NULL,
    impRef INT NOT NULL,
    impAct INT NOT NULL,
    sig INT NOT NULL,
    sigBip INT NOT NULL,
    press INT NOT NULL,
    cb INT NOT NULL,
    PRIMARY KEY(serialNumber)    
);