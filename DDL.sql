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

--建立tables
CREATE TABLE dbo.survey
(
survey_id   INT     NOT NULL,
age_type    INT     NOT NULL,
survey_type INT     NOT NULL,
year        INT     NOT NULL,
wave        INT     NOT NULL,

CONSTRAINT PK_survey PRIMARY KEY CLUSTERED ( survey_id)
);

CREATE TABLE dbo.auth
(
class_id    INT             NOT NULL,
class       VARCHAR( 4000) NOT NULL,
min_auth    INT             NOT NULL,

CONSTRAINT PK_auth PRIMARY KEY CLUSTERED ( class_id)
);

CREATE TABLE dbo.problems
(
problem_id      VARCHAR( 30)    NOT NULL,
topic           VARCHAR( 4000) NOT NULL,
class_id        INT             NOT NULL,
problem_type    VARCHAR( 4000) NOT NULL,

CONSTRAINT PK_problems PRIMARY KEY CLUSTERED ( problem_id),
CONSTRAINT FK_problems_class_id FOREIGN KEY ( class_id) REFERENCES dbo.auth ( class_id)
);

CREATE TABLE dbo.survey_problem
(
survey_id   INT             NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,

CONSTRAINT PK_survey_problem PRIMARY KEY CLUSTERED ( survey_id, problem_id),
CONSTRAINT FK_survey_problem_survey_id FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
CONSTRAINT FK_survey_problem_problem_id FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.answer
(
answer_id   BIGINT          NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,
survey_id   INT             NOT NULL,
answer      VARCHAR( 4000),

CONSTRAINT PK_answer PRIMARY KEY CLUSTERED ( answer_id, problem_id),
CONSTRAINT FK_answer_survey_id FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
CONSTRAINT FK_answer_problem_id FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.tag_value
(
problem_id  VARCHAR( 30)    NOT NULL,
tag_value   INT,
tag_name    VARCHAR( 4000) NOT NULL,

CONSTRAINT PK_tag_value PRIMARY KEY CLUSTERED ( problem_id),
CONSTRAINT FK_tag_value_problem_id FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.account
(
user_id         INT             NOT NULL,
account_name    VARCHAR( 4000) NOT NULL,
email           VARCHAR( 320) NOT NULL,
password        VARCHAR( 4000)   NOT NULL,
auth            INT             NOT NULL,

CONSTRAINT PK_account PRIMARY KEY CLUSTERED ( user_id)
);

CREATE TABLE dbo.auth_change_log
(
datetime    datetime        NOT NULL,
admin_id    INT             NOT NULL,
user_id     INT             NOT NULL,
old_auth    INT             NOT NULL,
new_auth    INT             NOT NULL,
reason      VARCHAR( 4000) NOT NULL,

CONSTRAINT PK_auth_change_log PRIMARY KEY CLUSTERED ( datetime),
CONSTRAINT FK_auth_change_log_admin_id FOREIGN KEY ( admin_id) REFERENCES dbo.account ( user_id),
CONSTRAINT FK_auth_change_log_user_id FOREIGN KEY ( user_id) REFERENCES dbo.account ( user_id)
);

GO

USE master;
GO
