SELECT CONCAT(p1.Name, " - ", p2.Name) as event,
CONCAT("handicap ", p1.Name, " ", forks.firstforward) as event_1,
CONCAT("handicap ", p2.Name, " ", forks.secondforward) as event_2,
forks.firstwin as coeff_1,
forks.secondwin as coeff_2,
forks.merge_percent * 100 as marge_percent,
forks.href1 as href_1,
forks.href2 as href_2,
b1.name as bookmaker1,
b2.name as bookmaker2
FROM forks LEFT JOIN participants as p1 ON forks.firstparticipant = p1.id
					LEFT JOIN participants as p2 ON forks.secondparticipant = p2.id
                    LEFT JOIN bookmakers as b1 ON forks.bk1 = b1.id
                    LEFT JOIN bookmakers as b2 ON forks.bk2 = b2.id
ORDER BY marge_percent DESC;
