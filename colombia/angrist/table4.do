clear
set memory 10m
set more on

use aerdata_colombia2

drop if phone==. | age==. | sex_name==.

**RESTRICTIONS FOR THIS TABLE**
keep if age>=9 & age<=25



********VARIABLES FOR THIS TABLE
centile math if vouch0==0, c(70)
gen mathpl70=$S_7
centile math if vouch0==0, c(75)
gen mathpl75=$S_7
more
centile math if vouch0==0, c(85)
gen mathpl85=$S_7
centile math if vouch0==0, c(95)
gen mathpl95=$S_7
more
centile math if vouch0==1, c(70)
gen mathpw70=$S_7
centile math if vouch0==1, c(75)
gen mathpw75=$S_7
centile math if vouch0==1, c(85)
gen mathpw85=$S_7
centile math if vouch0==1, c(95)
gen mathpw95=$S_7
more
centile read if vouch0==0, c(70)
gen readpl70=$S_7
centile read if vouch0==0, c(75)
gen readpl75=$S_7
more
centile read if vouch0==0, c(85)
gen readpl85=$S_7
centile read if vouch0==0, c(95)
gen readpl95=$S_7
more
centile read if vouch0==1, c(70)
gen readpw70=$S_7
centile read if vouch0==1, c(75)
gen readpw75=$S_7
centile read if vouch0==1, c(85)
gen readpw85=$S_7
centile read if vouch0==1, c(95)
gen readpw95=$S_7
more
***********PANEL A ****************
sum read if read>readpl70 & vouch0==0
sum read if read>readpl75 & vouch0==0
sum read if read>readpl85 & vouch0==0
sum read if read>readpl95 & vouch0==0
more

***** LOWER BOUND, NO COVARIATES
reg read vouch0 if read>readpl70, robust
more
reg read vouch0 if read>readpl75, robust
more
reg read vouch0 if read>readpl85, robust
more
reg read vouch0 if read>readpl95, robust
more
***** UPPER BOUND, NO COVARIATES
reg read vouch0 if (read>readpl70 & vouch0==0) | (read>readpw70 & vouch0==1), robust
more
reg read vouch0 if (read>readpl75 & vouch0==0) | (read>readpw75 & vouch0==1), robust
more
reg read vouch0 if (read>readpl85 & vouch0==0) | (read>readpw85 & vouch0==1), robust
more
set more on
reg read vouch0 if (read>readpl95 & vouch0==0) | (read>readpw95 & vouch0==1), robust
more
***** LOWER BOUND, COVARIATES
reg read vouch0 age sex_name if read>readpl70, robust
more
reg read vouch0 age sex_name if read>readpl75, robust
more
reg read vouch0 age sex_name if read>readpl85, robust
more
reg read vouch0 age sex_name if read>readpl95, robust
more
***** UPPER BOUND, COVARIATES
reg read vouch0 age sex_name if (read>readpl70 & vouch0==0) | (read>readpw70 & vouch0==1), robust
more
reg read vouch0 age sex_name if (read>readpl75 & vouch0==0) | (read>readpw75 & vouch0==1), robust
more
reg read vouch0 age sex_name if (read>readpl85 & vouch0==0) | (read>readpw85 & vouch0==1), robust
more
reg read vouch0 age sex_name if (read>readpl95 & vouch0==0) | (read>readpw95 & vouch0==1), robust
more



******************  PANEL B *******************
sum math if math>mathpl70 & vouch0==0
sum math if math>mathpl75 & vouch0==0
sum math if math>mathpl85 & vouch0==0
sum math if math>mathpl95 & vouch0==0
more
reg math vouch0 if math>mathpl70, robust
more
reg math vouch0 if math>mathpl75, robust
more
reg math vouch0 if math>mathpl85, robust
more
reg math vouch0 if math>mathpl95, robust
more
***** UPPER BOUND, NO COVARIATES
reg math vouch0 if (math>mathpl70 & vouch0==0) | (math>mathpw70 & vouch0==1), robust
more
reg math vouch0 if (math>mathpl75 & vouch0==0) | (math>mathpw75 & vouch0==1), robust
more
reg math vouch0 if (math>mathpl85 & vouch0==0) | (math>mathpw85 & vouch0==1), robust
more
reg math vouch0 if (math>mathpl95 & vouch0==0) | (math>mathpw95 & vouch0==1), robust
more
***** LOWER BOUND, COVARIATES
reg math vouch0 age sex_name if math>mathpl70, robust
more
reg math vouch0 age sex_name if math>mathpl75, robust
more
reg math vouch0 age sex_name if math>mathpl85, robust
more
reg math vouch0 age sex_name if math>mathpl95, robust
more
***** UPPER BOUND, COVARIATES
reg math vouch0 age sex_name if (math>mathpl70 & vouch0==0) | (math>mathpw70 & vouch0==1), robust
more
reg math vouch0 age sex_name if (math>mathpl75 & vouch0==0) | (math>mathpw75 & vouch0==1), robust
more
reg math vouch0 age sex_name if (math>mathpl85 & vouch0==0) | (math>mathpw85 & vouch0==1), robust
more
reg math vouch0 age sex_name if (math>mathpl95 & vouch0==0) | (math>mathpw95 & vouch0==1), robust
more

