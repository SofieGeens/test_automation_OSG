DROP TABLE protocols;
DROP TABLE sigProp;
DROP TABLE testParameters;
DROP TABLE coordinates;
DROP TABLE test;

CREATE TABLE test (
    testID int not null,
    noports int not null,
    testName VARCHAR(10),
    PRIMARY KEY (testID)
);

CREATE TABLE protocols (
    protocolName VARCHAR(25),
    fileName VARCHAR(25),
    testID int not null,
    PRIMARY KEY (protocolName),
    FOREIGN KEY (testID) REFERENCES test(testID)
);

CREATE TABLE sigProp (
    sigID int not null,
    freq int not null,
    amp int not null,
    shape VARCHAR(3),
    testID int not null,
    PRIMARY KEY (sigID),
    FOREIGN KEY (testID) REFERENCES test(testID)
);

CREATE TABLE coordinates (
    testID int not null,
    inputID int not null,
    x1 int not null,
    y1 int not null,
    x2 int not null,
    y2 int not null,
    PRIMARY KEY (inputID,testID),
    FOREIGN KEY (testID) REFERENCES test(testID)
);

CREATE TABLE testParameters (
    testID int not null,
    oxy bit(1),
    bodypos bit(1),
    impRef bit(1),
    impAct bit(1),
    sig bit(1),
    sigBip bit(1),
    press bit(1),
    flash bit(1),
    button bit(1),
    ctobt bit(1),
    bttoc bit(1),
    PRIMARY KEY (testID),
    FOREIGN KEY (testID) REFERENCES test(testID)
);