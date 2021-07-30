clear
set memory 10m
set more off
use aerdata_colombia2

**RESTRICTIONS FOR THIS TABLE**
keep if checkid==1 & age>=9 & age<=25


******************  PANEL A *******************
*******Full Sample
**Column 1
sum read if read>0
*more
reg read vouch0 age sex_name if read>0, robust
*more
sum readcens1
more
reg readcens1 vouch0 age sex_name , robust
more
tobit readcens1 vouch0 age sex_name, ll
more
sum readcens10
more
tobit readcens10 vouch0 age sex_name, ll
more
*******Females
**Column 1
sum read if read>0 & sex_name==0
*more
reg read vouch0 age if read>0  & sex_name==0, robust
*more
sum readcens1 if sex_name==0
more
reg readcens1 vouch0 age if sex_name==0, robust
more
tobit readcens1 vouch0 age if sex_name==0, ll
more
sum readcens10  if sex_name==0
more
tobit readcens10 vouch0 age if sex_name==0, ll
more
*******Males
**Column 1
sum read if read>0 & sex_name==1
*more
reg read vouch0 age if read>0  & sex_name==1, robust
*more
sum readcens1 if sex_name==1
more
reg readcens1 vouch0 age if sex_name==1, robust
more
tobit readcens1 vouch0 age if sex_name==1, ll
more
sum readcens10  if sex_name==1
more
tobit readcens10 vouch0 age if sex_name==1, ll
more


******************  PANEL B *******************
*******Full Sample
**Column 1
sum math if math>0
*more
reg math vouch0 age sex_name if math>0, robust
*more
sum mathcens1
more
reg mathcens1 vouch0 age sex_name , robust
more
tobit mathcens1 vouch0 age sex_name, ll
more
sum mathcens10
more
tobit mathcens10 vouch0 age sex_name, ll
more
*******Females
set more on
**Column 1
sum math if math>0 & sex_name==0
*more
reg math vouch0 age if math>0  & sex_name==0, robust
*more
sum mathcens1 if sex_name==0
more
reg mathcens1 vouch0 age if sex_name==0, robust
more
tobit mathcens1 vouch0 age if sex_name==0, ll
more
sum mathcens10  if sex_name==0
more
tobit mathcens10 vouch0 age if sex_name==0, ll
more
*******Males
**Column 1
sum math if math>0 & sex_name==1
*more
reg math vouch0 age if math>0  & sex_name==1, robust
*more
sum mathcens1 if sex_name==1
more
reg mathcens1 vouch0 age if sex_name==1, robust
more

tobit mathcens1 vouch0 age if sex_name==1, ll
more
sum mathcens10  if sex_name==1
more
tobit mathcens10 vouch0 age if sex_name==1, ll
more


