--清空資料庫
USE master;
GO
DROP DATABASE IF EXISTS big_DB;
GO

--資料庫
CREATE DATABASE big_DB;
GO

--切換使用中的資料庫
USE big_DB;
GO

--建立tables
CREATE TABLE dbo.survey
(
survey_id   INT     NOT NULL,
age_type    INT     NOT NULL,
survey_type INT     NOT NULL,
year        INT     NOT NULL,
wave        INT     NOT NULL,

CONSTRAINT PK_survey_survey_id PRIMARY KEY CLUSTERED ( survey_id)
);

CREATE TABLE dbo.survey_problem
(
survey_id   INT             NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,

CONSTRAINT PK_survey_problem_survey_id_problem_id PRIMARY KEY CLUSTERED ( survey_id, problem_id)
);

CREATE TABLE dbo.answer
(
answer_id   BIGINT          NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,
survey_id   INT             NOT NULL,
answer      NVARCHAR( 4000),

CONSTRAINT PK_answer_answer_id_problem_id PRIMARY KEY CLUSTERED ( answer_id, problem_id)
);

CREATE TABLE dbo.problems
(
problem_id      VARCHAR( 30)    NOT NULL,
topic           NVARCHAR( 4000) NOT NULL,
class_id        INT             NOT NULL,
problem_type    NVARCHAR( 4000) NOT NULL,

CONSTRAINT PK_answer_answer_id_problem_id PRIMARY KEY CLUSTERED ( answer_id, problem_id)
);

CREATE TABLE dbo.tag_value
(
problem_id  VARCHAR( 30)    NOT NULL,
tag_value   INT,
tag_name    NVARCHAR( 4000) NOT NULL
);

CREATE TABLE dbo.account
(
user_id         INT             NOT NULL,
account_name    NVARCHAR( 4000) NOT NULL,
email           NVARCHAR( 4000) NOT NULL,
password        VARCHAR( 200)   NOT NULL,
auth            INT             NOT NULL
);

CREATE TABLE dbo.auth
(
class_id    INT             NOT NULL,
class       NVARCHAR( 4000) NOT NULL,
min_auth    INT             NOT NULL
);

CREATE TABLE dbo.auth_change_log
(
datetime    datetime        NOT NULL,
admin_id    INT             NOT NULL,
user_id     INT             NOT NULL,
old_auth    INT             NOT NULL,
new_auth    INT             NOT NULL,
reason      NVARCHAR( 4000) NOT NULL
);

GO

USE master;
GO
