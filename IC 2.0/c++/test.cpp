#include <healpix_cxx/healpix_base.h>
#include <healpix_cxx/healpix_map.h>
#include <healpix_cxx/healpix_map_fitsio.h>
#include <healpix_cxx/healpix_tables.h>
#include <healpix_cxx/datatypes.h>
#include <iostream>

int main()
{
    const int order = 8;
    const int nside = 1 << order;

    Healpix_Map<double> map(nside, Healpix_Ordering_Scheme::NEST);

    return 0;
}
