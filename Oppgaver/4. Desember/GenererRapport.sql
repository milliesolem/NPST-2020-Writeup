DECLARE @year smallint = 2020;
DECLARE @fj datetime = CAST(cast(@year as varchar) + '0101' as datetime)

WHILE @year <= 2040
BEGIN 
	EXEC [dbo].[ProcedureDatoPaaske] @foerste_jan = @fj
	SET @year = @year + 1
	SET @fj = CAST(cast(@year as varchar) + '0101' as datetime);
END;

