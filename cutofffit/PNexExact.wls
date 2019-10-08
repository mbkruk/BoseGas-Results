#!/usr/bin/env wolframscript

$Output = Streams["stderr"];
$Urgent = Streams["stderr"];
$Messages = Streams["stderr"];

f1[x_, n_, ncut_, g_] := Sum[
	Exp[-g k^2 x] Product[
		If[j != k, 1/((1 - Exp[g (k^2 - j^2)])^2), 1],
		{j, 1, ncut}
	] (
		x + 1 + 2 Sum[
			If[l != k, 1/(1 - Exp[-g (k^2 - l^2)]), 0],
			{l, ncut}
		]
	),
	{k, ncut}
];

f2[n_, ncut_, g_] := (
	Product[
		1/((1 - Exp[-g j^2])^2),
		{j, ncut}
	] + Sum[
		Exp[-g k^2 n]/(1 - Exp[g k^2]) Product[
			If[j != k, 1/((1 - Exp[g (k^2 - j^2)])^2), 1],
			{j, ncut}
		] (n + 1 + 1/(1 - Exp[-g k^2]) + 2 Sum[
			If[l != k, 1/(1 - Exp[-g (k^2 - l^2)]), 0],
			{l, 1, ncut}
		]),
		{k, ncut}
	]
);

pexact[x_, n_, ncut_, g_] := f1[x, n, ncut, g]/f2[n, ncut, g];

If[Length[$ScriptCommandLine]!=3,
	Print["usage: PNexExact.wls <particle count> <beta>"];
	Exit[1];
];

prec = 64;
ncut = SetPrecision[50,prec];
n = SetPrecision[ToExpression[$ScriptCommandLine[[2]]],prec];
beta = SetPrecision[ToExpression[$ScriptCommandLine[[3]]],prec];(*0.03625*)

$Output = Streams["stdout"];

Module[{x,f,p},
	f = f2[n, ncut, beta];
	For[x=0,x<=n,x++,
		p = f1[SetPrecision[x,prec], n, ncut, beta]/f;
		Print[CForm[N[p]]];
	];
];
