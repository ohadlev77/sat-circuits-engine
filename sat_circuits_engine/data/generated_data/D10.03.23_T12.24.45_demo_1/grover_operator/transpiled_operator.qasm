OPENQASM 2.0;
include "qelib1.inc";
qreg q[20];
u(pi,0,pi) q[4];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
u(pi/2,pi/4,-pi) q[11];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[11];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[13];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[13];
cx q[9],q[13];
u(0,pi/2,-pi/2) q[9];
u(0,-0.6211848071941821,0.6211848071941821) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[0],q[14];
cx q[1],q[14];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
cx q[7],q[15];
cx q[6],q[15];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
cx q[2],q[16];
cx q[0],q[16];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[1],q[17];
cx q[7],q[17];
cx q[17],q[16];
cx q[7],q[17];
cx q[1],q[17];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
cx q[7],q[18];
cx q[5],q[18];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
u(pi/2,pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(pi/2,0,-3*pi/4) q[19];
u(0,0,pi/4) q[18];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
cx q[3],q[10];
cx q[5],q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[17];
cx q[17],q[16];
cx q[7],q[17];
cx q[1],q[17];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
cx q[2],q[16];
cx q[0],q[16];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
cx q[7],q[15];
cx q[6],q[15];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
u(pi/2,0,3*pi/4) q[14];
cx q[0],q[14];
cx q[1],q[14];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,pi/2,-pi/2) q[4];
u(0,0,pi/4) q[13];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(pi,0,pi) q[4];
u(0,0,pi/4) q[11];
cx q[8],q[11];
u(pi,0,pi) q[8];
u(pi/2,0,3*pi/4) q[11];
u(0,0,pi/4) q[13];
cx q[9],q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
cx q[6],q[9];
u(pi/2,0,3*pi/4) q[13];
