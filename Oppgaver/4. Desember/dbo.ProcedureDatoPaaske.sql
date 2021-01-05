USE [NPSTDB]
GO


DROP PROCEDURE [dbo].[ProcedureDatoPaaske]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





-- =============================================
-- Author:		Nissens hjelper
-- =============================================
CREATE PROCEDURE [dbo].[ProcedureDatoPaaske] @foerste_jan datetime
AS
BEGIN

	DECLARE @aar smallint,
			@paaskeaften datetime,
			@paaskeferie int,
			@maaltall int


	SELECT @aar = YEAR(DATEADD(day, 26 - DATEPART(isoww, @foerste_jan), @foerste_jan));
	EXECUTE @paaskeaften = [dbo].[FunctionPaaskeAften] @aar;
	SELECT @paaskeferie = DATEPART(ISOWK, @paaskeaften);
	SELECT @maaltall = CONVERT(INT, @paaskeaften);

	INSERT INTO [dbo].[DatoPaaske]
           ([PaaskeAften]
           ,[PaaskeFerieUke]
           ,[Aar]
           ,[MaalTall])
           
     	VALUES
           (@paaskeaften
           ,@paaskeferie
           ,@aar
           ,@maaltall)



END
GO


