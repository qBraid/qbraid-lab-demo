OPENQASM 3.0;
include "stdgates.inc";

def oracle(qubit[3] q, qubit[1] ancilla) {
    int[32] s = 7;
    int[16] n = 3;
    for int i in [0:n - 1] {
        if ((s >> i) & 1) {
            cx q[i], ancilla[0];
        }
    }
}
