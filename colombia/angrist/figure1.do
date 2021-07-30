clear
cap log close
use aerdata_colombia2

gen random=invnorm(uniform())/100000000000

gen math2=math+random

centile math2 if math>0, c(1 10 20 30 40 50 60 70 80 90)
more
centile math2 if math>0, c(1)
gen math_p01=math
replace math_p01=$S_7 if math2<$S_7
centile math2 if math>0, c(10)
gen math_p10=math
replace math_p10=$S_7 if math2<$S_7
centile math2 if math>0, c(20)
gen math_p20=math
replace math_p20=$S_7 if math2<$S_7
centile math2 if math>0, c(30)
gen math_p30=math
replace math_p30=$S_7 if math2<$S_7
centile math2 if math>0, c(40)
gen math_p40=math
replace math_p40=$S_7 if math2<$S_7
centile math2 if math>0, c(50)
gen math_p50=math
replace math_p50=$S_7 if math2<$S_7
centile math2 if math>0, c(60)
gen math_p60=math
replace math_p60=$S_7 if math2<$S_7
centile math2 if math>0, c(70)
gen math_p70=math
replace math_p70=$S_7 if math2<$S_7
centile math2 if math>0, c(80)
gen math_p80=math
replace math_p80=$S_7 if math2<$S_7
centile math2 if math>0, c(90)
gen math_p90=math
replace math_p90=$S_7 if math2<$S_7

tobit math vouch0 age sex_name , ll(0)
gen b00=_b[vouch0]
gen low00=b00-2*_se[vouch0]
gen hi00=b00+2*_se[vouch0]
tobit math_p01 vouch0 age sex_name , ll
more
gen b01=_b[vouch0]
gen low01=b01-2*_se[vouch0]
gen hi01=b01+2*_se[vouch0]
tobit math_p10 vouch0 age sex_name , ll
more
gen b10=_b[vouch0]
gen low10=b10-2*_se[vouch0]
gen hi10=b10+2*_se[vouch0]
tobit math_p20 vouch0 age sex_name , ll
more
gen b20=_b[vouch0]
gen low20=b20-2*_se[vouch0]
gen hi20=b20+2*_se[vouch0]
tobit math_p30 vouch0 age sex_name , ll
more
gen b30=_b[vouch0]
gen low30=b30-2*_se[vouch0]
gen hi30=b30+2*_se[vouch0]
tobit math_p40 vouch0 age sex_name , ll
more
gen b40=_b[vouch0]
gen low40=b40-2*_se[vouch0]
gen hi40=b40+2*_se[vouch0]
tobit math_p50 vouch0 age sex_name , ll
more
gen b50=_b[vouch0]
gen low50=b50-2*_se[vouch0]
gen hi50=b50+2*_se[vouch0]
tobit math_p60 vouch0 age sex_name , ll
more
gen b60=_b[vouch0]
gen low60=b60-2*_se[vouch0]
gen hi60=b60+2*_se[vouch0]
tobit math_p70 vouch0 age sex_name , ll
more
gen b70=_b[vouch0]
gen low70=b70-2*_se[vouch0]
gen hi70=b70+2*_se[vouch0]
tobit math_p80 vouch0 age sex_name , ll
more
gen b80=_b[vouch0]
gen low80=b80-2*_se[vouch0]
gen hi80=b80+2*_se[vouch0]
tobit math_p90 vouch0 age sex_name , ll
more
gen b90=_b[vouch0]
gen low90=b90-2*_se[vouch0]
gen hi90=b90+2*_se[vouch0]

keep b00-hi90
drop if _n>1
gen ones=1
reshape j Percentile 00 01 10 20 30 40 50 60 70 80 90
reshape xij b low hi
reshape i ones
reshape long
drop ones
label var b "Tobit Coeff on Voucher"
set more on

scatter b hi low Percentile, ylabel(-1(1)12) xlabel(0(10)90) c(l l l) symbol(i i i) t1(" ") l1("Tobit Coefficients") clpattern(l _ -) legend(off)
more

clear
use aerdata_colombia2

gen random=invnorm(uniform())/100000000000

gen read2=read+random

centile read2 if read>0, c(1 10 20 30 40 50 60 70 80 90)
more
centile read2 if read>0, c(1)
gen read_p01=read
replace read_p01=$S_7 if read2<$S_7
centile read2 if read>0, c(10)
gen read_p10=read
replace read_p10=$S_7 if read2<$S_7
centile read2 if read>0, c(20)
gen read_p20=read
replace read_p20=$S_7 if read2<$S_7
centile read2 if read>0, c(30)
gen read_p30=read
replace read_p30=$S_7 if read2<$S_7
centile read2 if read>0, c(40)
gen read_p40=read
replace read_p40=$S_7 if read2<$S_7
centile read2 if read>0, c(50)
gen read_p50=read
replace read_p50=$S_7 if read2<$S_7
centile read2 if read>0, c(60)
gen read_p60=read
replace read_p60=$S_7 if read2<$S_7
centile read2 if read>0, c(70)
gen read_p70=read
replace read_p70=$S_7 if read2<$S_7
centile read2 if read>0, c(80)
gen read_p80=read
replace read_p80=$S_7 if read2<$S_7
centile read2 if read>0, c(90)
gen read_p90=read
replace read_p90=$S_7 if read2<$S_7

tobit read vouch0 age sex_name , ll(0)
gen b00=_b[vouch0]
gen low00=b00-2*_se[vouch0]
gen hi00=b00+2*_se[vouch0]
tobit read_p01 vouch0 age sex_name , ll
more
gen b01=_b[vouch0]
gen low01=b01-2*_se[vouch0]
gen hi01=b01+2*_se[vouch0]
tobit read_p10 vouch0 age sex_name , ll
more
gen b10=_b[vouch0]
gen low10=b10-2*_se[vouch0]
gen hi10=b10+2*_se[vouch0]
tobit read_p20 vouch0 age sex_name , ll
more
gen b20=_b[vouch0]
gen low20=b20-2*_se[vouch0]
gen hi20=b20+2*_se[vouch0]
tobit read_p30 vouch0 age sex_name , ll
more
gen b30=_b[vouch0]
gen low30=b30-2*_se[vouch0]
gen hi30=b30+2*_se[vouch0]
tobit read_p40 vouch0 age sex_name , ll
more
gen b40=_b[vouch0]
gen low40=b40-2*_se[vouch0]
gen hi40=b40+2*_se[vouch0]
tobit read_p50 vouch0 age sex_name , ll
more
gen b50=_b[vouch0]
gen low50=b50-2*_se[vouch0]
gen hi50=b50+2*_se[vouch0]
tobit read_p60 vouch0 age sex_name , ll
more
gen b60=_b[vouch0]
gen low60=b60-2*_se[vouch0]
gen hi60=b60+2*_se[vouch0]
tobit read_p70 vouch0 age sex_name , ll
more
gen b70=_b[vouch0]
gen low70=b70-2*_se[vouch0]
gen hi70=b70+2*_se[vouch0]
tobit read_p80 vouch0 age sex_name , ll
more
gen b80=_b[vouch0]
gen low80=b80-2*_se[vouch0]
gen hi80=b80+2*_se[vouch0]
tobit read_p90 vouch0 age sex_name , ll
more
gen b90=_b[vouch0]
gen low90=b90-2*_se[vouch0]
gen hi90=b90+2*_se[vouch0]


keep b00-hi90
drop if _n>1
gen ones=1
reshape j Percentile 00 01 10 20 30 40 50 60 70 80 90
reshape xij b hi low
reshape i ones
reshape long
drop ones
label var b "Tobit Coeff on Voucher"
set more on
scatter b hi low Percentile, ylabel(-1(1)12) xlabel(0(10)90) c(l l l) symbol(i i i) t1(" ") l1("Tobit Coefficients") clpattern(l _ -) legend(off)

more
