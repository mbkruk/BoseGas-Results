#!/usr/bin/env wolframscript

(*
	Usage: InteractionCoefficients.wls <interaction type> <interaction range> <nmax>

	<interaction type> -- gauss
	<interaction range> -- positive real number
	<nmax> -- mode index cutoff from bgmc and bgev simulations

	Compute 2*<nmax>+1 interaction coefficients for a given interaction type
	and range to be used with bgmc and bgev programs. Generated coefficients
	are also valid for simulations using lesser mode cutoff values.

	Available interactions:
		* gauss -- Gaussian function normalized to 1, range is standard deviation,
		* dipol -- normalized dipol-dipol interaction

	Example:
		InteractionCoefficients.wls gauss 0.1 1

	Possible output:
		0.9999999968218156
		0.8208687169065808
		0.45404075356382717
*)

On[Assert]

Switch[$ScriptCommandLine[[2]],
	"gauss",
		gauss1[x_, sig_] := (1/Sqrt[2 Pi]/sig Exp[-(x/sig)^2/2]);

		Assert[Assuming[{l>0},Integrate[gauss1[x,l],{x,-Infinity,Infinity}]]===1,"gauss1 not normalized"];

		gaussPeriodic[x_, relsig_] := Module[{nlim},
			nlim = Max[Round[5 relsig], 1];
			Sum[gauss1[x - n, relsig], {n, -nlim, nlim}]
		];
		funcPeriodic = gaussPeriodic;
	,"dipol",
		dipolUnnormalized[u_] := (-2 u + Sqrt[2 Pi] (1 + u u) Exp[u^2/2] Erfc[u/Sqrt[2]]);
		dipolNorm = 2*Integrate[dipolUnnormalized[x],{x,0,Infinity}];

		dipol1[u_,l_] := dipolUnnormalized[Abs[u/l]]/l/dipolNorm;

		Assert[Assuming[{l>0},Integrate[dipol1[x,l],{x,-Infinity,Infinity}]]===1,"dipol1 not normalized"];

(* old version used to relate gaussian and dipole width
		lpr[lsigarg_] := (1.6/Sqrt[2 Pi] lsigarg);

		dipolPeriodic[x_, relsig_] := Module[{nlim, rell},
			nlim = Max[Round[11 relsig], 1];
			rell = lpr[relsig];
			Sum[dipol1[x - n, rell], {n, -nlim, nlim}]
		];
*)

		dipolPeriodic[x_, relsig_] := Module[{nlim},
			nlim = Max[Round[18 relsig], 1];
			Sum[dipol1[x - n, relsig], {n, -nlim, nlim}]
		];

		funcPeriodic = dipolPeriodic;
	,_,
		Print["unknown interaction type `"<>$ScriptCommandLine[[2]]<>"`"];
		Exit[1];
];

sigma = ToExpression[$ScriptCommandLine[[3]]];
nmax = ToExpression[$ScriptCommandLine[[4]]];

Print["interaction_coefficients"];
For[n = 0, n <= 2*nmax, n++,
	Print[NIntegrate[ funcPeriodic[x-y,sigma] Cos[2 Pi (n x - n y)], {x, 0, 1}, {y, 0, 1}, Method -> "LocalAdaptive"]];
];
