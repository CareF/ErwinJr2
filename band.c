#include "band.h"
/* Zincblende structure band, compatiable with structure BAND */
typedef struct ZBBAND {
	UpdateFunc updateM;
	numpyint N;
	const double *xVc;
	double *m;
	const double *xEg;
	const double *xF;
	const double *xEp; 
	const double *xESO;
}ZBBand; 

/* Update effective mass of a Zincblende band semiconductor */
numpyint ZBupdateM(Band *mat, double Eq) {
	ZBBand *zbmat = (ZBBand *) mat;
	int q; 
	for(q=0; q<zbmat->N; q++) {
		zbmat->m[q] = 1 / (1 + 2*zbmat->xF[q] + zbmat->xEp[q]/3 * 
				( 2 / (Eq - zbmat->xVc[q] + zbmat->xEg[q]) + 
				  1 / (Eq - zbmat->xVc[q] + zbmat->xEg[q] + zbmat->xESO[q]) 
				));
	}
	return zbmat->N;
}

Band *ZBband_new(numpyint N, const double *xEg, const double *xVc, 
		const double *xF, const double *xEp, const double *xESO) {
	ZBBand *zbband = (ZBBand *) malloc( sizeof(ZBBand) );
	zbband->updateM = ZBupdateM;
	zbband->N = N; 
	zbband->xEg = xEg; 
	zbband->xVc = xVc; 
	zbband->xF = xF; 
	zbband->xEp = xEp; 
	zbband->xESO = xESO;
	zbband->m = (double *)malloc( N*sizeof(double) );
	return (Band *) zbband; 
}

void ZBband_free(Band *zbband) {
	free( ((ZBBand *) zbband)->m );
	free( (ZBBand *) zbband );
	return;
}

