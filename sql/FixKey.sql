if object_id('FixKey') is not null
    drop procedure FixKey
go

create procedure FixKey @Acc           varchar(20),
                        @InstitutionID DSIDENTIFIER
as 
    declare @RetVal int,
            @KeyPos int

    select  @KeyPos = 1,
            @RetVal = -1
    if len(@Acc) <> 20
        set @Acc = 'Косячный номер'
            
    if @Acc <> 'Косячный номер'       
    while @RetVal <> 0
		begin
			select @Acc = stuff(@Acc, 9, 1, convert(char(1), @KeyPos))
			exec @RetVal = CheckAccountKey
                            @InstitutionID = @InstitutionID,
                            @Account       = @Acc
			if @RetVal = 0
				begin
					break
				end
   
			if @KeyPos = 9
				begin
					set @Acc = 'Чет не получилось'
					break
				end

			select @KeyPos = @KeyPos + 1
		end 
	select @Acc 	
go

grant execute on FixKey to public	
go