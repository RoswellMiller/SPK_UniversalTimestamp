import json

page_447 = [
(-214193,'Sunday',    1507231.5,-892769, -80641958400, -586, 7,24,-587, 7,30, -587,  8,1,  3,False,  48,2,  161, 7,15, -1138, 4,10),
( -61387,'Wednesday', 1660037.5,-739963, -67439520000, -168,12, 5,-169,12, 8, -169, 12,3,  6,False, 152,4,  580, 3, 6,  -720,12, 6),
(  25469,'Wednesday', 1746893.5,-653107, -59935161600,   70, 9,24,  70, 9,26,   70, 10,1,  6,False, 212,2,  818, 2,22,  -482,11,22),
(  49217,'Sunday',    1770641.5,-629359, -57883334400,  135,10, 2, 135,10, 3,  135, 10,2,  5,False, 228,3,  883, 3,15,  -417,12,15),
( 171307,'Wednesday', 1892731.5,-507269, -47334758400,  470, 1, 8, 470, 1, 7,  470,  1,3,  7,False, 312,2, 1217, 9,15,   -82, 6,10),
( 210155,'Monday',    1931579.5,-468421, -43978291200,  576, 5,20, 576, 5,18,  576,  6,1, 15,False, 338,4, 1324, 2,18,    24,11,18),
( 253427,'Saturday',  1974851.5,-425149, -40239590400,  694,11,10, 694,11, 7,  694, 11,3,  7,False, 368,2, 1442, 9,10,   143, 6, 5),
( 369740,'Sunday',    2091164.5,-308836, -30190147200, 1013, 4,25,1013, 4,19, 1013,  5,1, 13,False, 448,1, 1761, 5, 8,   462, 2, 3),
( 400085,'Sunday',    2121509.5,-278491, -27568339200, 1096, 5,24,1096, 5,18, 1096,  6,1, 15,False, 468,4, 1844, 6,28,   545, 3,23),
( 434355,'Friday',    2155779.5,-244221, -24607411200, 1190, 3,23,1190, 3,16, 1190,  4,1, 17,False, 492,2, 1938, 5,18,   639, 2,13),
( 452605,'Saturday',  2174029.5,-225971, -23030611200, 1240, 3,10,1240, 3, 3, 1240,  3,2,  5,False, 504,4, 1988, 5,18,   689, 2,13),
( 470160,'Friday',    2191584.5,-208416, -21513859200, 1288, 4, 2,1288, 3,26, 1288,  4,1,  7,False, 516,4, 2036, 6,23,   737, 3,18),
( 473837,'Sunday',    2195261.5,-204739, -21196166400, 1298, 4,27,1298, 4,20, 1298,  5,1, 12,False, 519,2, 2046, 7,20,   747, 4,15),
( 507850,'Sunday',    2229274.5,-170726, -18257443200, 1391, 6,12,1391, 6, 4, 1391,  6,2,  2,False, 542,3, 2139, 9,28,   840, 6,23),
( 524156,'Wednesday', 2245580.5,-154420, -16848604800, 1436, 2, 3,1436, 1,25, 1436,  2,1,  8,False, 553,4, 2184, 5,29,   885, 2,24),
( 544676,'Saturday',  2266100.5,-133900, -15075676800, 1492, 4, 9,1492, 3,31, 1492,  4,1,  2,False, 567,4, 2240, 8,19,   941, 5,14),
( 567118,'Saturday',  2288542.5,-111458, -13136688000, 1553, 9,19,1553, 9, 9, 1553,  9,3,  5,False, 583,1, 2302, 2,11,  1002,11,11),
( 569477,'Saturday',  2290901.5,-109099, -12932870400, 1560, 3, 5,1560, 2,24, 1560,  3,1,  6,False, 584,4, 2308, 7,30,  1009, 4,25),
( 601716,'Wednesday', 2323140.5, -76860, -10147420800, 1648, 6,10,1648, 5,31, 1648,  6,1,  2,False, 606,4, 2396,11,29,  1097, 8,24),
( 613424,'Sunday',    2334848.5, -65152,  -9135849600, 1680, 6,30,1680, 6,20, 1680,  7,1, 12,False, 614,4, 2428,12,27,  1129, 9,22),
( 626596,'Friday',    2348020.5, -51980,  -7997788800, 1716, 7,24,1716, 7,13, 1716,  7,3,  3,False, 623,4, 2465, 1,24,  1165,10,24),
( 645554,'Sunday',    2366978.5, -33022,  -6359817600, 1768, 6,19,1768, 6, 8, 1768,  6,3,  6,False, 636,4, 2517, 1, 2,  1217,10, 2),
( 664224,'Monday',    2385648.5, -14352,  -4746729600, 1819, 8, 2,1819, 7,21, 1819,  8,1, 12,False, 649,3, 2568, 2,27,  1268,11,27),
( 671401,'Wednesday', 2392825.5,  -7175,  -4126636800, 1839, 3,27,1839, 3,15, 1839,  3,3,  1,False, 654,3, 2587,10,29,  1288, 7,24),
( 694799,'Sunday',    2416223.5,  16223,  -2105049600, 1903, 4,19,1903, 4, 6, 1903,  4,3,  8,False, 670,3, 2651,12, 7,  1352, 9, 2),
( 704424,'Sunday',    2425848.5,  25848,  -1273449600, 1929, 8,25,1929, 8,12, 1929,  8,3,  2,False, 677,1, 2678, 4,17,  1379, 1,12),
( 708842,'Monday',    2430266.5,  30266,   -891734400, 1941, 9,29,1941, 9,16, 1941, 10,1, 16,False, 680,1, 2690, 5,25,  1391, 2,20),
( 709409,'Monday',    2430833.5,  30833,   -842745600, 1943, 4,19,1943, 4, 6, 1943,  4,3,  8,False, 680,3, 2691,12,17,  1392, 9,12),
( 709580,'Thursday',  2431004.5,  31004,   -827971200, 1943,10, 7,1943, 9,24, 1943, 10,1,  8,False, 680,3, 2692, 6, 3,  1393, 2,28),
( 727274,'Tuesday',   2448698.5,  48698,    700790400, 1992, 3,17,1992, 3, 4, 1992,  3,2,  4,False, 692,4, 2740,11,27,  1441, 8,22),
( 728714,'Sunday',    2450138.5,  50138,    825206400, 1996, 2,25,1996, 2,12, 1996,  2,3,  2,False, 693,4, 2744,11, 7,  1445, 8, 2),
( 744313,'Wednesday', 2465737.5,  65737,   2172960000, 2038,11,10,2038,10,28, 2038, 11,1,  5,False, 704,2, 2787, 8, 1,  1488, 4,26),
( 764652,'Sunday',    2486076.5,  86076,   3930249600, 2094, 7,18,2094, 7, 5, 2094,  7,2,  3,False, 718,2, 2843, 4,20,  1544, 1,15)
]
page_448 = [
(-214193,6, 5, -870,  12,  6, -594, 12,  6, -586, 29, 7,  -586,  90, 14, 0,-1245, 12, 9, -1245, 12, 11,-1245,12, 11, 3174, 5,10, 3174, 5, 11),
( -61387,4, 1, -451,   4, 12, -175,  4, 12, -168, 49, 3,  -168, 270,  6, 3, -813,  2,23,  -813,  2, 25, -813, 2, 26, 3593, 9,25, 3593, 9, 24),
(  25469,4, 1, -213,   1, 29,   63,  1, 29,   70, 39, 3,    70,  90, 22, 3, -568,  4, 1,  -568,  4,  2, -568, 4,  3, 3831, 7, 3, 3831, 7,  2),
(  49217,4, 5, -148,   2,  5,  128,  2,  5,  135, 39, 7,   135,  90, 24, 0, -501,  4, 6,  -501,  4,  7, -501, 4,  8, 3896, 7, 9, 3896, 7,  7),
( 171307,6, 1,  186,   5, 12,  462,  5, 12,  470,  2, 3,   469, 270, 11, 3, -157, 10,17,  -157, 10, 18, -157,10, 18, 4230,10,18, 4230,10, 18),
( 210155,4, 6,  292,   9, 23,  568,  9, 23,  576, 21, 1,   576,  90,  4, 1,  -47,  6, 3,   -47,  6,  3,  -47, 6,  4, 4336, 3, 4, 4336, 3,  3),
( 253427,4, 4,  411,   3, 11,  687,  3, 11,  694, 45, 6,   694, 270,  3, 6,   75,  7,13,    75,  7, 13,   75, 7, 14, 4455, 8,13, 4455, 9, 13),
( 369740,1, 5,  729,   8, 24, 1005,  8, 24, 1013, 16, 7,  1013,  90,  1, 0,  403, 10, 5,   403, 10,  5,  403,10,  6, 4773, 2, 6, 4773, 2,  5),
( 400085,4, 5,  812,   9, 23, 1088,  9, 23, 1096, 21, 7,  1096,  90,  5, 0,  489,  5,22,   489,  5, 22,  489, 5, 23, 4856, 2,23, 4856, 2, 22),
( 434355,2, 3,  906,   7, 20, 1182,  7, 20, 1190, 12, 5,  1189, 270, 22, 5,  586,  2, 7,   586,  2,  7,  586, 2,  8, 4950, 1, 7, 4950, 1,  7),
( 452605,6, 4,  956,   7,  7, 1232,  7,  7, 1240, 10, 6,  1239, 270, 21, 6,  637,  8, 7,   637,  8,  7,  637, 8,  8, 5000,13, 8, 5000,13,  7),
( 470160,5, 3, 1004,   7, 30, 1280,  7, 30, 1288, 14, 5,  1287, 270, 23, 5,  687,  2,20,   687,  2, 21,  687, 2, 22, 5048, 1,21, 5048, 1, 21),
( 473837,4, 5, 1014,   8, 25, 1290,  8, 25, 1298, 17, 7,  1298,  90,  1, 0,  697,  7, 7,   697,  7,  7,  697, 7,  8, 5058, 2, 7, 5058, 2,  7),
( 507850,3, 5, 1107,  10, 10, 1383, 10, 10, 1391, 23, 7,  1391,  90,  8, 0,  793,  7, 1,   793,  6, 30,  793, 7,  1, 5151, 4, 1, 5151, 3, 30),
( 524156,1, 1, 1152,   5, 29, 1428,  5, 29, 1436,  5, 3,  1435, 270, 15, 3,  839,  7, 6,   839,  7,  6,  839, 7,  7, 5196,11, 7, 5196,12,  6),
( 544676,1, 4, 1208,   8,  5, 1484,  8,  5, 1492, 14, 6,  1491, 270, 25, 6,  897,  6, 1,   897,  6,  2,  897, 6,  3, 5252, 1, 3, 5252, 2,  2),
( 567118,3, 4, 1270,   1, 12, 1546,  1, 12, 1553, 38, 6,  1553,  90, 22, 6,  960,  9,30,   960,  9, 30,  960,10,  1, 5314, 7, 1, 5313, 6, 30),
( 569477,4, 4, 1276,   6, 29, 1552,  6, 29, 1560,  9, 6,  1559, 270, 20, 6,  967,  5,27,   967,  5, 27,  967, 5, 28, 5320,12,27, 5320,12, 27),
( 601716,5, 1, 1364,  10,  6, 1640, 10,  6, 1648, 24, 3,  1648,  90,  7, 3, 1058,  5,18,  1058,  5, 18, 1058, 5, 19, 5408, 3,20, 5408, 3, 18),
( 613424,1, 5, 1396,  10, 26, 1672, 10, 26, 1680, 26, 7,  1680,  90, 10, 0, 1091,  6, 2,  1091,  6,  3, 1091, 6,  4, 5440, 4, 3, 5440, 4,  3),
( 626596,3, 3, 1432,  11, 19, 1708, 11, 19, 1716, 30, 5,  1716,  90, 14, 5, 1128,  8, 4,  1128,  8,  4, 1128, 8,  5, 5476, 5, 5, 5476, 5,  4),
( 645554,1, 5, 1484,  10, 14, 1760, 10, 14, 1768, 24, 7,  1768,  90,  9, 0, 1182,  2, 3,  1182,  2,  4, 1182, 2,  4, 5528, 4, 4, 5528, 4,  4),
( 664224,5, 6, 1535,  11, 27, 1811, 11, 27, 1819, 31, 1,  1819,  90, 15, 1, 1234, 10,10,  1234, 10, 10, 1234,10, 11, 5579, 5,11, 5579, 5, 10),
( 671401,6, 1, 1555,   7, 19, 1831,  7, 19, 1839, 13, 3,  1838, 270, 22, 3, 1255,  1,11,  1255,  1, 11, 1255, 1, 11, 5599, 1,12, 5599, 1, 11),
( 694799,4, 5, 1619,   8, 11, 1895,  8, 11, 1903, 16, 7,  1902, 270, 26, 0, 1321,  1,21,  1321,  1, 20, 1321, 1, 21, 5663, 1,22, 5663, 1, 20),
( 704424,5, 5, 1645,  12, 19, 1921, 12, 19, 1929, 34, 7,  1929,  90, 18, 0, 1348,  3,19,  1348,  3, 19, 1348, 3, 20, 5689, 5,19, 5689, 6, 19),
( 708842,1, 6, 1658,   1, 19, 1934,  1, 19, 1941, 40, 1,  1941,  90, 23, 1, 1360,  9, 8,  1360,  9,  7, 1360, 9,  8, 5702, 7, 8, 5702, 7,  7),
( 709409,4, 6, 1659,   8, 11, 1935,  8, 11, 1943, 16, 1,  1942, 270, 26, 1, 1362,  4,13,  1362,  4, 14, 1362, 4, 14, 5703, 1,14, 5703, 2, 14),
( 709580,1, 2, 1660,   1, 26, 1936,  1, 26, 1943, 40, 4,  1943,  90, 25, 4, 1362, 10, 7,  1362, 10,  7, 1362,10,  8, 5704, 7, 8, 5704, 8,  7),
( 727274,1, 7, 1708,   7,  8, 1984,  7,  8, 1992, 12, 2,  1991, 270, 21, 2, 1412,  9,13,  1412,  9, 12, 1412, 9, 12, 5752,13,12, 5752, 1, 12),
( 728714,1, 5, 1712,   6, 17, 1988,  6, 17, 1996,  8, 7,  1995, 270, 18, 0, 1416, 10, 5,  1416, 10,  5, 1416,10,  6, 5756,12, 5, 5756,12,  5),
( 744313,6, 1, 1755,   3,  1, 2031,  3,  1, 2038, 45, 3,  2038, 270,  3, 3, 1460, 10,12,  1460, 10, 12, 1460,10, 13, 5799, 8,12, 5799, 9, 12),
( 764652,5, 5, 1810,  11, 11, 2086, 11, 11, 2094, 28, 7,  2094,  90, 13, 0, 1518,  3, 5,  1518,  3,  5, 1518, 3,  6, 5854, 5, 5, 5854, 5,  5)    
]
page_451 = [
(-214193, 35, 11, 6,False, 12,  2, 10, -214191.633133, 2515,   5, 19, -664, 5,19,-664, 5, 13,2515, 6,  False, 11, -529, 6,False, 11,False, -529, 6,True,   11,False, -459,  8,False, 11,False),
( -61387, 42,  9,10,False, 27,  8,  8,  -61370.729673, 2933,   9, 26, -246, 9,26,-246, 9, 21,2933, 9,  False, 26, -111, 9,False, 27,False, -111, 9,False,  27,False, -411,  2,False, 27,False),
(  25469, 46,  7, 8,False,  4,  4,  8,   25498.215092, 3171,   7, 11,   -8, 7, 9,  -8, 7,  5,3171, 8,  False,  3,  127, 8,False,  3,False,  127, 8,False,   3,True,   197, 10,False,  3,False),
(  49217, 47, 12, 8,False,  9,  2,  8,   49239.004860, 3236,   7, 17,   57, 7,16,  57, 7, 11,3236, 8,  False,  9,  192, 8,False,  9,False,  192, 8,False,   9,False,  262, 10,False,  9,False),
( 171307, 52, 46,11,False, 20,  2, 10,  171318.588098, 3570,  10, 19,  391,10,21, 391,10, 17,3570,11,  True,  19,  526,11,False, 19,False,  526,10,False,  20,False,  596, 12,False, 19,False),
( 210155, 54, 33, 4,False,  5, 10,  2,  210156.745715, 3677,   2, 28,  498, 2,31, 498, 2, 27,3677, 3,  False,  5,  633, 3,False,  5,False,  633, 3,False,   5,False,  703,  5,False,  4,False),
( 253427, 56, 31,10,False, 15,  2,  2,  253439.318423, 3795,   8, 17,  616, 8,16, 616, 8, 13,3795, 9,  False, 15,  751, 9,False, 15,False,  751, 8,False,  15,False,  821, 10,False, 15,False),
( 369740, 61, 50, 3,False,  7,  5, 11,  369767.423610, 4114,   1, 26,  935, 1,28, 935, 1, 26,4114, 2,  False,  7, 1070, 2,False,  6,False, 1070, 2,False,   6,False, 1140,  4,False,  6,False),
( 400085, 63, 13, 4,False, 24, 10,  8,  400113.941895, 4197,   2, 24, 1018, 2,26,1018, 2, 24,4197, 2,  False, 24, 1153, 3,True,  23,False, 1153, 2,False,  23,False, 1223,  4,False, 23,False),
( 434355, 64, 47, 2,False,  9, 10,  6,  434384.035740, 4290,  12, 20, 1111,12,23,1111,12, 21,4291, 1,  False,  9, 1247, 1,False,  8,False, 1247, 1,False,   8,False, 1317,  3,False,  8,False),
( 452605, 65, 37, 2,False,  9, 10,  4,  452615.458234, 4340,  12,  7, 1161,12,10,1161,12,  8,4340,12,  False,  9, 1297, 1,False,  8,False, 1296,12,False,   8,False, 1367,  2,False,  8,False),
( 470160, 66, 25, 2,False, 23,  5,  3,  470177.759817, 4388,  12, 30, 1210, 1, 2,1209,12, 31,4389, 1,  False, 23, 1345, 1,False, 22,False, 1345, 1,False,  23,False, 1415,  2,False, 22,False),
( 473837, 66, 35, 3,False,  9,  2,  8,  473861.324287, 4399,   1, 24, 1220, 1,27,1220, 1, 25,4399, 2,  False,  8, 1355, 2,False,  8,False, 1355, 2,False,   8,False, 1425,  4,False,  8,False),
( 507850, 68,  8, 5,False,  2,  5,  1,  507860.235360, 4492,   3,  7, 1313, 3, 8,1313, 3,  7,4492, 4,  False,  2, 1448, 4,False,  1,False, 1448, 4,False,   1,False, 1518,  5,False,  1,False),
( 524156, 68, 53, 1,False,  8,  1, 11,  524172.836499, 4536,  10, 28, 1357,10,30,1357,10, 28,4536,11,  False,  7, 1492,11,False,  7,False, 1492,11,False,   7,False, 1563,  1,False,  7,False),
( 544676, 69, 49, 3,False,  4,  1, 11,  544687.134951, 4593,   1,  3, 1414, 1, 5,1414, 1,  4,4593, 1,  False,  3, 1549, 2,True,   3,False, 1549, 2,True,    4,False, 1619,  3,False,  3,False),
( 567118, 70, 50, 8,False,  2,  3,  1,  567122.835546, 4654,   6, 12, 1475, 6,10,1475, 6,  9,4654, 7,  False,  2, 1610, 7,False,  2,False, 1610, 7,False,   2,False, 1680,  8,False,  2,False),
( 569477, 70, 57, 1,False, 29,  2,  8,  569492.996631, 4660,  11, 27, 1481,11,29,1481,11, 28,4660,11,  False, 29, 1616,11,False, 28,True,  1616,11,False,  29,False, 1687,  1,False, 29,False),
( 601716, 72, 25, 4,True,  20,  1,  3,  601727.342101, 4749,   3,  1, 1570, 3, 3,1570, 3,  2,4749, 3,  False, 20, 1705, 3,False, 20,False, 1705, 3,False,  20,False, 1775,  4,False, 20,False),
( 613424, 72, 57, 6,False,  5,  9, 11,  613446.520844, 4781,   3, 21, 1602, 3,22,1602, 3, 22,4781, 4,  False,  4, 1737, 4,False,  4,False, 1737, 4,False,   5,False, 1807,  6,True,   4,False),
( 626596, 73, 33, 6,False,  6,  1,  7,  626626.467423, 4817,   4, 13, 1638, 4,13,1638, 4, 13,4817, 5,  False,  6, 1773, 5,False,  6,False, 1773, 5,False,   6,False, 1843,  6,False,  6,False),
( 645554, 74, 25, 5,False,  5,  9,  5,  645556.325334, 4869,   3,  8, 1690, 3,10,1690, 3,  9,4869, 4,  False,  5, 1825, 4,False,  5,False, 1825, 4,False,   5,False, 1895,  5,False,  5,False),
( 664224, 75, 16, 6,False, 12,  9,  3,  664246.376294, 4920,   4, 20, 1741, 4,20,1741, 4, 20,4920, 5,  False, 12, 1876, 5,False, 11,False, 1876, 5,False,  11,False, 1946,  6,False, 11,False),
( 671401, 75, 36, 2,False, 13,  6,  4,  671426.124336, 4939,  12, 13, 1760,12,16,1760,12, 15,4940, 1,  True,  13, 1896, 1,False, 13,False, 1896, 1,False,  13,False, 1966,  2,False, 13,False),
( 694799, 76, 40, 3,False, 22,  4,  2,  694801.614262, 5004,   1,  4, 1825, 1, 7,1825, 1,  7,5004, 1,  False, 23, 1960, 1,False, 22,False, 1960, 1,False,  22,False, 2030,  2,False, 22,False),
( 704424, 77,  6, 7,False, 21,  9,  3,  704453.869487, 5030,   5, 11, 1851, 5,10,1851, 5, 10,5030, 5,  False, 21, 1986, 5,False, 20,False, 1986, 5,False,  20,False, 2056,  7,False, 20,False),
( 708842, 77, 18, 8,False,  9,  7,  5,  708867.143728, 5042,   6, 15, 1863, 6,14,1863, 6, 14,5042, 7,  False,  9, 1998, 7,False,  9,False, 1998, 7,False,   9,False, 2068,  8,False,  9,False),
( 709409, 77, 20, 3,False, 15,  4,  8,  709411.313394, 5044,   1,  4, 1865, 1, 7,1865, 1,  6,5044, 1,  False, 15, 2000, 1,False, 14,False, 2000, 1,False,  14,False, 2070,  3,True,  14,False),
( 709580, 77, 20, 9,False,  9,  5, 11,  709597.630490, 5044,   6, 23, 1865, 6,21,1865, 6, 21,5044, 7,  False,  9, 2000, 7,False,  8,False, 2000, 7,False,   8,False, 2070,  8,False,  8,False),
( 727274, 78,  9, 2,False, 14,  9,  5,  727277.699910, 5092,  12,  2, 1913,12, 4,1913,12,  4,5092,12,  False, 14, 2048,12,False, 14,False, 2048,12,False,  14,False, 2119,  1,False, 14,False),
( 728714, 78, 13, 1,False,  7,  9,  5,  728738.668683, 5096,  11, 11, 1917,11,13,1917,11, 13,5096,12,  False,  7, 2052,12,False,  7,False, 2052,12,False,   7,False, 2123,  1,False,  7,False),
( 744313, 78, 55,10,False, 14,  8,  4,  744325.563213, 5139,   7, 26, 1960, 7,24,1960, 7, 25,5139, 8,  False, 14, 2095, 8,False, 14,False, 2095, 8,False,  14,False, 2165,  9,False, 14,False),
( 764652, 79, 51, 6,False,  7,  7,  3,  764656.564371, 5195,   4,  2, 2016, 4, 2,2016, 4,  2,5195, 4,  False,  6, 2151, 4,False,  6,False, 2151, 4,False,   6,False, 2221,  6,False,  6,False)    
]


def custom_format_json(json_file_path, output_file_path=None):
    """Format JSON with arrays on single lines but objects formatted normally."""
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # If no output path specified, use the input path
    if output_file_path is None:
        output_file_path = json_file_path
    
    # Format with 4-space indentation
    json_string = json.dumps(data, indent=4)
    
    # Use a custom approach to collapse arrays
    import re
    # Pattern to find arrays with newlines and indentation
    array_pattern = r'\[\s+(.+?)\s+\]'
    
    def replace_array(match):
        # Extract array content
        content = match.group(1)
        # Split by newlines and clean up each item
        items = [line.strip().rstrip(',') for line in content.split('\n')]
        # Join items on a single line
        return '[' + ', '.join(items) + ']'
    
    # Replace all arrays with their single-line version
    formatted_json = re.sub(array_pattern, replace_array, json_string, flags=re.DOTALL)
    
    # Write the formatted JSON back to file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_json)
    
    return f"JSON reformatted and saved to {output_file_path}"

# # Usage
# file_path = r"c:\Users\roswe\Python-Projects\SPK_UniversalTimestamp\Tests\appendix_c_page_447.json"
# result = custom_format_json(file_path)
# print(result)


def main():
    print("Page 447 Entries:")
    print("=" * 50)
    page_44n_dict = {}
    columns_447 = [
        {'name' : 'R.D.', 'index' : 0 },
        {'name' : 'Weekday', 'index' : 1 },
        {'name' : 'Julian Day', 'index' : 2 },
        {'name' : 'Modified Julian Day', 'index' : 3 },
        {'name' : 'Unix', 'index' : 4 },
        {'name' : 'Gregorian-year', 'index' : 5 },
        {'name' : 'Gregorian-month', 'index' : 6 },
        {'name' : 'Gregorian-day', 'index' : 7 },
        {'name' : 'Julian Date-year', 'index' : 8 },
        {'name' : 'Julian Date-month', 'index' : 9 },
        {'name' : 'Julian Date-day', 'index' : 10 },
        {'name' : 'Julian Roman name-year', 'index' : 11 },
        {'name' : 'Julian Roman name-month', 'index' : 12 },
        {'name' : 'Julian Roman name-day-i', 'index' : 13 },
        {'name' : 'Julian Roman name-day-ii', 'index' : 14 },
        {'name' : 'Olympiad-year', 'index' : 15 },
        {'name' : 'Olympiad-month', 'index' : 16 },
        {'name' : 'Egyptian-year', 'index' : 17 },
        {'name' : 'Egyptian-month', 'index' : 18 },
        {'name' : 'Egyptian-day', 'index' : 19 },
        {'name' : 'Armenian-year', 'index' : 20 },
        {'name' : 'Armenian-month', 'index' : 21 },
        {'name' : 'Armenian-day', 'index' : 22 },
    ]
    columns_448 = [
        {'name' : 'R.D.', 'index' : 0 },
        {'name' : 'Akan-one', 'index' : 1 },
        {'name' : 'Akan-two', 'index' : 2 },
        {'name' : 'Coptic-year', 'index' : 3 },
        {'name' : 'Coptic-month', 'index' : 4 },
        {'name' : 'Coptic-day', 'index' : 5 },
        {'name' : 'Ethiopic-year', 'index' : 6 },
        {'name' : 'Ethiopic-month', 'index' : 7 },
        {'name' : 'Ethiopic-day', 'index' : 8 },
        {'name' : 'ISO-year', 'index' : 9 },
        {'name' : 'ISO-month', 'index' : 10 },
        {'name' : 'ISO-day', 'index' : 11 },
        {'name' : 'Icelandic-year', 'index' : 12 },
        {'name' : 'Icelandic-month', 'index' : 13 },
        {'name' : 'Icelandic-day_one', 'index' : 14 },
        {'name' : 'Icelandic-day_two', 'index' : 15 },
        {'name' : 'Islamic Arithmetic-year', 'index' : 16 },
        {'name' : 'Islamic Arithmetic-month', 'index' : 17 },
        {'name' : 'Islamic Arithmetic-day', 'index' : 18 },
        {'name' : 'Islamic Observational-year', 'index' : 19 },
        {'name' : 'Islamic Observational-month', 'index' : 20 },
        {'name' : 'Islamic Observational-day', 'index' : 21 },
        {'name' : 'Islamic Umm il-Qura-year', 'index' : 22 },
        {'name' : 'Islamic Umm il-Qura-month', 'index' : 23 },
        {'name' : 'Islamic Umm il-Qura-day', 'index' : 24 },
        {'name' : 'Hebrew Standard-year', 'index' : 25 },
        {'name' : 'Hebrew Standard-month', 'index' : 26 },
        {'name' : 'Hebrew Standard-day', 'index' : 27 },
        {'name' : 'Hebrew Observational-year', 'index' : 28 },
        {'name' : 'Hebrew Observational-month', 'index' : 29 },
        {'name' : 'Hebrew Observational-day', 'index' : 30 },
    ]
    columns_451 = [
        {'name' : 'R.D.', 'index' : 0 },
        {'name' : 'Chinese Date-cycle', 'index' : 1},
        {'name' : 'Chinese Date-year', 'index' : 2},
        {'name' : 'Chinese Date-month', 'index' : 3},
        {'name' : 'Chinese Date-leap', 'index' : 4},
        {'name' : 'Chinese Date-day', 'index' : 5},        
        {'name' : 'Chinese Name-stem', 'index' : 6},
        {'name' : 'Chinese Name-branch', 'index' : 7},
        {'name' : 'Chinese Next Zhongqi', 'index' : 8},
        
        {'name' : 'Hindu Solar Old-year', 'index' : 9},
        {'name' : 'Hindu Solar Old-month', 'index' : 10},
        {'name' : 'Hindu Solar Old-day', 'index' : 11},
        {'name' : 'Hindu Solar Modern-year', 'index' : 12},
        {'name' : 'Hindu Solar Modern-month', 'index' : 13},
        {'name' : 'Hindu Solar Modern-day', 'index' : 14},
        {'name' : 'Hindu Solar Astronomical-year', 'index' : 15},
        {'name' : 'Hindu Solar Astronomical-month', 'index' : 16},
        {'name' : 'Hindu Solar Astronomical-day', 'index' : 17},
        
        {'name' : 'Hindu Lunisolar Old-year', 'index' : 18},
        {'name' : 'Hindu Lunisolar Old-month', 'index' : 19},
        {'name' : 'Hindu Lunisolar Old-leap', 'index' : 20},
        {'name' : 'Hindu Lunisolar Old-day', 'index' : 21},
        {'name' : 'Hindu Lunisolar Modern-year', 'index' : 22},
        {'name' : 'Hindu Lunisolar Modern-month', 'index' : 23},
        {'name' : 'Hindu Lunisolar Modern-leap-month', 'index' : 24},
        {'name' : 'Hindu Lunisolar Modern-day', 'index' : 25},
        {'name' : 'Hindu Lunisolar Modern-leap-day', 'index' : 26},
        {'name' : 'Hindu Lunisolar Astronomical-year', 'index' : 27},
        {'name' : 'Hindu Lunisolar Astronomical-month', 'index' : 28},
        {'name' : 'Hindu Lunisolar Astronomical-leap-month', 'index' : 29},
        {'name' : 'Hindu Lunisolar Astronomical-day', 'index' : 30},
        {'name' : 'Hindu Lunisolar Astronomical-leap-day', 'index' : 31},
    
        {'name' : 'Tibetan-year', 'index' : 32},
        {'name' : 'Tibetan-month', 'index' : 33},
        {'name' : 'Tibetan-leap-month', 'index' : 34},
        {'name' : 'Tibetan-day', 'index' : 35},
        {'name' : 'Tibetan-leap-day', 'index' : 36},
   ]
    for entry in columns_447:
        page_44n_dict[entry['name']] = []
    for row in page_447:
        for col in columns_447:
            page_44n_dict[col['name']].append(row[col['index']])
            
    errors = 0
    for entry in columns_448:
        if entry['index'] >0:
            page_44n_dict[entry['name']] = []
    row_i =  -1
    for row in page_448:
        row_i += 1
        for col in columns_448:
            if col['index'] == 0:
                if page_44n_dict['R.D.'][row_i] != row[col['index']] :
                    print(f"R.D. mismatch at row {row_i + 1}: {page_44n_dict['R.D.'][row_i]} != {row[col['index']]}")
                    errors += 1
                continue
            page_44n_dict[col['name']].append(row[col['index']])
                        
    for entry in columns_451:
        if entry['index'] >0:
            page_44n_dict[entry['name']] = []
    row_i =  -1
    for row in page_451:
        row_i += 1
        for col in columns_451:
            if col['index'] == 0:
                if page_44n_dict['R.D.'][row_i] != row[col['index']] :
                    print(f"R.D. mismatch at row {row_i + 1}: {page_44n_dict['R.D.'][row_i]} != {row[col['index']]}")
                    errors += 1
                continue
            page_44n_dict[col['name']].append(row[col['index']])            
    if errors >0:
        print(f"Total R.D. mismatches: {errors}")
        return
    print(f"Total rows processed: {row_i + 1}")    
    with open('Tests\\RandD_appendix_c.json', 'w') as f:
        json.dump(page_44n_dict, f, indent=4)
    custom_format_json('Tests\\RandD_appendix_c.json')
    
if __name__ == "__main__":
    main()