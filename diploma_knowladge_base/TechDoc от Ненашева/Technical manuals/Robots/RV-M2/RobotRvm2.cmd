55
4
Id	Signal	Description	-
-2	<-	Format Code	-
1	0	Nest robot and go to safe position	c:\cim\cell\nest\nestrvm2.rob	
0	0	5	9
0	0	0	9
2	0	Pick Part 1 from Passive Unit	c:\cim\cell\passive\1_sps_o.rob	
0	0	5	9
0	0	0	9
3	0	Pick Part 2 from Passive Unit	c:\cim\cell\passive\2_sps_o.rob	
0	0	5	9 
0	0	0	9
4	0	Place part 1 / 2 in Lathe	c:\cim\cell\latherob\1-2_sl_c.rob
0	0	9	-
0	0	0	-
5	0	Release part in lathe and move to Safe position	c:\cim\cell\latherob\1-2_ls_o.rob
0	0	9	-
0	0	9	-
6	0	Move from Safe position to Lathe (GO)	c:\cim\cell\latherob\1-2_sl_o.rob
0	0	5	9
0	0	0	0
7	0	Take part from Lathe to Safe position (GC)	c:\cim\cell\latherob\1-2_ls_c.rob
0	0	5	9
0	0	0	0
8	0	Place part 1 in Passive Unit	c:\cim\cell\passive\1_sps_c.rob	
0	0	5	9
0	0	0	0
9	0	Place part 2 in Passive Unit	c:\cim\cell\passive\2_sps_c.rob
0	0	5	9
0	0	0	0
10	0	Place part 1 / 2 in Miller	c:\cim\cell\millrob\1-2_sm_c.rob
0	0	9	-
0	0	0	-
11	0	Release in Miller and move to Safe position	c:\cim\cell\millrob\1-2_ms_o.rob
0	0	9	-
0	0	9	-
12	0	Move from Safe to Miller (GO)	c:\cim\cell\millrob\1-2_sm_o.rob
0	0	5	9
0	0	0	0
13	0	Take part from Miller to Safe position (GC)	c:\cim\cell\millrob\1-2_ms_c.rob
0	0	5	9
0	0	0	0
14	0	Place Part 1 in CMM (GC)	c:\cim\cell\cmm\1_scs_c.rob	
0	0	5	9
0	0	0	9
15	0	Take Part 1 from CMM to Safe position (GO)	c:\cim\cell\cmm\1_scs_o.rob	
0	0	5	9
0	0	0	9
16	0	Gripper Close (GC)	c:\cim\cell\Robaux\gc.rob	
0	0	5	9
0	0	0	9
17	0	Gripper Open (GO)	c:\cim\cell\Robaux\go.rob	
0	0	5	9
0	0	0	9
18	0	Lumin test	c:\cim\cell\Lumin1\Lumin.rob	
0	0	5	9
0	0	0	9

