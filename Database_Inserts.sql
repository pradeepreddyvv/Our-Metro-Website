-- \c metromanagement;
INSERT into members values('abc@gmail.com' ,   'Daniel',  'M',   'Password@123'  );
INSERT into members values('abc1@gmail.com',   'Martin',  'F',   'Password@34'   );
INSERT into members values('abc2@gmail.com',   'Garter',  'M',   'Password@345'  );
INSERT into members values('abc3@gmail.com',   'Harry',   'F' ,  'Password@456'   );
INSERT into members values('abc4@gmail.com',   'Anil' ,   'F'  , 'Password@454'    );
INSERT into members values('abc5@gmail.com',   'Subash',  'M',   'Password@34'   );
INSERT into members values('abc6@gmail.com',   'Aditi',   'M' ,  'Password@23'    );
INSERT into members values('abc7@gmail.com',   'Sheela',  'F',   'Password@23'  );

INSERT into lines values('LBN1120','BL','st_01','st_06');
INSERT into lines values('LBN1121','RD','st_07','st_11');

INSERT into station values(348920,'st_01','LBN1120');
INSERT into station values(348921,'st_02','LBN1120');
INSERT into station values(348922,'st_03','LBN1120');
INSERT into station values(348923,'st_04','LBN1120');
INSERT into station values(348924,'st_05','LBN1120');
INSERT into station values(348925,'st_06','LBN1120');
INSERT into station values(348926,'st_07','LBN1121');
INSERT into station values(348927,'st_08','LBN1121');
INSERT into station values(348928,'st_09','LBN1121');
INSERT into station values(348929,'st_10','LBN1121');
INSERT into station values(348930,'st_11','LBN1121');

INSERT into users values(10001,'M', 348920);
INSERT into users values(10002,'F', 348921);
INSERT into users values(10003,'F', 348922);
INSERT into users values(10004,'M', 348923);
INSERT into users values(10005,'M', 348924);
INSERT into users values(10006,'F', 348925);
INSERT into users values(10007,'M', 348926);
INSERT into users values(10008,'M', 348927);
INSERT into users values(10009,'M', 348928);
INSERT into users values(10010,'M', 348929);
INSERT into users values(10011,'M', 348930);

INSERT into ticket values(349393, '20-11-2021' ,'08:30:31', '09:21:11', 55, 'st_01', 'st_02',10001);
INSERT into ticket values(349391, '20-11-2021' ,'08:31:32', '09:20:12', 45, 'st_01', 'st_02',10002);
INSERT into ticket values(349392, '20-11-2021' ,'08:32:33', '09:20:13', 65, 'st_01', 'st_04',10003);
INSERT into ticket values(349394, '20-11-2021' ,'08:33:34', '09:20:14', 55, 'st_01', 'st_04',10004);
INSERT into ticket values(349395, '20-11-2021' ,'08:33:35', '09:20:15', 55, 'st_01', 'st_05',10005);
INSERT into ticket values(349396, '20-11-2021' ,'08:34:36', '09:21:16', 45, 'st_01', 'st_05',10006);
INSERT into ticket values(349397, '20-11-2021' ,'08:34:37', '09:22:17', 25, 'st_01', 'st_06',10007);
INSERT into ticket values(349398, '20-11-2021' ,'08:35:38', '09:22:18', 35, 'st_01', 'st_06',10008);

INSERT into metro_card values(98738393, 200, 'st_01', 'st_03', '08:30:31', '09:21:11',  'abc@gmail.com' );
INSERT into metro_card values(98738391, 600, 'st_01', 'st_03', '08:31:32', '09:20:12',  'abc1@gmail.com'  );
INSERT into metro_card values(98738392, 500, 'st_02', 'st_03', '08:31:33', '09:20:13',  'abc2@gmail.com'  );
INSERT into metro_card values(98738394, 500, 'st_02', 'st_04', '08:32:34', '09:20:14',  'abc3@gmail.com'  );
INSERT into metro_card values(98738395, 300, 'st_02', 'st_04', '08:33:35', '09:20:15',  'abc4@gmail.com'  );
INSERT into metro_card values(98738396, 500, 'st_03', 'st_05', '08:33:36', '09:21:16',  'abc5@gmail.com'  );
INSERT into metro_card values(98738397, 100, 'st_03', 'st_05', '08:34:37', '09:22:17',  'abc6@gmail.com'  );
INSERT into metro_card values(98738398, 800, 'st_04', 'st_06', '08:34:38', '09:22:18',  'abc7@gmail.com'  );

INSERT into payment values(1817199,'paid',98738393);
INSERT into payment values(1817190,'paid',98738391);
INSERT into payment values(1817191,'paid',98738392);
INSERT into payment values(1817192,'paid',98738394);
INSERT into payment values(1817193,'paid',98738395);
INSERT into payment values(1817194,'paid',98738396);
INSERT into payment values(1817195,'paid',98738397);
INSERT into payment values(1817196,'paid',98738398);



INSERT into admins values('10001','Daniel12','abc@gmail.com'    );
INSERT into admins values('10002','Martin23','abc1@gmail.com'  );
INSERT into admins values('10003','Garter232','abc2@gmail.com'  );
INSERT into admins values('10004','Harry1','abc3@gmail.com'     );


INSERT into phoneno values(9472288, 9384470 ,'abc@gmail.com'  );
INSERT into phoneno values(9442480, 9384471 ,'abc1@gmail.com'  );
INSERT into phoneno values(9442485, 9384472 ,'abc2@gmail.com');
INSERT into phoneno values(9776230, 9384473 ,'abc3@gmail.com' );
INSERT into phoneno values(9442483, 9384474 ,'abc4@gmail.com');
INSERT into phoneno values(9442481, 9384475 ,'abc5@gmail.com');
INSERT into phoneno values(9442482, 9384476 ,'abc6@gmail.com');
INSERT into phoneno values(9816210, 9384477 ,'abc7@gmail.com');



INSERT into metro values(384951,'LBN1120');
INSERT into metro values(384952,'LBN1121');
-- INSERT into metro values(384953,'LBN1120');
-- INSERT into metro values(384954,'LBN1121');


INSERT into boards values(384951,10001, 348920);
INSERT into boards values(384951,10002, 348921);
INSERT into boards values(384951,10003, 348922);
INSERT into boards values(384951,10004, 348923);
INSERT into boards values(384951,10005, 348924);
INSERT into boards values(384951,10006, 348925);
INSERT into boards values(384951,10007, 348926);
INSERT into boards values(384951,10008, 348927);




INSERT into platform values(1,'08:00','08:05','00:05:30', 348920, 10001);
INSERT into platform values(1,'08:10','08:15','00:09:30', 348921, 10002);
INSERT into platform values(1,'08:10','08:15','00:05:30', 348922, 10003);
INSERT into platform values(1,'08:10','08:15','00:03:30', 348923, 10004);
INSERT into platform values(1,'08:10','08:15','00:05:30', 348924, 10005);
INSERT into platform values(1,'08:20','08:35','00:09:30', 348925, 10006);
INSERT into platform values(1,'08:20','08:35','00:08:30', 348926, 10007);
INSERT into platform values(1,'08:20','08:45','00:06:30', 348927, 10008);


INSERT into crossing values(01,'LBN1120','LBN1121',348922);
-- INSERT into crossing values(02,'LBN1121','LBN4451',348921);










