def fv_calc(cv, r, t):
    r = r / 100
    factor = pow((1 + r), t)
    amt = cv * factor
    return round(amt)


def pv_calc(fv, r, t):
    r = r / 100
    factor = pow((1 + r), t)
    amt = (fv / factor)
    return round(amt)


def mly_fv_calc(cv, new_add, r, t,time_period):
    if time_period=='MLY':
        r = r / 1200
        t = t * 12
    elif time_period=='ANNUAL':
        r=r/100
        t=t
    elif time_period=='NIL':
        return fv_calc(cv,r,t)
    # print("mly",round((new_add* ((pow((1+r),t)-1))/r)))
    amt = (cv * pow((1 + r), t)) + (new_add * (pow((1 + r), t) - 1) / r)
    return round(amt)

def equivalent_monthly_rate(annual_rate):
    # Convert annual rate from percentage to decimal
    annual_rate_decimal = annual_rate / 100
    # Calculate equivalent monthly rate
    rm = (1 + annual_rate_decimal) ** (1/12) - 1
    # Convert back to percentage
    monthly_rate_percentage = rm * 100
    return (monthly_rate_percentage)

# Example usage


def pmt(pv, r, t):
    r = r / 100
    t=t*12
    factor = 1-pow((1 + r), (-t))
    amt = ((r*pv) / factor)
    return round(amt)

#print(round(fv_calc(150000,9,10)))
# print(round(pv_calc(89850078,7,9)))

#amt2 = mly_fv_calc(5000000, 50000, 7, 15,'MLY')

##print(round(fv_calc(18702547,3.5,35)))
print(equivalent_monthly_rate(9))