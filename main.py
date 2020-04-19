import re
import os
import openpyxl

class ParserLogs():

    def regExFinder(self, regex, test_str):
        grouplist = []
        matches = re.finditer(regex, test_str, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                grouplist.append(match.group(groupNum))
        return grouplist

    def readLogFile(self, logFileName, path):
        fullLog = ''
        with open(logFileName, "r") as f:
            fullLog = f.read()
        return fullLog

    def parseLogFile(self, logData):
        logDataMap = {}
        todaysDateRegEx = r"Today\s+is\s+(\d+-\d+-\d+)"
        intCreditCountRegEx = r"intCreditcount\s+:(\d+)"
        creditAmountRegEx =  r"Debit\s+Amount\s+:\S+\s+Credit\s+Amount\s+:(\S+)"
        totalHKD_SACRM_records_readRegEx = r"Total\s+HKD\s+SACRM\s+record\s+read\s+:\s+(\S+)"
        totalHKD_SACRM_records_writtenRegEx = r"Total\s+HKD\s+SACRM\s+record\s+written\s+:\s+(\S+)"
        totalHKD_SACRM_records_rejectedRegEx = r"Total\s+HKD\s+SACRM\s+record\s+rejected\s+:\s+(\S+)"

        todaysDate = pl.regExFinder(todaysDateRegEx, logData)
        logDataMap['todaysDate'] = todaysDate[0]

        intCreditCount = pl.regExFinder(intCreditCountRegEx, logData)
        logDataMap['intCreditCount'] = intCreditCount[0]

        creditAmount = pl.regExFinder(creditAmountRegEx, logData)
        logDataMap['creditAmount'] = creditAmount[0]

        totalHKD_SACRM_records_read = pl.regExFinder(totalHKD_SACRM_records_readRegEx, logData)
        logDataMap['totalHKD_SACRM_records_read'] = totalHKD_SACRM_records_read[0]

        totalHKD_SACRM_records_written = pl.regExFinder(totalHKD_SACRM_records_writtenRegEx, logData)
        logDataMap['totalHKD_SACRM_records_written'] = totalHKD_SACRM_records_written[0]

        totalHKD_SACRM_records_rejected = pl.regExFinder(totalHKD_SACRM_records_rejectedRegEx, logData)
        logDataMap['totalHKD_SACRM_records_rejected'] = totalHKD_SACRM_records_rejected[0]

        print(logDataMap)
        return logDataMap

    def parseExcelFile(self, excelFileName):
        excelDataMap = {}
        wb =  openpyxl.load_workbook(excelFileName, data_only=True)
        sheet = wb['Sheet2']

        excelDataMap['finacle'] = sheet["H4"].value
        excelDataMap['si_ta_mift'] = sheet["H5"].value
        excelDataMap['tas'] = sheet["H6"].value

        excelDataMap['finacleTotalAmt'] = sheet["I4"].value
        excelDataMap['si_ta_mift_TotalAmt'] = sheet["I5"].value
        excelDataMap['tas_TotalAmt'] = sheet["I6"].value

        print(excelDataMap)
        return excelDataMap

    def compareValues(self, logDataMap, excelDataMap):
        finalStatus = False
        if (logDataMap['creditAmount'] == excelDataMap['tas_TotalAmt']):
            print('credit and totalamount matched') 
            finalStatus = True
        if (logDataMap['totalHKD_SACRM_records_read'] == excelDataMap['si_ta_mift']):
            print('totalHKD_SACRM_records_read and si_ta_mift matched') 
            finalStatus = True        
        return finalStatus
            

pl = ParserLogs()
pwd = os.getcwd()
logData = pl.readLogFile("Merging_TO_HKICL_SACRM_26032020_ 4300098.log", pwd)
#print(logData)
logDataMap = pl.parseLogFile(logData)
excelDataMap = pl.parseExcelFile('outward_SACRM_12042020.xlsx')
status = pl.compareValues(logDataMap, excelDataMap)
if(status == True):
    print("all data is matched with expected values, invoke new job")
else:
    print("there is data mis-match with expected values")