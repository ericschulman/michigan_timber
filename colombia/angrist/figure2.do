clear
cap log close
use aerdata_colombia2



kdensity read if read>0, gen(x fx1) nograph
kdensity read if vouch0==0 & read>0, at(x) gen(x1 fx2) nograph
kdensity read if vouch0==1 & read>0, at(x) gen(x2 fx3) nograph
scatter fx2 fx3 x, xlabel(25(10)65) ylabel(0(.025).1) connect(l l) symbol(0 T)

more
drop x fx1 x1 x2 fx2 fx3
kdensity math if math>0, gen(x fx1) nograph
kdensity math if vouch0==0 & math>0, at(x) gen(x1 fx2) nograph
kdensity math if vouch0==1 & math>0, at(x) gen(x2 fx3) nograph
scatter fx2 fx3 x, xlabel(25(10)65) ylabel(0(.025).1) connect(l l) symbol(0 T)

more
drop x fx1 x1 x2 fx2 fx3


kdensity read if read>0, gen(x fx1) nograph
kdensity read if vouch0==0 & read>0, at(x) gen(x1 fx2) nograph

centile read if vouch0==1 & read>0, c(7.2)
gen read_winlow=$S_7
kdensity read if vouch0==1 & read>read_winlow, at(x) gen(x2 fx3) nograph
scatter fx2 fx3 x, xlabel(25(10)65) ylabel(0(.025).1) connect(l l) symbol(0 T)


more
drop x fx1 x1 x2 fx2 fx3


kdensity math if math>0, gen(x fx1) nograph
kdensity math if vouch0==0 & math>0, at(x) gen(x1 fx2) nograph
centile math if vouch0==1 & math>0, c(7.2)
gen math_winlow=$S_7
kdensity math if vouch0==1 & math>math_winlow, at(x) gen(x2 fx3) nograph
scatter fx2 fx3 x, xlabel(25(10)65) ylabel(0(.025).1) connect(l l) symbol(0 T)

