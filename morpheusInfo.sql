#needed for testing purposes, can also be used when finished and db needs to be reset
INSERT INTO test (testId, testName) VALUES (0, 'morpheus');

INSERT INTO protocols (testId, fileName,protocolId) VALUES (0, 'Validation Morpheus v3 ref 1.XML',0);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (0, 'Validation Morpheus v3 ref 2.xml',1);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (0, 'Validation Morpheus v3 ref 3.xml',2);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (0, 'Validation Morpheus v3 bip.XML',3);

INSERT INTO sigProp (amp,testId,sigId,freq) VALUES (4.0,0,0,10);

INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,0,0,"refInput");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,1,0,"1");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,2,0,"2");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,3,0,"3");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,4,0,"4");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,5,0,"5");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,6,0,"6");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,7,0,"7");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,8,0,"8");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,9,0,"9");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,10,0,"10");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,11,0,"11");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,12,0,"12");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,13,1,"13");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,14,1,"14");
INSERT INTO inputs (testId,inputId,bip,inputName) VALUES (0,15,1,"15");

INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (0,190,350,230,370);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (1,85,510,130,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (2,140,510,180,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (3,190,510,235,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (4,240,510,285,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (5,295,510,340,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (6,345,510,390,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (7,400,510,445,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (8,455,510,495,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (9,505,510,550,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (10,560,510,600,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (11,610,510,655,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (12,665,510,710,530);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (13,85,455,130,480);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (14,140,455,180,480);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (15,190,455,235,480);

INSERT INTO testParameters (testId,oxy,cb,bodypos,impRef,impAct,sig,sigBip,press,flash,button) VALUES (0,1,1,1,1,1,1,1,1,0,0);