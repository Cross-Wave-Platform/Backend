-- change to database
USE KIT_DB;
GO

-- drop user if exists
DROP USER IF EXISTS test;
GO

-- create login
USE master;
GO

-- renew login
IF EXISTS ( SELECT name FROM sys.server_principals WHERE name = 'test')
BEGIN
    DROP LOGIN test;
END
GO

CREATE LOGIN test WITH PASSWORD = 'ASDASDzxc123';
USE KIT_DB;
GO

--create restrictive user
CREATE USER test FOR LOGIN test;
GO

-- grant permission to view tables
GRANT SELECT ON dbo.survey TO test;
GRANT SELECT ON dbo.problems TO test;
GRANT SELECT ON dbo.survey_problems TO test;
GRANT SELECT ON dbo.answers TO test;
GO

