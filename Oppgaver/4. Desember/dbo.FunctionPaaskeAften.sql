USE [NPSTDB]
GO


DROP FUNCTION [dbo].[FunctionPaaskeAften]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



-- =============================================
-- Author:		Nissens hjelper
-- =============================================
CREATE FUNCTION [dbo].[FunctionPaaskeAften]
(
	@aar smallint
)
RETURNS date
AS
BEGIN
	DECLARE @a tinyint, @b tinyint, @c tinyint,
	@d tinyint, @e tinyint, @f tinyint,
        @g tinyint, @h tinyint, @i tinyint,
        @k tinyint, @l tinyint, @m tinyint,
	@year date, @month date, @easterday date,
	@paaskeaften date;

    --- Calculation steps:
	SELECT @a=@aar%19, @b=FLOOR(1.0*@aar/100), @c=@aar%100;
	SELECT @d=FLOOR(1.0*@b/4), @e=@b%4, @f=FLOOR((8.0+@b)/25);
	SELECT @g=FLOOR((1.0+@b-@f)/3);
	SELECT @h=(19*@a+@b-@d-@g+15)%30, @i=FLOOR(1.0*@c/4), @k=@aar%4;
	SELECT @l=(32.0+2*@e+2*@i-@h-@k)%7;
	SELECT @m=FLOOR((1.0*@a+11*@h+22*@l)/451);
	SELECT @year = DATEADD(yy, @aar-2000, '2000/01/01');
	SELECT @month = DATEADD(mm, FLOOR((1.0*@h+@l-7*@m+114)/31)-1, @year);
	SELECT @easterday = DATEADD(dd, (@h+@l-7*@m+114)%31, @month);
	SELECT @paaskeaften = CONVERT(DATETIME, @easterday) - 1;

	-- Return the result of the function
	RETURN @paaskeaften

END
GO


