OPENQASM 2.0;
include "qelib1.inc";
qreg input_reg[4];
qreg left_aux_reg[0];
qreg right_aux_reg[0];
qreg comparison_aux_reg[0];
qreg out_reg[2];
qreg ancilla[1];
cx input_reg[2],out_reg[0];
cx input_reg[3],out_reg[0];
u(pi,0,pi) out_reg[0];
cx input_reg[0],out_reg[1];
cx input_reg[1],out_reg[1];
u(pi,0,pi) out_reg[1];
u(pi/2,0,pi) ancilla[0];
cx out_reg[1],ancilla[0];
u(0,0,-pi/4) ancilla[0];
cx out_reg[0],ancilla[0];
u(0,0,pi/4) ancilla[0];
cx out_reg[1],ancilla[0];
u(0,0,-pi/4) ancilla[0];
cx out_reg[0],ancilla[0];
u(pi/2,0,-3*pi/4) ancilla[0];
u(0,0,pi/4) out_reg[1];
cx out_reg[0],out_reg[1];
u(0,0,pi/4) out_reg[0];
u(0,0,-pi/4) out_reg[1];
cx out_reg[0],out_reg[1];
barrier input_reg[0],input_reg[1],input_reg[2],input_reg[3],out_reg[0],out_reg[1],ancilla[0];
u(pi,0,pi) out_reg[1];
cx input_reg[1],out_reg[1];
cx input_reg[0],out_reg[1];
barrier input_reg[0],input_reg[1],input_reg[2],input_reg[3],out_reg[0],out_reg[1],ancilla[0];
u(pi,0,pi) out_reg[0];
cx input_reg[3],out_reg[0];
cx input_reg[2],out_reg[0];
