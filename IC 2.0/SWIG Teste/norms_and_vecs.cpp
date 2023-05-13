#include "norms_and_vecs.h"

using namespace std;

vector<int> norm_square(int nmax, int alpha)
{
    vector<int> norms2;

    for (int i = 0; i <= nmax; i++)
    {
        for (int j = 0; j <= nmax; j++)
        {
            for (int k = 1; k <= nmax; k++)
            { // nz always greater than zero
                int n2 = pow(i, 2) + pow(j, 2) + pow(alpha * k, 2);
                if (!(find(norms2.begin(), norms2.end(), n2) != norms2.end()))
                {
                    norms2.push_back(n2);
                }
            }
        }
    }

    return norms2;
}

map<double, vector<vector<double>>> vector_n(int nmax, int alpha)
{
    map<double, vector<vector<double>>> vec_n;
    vector<int> norms2 = norm_square(nmax, alpha);

    for (int i = 0; i < norms2.size(); i++)
    {
        vec_n[sqrt(norms2[i])] = vector<vector<double>>();
        int nz_count{static_cast<int>(floor(sqrt(norms2[i])))};

        for (int z = 1; z <= nz_count; z++)
        {
            double nx2_plus_ny2 = norms2[i] - pow(z, 2);
            int nx2_ny2_count{static_cast<int>(floor(sqrt(nx2_plus_ny2)))};

            for (int y = 0; y <= nx2_ny2_count; y++)
            {
                int x{static_cast<int>(floor(sqrt(norms2[i] - pow(z, 2) - pow(y, 2))))};

                if (z % alpha == 0 && pow(x, 2) + pow(y, 2) + pow(z, 2) == norms2[i])
                {
                    vector<double> values;

                    double xdn{static_cast<double>(x) / sqrt(norms2[i])};
                    double ydn{static_cast<double>(y) / sqrt(norms2[i])};
                    double zdn{static_cast<double>(z) / sqrt(norms2[i])};

                    values.push_back(xdn);
                    values.push_back(ydn);
                    values.push_back(zdn);

                    vec_n[sqrt(norms2[i])].push_back(values);
                }
            }
        }
    }

    return vec_n;
}

vector<vector<int>> teste_lista_aninhada(int n){
    vector<vector<int>> lista_aninhada;
    for(int i = 0; i < n; i++){
        vector<int> lista_interna;
        for(int j = 0; j < n; j++){
            lista_interna.push_back(j);
        }
        lista_aninhada.push_back(lista_interna);
    }
    return lista_aninhada;
}