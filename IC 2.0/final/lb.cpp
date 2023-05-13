#include <iostream>
#include <cmath>

using namespace std;

double leibniz_series(int n) {
    double sum = 0;
    for (int i = 0; i < n; i++) {
        double term {pow(-1, i) / (2*i + 1)};
        sum += term;
    }
    return sum;
}

int main() {
    int n;
    cout << "Digite o número de termos da série: ";
    cin >> n;
    double result = leibniz_series(n);
    cout << "O resultado da série de Leibniz com " << n << " termos é: " << result << endl;
    return 0;
}
