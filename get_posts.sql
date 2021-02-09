-- SELECT * FROM Posts

-- INSERT INTO Posts ([Handle], [Text])
-- VALUES 
--     ('melba', 'I''m so excited to move to California!'),
--     ('melba', 'Great game of fetch today with my Dad, Paul'),
--     ('chucky', 'Took a great 8 hour nap today, then guarded the household'),
--     ('melba', 'Peanut butter is my favorite snack!'),
--     ('rose', 'Today I stole food from a blind dog.'),
--     ('chucky', 'I''m sleepy today.......')

-- SELECT Posts.Handle, Posts.Text, Dogs.Name FROM Posts
-- INNER JOIN Dogs
-- ON Posts.Handle = Dogs.Handle



-- SELECT * From Dogs
-- WHERE Handle = 'chucky'

-- SELECT * FROM Likes

-- INSERT INTO Likes ([Handle],[PostId])
-- VALUES
--     ('melba', 3),
--     ('rose', 3),
--     ('chucky',1),
--     ('rose',1),
--     ('melba', 6),
--     ('rose', 6),
--     ('chucky',6)

SELECT 
    Posts.Handle, 
    Posts.Text,
    Dogs.Name,
    LikeCountQueryResult.LikeCount

FROM Posts

INNER JOIN Dogs
        ON Posts.Handle = Dogs.Handle

INNER JOIN (SELECT 
        Posts.Id,
        -- Posts.Handle, 
        -- Posts.Text, 
        -- Dogs.Name,
        COUNT(Likes.Handle) AS LikeCount
    FROM Posts
    
    LEFT JOIN Likes
        ON Posts.Id = Likes.PostId
    GROUP BY Id) LikeCountQueryResult
        ON LikeCountQueryResult.Id = Posts.ID



SELECT * FROM Posts

DELETE FROM Posts WHERE Id=15


