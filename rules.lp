% --- Default contradiction rule ---
contradiction(S, A) :-
    judgment(S, A, allow, _),
    judgment(S, A, forbid, _),
    not justified(S, A).

% --- Context facts and justification rules ---
% Example: context(1, protect_life).
%          context(1, truth).

justified(S, A) :-
    context(S, protect_life),
    A = lying.

% --- Priorities ---
priority(protect_life, 10).
priority(truth, 5).

overrides(R1, R2) :-
    priority(R1, P1),
    priority(R2, P2),
    P1 > P2.

% --- Contradiction only if not overridden ---
contradiction(S, A) :-
    judgment(S, A, allow, R1),
    judgment(S, A, forbid, R2),
    not overrides(R1, R2),
    not justified(S, A).

% --- Explanation system ---
explain(S, A, conflict) :- contradiction(S, A).
