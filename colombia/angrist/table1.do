clear
set memory 10m

use aerdata_colombia2

**Column 1
sum vouch0 checkid age sex_name phone
more
**Column 2
sum vouch0 checkid age sex_name phone if age>=9 & age<=25
more
**Column 3
reg checkid vouch0, robust
reg age vouch0, robust
reg sex_name vouch0, robust
reg phone vouch0, robust
**Column 4
reg checkid vouch0 if age>=9 & age<=25, robust
reg age vouch0 if age>=9 & age<=25, robust
reg sex_name vouch0 if age>=9 & age<=25, robust
reg phone vouch0 if age>=9 & age<=25, robust
**Column 5
reg age vouch0 if age>=9 & age<=25 & checkid==1, robust
reg sex_name vouch0 if age>=9 & age<=25 & checkid==1, robust
reg phone vouch0 if age>=9 & age<=25 & checkid==1, robust
**Column 6
reg age vouch0 if age>=9 & age<=25 & checkid==1 & phone==1, robust
reg sex_name vouch0 if age>=9 & age<=25 & checkid==1 & phone==1, robust

