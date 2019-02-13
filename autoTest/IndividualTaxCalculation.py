# coding:utf-8
def calculation(income=16000.0,specialDeduction=5000.0,additionalDeduction=1500.0,fiveRisksAndOneGoldBase=16000,bonusMonth=None,bonus=0.0):
    incomeTotal = 0
    specialDeductionTotal = 0
    additionalDeductionTotal = 0
    fiveRisksAndOneGoldTotal = 0
    taxTotal = 0
    currentTax = 0
    realIncomeToal = 0
    fiveRisksAndOneGold = (0.08+0.02+0.005+0.07)*fiveRisksAndOneGoldBase  # 养老8%,医疗2%，失业0.5%,公积金7%
    for i in range(1,13):
        incomeOld = incomeTotal
        if bonusMonth or bonus:
            if i == bonusMonth:
                incomeTotal = int(incomeTotal+income+bonus)
            else:
                incomeTotal += income
        else:
            incomeTotal += income
        specialDeductionTotal += specialDeduction
        additionalDeductionTotal += additionalDeduction
        fiveRisksAndOneGoldTotal += fiveRisksAndOneGold
        taxDeduction = (incomeTotal-specialDeductionTotal-additionalDeductionTotal-fiveRisksAndOneGoldTotal)
        if int(taxDeduction) in range(0,36000):
            currentTax = taxDeduction * 0.03 - 0 - taxTotal
            taxTotal += currentTax
            realIncome = incomeTotal-incomeOld - fiveRisksAndOneGold - currentTax
        elif int(taxDeduction) in range(36000,144000):
            currentTax = taxDeduction * 0.1 - 2520 - taxTotal
            taxTotal += currentTax
            realIncome = incomeTotal-incomeOld - fiveRisksAndOneGold - currentTax
        elif int(taxDeduction) in range(144000,300000):
            currentTax = taxDeduction * 0.2 - 16920 - taxTotal
            taxTotal += currentTax
            realIncome = incomeTotal-incomeOld - fiveRisksAndOneGold - currentTax
        else:
            realIncome = incomeTotal - incomeOld - fiveRisksAndOneGold
        realIncomeToal += realIncome
        print("第%s月工资收入%d：缴税%d,五险一金%.f,实发工资%d" % (i, incomeTotal-incomeOld, currentTax, fiveRisksAndOneGold, realIncome))
    print("工资总收入:%d,公积金总收入:%d,总收入:%d" % (realIncomeToal,fiveRisksAndOneGoldBase*0.07*12*2,realIncomeToal+income*0.07*12*2))
if __name__ == '__main__':
    calculation(bonusMonth=1,bonus=14595.42)
    # print("++++++")
    # calculation(income=5440,fiveRisksAndOneGoldBase=5000)