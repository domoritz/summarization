% Generate
% { cl(F,A,S,V) : lit(T, A, S, V), formula(F) } = 2.

lit(L) :- lit(L,_,_,_,_).

{ use(F, L) : formula(F), lit(L) }.

% sat(t, f) :- lit(t, a, s, v).

#show use/2.
