OPENQASM 2.0;
include "qelib1.inc";
qreg q[27];
cx q[2],q[8];
u(pi,0,pi) q[9];
cx q[8],q[12];
cx q[3],q[12];
u(pi,0,pi) q[12];
cx q[9],q[13];
cx q[4],q[13];
u(pi,0,pi) q[13];
u(pi,0,pi) q[4];
cx q[5],q[14];
cx q[3],q[14];
u(pi,0,pi) q[14];
cx q[1],q[15];
u(pi/2,pi/4,-pi) q[16];
cx q[12],q[16];
u(0,0,-pi/4) q[16];
cx q[13],q[16];
u(0,0,pi/4) q[16];
cx q[12],q[16];
u(pi/2,0,-pi/4) q[16];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,pi/4,-pi) q[18];
cx q[14],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[14],q[18];
u(pi/2,0,-pi/4) q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[14],q[18];
u(0,0,-pi/4) q[18];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[14],q[18];
u(0,-0.6211848071941821,0.6211848071941821) q[18];
cx q[17],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[14];
cx q[3],q[14];
cx q[3],q[15];
u(pi,0,pi) q[15];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[14];
u(pi/2,pi/4,-pi) q[19];
cx q[15],q[19];
u(0,0,-pi/4) q[19];
cx q[4],q[19];
u(0,0,pi/4) q[19];
cx q[15],q[19];
u(pi/2,0,-pi/4) q[19];
cx q[19],q[18];
u(0,0,pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,3*pi/4) q[18];
u(pi/2,-3*pi/4,-pi) q[19];
cx q[15],q[19];
u(0,0,-pi/4) q[19];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[19];
u(0,0,pi/4) q[19];
cx q[15],q[19];
u(0,-0.6211848071941821,0.6211848071941821) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
u(pi,0,pi) q[15];
cx q[3],q[15];
u(pi,0,pi) q[3];
u(pi,0,pi) q[4];
u(pi/2,pi/4,-pi) q[20];
cx q[3],q[20];
u(0,0,-pi/4) q[20];
cx q[4],q[20];
u(0,0,pi/4) q[20];
cx q[3],q[20];
u(pi/2,0,3*pi/4) q[20];
cx q[20],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(pi/2,0,3*pi/4) q[19];
u(pi/2,pi/4,-pi) q[20];
u(0,pi/2,-pi/2) q[3];
cx q[3],q[20];
u(0,0,-pi/4) q[20];
cx q[4],q[20];
u(0,0,pi/4) q[20];
cx q[3],q[20];
u(0,-0.6211848071941821,0.6211848071941821) q[20];
cx q[19],q[20];
u(0,0,-pi/4) q[20];
u(pi,0,pi) q[3];
cx q[3],q[10];
u(pi/2,pi/2,0.20220131104139316) q[10];
cx q[4],q[11];
u(0.9806737259473847,2.295336868449164,2.683927693682916) q[11];
cx q[10],q[11];
u(pi/2,-pi/2,-pi/2) q[10];
u(0.9817498751378533,-0.6405278637538672,-0.6405278637538672) q[11];
cx q[10],q[11];
u(pi/4,-pi,-pi/2) q[10];
u(2.090822159332339,-2.446835860047982,2.603927236866438) q[11];
cx q[10],q[11];
u(pi/2,0.20220131104139272,pi/2) q[10];
u(0.7659608332674918,-1.194051989929517,2.8638183100986367) q[11];
cx q[0],q[21];
cx q[1],q[21];
cx q[21],q[20];
u(0,0,pi/4) q[20];
cx q[19],q[20];
u(pi/2,0,3*pi/4) q[20];
cx q[1],q[21];
cx q[0],q[21];
u(pi/2,pi/4,-pi) q[21];
cx q[20],q[21];
u(0,0,-pi/4) q[21];
cx q[6],q[22];
cx q[7],q[22];
cx q[22],q[21];
u(0,0,pi/4) q[21];
cx q[20],q[21];
u(pi/2,0,3*pi/4) q[21];
cx q[7],q[22];
cx q[6],q[22];
u(pi/2,pi/4,-pi) q[22];
cx q[21],q[22];
u(0,0,-pi/4) q[22];
cx q[0],q[23];
cx q[2],q[23];
cx q[23],q[22];
u(0,0,pi/4) q[22];
cx q[21],q[22];
u(pi/2,0,3*pi/4) q[22];
cx q[2],q[23];
cx q[0],q[23];
u(pi/2,pi/4,-pi) q[23];
cx q[22],q[23];
u(0,0,-pi/4) q[23];
u(0,0,pi/4) q[2];
cx q[2],q[10];
u(0,0,-pi/4) q[10];
cx q[2],q[10];
u(0,0,pi/4) q[10];
u(pi,1.4065829705916304,-0.1642133562032666) q[2];
cx q[2],q[11];
u(pi,-pi,0) q[11];
u(pi,-1.4065829705916295,1.7350096829981627) q[2];
cx q[1],q[24];
cx q[6],q[24];
cx q[24],q[23];
u(0,0,pi/4) q[23];
cx q[22],q[23];
u(pi/2,0,3*pi/4) q[23];
cx q[6],q[24];
cx q[1],q[24];
u(pi/2,pi/4,-pi) q[24];
cx q[23],q[24];
u(0,0,-pi/4) q[24];
cx q[5],q[25];
cx q[7],q[25];
cx q[25],q[24];
u(0,0,pi/4) q[24];
cx q[23],q[24];
u(pi/2,0,3*pi/4) q[24];
cx q[7],q[25];
cx q[5],q[25];
u(pi/2,pi/4,-pi) q[25];
u(0,0,pi/4) q[5];
cx q[5],q[10];
u(0,0,-pi/4) q[10];
cx q[5],q[10];
u(pi/2,-pi/2,-pi/4) q[10];
u(pi,1.4065829705916304,-0.1642133562032666) q[5];
cx q[5],q[11];
u(2.0908221593323386,0.5376654167233541,-0.6947567935418113) q[11];
cx q[10],q[11];
u(pi/2,-pi/2,-pi/2) q[10];
u(0.9817498751378533,-0.6405278637538672,-0.6405278637538672) q[11];
cx q[10],q[11];
u(pi/4,0,pi/2) q[10];
u(2.090822159332339,-2.446835860047982,2.603927236866438) q[11];
cx q[10],q[11];
u(pi/2,3*pi/4,-pi/2) q[10];
cx q[10],q[25];
u(0,0,-pi/4) q[25];
u(0.05568345982489404,-pi/2,pi/2) q[11];
cx q[11],q[25];
u(0,0,pi/4) q[25];
cx q[10],q[25];
u(pi/2,0,3*pi/4) q[25];
u(pi,-1.4065829705916295,1.7350096829981627) q[5];
u(pi/2,0,pi) q[26];
cx q[25],q[26];
u(0,0,-pi/4) q[26];
cx q[24],q[26];
u(0,0,pi/4) q[26];
cx q[25],q[26];
u(0,0,-pi/4) q[26];
cx q[24],q[26];
u(pi/2,0,-3*pi/4) q[26];
u(0,0,pi/4) q[25];
cx q[24],q[25];
u(0,0,pi/4) q[24];
u(0,0,-pi/4) q[25];
cx q[24],q[25];
u(pi/2,pi/4,-pi) q[24];
cx q[23],q[24];
u(0,0,-pi/4) q[24];
u(pi/2,pi/4,-pi) q[25];
cx q[10],q[25];
u(0,0,-pi/4) q[25];
cx q[11],q[25];
u(0,0,pi/4) q[25];
cx q[10],q[25];
u(pi/2,0,3*pi/4) q[25];
u(pi/2,pi/2,0.20220131104139316) q[10];
u(0.9806737259473847,2.295336868449164,2.683927693682916) q[11];
cx q[10],q[11];
u(pi/2,-pi/2,-pi/2) q[10];
u(0.9817498751378533,-0.6405278637538672,-0.6405278637538672) q[11];
cx q[10],q[11];
u(pi/4,-pi,-pi/2) q[10];
u(2.090822159332339,-2.446835860047982,2.603927236866438) q[11];
cx q[10],q[11];
u(pi/2,0.20220131104139272,pi/2) q[10];
u(0.7659608332674918,-1.194051989929517,2.8638183100986367) q[11];
cx q[5],q[11];
u(0,-0.46364760900080615,0.46364760900080615) q[11];
cx q[2],q[11];
u(1.0507704942574547,-2.603927236866439,0.6947567935418117) q[11];
u(0,2.9938722350179336,0.9331185819693086) q[2];
u(0,2.9938722350179336,0.9331185819693086) q[5];
cx q[5],q[10];
u(0,0,pi/4) q[10];
cx q[5],q[10];
u(0,0,-pi/4) q[10];
cx q[2],q[10];
u(0,0,pi/4) q[10];
cx q[2],q[10];
u(pi/2,-pi/2,-3*pi/4) q[10];
cx q[10],q[11];
u(pi/2,-pi/2,-pi/2) q[10];
u(0.9817498751378533,-0.6405278637538672,-0.6405278637538672) q[11];
cx q[10],q[11];
u(pi/4,0,pi/2) q[10];
u(2.090822159332339,-2.446835860047982,2.603927236866438) q[11];
cx q[10],q[11];
u(pi/2,3*pi/4,-pi/2) q[10];
u(0.05568345982489404,-pi/2,pi/2) q[11];
cx q[3],q[10];
u(pi,0,pi) q[3];
cx q[4],q[11];
cx q[5],q[25];
cx q[7],q[25];
cx q[25],q[24];
u(0,0,pi/4) q[24];
cx q[23],q[24];
u(pi/2,pi/4,-pi) q[23];
cx q[22],q[23];
u(0,0,-pi/4) q[23];
u(pi/2,0,3*pi/4) q[24];
cx q[1],q[24];
cx q[6],q[24];
cx q[24],q[23];
u(0,0,pi/4) q[23];
cx q[22],q[23];
u(pi/2,pi/4,-pi) q[22];
cx q[21],q[22];
u(0,0,-pi/4) q[22];
u(pi/2,0,3*pi/4) q[23];
cx q[0],q[23];
cx q[2],q[23];
cx q[23],q[22];
u(0,0,pi/4) q[22];
cx q[21],q[22];
u(pi/2,pi/4,-pi) q[21];
cx q[20],q[21];
u(0,0,-pi/4) q[21];
u(pi/2,0,3*pi/4) q[22];
cx q[2],q[23];
cx q[0],q[23];
cx q[6],q[24];
cx q[1],q[24];
cx q[6],q[22];
cx q[7],q[25];
cx q[5],q[25];
cx q[5],q[14];
cx q[7],q[22];
cx q[22],q[21];
u(0,0,pi/4) q[21];
cx q[20],q[21];
u(pi/2,pi/4,-pi) q[20];
cx q[19],q[20];
u(0,0,-pi/4) q[20];
u(pi/2,0,3*pi/4) q[21];
cx q[0],q[21];
cx q[1],q[21];
cx q[21],q[20];
u(0,0,pi/4) q[20];
cx q[19],q[20];
u(pi/2,pi/4,-pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
u(0,2.1919811339890787,-2.1919811339890787) q[20];
cx q[1],q[21];
cx q[0],q[21];
cx q[3],q[20];
u(0,0,-pi/4) q[20];
cx q[4],q[20];
u(0,0,pi/4) q[20];
cx q[3],q[20];
u(pi/2,0,3*pi/4) q[20];
cx q[20],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
cx q[17],q[18];
u(0,0,-pi/4) q[18];
u(0,2.1919811339890787,-2.1919811339890787) q[19];
u(pi/2,pi/4,-pi) q[20];
u(0,pi/2,-pi/2) q[3];
cx q[3],q[20];
u(0,0,-pi/4) q[20];
cx q[4],q[20];
u(0,0,pi/4) q[20];
cx q[3],q[20];
u(pi/2,0,3*pi/4) q[20];
u(pi,0,pi) q[3];
cx q[3],q[15];
u(pi,0,pi) q[15];
cx q[15],q[19];
u(0,0,-pi/4) q[19];
u(pi,0,pi) q[4];
cx q[4],q[19];
u(0,0,pi/4) q[19];
cx q[15],q[19];
u(pi/2,0,-pi/4) q[19];
cx q[19],q[18];
u(0,0,pi/4) q[18];
cx q[17],q[18];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(0,2.1919811339890787,-2.1919811339890787) q[18];
u(pi/2,-3*pi/4,-pi) q[19];
cx q[15],q[19];
u(0,0,-pi/4) q[19];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[19];
u(0,0,pi/4) q[19];
cx q[15],q[19];
u(pi/2,0,3*pi/4) q[19];
u(pi,0,pi) q[15];
cx q[3],q[15];
cx q[1],q[15];
cx q[3],q[14];
u(pi,0,pi) q[14];
cx q[14],q[18];
u(0,0,-pi/4) q[18];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[14],q[18];
u(pi/2,0,-pi/4) q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,-3*pi/4,-pi) q[16];
u(pi/2,0,3*pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[12],q[16];
u(0,0,-pi/4) q[16];
cx q[13],q[16];
u(0,0,pi/4) q[16];
cx q[12],q[16];
u(pi/2,0,3*pi/4) q[16];
u(pi,0,pi) q[12];
u(pi,0,pi) q[13];
cx q[14],q[18];
u(0,0,-pi/4) q[18];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[14],q[18];
u(pi/2,0,3*pi/4) q[18];
u(pi,0,pi) q[14];
cx q[3],q[14];
cx q[3],q[12];
cx q[8],q[12];
cx q[2],q[8];
u(pi,0,pi) q[4];
cx q[4],q[13];
cx q[9],q[13];
u(pi,0,pi) q[9];
cx q[5],q[14];
cx q[7],q[22];
cx q[6],q[22];
