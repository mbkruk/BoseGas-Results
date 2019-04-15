#!/usr/bin/env wolframscript

On[Assert]

(*
	gaussian state
	|gauss|^2 has to integrate to 1
*)

gauss[x_, u_] := (Exp[-(x/u)^2/2]/Sqrt[Sqrt[Pi] u]);

Assert[Assuming[{l > 0}, Integrate[Abs[gauss[x,l]]^2, {x, -Infinity, Infinity}]]===1,"state not normalized"];

(* dipol-dipol interaction *)

dipolUnnormalized[u_] := (-2 u + Sqrt[2 Pi] (1 + u u) Exp[u^2/2] Erfc[u/Sqrt[2]]);
dipolNorm = 2*Integrate[dipolUnnormalized[x],{x,0,Infinity}];

dipol1[u_,l_] := dipolUnnormalized[Abs[u/l]]/l/dipolNorm;

Assert[Assuming[{l>0},Integrate[dipol1[x,l],{x,-Infinity,Infinity}]]===1,"dipol1 not normalized"];

(* energy *)

kineticFunc = (Conjugate[gauss[x,u]] (-D[ gauss[x,u], x, x]/(4 Pi^2)));

kineticEnergy1[nu_] := NIntegrate[ kineticFunc/. {x->nx,u->nu}, {nx, -Infinity, Infinity}, Method->"LocalAdaptive"];

interactionEnergy1[u_,l_] := NIntegrate[ Conjugate[gauss[x,u]] Conjugate[gauss[y,u]] dipol1[x-y,l] gauss[y,u] gauss[x,u], {x, -Infinity, Infinity}, {y, -Infinity, Infinity}, Method->"LocalAdaptive"];

(*
	parameters:
	n - particle count
	l - interaction range
	g - gamma
*)

n = ToExpression[$ScriptCommandLine[[2]]];
l = ToExpression[$ScriptCommandLine[[3]]]*1.6/Sqrt[2*Pi];
g = ToExpression[$ScriptCommandLine[[4]]];

(* energy in units of epsilon, length in units of trap length L *)

energy[lnu_] := (n kineticEnergy1[Exp[lnu]] + n (n-1) g interactionEnergy1[Exp[lnu],l]);

(* Netwon's method for finding energy'[u]==0 *)

u0 = 0.03;
h = 0.0001;
niter = 20;
eps = 0.0001

lnu = Log[u0];
e = energy[lnu];

lnumin = lnu;
emin = e;

Print[Exp[lnumin]," ",emin];

Module[{i,e0,e1,e2,lnv,f},For[i=1,i<=niter,i++,
	e0 = energy[lnu-h];
	e1 = e;
	e2 = energy[lnu+h];
	(*
		E' = (e2-e0)/h/2
		E'' = (e0+e2-2*e1)/h^2
		E'/E'' = h/2*(e2-e0)/(2*e1-e0-e2)
	*)
	m = (e0+e2-2*e1);
	(*
		lnv = lnu-h/2*(e2-e0)/m;
		lnv = lnu-h/2*(e2-e0)/(Sign[m]*Abs[m])
		go away from maxima(E''<0):
		lnv = lnu-h/2*(e2-e0)/(Abs[m])
		deal with near 0 m:
	*)
	lnv = lnu-h/2*(e2-e0)/(Sqrt[eps^2+m^2]);
	f = energy[lnv];
	If[f>emin,
		h = h/2;
		Print["retry ",h," ",f];
	,
		lnu = lnv;
		e = f;
		lnumin = lnu;
		emin = e;
		Print[Exp[lnumin]," ",emin];
	];
]];

Print[energy[lnumin*0.95]];
Print[energy[lnumin]];
Print[energy[lnumin*1.05]];

Print[Exp[lnumin]," ",emin];
