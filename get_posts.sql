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
    Posts.Id,
    Posts.Handle, 
    Posts.Text,
    Dogs.Name,
    LikeCountQueryResult.LikeCount,
    DL.CurrentDogLike

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

INNER JOIN (SELECT Posts.Id AS Id, COUNT(L.Handle) AS CurrentDogLike FROM Posts
    LEFT JOIN (SELECT * FROM Likes WHERE Handle='melba') AS L 
        ON Posts.Id = L.PostId
    GROUP BY Posts.Id) AS DL
    ON Posts.Id = DL.Id


SELECT Posts.Id AS Id, COUNT(L.Handle) AS CurrentDogLike FROM Posts
    LEFT JOIN (SELECT * FROM Likes WHERE Handle='melba') AS L 
        ON Posts.Id = L.PostId
    GROUP BY Posts.Id


SELECT * FROM Posts

DELETE FROM Posts WHERE Id=15


SELECT * FROM Dogs

UPDATE Dogs SET AvatarImageName='fido.jpg'
WHERE Handle='fido'

UPDATE Dogs SET AvatarImageName='rover.PNG'
WHERE Handle='rover'

UPDATE Dogs SET AvatarImageName='melba.png'
WHERE Handle='melba'
UPDATE Dogs SET AvatarImageName='chucky.png'
WHERE Handle='chucky'
UPDATE Dogs SET AvatarImageName='rose.png'
WHERE Handle='rose'


UPDATE Dogs SET Email = 'paul@epi.school'


SELECT * FROM Likes


INSERT INTO Likes (Handle, PostId)
VALUES
('rover', 3),
('rover', 6)

SELECT COUNT(*) FROM Likes WHERE PostId = 3

SELECT * FROM Posts

INSERT INTO Comment (Handle, PostId, [Text])
VALUES
    ('chucky', 1, 'Can''t wait to see you when you get here!')
    ('rose', 1, 'You should have moved to Miami!')
    ('rover', 1, 'I''m so jealous, enjoy the sunshine!')
