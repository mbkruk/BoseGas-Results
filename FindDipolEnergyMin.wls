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

n = 100
l = 0.1*1.6/Sqrt[2*Pi]
g = -0.0821470168102332

(* energy in units of epsilon, length in units of trap length L *)

energy[u_] := (n kineticEnergy1[u] + n (n-1) g interactionEnergy1[u,l]);

(*umin = NMinimize[{energy[u],u>=0},{u}];
Print[umin];*)

uLowerBound = 0.01
u0 = 0.03;
ntest = 10;

umin = u0;
emin = energy[umin];

searchRadius = Table[0.25*0.95^n,{n,30}];

Module[{i,j,newmin},For[j=1,j<=Length[searchRadius],j++,
	Print["round ",j," sigma=",searchRadius[[j]]];
	utest = umin*Exp[RandomVariate[NormalDistribution[0,searchRadius[[j]]], ntest]];
	utest = Table[Max[utest[[i]],uLowerBound],{i,Length[utest]}];
	(*Print["u: ",utest];*)
	etest = energy[utest];
	(*Print["e: ",etest];*)
	newmin = False;
	For[i=1,i<=Length[utest],i++,
		If[etest[[i]]<emin,
			umin = utest[[i]];
			emin = etest[[i]];
			newmin = True;
		];
	];
	If[newmin,
		Print[umin," ",emin];
	];
]];
Print[umin," ",emin];
