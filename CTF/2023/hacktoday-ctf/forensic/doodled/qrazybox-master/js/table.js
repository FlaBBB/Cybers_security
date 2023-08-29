/********************************************************************
			Tables and references used for QR code
*********************************************************************/


//Pattern (bitmatri-1) template for Function pattern and Format info
var function_pattern_with_format_info = {
	/*
		0		: white
		1		: black
		2-16	: Format info
	*/
	TOP_LEFT: [
		[1,1,1,1,1,1,1,0,2],
		[1,0,0,0,0,0,1,0,3],
		[1,0,1,1,1,0,1,0,4],
		[1,0,1,1,1,0,1,0,5],
		[1,0,1,1,1,0,1,0,6],
		[1,0,0,0,0,0,1,0,7],
		[1,1,1,1,1,1,1,0,1],
		[0,0,0,0,0,0,0,0,8],
		[16,15,14,13,12,11,1,10,9]
	],

	TOP_RIGHT: [
		[0,1,1,1,1,1,1,1],
		[0,1,0,0,0,0,0,1],
		[0,1,0,1,1,1,0,1],
		[0,1,0,1,1,1,0,1],
		[0,1,0,1,1,1,0,1],
		[0,1,0,0,0,0,0,1],
		[0,1,1,1,1,1,1,1],
		[0,0,0,0,0,0,0,0],
		[9,8,7,6,5,4,3,2]
	],

	BOTTOM_LEFT: [
		[0,0,0,0,0,0,0,0,1],
		[1,1,1,1,1,1,1,0,10],
		[1,0,0,0,0,0,1,0,11],
		[1,0,1,1,1,0,1,0,12],
		[1,0,1,1,1,0,1,0,13],
		[1,0,1,1,1,0,1,0,14],
		[1,0,0,0,0,0,1,0,15],
		[1,1,1,1,1,1,1,0,16],
	]
};


var alignment_pattern_array = [
	[],											//1 		
	[6, 18],									//2 		
	[6, 22],									//3 		
	[6, 26],									//4 		
	[6, 30],									//5 		
	[6, 34],									//6 		
	[6, 22, 38],								//7 		
	[6, 24, 42],								//8 		
	[6, 26, 46],								//9 		
	[6, 28, 50],								//10		
	[6, 30, 54],								//11		
	[6, 32, 58],								//12		
	[6, 34, 62],								//13		
	[6, 26, 46, 66],							//14		
	[6, 26, 48, 70],							//15		    
	[6, 26, 50, 74],							//16		    
	[6, 30, 54, 78],							//17		    
	[6, 30, 56, 82],							//18		    
	[6, 30, 58, 86],							//19		    
	[6, 34, 62, 90],							//20		    
	[6, 28, 50, 72, 94],						//21		    
	[6, 26, 50, 74, 98],						//22		    
	[6, 30, 54, 78, 102],						//23		    
	[6, 28, 54, 80, 106],						//24		    
	[6, 32, 58, 84, 110],						//25		    
	[6, 30, 58, 86, 114],						//26		    
	[6, 34, 62, 90, 118],						//27		    
	[6, 26, 50, 74, 98, 122],					//28		    
	[6, 30, 54, 78, 102, 126],					//29		    
	[6, 26, 52, 78, 104, 130],					//30		    
	[6, 30, 56, 82, 108, 134],					//31		    
	[6, 34, 60, 86, 112, 138],					//32		    
	[6, 30, 58, 86, 114, 142],					//33		    
	[6, 34, 62, 90, 118, 146],					//34		    
	[6, 30, 54, 78, 102, 126, 150],				//35		    
	[6, 24, 50, 76, 102, 128, 154],				//36		    
	[6, 28, 54, 80, 106, 132, 158],				//37		    
	[6, 32, 58, 84, 110, 136, 162],				//38		    
	[6, 26, 54, 82, 110, 138, 166],				//39		    
	[6, 30, 58, 86, 114, 142, 170]				//40		    
];

var format_information_bits_raw = {
	ecc: [
		"11",	//L
		"10",	//M
		"01",	//Q
		"00"	//H
	],
	mask: [
		"101",
		"001",
		"111",
		"110",
		"001",
		"000",
		"011",
		"010"
	]
}

var format_information_bits_partial = {
	BOTTOM_LEFT: [
	"1110111",
	"1110010",
	"1111101",
	"1111000",
	"1100110",
	"1100011",
	"1101100",
	"1101001",
	//ECC M
	"1010100",
	"1010001",
	"1011110",
	"1011011",
	"1000101",
	"1000000",
	"1001111",
	"1001010",
	//ECC Q
	"0110101",
	"0110000",
	"0111111",
	"0111010",
	"0100100",
	"0100001",
	"0101110",
	"0101011",
	//ECC H
	"0010110",
	"0010011",
	"0011100",
	"0011001",
	"0000111",
	"0000010",
	"0001101",
	"0001000"
	],
	TOP_RIGHT: [
	"11000100",
	"11110011",
	"10101010",
	"10011101",
	"00101111",
	"00011000",
	"01000001",
	"01110110",
	//ECC M
	"00010010",
	"00100101",
	"01111100",
	"01001011",
	"11111001",
	"11001110",
	"10010111",
	"10100000",
	//ECC Q
	"01011111",
	"01101000",
	"00110001",
	"00000110",
	"10110100",
	"10000011",
	"11011010",
	"11101101",
	//ECC H
	"10001001",
	"10111110",
	"11100111",
	"11010000",
	"01100010",
	"01010101",
	"00001100",
	"00111011"
	]
}

var format_information_bits = [
	//ECC L
	["111011111000100",
	"111001011110011",
	"111110110101010",
	"111100010011101",
	"110011000101111",
	"110001100011000",
	"110110001000001",
	"110100101110110"],
	//ECC M
	["101010000010010",
	"101000100100101",
	"101111001111100",
	"101101101001011",
	"100010111111001",
	"100000011001110",
	"100111110010111",
	"100101010100000"],
	//ECC Q
	["011010101011111",
	"011000001101000",
	"011111100110001",
	"011101000000110",
	"010010010110100",
	"010000110000011",
	"010111011011010",
	"010101111101101"],
	//ECC H
	["001011010001001",
	"001001110111110",
	"001110011100111",
	"001100111010000",
	"000011101100010",
	"000001001010101",
	"000110100001100",
	"000100000111011"]
];

var format_information_unmask = [
'000000000000000',
'000010100110111',
'000101001101110',
'000111101011001',
'001000111101011',
'001010011011100',
'001101110000101',
'001111010110010',
'010001111010110',
'010011011100001',
'010100110111000',
'010110010001111',
'011001000111101',
'011011100001010',
'011100001010011',
'011110101100100',
'100001010011011',
'100011110101100',
'100100011110101',
'100110111000010',
'101001101110000',
'101011001000111',
'101100100011110',
'101110000101001',
'110000101001101',
'110010001111010',
'110101100100011',
'110111000010100',
'111000010100110',
'111010110010001',
'111101011001000',
'111111111111111'
];


/* https://www.thonky.com/qr-code-tutorial/format-version-tables  */
//Version information table for QR version 7 and higher
var version_information_table = [
	"000111110010010100",			//7
	"001000010110111100",			//8	
	"001001101010011001",			//9
	"001010010011010011",         //10
	"001011101111110110",         //11
	"001100011101100010",         //12
	"001101100001000111",         //13
	"001110011000001101",         //14
	"001111100100101000",         //15
	"010000101101111000",         //16
	"010001010001011101",         //17
	"010010101000010111",         //18
	"010011010100110010",         //19
	"010100100110100110",         //20
	"010101011010000011",         //21
	"010110100011001001",         //22
	"010111011111101100",         //23
	"011000111011000100",         //24
	"011001000111100001",         //25
	"011010111110101011",         //26
	"011011000010001110",         //27
	"011100110000011010",         //28
	"011101001100111111",         //29
	"011110110101110101",         //30
	"011111001001010000",         //31
	"100000100111010101",         //32
	"100001011011110000",         //33
	"100010100010111010",         //34
	"100011011110011111",         //35
	"100100101100001011",         //36
	"100101010000101110",         //37
	"100110101001100100",         //38
	"100111010101000001",         //39
	"101000110001101001"			//40
];


/*  https://www.thonky.com/qr-code-tutorial/format-version-information */
// L = 1
// M = 0
// Q = 3
// H = 2 


/*     M    L      H     Q     https://www.thonky.com/qr-code-tutorial/error-correction-table  adding code block 1 and 2  */

var data_code_num_table = [
	[  16,   19,    9,   13],  //1
	[  28,   34,   16,   22],  //2
	[  44,   55,   26,   34],  //3
	[  64,   80,   36,   48],  //4
	[  86,  108,   46,   62],  //5
	[ 108,  136,   60,   76],  //6
	[ 124,  156,   66,   88],  //7
	[ 154,  194,   86,  110],  //8
	[ 182,  232,  100,  132],  //9
	[ 216,  274,  122,  154],  //10
	[ 254,  324,  140,  180],  //11
	[ 290,  370,  158,  206],  //12
	[ 334,  428,  180,  244],  //13
	[ 365,  461,  197,  261],  //14
	[ 415,  523,  223,  295],  //15
	[ 453,  589,  253,  325],  //16
	[ 507,  647,  283,  367],  //17
	[ 563,  721,  313,  397],  //18
	[ 627,  795,  341,  445],  //19
	[ 669,  861,  385,  485],  //20
	[ 714,  932,  406,  512],  //21
	[ 782, 1006,  442,  568],  //22
	[ 860, 1094,  464,  614],  //23
	[ 914, 1174,  514,  664],  //24
	[1000, 1276,  538,  718],  //25
	[1062, 1370,  596,  754],  //26
	[1128, 1468,  628,  808],  //27
	[1193, 1531,  661,  871],  //28
	[1267, 1631,  701,  911],  //29
	[1373, 1735,  745,  985],  //30
	[1455, 1843,  793, 1033],  //31
	[1541, 1955,  845, 1115],  //32
	[1631, 2071,  901, 1171],  //33
	[1725, 2191,  961, 1231],  //34
	[1812, 2306,  986, 1286],  //35
	[1914, 2434, 1054, 1354],  //36
	[1992, 2566, 1096, 1426],  //37
	[2102, 2702, 1142, 1502],  //38
	[2216, 2812, 1222, 1582],  //39
	[2334, 2956, 1276, 1666]   //40

];

/*   M  L  H  Q     https://www.thonky.com/qr-code-tutorial/error-correction-table  adding code block 1 and 2  */
var RS_block_num_table = [
	[1, 1, 1, 1],     //1
	[1, 1, 1, 1],     //2
	[1, 1, 2, 2],     //3
	[2, 1, 4, 2],     //4
	[2, 1, 4, 4],     //5
	[4, 2, 4, 4],     //6
	[4, 2, 5, 6],     //7
	[4, 2, 6, 6],     //8
	[5, 2, 8, 8],     //9
	[5, 4, 8, 8],     //10
	[5, 4, 11,8],     //11
	[8, 4, 11,10],    //12
	[9, 4, 16,12],    //13
	[9, 4, 16,16],    //14
	[10,6, 18,12],    //15
	[10,6, 16,17],    //16
	[11,6, 19,16],    //17
	[13, 6, 21, 18],  //18
	[14, 7, 25, 21],  //19
	[16, 8, 25, 20],  //20
	[17, 8, 25, 23],  //21
	[17, 9, 34, 23],  //22
	[18, 9, 30, 25],  //23
	[20, 10, 32, 27], //24
	[21, 12, 35, 29], //25
	[23, 12, 37, 34], //26
	[25, 12, 40, 34], //27
	[26, 13, 42, 35], //28
	[28, 14, 45, 38], //29
	[29, 15, 48, 40], //30
	[31, 16, 51, 43], //31
	[33, 17, 54, 45], //32
	[35, 18, 57, 48], //33
	[37, 19, 60, 51], //34
	[38, 19, 63, 53], //35
	[40, 20, 66, 56], //36
	[43, 21, 70, 59], //37
	[45, 22, 74, 62], //38
	[47, 24, 77, 65], //39
	[49, 25, 81, 68]  //40
];

/*   M  L  H  Q     https://www.thonky.com/qr-code-tutorial/error-correction-table  adding code block 1 and 2  */
var error_correction_code_table = [
	[10, 7,17,13],    //1
	[16,10,28,22],	  //2
	[26,15,22,18],	  //3
	[18,20,16,26],	  //4
	[24,26,22,18],	  //5
	[16,18,28,24],	  //6
	[18,20,26,18],	  //7
	[22,24,26,22],	  //8
	[22,30,24,20],	  //9
	[26,18,28,24],	  //10
	[30,20,24,28],	  //11
	[22,24,28,26],	  //12
	[22,26,22,24],	  //13
	[24,30,24,20],	  //14
	[24,22,24,30],	  //15
	[28,24,30,24],	  //16
	[28,28,28,28],	  //17
	[26,30,28,28],	  //18
	[26,28,26,26],	  //19
	[26,28,28,30],	  //20
	[26,28,30,28],	  //21
	[28,28,24,30],	  //22
	[28,30,30,30],	  //23
	[28,30,30,30],	  //24
	[28,26,30,30],	  //25
	[28,28,30,28],	  //26
	[28,30,30,30],	  //27
	[28,30,30,30],	  //28
	[28,30,30,30],	  //29
	[28,30,30,30],	  //30
	[28,30,30,30],	  //31
	[28,30,30,30],	  //32
	[28,30,30,30],	  //33
	[28,30,30,30],	  //34
	[28,30,30,30],	  //35
	[28,30,30,30],	  //36
	[28,30,30,30],	  //37
	[28,30,30,30],	  //38
	[28,30,30,30],	  //39
	[28,30,30,30]	  //40

];



var alphanumeric_table = [
	"0", "1", "2", "3", "4", "5",
	"6", "7", "8", "9", "A", "B",
	"C", "D", "E", "F", "G", "H",
	"I", "J", "K", "L", "M", "N",
	"O", "P", "Q", "R", "S", "T",
	"U", "V", "W", "X", "Y", "Z",
	" ", "$", "%", "*", "+", "-",
	".", "/", ":"
];

/* 
   https://www.thonky.com/qr-code-tutorial/structure-final-message 
   up to QR version 40

                            1 2 3 4 5 6 7 8 910111213141516171819202122232425262728293031323334353637383940 */
var remainder_bits_table = [0,7,7,7,7,7,0,0,0,0,0,0,0,3,3,3,3,3,3,3,4,4,4,4,4,4,4,3,3,3,3,3,3,3,0,0,0,0,0,0];

