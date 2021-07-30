clear
set memory 10m
set more on

use aerdata_colombia2
drop if phone==. | age==. | sex_name==.

**RESTRICTIONS FOR THIS TABLE**
keep if age>=9 & age<=25 & checkid==1



********VARIABLES FOR THIS TABLE
centile math if math>0, c(10)
gen mathp10a=$S_7
centile math if math>0, c(25)
gen mathp25a=$S_7
centile math if math>0, c(50)
gen mathp50a=$S_7
centile math if math>0, c(75)
gen mathp75a=$S_7
centile math if math>0, c(90)
gen mathp90a=$S_7
more

gen mathp10=math>mathp10a
replace mathp10=. if math==.
gen mathp25=math>mathp25a
replace mathp25=. if math==.
gen mathp50=math>mathp50a
replace mathp50=. if math==.
gen mathp75=math>mathp75a
replace mathp75=. if math==.
gen mathp90=math>mathp90a
replace mathp90=. if math==.


centile read if read>0, c(10)
gen readp10a=$S_7
centile read if read>0, c(25)
gen readp25a=$S_7
centile read if read>0, c(50)
gen readp50a=$S_7
centile read if read>0, c(75)
gen readp75a=$S_7
centile read if read>0, c(90)
gen readp90a=$S_7
more

gen readp10=read>readp10a
replace readp10=. if read==.
gen readp25=read>readp25a
replace readp25=. if read==.
gen readp50=read>readp50a
replace readp50=. if read==.
gen readp75=read>readp75a
replace readp75=. if read==.
gen readp90=read>readp90a
replace readp90=. if read==.


reg readp10 vouch0   , robust
more
reg readp25 vouch0   , robust
more
reg readp50 vouch0   , robust
more
reg readp75 vouch0   , robust
more
reg readp90 vouch0   , robust
more
reg readp10 vouch0 age sex_name , robust
more
reg readp25 vouch0 age sex_name , robust
more
reg readp50 vouch0 age sex_name , robust
more
reg readp75 vouch0 age sex_name , robust
more
reg readp90 vouch0 age sex_name , robust
more
 

dprobit readp10 vouch0 age sex_name , robust
more
dprobit readp25 vouch0 age sex_name , robust
more
dprobit readp50 vouch0 age sex_name , robust
more
dprobit readp75 vouch0 age sex_name , robust
more
dprobit readp90 vouch0 age sex_name , robust
more


**********MATH
reg mathp10 vouch0   , robust
more
reg mathp25 vouch0   , robust
more
reg mathp50 vouch0   , robust
more
reg mathp75 vouch0   , robust
more
reg mathp90 vouch0   , robust
more
reg mathp10 vouch0 age sex_name , robust
more
reg mathp25 vouch0 age sex_name , robust
more
reg mathp50 vouch0 age sex_name , robust
more
reg mathp75 vouch0 age sex_name , robust
more
reg mathp90 vouch0 age sex_name , robust
more
 

dprobit mathp10 vouch0 age sex_name , robust
more
dprobit mathp25 vouch0 age sex_name , robust
more
dprobit mathp50 vouch0 age sex_name , robust
more
dprobit mathp75 vouch0 age sex_name , robust
more
dprobit mathp90 vouch0 age sex_name , robust
more

