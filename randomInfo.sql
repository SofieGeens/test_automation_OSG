#needed for testing purposes, can also be used when finished and db needs to be reset
INSERT INTO test (testId, testName) VALUES (1, 'random1');
INSERT INTO test (testId, testName) VALUES (2, 'random2');
INSERT INTO test (testId, testName) VALUES (3, 'random3');

INSERT INTO protocols (testId, fileName,protocolId) VALUES (1, 'does not matter',4);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (2, 'randomString',5);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (1, 'somethin random',6);
INSERT INTO protocols (testId, fileName,protocolId) VALUES (3, 'also random string',7);

INSERT INTO sigProp (amp,testId,sigId,freq) VALUES (8.3,1,1,100);
INSERT INTO sigProp (amp,testId,sigId,freq) VALUES (5.5,2,2,200);
INSERT INTO sigProp (amp,testId,sigId,freq) VALUES (10.0,3,3,500);

INSERT INTO inputs (testId,inputId,inputName) VALUES (1,16,"refInput");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,17,"a");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,18,"b");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,19,"c");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,20,"d");
INSERT INTO inputs (testId,inputId,inputName) VALUES (2,21,"e");
INSERT INTO inputs (testId,inputId,inputName) VALUES (2,22,"f");
INSERT INTO inputs (testId,inputId,inputName) VALUES (2,23,"g");
INSERT INTO inputs (testId,inputId,inputName) VALUES (3,24,"h");
INSERT INTO inputs (testId,inputId,inputName) VALUES (3,25,"i");
INSERT INTO inputs (testId,inputId,inputName) VALUES (3,26,"j");
INSERT INTO inputs (testId,inputId,inputName) VALUES (3,27,"k");
INSERT INTO inputs (testId,inputId,inputName) VALUES (3,28,"l");
INSERT INTO inputs (testId,inputId,inputName) VALUES (2,29,"m");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,30,"n");
INSERT INTO inputs (testId,inputId,inputName) VALUES (1,31,"o");

INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (16,1900,3500,2300,3070);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (17,805,501000,10300,5030);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (18,1040,5010,1080,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (19,1900,5010,2035,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (20,2040,5100,2850,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (21,2905,5010,3040,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (22,3045,5010,3900,5030);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (23,4000,5100,4045,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (24,4055,5010,4950,5030);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (25,5005,5010,5500,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (26,5600,5100,6000,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (27,6100,5010,6505,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (28,0665,5010,7100,5300);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (29,850,4055,1030,4080);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (30,1040,4505,1800,4800);
INSERT INTO impedanceCoordinates (inputId,x1,y1,x2,y2) VALUES (31,1900,4505,2035,4080);

INSERT INTO testParameters (testId,oxy,cb,bodypos,impRef,impAct,sig,sigBip,press,flash,button) VALUES (1,1,0,1,0,1,0,1,1,1,1);
INSERT INTO testParameters (testId,oxy,cb,bodypos,impRef,impAct,sig,sigBip,press,flash,button) VALUES (2,1,1,1,1,0,1,0,1,0,1);
INSERT INTO testParameters (testId,oxy,cb,bodypos,impRef,impAct,sig,sigBip,press,flash,button) VALUES (3,1,0,1,1,0,1,1,0,1,0);