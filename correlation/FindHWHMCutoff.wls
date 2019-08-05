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


nmax = ToExpression[$ScriptCommandLine[[2]]];

precision = 1024
n = SetPrecision[100,precision];
ncut = SetPrecision[30,precision];
nmax = SetPrecision[nmax,precision];
mt = {0,0.4,0.64,0.9};
m[nn_]:=If[nn<=Length[mt],mt[[nn]],1];
beta = SetPrecision[m[nmax]0.58/nmax^2,precision];(* nmax=3 => *0.64, nmax=2 => *0.4 *)
lnbeta = Log[beta]
lnbeps = SetPrecision[0.0001,precision];
xeps = SetPrecision[10^(-6),precision];
lnbeta0 = lnbeta

calcCoeffs[n_,beta_]:=Table[((dZdE[q, n, ncut] /. {\[Beta] -> 1, energy[arg_] -> ebeta (arg)^2})/.{ebeta->beta})/f2[0,n,ncut,beta]/n,{q,0,ncut}];

cce[coeffs_,deltax_]:=Sum[coeffs[[q+1]]Cos[2 Pi q deltax],{q,0,ncut}];
cced[coeffs_,deltax_]:=Sum[(-2 Pi q)coeffs[[q+1]]Sin[2 Pi q deltax],{q,0,ncut}];

x = SetPrecision[0.5/(nmax+1),precision];
y = SetPrecision[0.5/(nmax+1),precision];

widthDiff[lnb_]:=Module[{beta,i,dx,dy,coeffs},
	beta = Exp[lnb];
	coeffs = calcCoeffs[n,beta];
	dx = 1;
	While[Abs[dx]>xeps,
		dy = cced[coeffs,x];
		dx = (cce[coeffs,x] - SetPrecision[0.5,precision])/dy;
		x -= dx;
	];
	dy = 1;
	While[Abs[dy]>xeps,
		dx = correlationClassD[y,n,nmax,beta];
		dy = (correlationClass[y,n,nmax,beta] - SetPrecision[0.5,precision])/dx;
		y -= dy;
	];
	x-y
];
d1 = 1;
While[Abs[d1]>=xeps,
	d0 = widthDiff[lnbeta-lnbeps];
	d1 = widthDiff[lnbeta];
	d2 = widthDiff[lnbeta+lnbeps];
	plb = N[Exp[lnbeta]];
	delta = -2 lnbeps d1/(d2-d0);
	delta = delta/(1+Abs[delta]/0.1);
	lnbeta += delta;
];

beta = N[Exp[lnbeta]]

Print["nmax = ",N[nmax]];
Print["diff = ",N[d1]];
Print["beta = ",beta];
Print["nmax' = ",Sqrt[0.58/beta]]
Print["b/b = ",beta/(0.58/nmax^2)];
