clear
set memory 10m

use aerdata_colombia2

**RESTRICTIONS FOR THIS TABLE**
keep if checkid==1 & age>=9 & age<=25

******************  PANEL A *******************
**Row 1
sum match*
more
**Columns
reg match_i vouch0, robust
reg match_i vouch0 sex_name age, robust
more
reg match_ic vouch0, robust
reg match_ic vouch0 sex_name age, robust
more
reg match_i7 vouch0, robust
reg match_i7 vouch0 sex_name age, robust
more
reg match_ic7 vouch0, robust
reg match_ic7 vouch0 sex_name age, robust
more
******************  PANEL B *******************
**Row 1
sum match* if sex_name==0
more
**Columns
reg match_i vouch0 if sex_name==0, robust
reg match_i vouch0 age if sex_name==0, robust
more
reg match_ic vouch0 if sex_name==0, robust
reg match_ic vouch0 age if sex_name==0, robust
more
reg match_i7 vouch0 if sex_name==0, robust
reg match_i7 vouch0 age if sex_name==0, robust
more
reg match_ic7 vouch0 if sex_name==0, robust
reg match_ic7 vouch0 age if sex_name==0, robust
more
******************  PANEL C *******************
**Row 1
sum match* if sex_name==1
more
**Columns
reg match_i vouch0 if sex_name==1, robust
reg match_i vouch0 age if sex_name==1, robust
more
reg match_ic vouch0 if sex_name==1, robust
reg match_ic vouch0 age if sex_name==1, robust
more
reg match_i7 vouch0 if sex_name==1, robust
reg match_i7 vouch0 age if sex_name==1, robust
more
reg match_ic7 vouch0 if sex_name==1, robust
reg match_ic7 vouch0 age if sex_name==1, robust
more


