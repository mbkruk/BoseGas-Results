#!/usr/bin/env wolframscript

f2[x_, n_, ncut_, g_] := 
  Product[1/((1 - Exp[-g j^2])^2), {j, ncut}] + 
   Sum[Exp[-g k^2 n]/(1 - Exp[g k^2]) Product[
      If[j != k, 1/((1 - Exp[g (k^2 - j^2)])^2), 1], {j, ncut}] (n + 
       1 + 1/(1 - Exp[-g k^2]) + 
       2 Sum[If[l != k, 1/(1 - Exp[-g (k^2 - l^2)]), 0], {l, 1, 
          ncut}]), {k, ncut}];

g2[x_, n_, nmax_, g_] := 
  1/(nmax!)^4 - 
   g Sum[Exp[-g k^2 n]/k^2 Product[
       If[j != k, 1/((k^2 - j^2)^2), 1], {j, nmax}] (n + 
        1/g (1/k^2 + 
           2 Sum[If[l != k, 1/(k^2 - l^2), 0], {l, nmax}])), {k, 
      nmax}];

dZdE[q_, n_, 
   ncut_] := -D[
    Exp[-\[Beta] energy[0] n] Product[
       1/((1 - Exp[-\[Beta] (energy[j] - energy[0])])^2), {j, ncut}] +
      Sum[Exp[-\[Beta] energy[k] n]/(1 - 
          Exp[\[Beta] (energy[k] - energy[0])]) Product[
        If[j != k, 1/((1 - Exp[\[Beta] (energy[k] - energy[j])])^2), 
         1], {j, ncut}] (n + 1 + 
         1/(1 - Exp[-\[Beta] (energy[k] - energy[0])]) + 
         2 Sum[If[l != k, 
            1/(1 - Exp[-\[Beta] (energy[k] - energy[l])]), 0], {l, 1, 
            ncut}]), {k, ncut}], energy[q]];

correlationExact[deltax_, n_, ncut_, g_] := 
  Sum[(dZdE[q, n, ncut] /. {\[Beta] -> 1, 
         energy[arg_] -> g (arg)^2}) Cos[2 Pi q deltax], {q, 0, 
      ncut}]/f2[asd, n, ncut, g]/n;

correlationExactD[deltax_, n_, ncut_, g_] := 
  Sum[-2 Pi q (dZdE[q, n, ncut] /. {\[Beta] -> 1, 
         energy[arg_] -> g (arg)^2}) Sin[2 Pi q deltax], {q, 0, 
      ncut}]/f2[asd, n, ncut, g]/n;

z[x_, n_, nmax_, g_] := 1/g^(2 nmax)*g2[x, n, nmax, g];
intZero[n_, nmax_, g_] := 
  1/g^(2 nmax)*
   Sum[Exp[-g  p^2 n] * 
     Product[If[k != p, 1/(p^2 - k^2)^2, 1], {k, 0, nmax}]*(n + 
       2/g*Sum[If[l != p, 1/(p^2 - l^2), 0], {l, 0, nmax}]), {p, 0, 
     nmax}];

int[q_, n_, nmax_, g_] := 
  1/g^(2 nmax)*
    Sum[If[p != q, 
      Exp[-g p^2 n] * 1/p^2 * 1/(p^2 - q^2) * 
       Product[If[k != p, 1/(p^2 - k^2)^2, 1], {k, 1, nmax}]*(n + 
         1/g*(1/(p^2 - q^2) + 1/p^2 + 
            2*Sum[If[l != p, 1/(p^2 - l^2), 0], {l, 1, nmax}])), 
      0], {p, 1, nmax}] + 
   1/g^(2 nmax + 1) * 1/q^2 * Product[1/k^4, {k, 1, nmax}] - 
   1/g^(2 nmax - 1) * Exp[-g q^2 n] * 1/q^2 * 
    Product[If[k != q, 1/(q^2 - k^2)^2, 1], {k, 1, nmax}]*(n^2/2 + 
      1/g*n/q^2 + 1/g^2 * 1/q^4 + 
      2/g*(n + 1/g*1/q^2)*
       Sum[If[l != q, 1/(q^2 - l^2), 0], {l, 1, nmax}] + 
      2/g^2*Sum[
        If[l != q && l' != q && l != l', 1/((q^2 - l^2)*(q^2 - l'^2)),
          0], {l, 1, nmax}, {l', 1, nmax}] + 
      3/g^2*Sum[If[l != q, 1/(q^2 - l^2)^2, 0], {l, 1, nmax}]);

correlationClass[x_, n_, nmax_, g_] := 
  1/z[asd, n, nmax, 
     g]*(intZero[n, nmax, g] + 
      2 Sum[Cos[2 Pi*q*x]*int[q, n, nmax, g], {q, 1, nmax}])/n;

correlationClassD[x_, n_, nmax_, g_] := 
  1/z[asd, n, nmax, 
     g]*(-2 Sum[
       2 Pi q Sin[2 Pi*q*x]*int[q, n, nmax, g], {q, 1, nmax}])/n;

n = SetPrecision[100, 30];
ncut = SetPrecision[50, 30];
nmax = SetPrecision[3, 30];
beta = SetPrecision[0.58/nmax^2, 30];
lnbeta = Log[beta]
lnbeps = SetPrecision[0.001, 30];

niter = 8;

widthDiff[lnb_]:=Module[{x,y,beta,i,dx,dy},
	beta = Exp[lnb];
	x = SetPrecision[0.05, 30];
	y = SetPrecision[0.05, 30];
	For[i = 1, i <= niter, i++,
		dx = (correlationExact[x,n,ncut,beta] - SetPrecision[0.5, 30])/correlationExactD[x,n,ncut,beta];
		dy = (correlationClass[y,n,nmax,beta] - SetPrecision[0.5, 30])/correlationClassD[y,n,nmax,beta];
		If[N[Abs[dx]+Abs[dy]]>0.05,Print["! ",i," ",N[dx]," ",N[dy]]];
		x -= dx;
		y -= dy;
	];
	x-y
];

For[j=1,j<=5,j++,
	d0 = widthDiff[lnbeta-lnbeps];
	d1 = widthDiff[lnbeta];
	d2 = widthDiff[lnbeta+lnbeps];
	Print[N[d0],"  ",N[d1],"  ",N[d2]];
	lnbeta -= 2 lnbeps d1/(d2-d0);
	Print["wd=",d1," beta=",Exp[lnbeta]];
];

Print["beta=",Exp[lnbeta]];
