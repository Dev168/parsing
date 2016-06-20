CREATE TEMPORARY TABLE IF NOT EXISTS forks (SELECT h1.firstparticipant,
        h2.secondparticipant,
        h1.firstforward,
        h2.secondforward,
        h1.firstwin,
        h2.secondwin,
        h1.bookmaker                 AS bk1,
        h2.bookmaker                 AS bk2,
        h1.href as href1,
        h2.href as href2,
        ( h1.firstwin * h2.secondwin - h1.firstwin - h2.secondwin ) / (
        h1.firstwin + h2.secondwin ) AS merge_percent
 FROM   handicaps AS h1,
        handicaps AS h2
 WHERE  h1.firstparticipant = h2.firstparticipant
        AND h1.secondparticipant = h2.secondparticipant
        AND h1.bookmaker != h2.bookmaker
        AND h1.actual
        AND h2.actual
        AND ( h1.firstforward + h2.secondforward ) >= 0)
UNION
(SELECT h1.firstparticipant,
        h2.secondparticipant,
        h1.firstforward,
        h2.secondforward,
        h1.firstwin,
        h2.secondwin,
        h1.bookmaker                 AS bk1,
        h2.bookmaker                 AS bk2,
        h1.href,
        h2.href,
        ( h1.secondwin * h2.firstwin - h1.secondwin - h2.firstwin ) / (
        h1.secondwin + h2.firstwin ) AS merge_percent
 FROM   handicaps AS h1,
        handicaps AS h2
 WHERE  h1.firstparticipant = h2.firstparticipant
        AND h1.secondparticipant = h2.secondparticipant
        AND h1.bookmaker != h2.bookmaker
        AND h1.actual
        AND h2.actual
        AND ( h1.secondforward + h2.firstforward ) >= 0)



