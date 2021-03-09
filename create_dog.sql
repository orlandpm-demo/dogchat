CREATE TABLE [dbo].[Dogs](
	[Handle] [varchar](50) NULL,
	[Name] [varchar](50) NULL,
	[Bio] [text] NULL,
	[Age] [int] NULL
)

ALTER TABLE [dbo].[Dogs]
ADD [PasswordHash] [varchar](100)

ALTER TABLE [dbo].[Dogs]
ADD [AvatarImageName] [varchar](50)


ALTER TABLE [dbo].[Dogs]
ADD [Email] [varchar](50)
