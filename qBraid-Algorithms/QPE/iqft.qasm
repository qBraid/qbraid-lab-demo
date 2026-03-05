OPENQASM 3.0;
include "stdgates.inc";

def iqft(qubit[3] q) {
    int n = 3;
  
    for int[16] i in [0:n-1] {
        int[16] target = n - i - 1;
        for int[16] j in [0:(n - target - 2)] {
            int[16] control = n - j - 1;
            int[16] k = control - target;
            cp(-2 * pi / (1 << (k + 1))) q[control], q[target];
        }
        h q[target];
    }

    for int[16] i in [0:(n >> 1) - 1] {
        swap q[i], q[n - i - 1];
    }
}