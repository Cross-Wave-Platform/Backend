-- change to database
USE KIT_DB;
GO

-- drop user if exists
DROP USER IF EXISTS insert_account;
GO

-- create login
USE master;
GO

-- renew login
IF EXISTS ( SELECT name FROM sys.server_principals WHERE name = 'insert_account')
BEGIN
    DROP LOGIN insert_account;
END
GO

CREATE LOGIN insert_account WITH PASSWORD = 'ASDASDzxc123';
USE KIT_DB;
GO

--create restrictive user
CREATE USER insert_account FOR LOGIN insert_account;
GO

-- grant permission to view tables
GRANT INSERT ON dbo.account TO insert_account;
GO

