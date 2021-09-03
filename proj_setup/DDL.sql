--清空資料庫
USE master;
GO
DROP DATABASE IF EXISTS KIT_DB;
GO

--資料庫
-- with utf8 enabled( sql server 2019+)
CREATE DATABASE KIT_DB COLLATE Latin1_General_100_CS_AS_SC_UTF8;
GO

--切換使用中的資料庫
USE KIT_DB;
GO
-- fix jump number issue
ALTER DATABASE SCOPED CONFIGURATION SET IDENTITY_CACHE = OFF
GO

--建立tables
CREATE TABLE dbo.class
(
    class_id INT IDENTITY,
    class VARCHAR( 800) NOT NULL,
    subclass VARCHAR( 800),

    CONSTRAINT  PK_class PRIMARY KEY CLUSTERED ( class_id)
);

INSERT INTO dbo.class
    ( class)
VALUES
    ('no_group');

CREATE TABLE dbo.survey
(
    survey_id INT IDENTITY,
    age_type INT NOT NULL,
    survey_type INT NOT NULL,
    wave VARCHAR(10) NOT NULL,
    release INT NOT NULL DEFAULT 0,

    CONSTRAINT PK_survey PRIMARY KEY CLUSTERED ( survey_id)
);

CREATE TABLE dbo.problem
(
    problem_id INT IDENTITY,
    problem_name VARCHAR( 30) NOT NULL,
    topic VARCHAR( 1000) NOT NULL,
    class_id INT NOT NULL DEFAULT 1,

    CONSTRAINT PK_problem PRIMARY KEY CLUSTERED ( problem_id),
    CONSTRAINT FK_problem_class FOREIGN KEY ( class_id) REFERENCES dbo.class ( class_id)
);

CREATE TABLE dbo.account
(
    account_id INT IDENTITY,
    nickname VARCHAR( 800)
    account_name VARCHAR( 800) UNIQUE NOT NULL,
    email VARCHAR( 320) UNIQUE NOT NULL,
    password VARCHAR( 25) NOT NULL,
    auth INT NOT NULL DEFAULT 2,
    last_combo VARCHAR( 800) NOT NULL DEFAULT '__'

        CONSTRAINT PK_account PRIMARY KEY CLUSTERED ( account_id)
);

CREATE TABLE dbo.shop_cart
(
    account_id INT NOT NULL,
    survey_id INT NOT NULL,
    problem_id INT NOT NULL,

    CONSTRAINT PK_shop_cart PRIMARY KEY CLUSTERED ( account_id, survey_id, problem_id),
    CONSTRAINT FK_shop_cart_account FOREIGN KEY ( account_id) REFERENCES dbo.account ( account_id),
    CONSTRAINT FK_shop_cart_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
    CONSTRAINT FK_shop_cart_problem FOREIGN KEY ( problem_id) REFERENCES dbo.problem ( problem_id)
);

CREATE TABLE dbo.survey_class_auth
(
    account_id INT NOT NULL,
    survey_id INT NOT NULL,
    class_id INT NOT NULL,

    CONSTRAINT PK_survey_class_auth PRIMARY KEY CLUSTERED ( account_id, survey_id, class_id),
    CONSTRAINT FK_survey_class_auth_account FOREIGN KEY ( account_id) REFERENCES dbo.account ( account_id),
    CONSTRAINT FK_survey_class_auth_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
    CONSTRAINT FK_survey_class_auth_class FOREIGN KEY ( class_id) REFERENCES dbo.class ( class_id)
);

CREATE TABLE dbo.survey_problem
(
    survey_id INT NOT NULL,
    problem_id INT NOT NULL,
    release INT DEFAULT 0,

    CONSTRAINT PK_survey_problem PRIMARY KEY CLUSTERED ( survey_id, problem_id),
    CONSTRAINT FK_survey_problem_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
    CONSTRAINT FK_survey_problem_problem FOREIGN KEY ( problem_id) REFERENCES dbo.problem ( problem_id)
);

GO

USE master;
GO
