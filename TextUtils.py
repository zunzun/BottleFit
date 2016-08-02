import os, sys
import scipy

import pyeq3


def DataArrayStatistics(inArray):
    returnString = '' # build this as we progress
    
    # must at least have max and min
    minData = min(inArray)
    maxData = max(inArray)
    
    if maxData == minData:
        returnString += 'All data has the same value,\n'
        returnString += "value = %-.16E\n" % (minData)
        returnString += 'statistics cannot be calculated.'
    else:
        returnString += "max = %-.16E\n" % (maxData)
        returnString += "min = %-.16E\n" % (minData)
        
        try:
            temp = scipy.mean(inArray)
            returnString += "mean = %-.16E\n" % (temp)
        except:
            returnString += "mean gave error in calculation\n"

        try:
            temp = scipy.stats.sem(inArray)
            returnString += "standard error of mean = %-.16E\n" % (temp)
        except:
            returnString += "standard error of mean gave error in calculation\n"

        try:
            temp = scipy.median(inArray)
            returnString += "median = %-.16E\n" % (temp)
        except:
            returnString += "median gave error in calculation\n"

        try:
            temp = scipy.var(inArray)
            returnString += "variance = %-.16E\n" % (temp)
        except:
            returnString += "variance gave error in calculation\n"

        try:
            temp = scipy.std(inArray)
            returnString += "std. deviation = %-.16E\n" % (temp)
        except:
            returnString += "std. deviation gave error in calculation\n"

        try:
            temp = scipy.stats.skew(inArray)
            returnString += "skew = %-.16E\n" % (temp)
        except:
            returnString += "skew gave error in calculation\n"

        try:
            temp = scipy.stats.kurtosis(inArray)
            returnString += "kurtosis = %-.16E\n" % (temp)
        except:
            returnString += "kurtosis gave error in calculation\n"
    
    return returnString


def SaveCoefficientAndFitStatistics(in_filePathFitStatistics, in_equation):
    
    outputFile = open(in_filePathFitStatistics, 'w')
    
    if in_equation.upperCoefficientBounds or in_equation.lowerCoefficientBounds:
        outputFile.write('This model has coefficient bounds. Parameter statistics may\n')
        outputFile.write('not be valid for parameter values at or near the bounds.\n')
        outputFile.write('\n')
    
    outputFile.write('Degress of freedom error ' + str(in_equation.df_e) + '\n')
    outputFile.write('Degress of freedom regression ' + str(in_equation.df_r) + '\n')
    
    if in_equation.rmse == None:
        outputFile.write('Root Mean Squared Error (RMSE): n/a\n')
    else:
        outputFile.write('Root Mean Squared Error (RMSE): ' + str(in_equation.rmse) + '\n')
    
    if in_equation.r2 == None:
        outputFile.write('R-squared: n/a\n')
    else:
        outputFile.write('R-squared: ' + str(in_equation.r2) + '\n')
    
    if in_equation.r2adj == None:
        outputFile.write('R-squared adjusted: n/a\n')
    else:
        outputFile.write('R-squared adjusted: ' + str(in_equation.r2adj) + '\n')
    
    if in_equation.Fstat == None:
        outputFile.write('Model F-statistic: n/a\n')
    else:
        outputFile.write('Model F-statistic: ' + str(in_equation.Fstat) + '\n')
    
    if in_equation.Fpv == None:
        outputFile.write('Model F-statistic p-value: n/a\n')
    else:
        outputFile.write('Model F-statistic p-value: ' + str(in_equation.Fpv) + '\n')
    
    if in_equation.ll == None:
        outputFile.write('Model log-likelihood: n/a\n')
    else:
        outputFile.write('Model log-likelihood: ' + str(in_equation.ll) + '\n')
    
    if in_equation.aic == None:
        outputFile.write('Model AIC: n/a\n')
    else:
        outputFile.write('Model AIC: ' + str(in_equation.aic) + '\n')
    
    if in_equation.bic == None:
        outputFile.write('Model BIC: n/a\n')
    else:
        outputFile.write('Model BIC: ' + str(in_equation.bic) + '\n')
    
    outputFile.write('\n')
    outputFile.write("Individual Parameter Statistics:\n")
    for i in range(len(in_equation.solvedCoefficients)):
        if type(in_equation.tstat_beta) == type(None):
            tstat = 'n/a'
        else:
            tstat = '%-.5E' %  ( in_equation.tstat_beta[i])
    
        if type(in_equation.pstat_beta) == type(None):
            pstat = 'n/a'
        else:
            pstat = '%-.5E' %  ( in_equation.pstat_beta[i])
    
        if type(in_equation.sd_beta) != type(None):
            outputFile.write("Coefficient %s = %-.16E, std error: %-.5E\n" % (in_equation.GetCoefficientDesignators()[i], in_equation.solvedCoefficients[i], in_equation.sd_beta[i]))
        else:
            outputFile.write("Coefficient %s = %-.16E, std error: n/a\n" % (in_equation.GetCoefficientDesignators()[i], in_equation.solvedCoefficients[i]))
        outputFile.write("          t-stat: %s, p-stat: %s, 95 percent confidence intervals: [%-.5E, %-.5E]\n" % (tstat,  pstat, in_equation.ci[i][0], in_equation.ci[i][1]))
        
    outputFile.write('\n')
    outputFile.write("Coefficient Covariance Matrix:\n")
    for i in  in_equation.cov_beta:
        outputFile.write(str(i) + '\n')
    
    # absolute error statistics
    outputFile.write('\n\n\n')
    outputFile.write('Absolute Error Statistics:\n')
    outputFile.write(DataArrayStatistics(in_equation.modelAbsoluteError))
    
    if in_equation.dataCache.DependentDataContainsZeroFlag == 1:
        outputFile.write('\n\n\n')
        outputFile.write('Percent Error Statistics cannot be calculated, as\ndependent data contains at least one value of exactly zero.\n')
    else:
        outputFile.write('\n\n\n')
        outputFile.write('Percent Error Statistics:\n')
        outputFile.write(DataArrayStatistics(in_equation.modelPercentError))
        
    outputFile.close()


def SaveSourceCode(in_sourceCodeFilePath,  in_equation):
    
    outputFile = open(in_sourceCodeFilePath, 'w')
        
    outputFile.write('<html><body>\n\n')
    
    try:
        outputFile.write('<b>C++</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeCPP(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>CSHARP</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeCSHARP(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>VBA</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeVBA(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>PYTHON</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodePYTHON(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>JAVA</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeJAVA(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>JAVASCRIPT</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeJAVASCRIPT(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>JULIA</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeJULIA(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>FORTRAN90</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeFORTRAN90(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>SCILAB</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeSCILAB(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    try:
        outputFile.write('<b>MATLAB</b><br><textarea rows="20" cols="85" wrap="OFF">')
        outputFile.write(pyeq3.outputSourceCodeService().GetOutputSourceCodeMATLAB(in_equation))
        outputFile.write('</textarea><br><br>\n\n')
    except:
        pass

    outputFile.write('</body></html>\n')
    
    outputFile.close()
