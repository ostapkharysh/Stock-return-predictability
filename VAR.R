library("vars")
library("tidyr")
library("xts", quietly=TRUE, warn.conflicts=FALSE);
library("quantreg")
library("rugarch")

all = read.csv("//home/ostapkharysh/Documents/bt_data/DescriptiveFebruary29June05_2016/ET/AMZN/PR.csv", header=TRUE);
date = as.POSIXct(all[,idx]);
all.xts = xts(all[-idx], order.by = date);

all.xts = all[,c("tone", "polarity", "positive", "negative", "fin_return", "date")]
all.raw.clean = na.omit(all.xts);

all.raw = data.frame(coredata(all.raw.clean), ret.abs = abs(all.raw.clean[,5]));
names(all.raw)[6] <- "abs_return"

all.raw$fin_return[all.raw$fin_return> 0.08]=0.01
exp = data.frame()

r.garch.spec = ugarchspec(variance.model=list(model="fGARCH", submodel="APARCH",  garchOrder=c(1,1), external.regressors = cbind(all.raw$tone)) , 
                          mean.model = list(armaOrder=c(1,0), include.mean=TRUE ), distribution.model = "norm" )  

#r.garch = ugarchfit(r.garch.spec, all.raw$fin_return,  solver="solnp",  solver.control=list( maxeval=20, rseed=9876 ))
aptone = ugarchfit(r.garch.spec, all.raw$fin_return)

r.garch.spec = ugarchspec(variance.model=list(model="fGARCH", submodel="APARCH",  garchOrder=c(1,1)) , 
                          mean.model = list(armaOrder=c(1,0), include.mean=TRUE ), distribution.model = "norm" )  

#r.garch = ugarchfit(r.garch.spec, all.raw$fin_return,  solver="solnp",  solver.control=list( maxeval=20, rseed=9876 ))
ap = ugarchfit(r.garch.spec, all.raw$fin_return)


r.garch.spec = ugarchspec(variance.model=list(model="sGARCH", garchOrder=c(1,1)) , 
                          mean.model = list(armaOrder=c(1,0), include.mean=TRUE ), distribution.model = "norm" )  

#r.garch = ugarchfit(r.garch.spec, all.raw$fin_return,  solver="solnp",  solver.control=list( maxeval=20, rseed=9876 ))
ga = ugarchfit(r.garch.spec, all.raw$fin_return)


#Sys.setlocale(category = "LC_ALL", locale = "english")

exp.data = data.frame(all.raw.clean$date, c(sigma(aptone)), c(sigma(ap)), c(sigma(ga)))
temp10 = zoo(exp.data[,2], exp.data[,1])
temp11 = xts(exp.data[,-1], order.by = as.POSIXct(exp.data[,1]), locale = "english")


#pdf("hgh.pdf", width=10, height=6)
plot.xts(temp11, observation.based=TRUE,main = "Volatility")
#legend(x="topright", lty=1)
