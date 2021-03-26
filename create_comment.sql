CREATE TABLE [dbo].[Comment](
	[Handle] [varchar](50) NOT NULL, --handle of dog that doing the commenting
	[PostId] [int] NOT NULL, --post that is being commented on
	[Text] [varchar](200) NOT NULL -- text of the comment
)