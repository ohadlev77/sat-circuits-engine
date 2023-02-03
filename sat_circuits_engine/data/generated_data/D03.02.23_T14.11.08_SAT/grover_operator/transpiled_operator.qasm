OPENQASM 2.0;
include "qelib1.inc";
qreg input_reg[8];
qreg left_aux_reg[4];
qreg right_aux_reg[0];
qreg comparison_aux_reg[0];
qreg out_reg[3];
qreg ancilla[1];
u(0,0,pi/8) input_reg[0];
u(0,0,pi/8) input_reg[1];
u(0,0,pi/8) input_reg[3];
u(pi,pi/8,-pi) input_reg[7];
cx input_reg[7],input_reg[1];
u(0,0,-pi/8) input_reg[1];
cx input_reg[7],input_reg[1];
cx input_reg[1],input_reg[0];
u(0,0,-pi/8) input_reg[0];
cx input_reg[7],input_reg[0];
u(0,0,pi/8) input_reg[0];
cx input_reg[1],input_reg[0];
u(0,0,-pi/8) input_reg[0];
cx input_reg[7],input_reg[0];
cx input_reg[5],left_aux_reg[0];
cx input_reg[6],left_aux_reg[1];
u(pi/2,pi/4,-pi) left_aux_reg[3];
u(pi/2,pi/8,-pi) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[1],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[7],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[1],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
u(0,0,pi/8) input_reg[0];
u(0,0,pi/8) input_reg[1];
cx input_reg[7],out_reg[0];
u(pi/2,0,0) out_reg[0];
u(pi,0,pi) input_reg[7];
cx input_reg[7],left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(pi/2,pi/4,-3*pi/4) left_aux_reg[2];
u(0,0,pi/8) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[1];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(pi/2,pi/4,-3*pi/4) left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[2];
u(0,0,pi/16) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,0,-3*pi/4) left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
cx left_aux_reg[1],left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
u(pi/2,-pi,-0.82697089) left_aux_reg[3];
u(pi/2,pi/4,-pi) out_reg[1];
cx out_reg[0],out_reg[1];
u(0,0,-pi/4) out_reg[1];
cx input_reg[4],out_reg[2];
cx input_reg[2],out_reg[2];
u(pi,0,pi) out_reg[2];
cx out_reg[2],out_reg[1];
u(0,0,pi/4) out_reg[1];
cx out_reg[0],out_reg[1];
u(pi/2,0,3*pi/4) out_reg[1];
u(pi,0,pi) out_reg[2];
cx input_reg[2],out_reg[2];
u(0,0,pi/16) input_reg[2];
cx input_reg[2],left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[0];
cx input_reg[2],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
u(0,0,pi/8) input_reg[2];
cx input_reg[2],left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[1];
cx input_reg[2],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
u(0,0,pi/4) input_reg[2];
cx input_reg[2],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[2];
cx input_reg[2],left_aux_reg[2];
u(pi/2,-pi,-0.041572731) left_aux_reg[2];
u(0,-pi,-pi/2) input_reg[2];
cx input_reg[2],left_aux_reg[3];
u(pi/2,-2.3146218,0) left_aux_reg[3];
u(pi,-1.2897262,1.8518665) input_reg[2];
cx input_reg[3],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
cx input_reg[3],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
u(pi/2,0,pi) left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[3];
u(0,0,pi/4) input_reg[3];
cx input_reg[3],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
cx input_reg[3],left_aux_reg[1];
u(0,0,pi/4) left_aux_reg[1];
u(0,-pi,-pi/2) input_reg[3];
cx input_reg[3],left_aux_reg[2];
u(pi/2,-2.3146218,0) left_aux_reg[2];
cx left_aux_reg[1],left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
u(pi/2,0,pi) left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,pi/4) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
u(pi/2,0,pi) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0.29452431,0.29452431) left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
cx left_aux_reg[3],left_aux_reg[1];
u(pi,0,7*pi/8) left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,pi/4) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(pi,0,3*pi/4) left_aux_reg[2];
u(pi/2,0,pi) left_aux_reg[3];
u(pi,-1.2897262,1.8518665) input_reg[3];
cx input_reg[4],out_reg[2];
u(pi/2,0,pi) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,0,-pi/4) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,1.406583,-0.62118481) out_reg[2];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,0,3*pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(pi/2,pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,-pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[0],out_reg[2];
u(0,0,pi/4) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,1.406583,-2.1919811) out_reg[2];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,pi/4,3*pi/4) left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[3];
cx left_aux_reg[3],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[3],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,-pi/16) left_aux_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,pi/16) left_aux_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
u(0,pi/2,-pi/2) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(pi/2,0,-15*pi/16) out_reg[2];
u(0,pi/2,-pi/2) left_aux_reg[1];
u(pi/2,0,pi) ancilla[0];
cx out_reg[2],ancilla[0];
u(0,0,-pi/4) ancilla[0];
cx out_reg[1],ancilla[0];
u(0,0,pi/4) ancilla[0];
cx out_reg[2],ancilla[0];
u(0,0,-pi/4) ancilla[0];
cx out_reg[1],ancilla[0];
u(pi/2,0,-3*pi/4) ancilla[0];
u(0,0,pi/4) out_reg[2];
cx out_reg[1],out_reg[2];
u(0,0,pi/4) out_reg[1];
u(0,0,-pi/4) out_reg[2];
cx out_reg[1],out_reg[2];
u(pi/2,pi/4,-pi) out_reg[1];
cx out_reg[0],out_reg[1];
u(0,0,-pi/4) out_reg[1];
u(pi/2,0,pi) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,0,-pi/4) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,1.406583,-0.62118481) out_reg[2];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,0,3*pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(pi/2,pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,-pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[0],out_reg[2];
u(0,0,pi/4) out_reg[2];
cx left_aux_reg[0],out_reg[2];
u(0,1.406583,-2.1919811) out_reg[2];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,pi/4,3*pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(pi/2,pi/4,-pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,0,3*pi/4) left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[3];
cx left_aux_reg[3],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[3],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,-pi/16) left_aux_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,pi/16) left_aux_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[2],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.2102334) out_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(0,1.406583,-1.6029325) out_reg[2];
u(pi,0,pi) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/16) left_aux_reg[1];
cx left_aux_reg[1],out_reg[2];
u(0,0,-pi/16) out_reg[2];
cx left_aux_reg[1],out_reg[2];
u(pi/2,0,-15*pi/16) out_reg[2];
u(pi,0,pi) left_aux_reg[1];
u(pi/2,pi/4,-pi) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(pi/2,pi/4,-3*pi/4) left_aux_reg[2];
u(0,0,pi/8) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[1];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(pi/2,pi/4,-3*pi/4) left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[2];
u(0,0,pi/16) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(pi/2,0,-3*pi/4) left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
cx left_aux_reg[1],left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[2];
u(pi/2,-pi,-0.82697089) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
u(pi/2,-pi,-0.82697089) left_aux_reg[3];
cx input_reg[2],left_aux_reg[3];
u(pi/2,0.82697089,0) left_aux_reg[3];
u(pi,0.59177511,-0.19362305) input_reg[2];
cx input_reg[3],left_aux_reg[2];
u(pi/2,0.82697089,0) left_aux_reg[2];
cx input_reg[2],left_aux_reg[2];
u(0,0,pi/4) left_aux_reg[2];
cx input_reg[2],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[2];
u(0,0,-pi/8) input_reg[2];
u(pi,0.59177511,-0.19362305) input_reg[3];
cx input_reg[3],left_aux_reg[1];
u(0,0,pi/4) left_aux_reg[1];
cx input_reg[3],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
cx input_reg[2],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
cx input_reg[2],left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
cx left_aux_reg[1],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[2];
u(0,0,-pi/16) input_reg[2];
u(0,0,-pi/8) input_reg[3];
cx input_reg[3],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx input_reg[3],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
cx input_reg[2],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
cx input_reg[2],left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[0];
cx left_aux_reg[0],left_aux_reg[3];
u(pi/2,0,pi) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,pi/4) left_aux_reg[0];
cx left_aux_reg[1],left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[0];
u(pi/2,0,pi) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,pi/8) left_aux_reg[0];
cx left_aux_reg[2],left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[0];
u(0,0,-pi/4) left_aux_reg[2];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,pi/4) left_aux_reg[1];
cx left_aux_reg[2],left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[1];
u(pi/2,0,pi) left_aux_reg[2];
u(0,0,-pi/16) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,pi/16) left_aux_reg[0];
cx left_aux_reg[3],left_aux_reg[0];
u(0,0,-pi/16) left_aux_reg[0];
u(0,0,-pi/8) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,pi/8) left_aux_reg[1];
cx left_aux_reg[3],left_aux_reg[1];
u(0,0,-pi/8) left_aux_reg[1];
u(0,0,-pi/4) left_aux_reg[3];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,pi/4) left_aux_reg[2];
cx left_aux_reg[3],left_aux_reg[2];
u(0,0,-pi/4) left_aux_reg[2];
u(pi/2,0,pi) left_aux_reg[3];
cx input_reg[4],out_reg[2];
cx input_reg[2],out_reg[2];
u(pi,0,pi) out_reg[2];
cx out_reg[2],out_reg[1];
u(0,0,pi/4) out_reg[1];
cx out_reg[0],out_reg[1];
u(pi/2,-7*pi/8,-pi) out_reg[0];
u(pi/2,0,3*pi/4) out_reg[1];
u(pi,0,pi) out_reg[2];
cx input_reg[2],out_reg[2];
cx input_reg[4],out_reg[2];
cx input_reg[5],left_aux_reg[0];
cx input_reg[6],left_aux_reg[1];
cx input_reg[7],left_aux_reg[2];
u(pi,pi/8,-pi) input_reg[7];
cx input_reg[7],input_reg[1];
u(0,0,-pi/8) input_reg[1];
cx input_reg[7],input_reg[1];
cx input_reg[1],input_reg[0];
u(0,0,-pi/8) input_reg[0];
cx input_reg[7],input_reg[0];
u(0,0,pi/8) input_reg[0];
cx input_reg[1],input_reg[0];
u(0,0,-pi/8) input_reg[0];
cx input_reg[7],input_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[1],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[7],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[1],out_reg[0];
u(0,0,pi/8) out_reg[0];
cx input_reg[0],out_reg[0];
u(0,0,-pi/8) out_reg[0];
cx input_reg[7],out_reg[0];
u(pi/2,0,pi) out_reg[0];
u(pi,0,pi) input_reg[7];
