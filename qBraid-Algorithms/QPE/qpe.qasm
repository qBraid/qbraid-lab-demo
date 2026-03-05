OPENQASM 3.0;
include "stdgates.inc";
include "iqft.qasm";

gate custom_t q {
  z q;
}

gate CU a, b {
  ctrl @ custom_t a, b;
}
 

def qpe(qubit[4] q, qubit[1] psi) {
    int n = 4;
    for int i in [0:n-1] {
        h q[i];
    }
    for int j in [0:n-1] {
        int[16] k = 1 << j;
        for int m in [0:k-1] {
            CU q[j], psi[0];
        }
    }
    iqft(q);

}