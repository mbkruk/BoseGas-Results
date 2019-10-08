#!/usr/bin/env wolframscript

$Output = Streams["stderr"];
$Urgent = Streams["stderr"];
$Messages = Streams["stderr"];

g1[x_, n_, nmax_, g_] := g^2 Sum[
	Exp[-g k^2 x] Product[
		If[
			j != k,
			1/((k^2 - j^2)^2),
			1
		],
		{j, nmax}
	] (x + 2/g Sum[
		If[
			l != k,
			1/(k^2 - l^2),
			0
		],
		{l, nmax}
	]),
	{k, nmax}
];

g2[n_, nmax_, g_] := 1/(nmax!)^4 - g Sum[
	Exp[-g k^2 n]/k^2 Product[
		If[
			j != k,
			1/((k^2 - j^2)^2),
			1
		],
		{j, nmax}
	] (n + 1/g (1/k^2 + 2 Sum[
		If[
			l != k,
			1/(k^2 - l^2),
			0
		],
		{l, nmax}
	])),
	{k, nmax}
];

pclass[x_, n_, nmax_, g_] := g1[x, n, nmax, g]/g2[n, nmax, g];

If[Length[$ScriptCommandLine]!=4,
	Print["usage: PNexCF.wls <particle count> <nmax> <beta>"];
	Exit[1];
];

prec = 64;
n = SetPrecision[ToExpression[$ScriptCommandLine[[2]]],prec];
nmax = SetPrecision[ToExpression[$ScriptCommandLine[[3]]],prec];
beta = SetPrecision[ToExpression[$ScriptCommandLine[[4]]],prec];(*0.03625*)

$Output = Streams["stdout"];

Module[{d,x,p},
	d = g2[n,nmax,beta];
	For[x=0,x<=n,x++,
		p = NIntegrate[g1[SetPrecision[t,prec],n,nmax,beta]/d, {t, SetPrecision[n x/(n + 1),prec], SetPrecision[n (x + 1)/(n + 1),prec]}];
		Print[CForm[N[p]]];
	];
];
