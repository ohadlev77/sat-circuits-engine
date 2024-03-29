OPENQASM 2.0;
include "qelib1.inc";
qreg q[20];
creg c[8];
u(pi/2,0,pi) q[0];
u(pi/2,0,pi) q[1];
u(pi/2,0,pi) q[2];
u(pi/2,0,pi) q[3];
u(pi/2,0,0) q[4];
u(pi/2,0,pi) q[5];
u(pi/2,0,pi) q[6];
u(pi/2,0,pi) q[7];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
u(pi/2,pi/4,-pi) q[11];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi,0,pi) q[4];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,-pi,-pi) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
u(pi,0,pi) q[4];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
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
u(0,0,pi/4) q[13];
u(pi,0,pi) q[4];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[6],q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[14];
cx q[1],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
cx q[7],q[15];
cx q[6],q[15];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[1],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
cx q[7],q[17];
cx q[1],q[17];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
cx q[7],q[18];
cx q[5],q[18];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
u(pi,0,pi) q[4];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi,0,pi) q[4];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,pi/4) q[18];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,-3*pi/4) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[3],q[10];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[10];
u(pi/2,pi/4,-pi) q[10];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(pi/2,0,0) q[5];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
u(pi/2,0,0) q[2];
cx q[6],q[15];
cx q[7],q[17];
cx q[1],q[17];
cx q[7],q[15];
cx q[15],q[14];
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
u(pi/2,0,0) q[0];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[7],q[15];
cx q[6],q[15];
cx q[6],q[9];
cx q[3],q[9];
u(pi/2,0,0) q[7];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi/2,-pi,0) q[4];
cx q[8],q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[11];
u(pi,0,pi) q[8];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
u(pi/2,0,0) q[1];
u(pi/2,0,0) q[3];
cx q[6],q[9];
u(pi/2,0,0) q[6];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,0,3*pi/4) q[9];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,0,3*pi/4) q[11];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
cx q[12],q[7];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
u(0,0,pi/4) q[7];
cx q[12],q[7];
u(0,0,pi/4) q[12];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
cx q[6],q[12];
u(0,0,-pi/4) q[12];
u(0,0,pi/4) q[6];
cx q[6],q[12];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,pi/4,-pi) q[11];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,pi/4,-pi) q[10];
u(0,2.191981133989078,-2.1919811339890782) q[11];
u(pi/2,-pi,0) q[4];
u(pi/2,-pi,-pi) q[5];
u(pi/2,-pi,-pi) q[6];
u(pi/2,-pi,-3*pi/4) q[7];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
u(pi/2,-pi,-pi) q[3];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(pi/2,-pi,-pi) q[2];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(pi/2,-pi,-pi) q[0];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,-pi,-pi) q[1];
u(pi/2,0,3*pi/4) q[8];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi,0,pi) q[4];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
u(pi,0,pi) q[4];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
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
u(0,0,pi/4) q[13];
u(pi,0,pi) q[4];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[6],q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[14];
cx q[1],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
cx q[7],q[15];
cx q[6],q[15];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[1],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
cx q[7],q[17];
cx q[1],q[17];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
cx q[7],q[18];
cx q[5],q[18];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
u(pi,0,pi) q[4];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi,0,pi) q[4];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,pi/4) q[18];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,-3*pi/4) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[3],q[10];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[10];
u(pi/2,pi/4,-pi) q[10];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(pi/2,0,0) q[5];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
u(pi/2,0,0) q[2];
cx q[6],q[15];
cx q[7],q[17];
cx q[1],q[17];
cx q[7],q[15];
cx q[15],q[14];
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
u(pi/2,0,0) q[0];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[7],q[15];
cx q[6],q[15];
cx q[6],q[9];
cx q[3],q[9];
u(pi/2,0,0) q[7];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi/2,-pi,0) q[4];
cx q[8],q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[11];
u(pi,0,pi) q[8];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
u(pi/2,0,0) q[1];
u(pi/2,0,0) q[3];
cx q[6],q[9];
u(pi/2,0,0) q[6];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,0,3*pi/4) q[9];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,0,3*pi/4) q[11];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
cx q[12],q[7];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
u(0,0,pi/4) q[7];
cx q[12],q[7];
u(0,0,pi/4) q[12];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
cx q[6],q[12];
u(0,0,-pi/4) q[12];
u(0,0,pi/4) q[6];
cx q[6],q[12];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,pi/4,-pi) q[11];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,pi/4,-pi) q[10];
u(0,2.191981133989078,-2.1919811339890782) q[11];
u(pi/2,-pi,0) q[4];
u(pi/2,-pi,-pi) q[5];
u(pi/2,-pi,-pi) q[6];
u(pi/2,-pi,-3*pi/4) q[7];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
u(pi/2,-pi,-pi) q[3];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(pi/2,-pi,-pi) q[2];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(pi/2,-pi,-pi) q[0];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,-pi,-pi) q[1];
u(pi/2,0,3*pi/4) q[8];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi,0,pi) q[4];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
u(pi,0,pi) q[4];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
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
u(0,0,pi/4) q[13];
u(pi,0,pi) q[4];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[6],q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[14];
cx q[1],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
cx q[7],q[15];
cx q[6],q[15];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[1],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
cx q[7],q[17];
cx q[1],q[17];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
cx q[7],q[18];
cx q[5],q[18];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
u(pi,0,pi) q[4];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi,0,pi) q[4];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,pi/4) q[18];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,-3*pi/4) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[3],q[10];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[10];
u(pi/2,pi/4,-pi) q[10];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(pi/2,0,0) q[5];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
u(pi/2,0,0) q[2];
cx q[6],q[15];
cx q[7],q[17];
cx q[1],q[17];
cx q[7],q[15];
cx q[15],q[14];
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
u(pi/2,0,0) q[0];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[7],q[15];
cx q[6],q[15];
cx q[6],q[9];
cx q[3],q[9];
u(pi/2,0,0) q[7];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi/2,-pi,0) q[4];
cx q[8],q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[11];
u(pi,0,pi) q[8];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
u(pi/2,0,0) q[1];
u(pi/2,0,0) q[3];
cx q[6],q[9];
u(pi/2,0,0) q[6];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,0,3*pi/4) q[9];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,0,3*pi/4) q[11];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
cx q[12],q[7];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
u(0,0,pi/4) q[7];
cx q[12],q[7];
u(0,0,pi/4) q[12];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
cx q[6],q[12];
u(0,0,-pi/4) q[12];
u(0,0,pi/4) q[6];
cx q[6],q[12];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,pi/4,-pi) q[11];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,pi/4,-pi) q[10];
u(0,2.191981133989078,-2.1919811339890782) q[11];
u(pi/2,-pi,0) q[4];
u(pi/2,-pi,-pi) q[5];
u(pi/2,-pi,-pi) q[6];
u(pi/2,-pi,-3*pi/4) q[7];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
u(pi/2,-pi,-pi) q[3];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(pi/2,-pi,-pi) q[2];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(pi/2,-pi,-pi) q[0];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,-pi,-pi) q[1];
u(pi/2,0,3*pi/4) q[8];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi,0,pi) q[4];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
u(pi,0,pi) q[4];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
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
u(0,0,pi/4) q[13];
u(pi,0,pi) q[4];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[6],q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[14];
cx q[1],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
cx q[7],q[15];
cx q[6],q[15];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[1],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
cx q[7],q[17];
cx q[1],q[17];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
cx q[7],q[18];
cx q[5],q[18];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
u(pi,0,pi) q[4];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi,0,pi) q[4];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,pi/4) q[18];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,-3*pi/4) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[3],q[10];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[10];
u(pi/2,pi/4,-pi) q[10];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(pi/2,0,0) q[5];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
u(pi/2,0,0) q[2];
cx q[6],q[15];
cx q[7],q[17];
cx q[1],q[17];
cx q[7],q[15];
cx q[15],q[14];
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
u(pi/2,0,0) q[0];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[7],q[15];
cx q[6],q[15];
cx q[6],q[9];
cx q[3],q[9];
u(pi/2,0,0) q[7];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi/2,-pi,0) q[4];
cx q[8],q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[11];
u(pi,0,pi) q[8];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
u(pi/2,0,0) q[1];
u(pi/2,0,0) q[3];
cx q[6],q[9];
u(pi/2,0,0) q[6];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,0,3*pi/4) q[9];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,0,3*pi/4) q[11];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
cx q[12],q[7];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
u(0,0,pi/4) q[7];
cx q[12],q[7];
u(0,0,pi/4) q[12];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
cx q[6],q[12];
u(0,0,-pi/4) q[12];
u(0,0,pi/4) q[6];
cx q[6],q[12];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,pi/4,-pi) q[11];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,pi/4,-pi) q[10];
u(0,2.191981133989078,-2.1919811339890782) q[11];
u(pi/2,-pi,0) q[4];
u(pi/2,-pi,-pi) q[5];
u(pi/2,-pi,-pi) q[6];
u(pi/2,-pi,-3*pi/4) q[7];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
u(pi/2,-pi,-pi) q[3];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(pi/2,-pi,-pi) q[2];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(pi/2,-pi,-pi) q[0];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,-pi,-pi) q[1];
u(pi/2,0,3*pi/4) q[8];
cx q[1],q[8];
cx q[3],q[8];
u(pi,0,pi) q[8];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi,0,pi) q[4];
cx q[8],q[11];
u(pi/2,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(pi/2,pi/4,-pi) q[13];
u(pi,0,pi) q[4];
cx q[6],q[9];
cx q[3],q[9];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
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
u(0,0,pi/4) q[13];
u(pi,0,pi) q[4];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[6],q[9];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[14];
cx q[1],q[14];
u(pi/2,pi/4,-pi) q[13];
cx q[12],q[13];
u(0,0,-pi/4) q[13];
cx q[14],q[13];
cx q[1],q[14];
cx q[0],q[14];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,0,3*pi/4) q[13];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
cx q[6],q[15];
cx q[7],q[15];
cx q[15],q[14];
u(0,0,pi/4) q[14];
cx q[13],q[14];
u(pi/2,0,3*pi/4) q[14];
cx q[7],q[15];
cx q[6],q[15];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[0],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
cx q[1],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,0,3*pi/4) q[16];
cx q[7],q[17];
cx q[1],q[17];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,0,3*pi/4) q[17];
cx q[7],q[18];
cx q[5],q[18];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[18];
u(pi,0,pi) q[4];
cx q[5],q[10];
cx q[3],q[10];
u(pi,0,pi) q[10];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi/2,0,-pi/4) q[18];
u(pi,0,pi) q[4];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,0,pi) q[19];
cx q[18],q[19];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
u(0,0,pi/4) q[19];
cx q[18],q[19];
u(0,0,pi/4) q[18];
u(0,0,-pi/4) q[19];
cx q[17],q[19];
cx q[17],q[18];
u(0,0,pi/4) q[17];
u(0,0,-pi/4) q[18];
cx q[17],q[18];
u(pi/2,0,-3*pi/4) q[19];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19];
u(pi/2,pi/4,-pi) q[17];
cx q[16],q[17];
u(0,0,-pi/4) q[17];
u(pi/2,-3*pi/4,-pi) q[18];
cx q[10],q[18];
u(0,0,-pi/4) q[18];
u(pi,0,pi) q[4];
cx q[4],q[18];
u(0,0,pi/4) q[18];
cx q[10],q[18];
u(pi,0,pi) q[10];
u(pi/2,0,3*pi/4) q[18];
cx q[3],q[10];
u(0,pi/2,-pi/2) q[4];
cx q[5],q[10];
u(pi/2,pi/4,-pi) q[10];
cx q[5],q[18];
cx q[7],q[18];
cx q[18],q[17];
u(0,0,pi/4) q[17];
cx q[16],q[17];
u(pi/2,pi/4,-pi) q[16];
cx q[15],q[16];
u(0,0,-pi/4) q[16];
u(pi/2,0,3*pi/4) q[17];
cx q[1],q[17];
cx q[7],q[18];
cx q[5],q[18];
u(pi/2,0,0) q[5];
cx q[7],q[17];
cx q[17],q[16];
u(0,0,pi/4) q[16];
cx q[15],q[16];
u(pi/2,pi/4,-pi) q[15];
cx q[14],q[15];
u(0,0,-pi/4) q[15];
u(pi/2,0,3*pi/4) q[16];
cx q[0],q[16];
cx q[2],q[16];
cx q[16],q[15];
u(0,0,pi/4) q[15];
cx q[14],q[15];
u(pi/2,pi/4,-pi) q[14];
cx q[13],q[14];
u(0,0,-pi/4) q[14];
u(pi/2,0,3*pi/4) q[15];
cx q[2],q[16];
cx q[0],q[16];
u(pi/2,0,0) q[2];
cx q[6],q[15];
cx q[7],q[17];
cx q[1],q[17];
cx q[7],q[15];
cx q[15],q[14];
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
u(pi/2,0,0) q[0];
u(0,0,pi/4) q[13];
cx q[12],q[13];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
u(0,2.1919811339890787,-2.1919811339890787) q[13];
cx q[7],q[15];
cx q[6],q[15];
cx q[6],q[9];
cx q[3],q[9];
u(pi/2,0,0) q[7];
u(pi,0,pi) q[9];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[9],q[13];
u(pi/2,0,-pi/4) q[13];
cx q[13],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,-3*pi/4,-pi) q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[12];
u(pi/2,-3*pi/4,-pi) q[13];
cx q[8],q[11];
u(0,0,-pi/4) q[11];
cx q[9],q[13];
u(0,0,-pi/4) q[13];
cx q[4],q[13];
u(0,0,pi/4) q[13];
u(0,pi/2,-pi/2) q[4];
cx q[4],q[11];
u(0,0,pi/4) q[11];
u(pi/2,-pi,0) q[4];
cx q[8],q[11];
u(0,-0.6211848071941821,0.6211848071941821) q[11];
u(pi,0,pi) q[8];
cx q[9],q[13];
u(pi/2,0,3*pi/4) q[13];
u(pi,0,pi) q[9];
cx q[3],q[9];
cx q[3],q[8];
cx q[1],q[8];
u(pi/2,0,0) q[1];
u(pi/2,0,0) q[3];
cx q[6],q[9];
u(pi/2,0,0) q[6];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,0,3*pi/4) q[9];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,0,3*pi/4) q[11];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,0,3*pi/4) q[12];
cx q[12],q[7];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
u(0,0,pi/4) q[7];
cx q[12],q[7];
u(0,0,pi/4) q[12];
u(0,0,-pi/4) q[7];
cx q[6],q[7];
cx q[6],q[12];
u(0,0,-pi/4) q[12];
u(0,0,pi/4) q[6];
cx q[6],q[12];
u(pi/2,pi/4,-pi) q[12];
cx q[11],q[12];
u(0,0,-pi/4) q[12];
cx q[5],q[12];
u(0,0,pi/4) q[12];
cx q[11],q[12];
u(pi/2,pi/4,-pi) q[11];
cx q[10],q[11];
u(0,0,-pi/4) q[11];
u(pi/2,0,3*pi/4) q[12];
cx q[4],q[11];
u(0,0,pi/4) q[11];
cx q[10],q[11];
u(pi/2,pi/4,-pi) q[10];
u(pi/2,0,3*pi/4) q[11];
u(pi/2,-pi,-pi) q[4];
u(pi/2,-pi,-pi) q[5];
u(pi/2,-pi,-pi) q[6];
u(pi/2,-pi,-3*pi/4) q[7];
cx q[9],q[10];
u(0,0,-pi/4) q[10];
cx q[3],q[10];
u(0,0,pi/4) q[10];
u(pi/2,-pi,-pi) q[3];
cx q[9],q[10];
u(pi/2,0,3*pi/4) q[10];
u(pi/2,pi/4,-pi) q[9];
cx q[8],q[9];
u(0,0,-pi/4) q[9];
cx q[2],q[9];
u(pi/2,-pi,-pi) q[2];
u(0,0,pi/4) q[9];
cx q[8],q[9];
u(pi/2,pi/4,-pi) q[8];
cx q[1],q[8];
u(0,0,-pi/4) q[8];
cx q[0],q[8];
u(pi/2,-pi,-pi) q[0];
u(0,0,pi/4) q[8];
cx q[1],q[8];
u(pi/2,-pi,-pi) q[1];
u(pi/2,0,3*pi/4) q[8];
u(pi/2,0,3*pi/4) q[9];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
measure q[6] -> c[6];
measure q[7] -> c[7];
