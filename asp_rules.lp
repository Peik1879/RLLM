% Standardregel: Widerspruch, wenn für dasselbe Szenario und dieselbe Aktion sowohl obligatory als auch forbidden vorliegt
contradiction(S, A) :- judgment(S, obligatory, A, _), judgment(S, forbidden, A, _).

% Optional: Widerspruch, wenn permitted und forbidden für dieselbe Aktion
contradiction(S, A) :- judgment(S, permitted, A, _), judgment(S, forbidden, A, _).

% Optional: Widerspruch, wenn permitted und obligatory für dieselbe Aktion (kann je nach Definition auch als konsistent gelten)
% contradiction(S, A) :- judgment(S, permitted, A, _), judgment(S, obligatory, A, _).

% Ausgabe aller gefundenen Widersprüche
#show contradiction/2.
