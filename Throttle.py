def result(sat,Cp_in):
    Cp_out={200:118.87,210:120.28,220:121.98,230:123.94,240:126.13,250:128.54,260:131.15,270:133.95,280:96.22,290:98.31,
    300:100.54,310:102.86,320:105.25,330:107.68,340:110.13,350:112.61,360:115.1,370:117.59,380:120.09,390:122.57,400:125.04}
    H_in={}
    S_in={}
    H_outlet={}
    S_out={}
    #Calculation of entropy and enthalpy at various temperatures for inlet pressure.
    T=(sat[0]//10)*10
    H_in[T]=sat[1] + (((Cp_in[T]+sat[2])/2)*(T-sat[0]))
    S_in[T] =sat[3] + (((Cp_in[T]/(T)+(sat[2]/sat[0]))/2)*(T-sat[0]))
    T=T-10
    while T in Cp_out:
        H_in[T]= H_in[T+10]-(((Cp_in[T]+Cp_in[T+10])/2)*10)
        S_in[T]= S_in[T+10]-((((Cp_in[T]/T)+(Cp_in[T+10]/(T+10)))/2)*10)
        T=T-10
    T=((sat[0]//10)*10)+10
    H_in[T]=sat[4]+(((Cp_in[T]+sat[5])/2)*(T-sat[0]))
    S_in[T]=sat[6]+((((Cp_in[T]/T)+(sat[5]/sat[0]))/2)*(T-sat[0]))
    T=T+10
    while T in Cp_out:
        H_in[T]= H_in[T-10]+(((Cp_in[T]+Cp_in[T-10])/2)*10)
        S_in[T]=S_in[T-10]+((((Cp_in[T]/T)+(Cp_in[T-10]/(T-10)))/2)*10)
        T=T+10
    #Calculation of enthalpy at various temperature for outlet pressure
    H_outlet[270]=16770.1 - (((Cp_out[270]+134.73)/2)*(2.64))
    S_out[270]= 218.485 - (((Cp_out[270]/270)+(134.73/272.64))*1.32)
    T=260
    while T in Cp_out:
        H_outlet[T]=H_outlet[T+10]-(((Cp_out[T]+Cp_out[T+10])/2)*(10))
        S_out[T]=S_out[T+10]-(((Cp_out[T]/T)+(Cp_out[T+10]/(T+10)))*5)
        T=T-10
    H_outlet[280]=39202.7 +(((Cp_out[280]+94.82)/2)*(7.36))
    S_out[280]= 300.764 + (((Cp_out[280]/280)+(94.82/272.64))*3.68)
    T=290
    while T in Cp_out:
        H_outlet[T]=H_outlet[T-10]+(((Cp_out[T]+Cp_out[T-10])/2)*(10))
        S_out[T]=S_out[T-10]+(((Cp_out[T]/T)+(Cp_out[T-10]/(T-10)))*5)
        T=T+10
    #Calculation of outlet enthalpy.
    if T_in == sat[0]:
        x=float(input("Enter quality(x) for inlet stream:"))
        H_out=(x*sat[4])+((1-x)*sat[1])
    else:
        if T_in in H_in:
            H_out=H_in[T_in]
        elif T_in<((sat[0]//10)*10)+10 and T_in>sat[0]:
            H_out=sat[4]+(((H_in[((sat[0]//10)*10)+10]-sat[4])/(((sat[0]//10)*10)+10-sat[0]))*(T_in - sat[0]))
        elif T_in>(sat[0]//10)*10 and T_in<sat[0]:
            H_out=sat[1]-(((H_in[(sat[0]//10)*10]-sat[1])/(((sat[0]//10)*10)-sat[0]))*(T_in - sat[0]))
        else:
            T_1=(T_in//10)*10
            T_2=T_1+10
            H_out= H_in[T_1]-(((H_in[T_1]-H_in[T_2])/10)*(T_in - T_1))
    #Calculation of exit stream phase and temperature.
    for key in H_outlet:
        if H_outlet[key]==H_out:
            T_out= key
        elif key<400:
            if H_outlet[key]<H_out and H_out<H_outlet[key+10]:
                T_out=key+(((H_out-H_outlet[key])*10)/(H_outlet[key+10]-H_outlet[key]))
    if H_out>=39202.7:
        print("Phase of exit stream is superheated vapor.")
        print("Exit stream temperature(in K) is",T_out)
    elif H_out<=16770.1:
        print("Phase of exit stream is subcooled liquid.")
        print("Exit stream temperature(in K) is",T_out)
    else:
        print("Exit stream phase is liquid vapor coexistence.")
        print("Exit stream temperature(in K) is",272.64)
        x_out=(H_out-16770.1)/(39202.7-16770.1)
        print("Quality of exit stream is",x_out)
    #Calculation of output entropy for adiabatic reversible expansion.
    if T_in==sat[0]:
        S_2=(x*sat[6])+((1-x)*sat[3])
    else:
        if T_in in S_in:
            S_2=S_in[T_in]
        elif T_in<((sat[0]//10)*10)+10 and T_in>sat[0]:
            S_2=sat[6]+(((S_in[((sat[0]//10)*10)+10]-sat[6])/(((sat[0]//10)*10)+10-sat[0]))*(T_in - sat[0]))
        elif T_in>(sat[0]//10)*10 and T_in<sat[0]:
            S_2=sat[3]-(((S_in[(sat[0]//10)*10]-sat[3])/(((sat[0]//10)*10)-sat[0]))*(T_in - sat[0]))
        else:
            T_1=(T_in//10)*10
            T_2=T_1+10
            S_2= S_in[T_1] - (((S_in[T_1]-S_in[T_2])/10)*(T_in - T_1))
    #Calculation of outlet temperature for this process from output entropy
    for key in S_out:
        if S_out[key]==S_2:
            T_out=key
        elif key<400:
            if S_out[key]<S_2 and S_2<S_out[key+10]:
                T_out=key+(((S_2-S_out[key])*10)/(S_out[key+10]-S_out[key]))
    #Calculating outlet enthalpy for this process.
    if S_2>218.485 and S_2<300.764:
        x=(S_2-218.485)/(300.764-218.485)
        H_2_ad=(x*39202.7)+((1-x)*16770.1)
    else:
        if T_out in H_outlet:
            H_2_ad=H_outlet[T_out]
        elif T_out<280 and T_in>272.64:
            H_2_ad=39202.7+(((H_outlet[280]-39202.7)/7.36)*(T_out - 272.64))
        elif T_in>(sat[0]//10)*10 and T_in<sat[0]:
            H_2_ad=16770.1-(((H_outlet[270]-16770.1)/2.64)*(T_out - 272.64))
        else:
            T_1=(T_out//10)*10
            T_2=T_1+10
            H_2_ad= H_outlet[T_1]-(((H_outlet[T_1]-H_outlet[T_2])/10)*(T_out - T_1))
    #Calculating maximum work as differnce in inlet and outlet enthalpy for this process
    W=H_2_ad-H_out
    print("Maximum Work done(in J/mol) that can be obtained on adiabatic expansion is",W)
P_in=float(input("Enter inlet pressure(in MPa)-"))
T_in=float(input("Enter inlet Temperature(in K)-"))
#sat={T_sat,H_sat_liq,Cp_sat_liq,S_sat_liq,H_sat_vap,Cp_sat_vap,S_sat_vap}
if P_in ==1.4:
    Cp_in={200:118.76,210:120.15,220:121.83,230:123.75,240:125.91,250:128.28,260:130.84,270:133.59,280:136.52,290:139.63,
    300:142.95,310:146.49,320:150.29,330:154.41,340:158.95,350:164.06,360:170.09,370:148.90,380:142.82,390:140.36,400:139.56}
    sat=[368.76,31450.9,176.63,263.868,46891.0,150.15,305.738]
    result(sat,Cp_in)
else:
    Cp_in={200:118.74,210:120.13,220:121.8,230:123.73,240:125.88,250:128.24,260:130.8,270:133.53,280:136.45,290:139.55,
    300:142.85,310:146.37,320:150.14,330:154.21,340:158.69,350:163.71,360:169.56,370:176.87,380:153.78,390:147.2,400:144.38}
    sat=[375.611,32665.2,182.1,267.065,47338.3,159.3,306.130]
    result(sat,Cp_in)
