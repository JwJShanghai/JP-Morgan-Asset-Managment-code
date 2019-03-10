# install.packages("riskParityPortfolio")
library(riskParityPortfolio)

# read in the data
RealRet <- read.csv("F:\\大四下\\AWMC\\资产收益率\\real return 月度调仓实际收益率.csv")
ExpectedRet <- read.csv("F:\\大四下\\AWMC\\资产收益率\\monthly return 月度调仓预测用.csv")
RealRet <- as.matrix(RealRet[,2:16])
ExpectedRet <- as.matrix(ExpectedRet[,2:16])

# Risk Parity portfolio optimization, unconstrained
# RiskParity = function(Sub) #Sub是N行M列的数据，N个日期，M个资产的收益
# {
#   m = ncol(Sub)
#   Cov = matrix(cov(Sub, use = "na.or.complete"), m, m)
#   TotalTRC = function(x)
#   {
#     x = matrix(c(x, 1-sum(x)))
#     TRC = as.vector((Cov %*% x) * x)
#     return(sum(outer(TRC, TRC, "-")^2))
#   }
#   sol = optim(par = rep(1/m,m-1), TotalTRC)
#   w = c(sol$par, 1-sum(sol$par))
#   return(w)
# }

# Risk Parity portfolio optimization, constrained
RiskParity_constrained = function(Sub,upperbound,lowerbound) #Sub是N行M列的数据，N个日期，M个资产的收益
{
  m = ncol(Sub)
  Cov = matrix(cov(Sub, use = "na.or.complete"), m, m) #计算输入收益率的协方差矩阵
  result <- riskParityPortfolio::riskParityPortfolio(Sigma = Cov, w_lb=lowerbound, w_ub=upperbound)
  w <- result$w
  return(w)
}


weight <- c()
RP_annnual_return <- c()
for (i in 1:Nperiod)
{

  # input the asset return data of the ith year
  assetReturn <- ExpectedRet[i:(i+11),1:14]
  # calculate the optimal weight according to RP model
  opt_weight <- RiskParity_constrained(assetReturn,upperbound = 0.4,lowerbound = 0)
  weight <- rbind(weight, t(opt_weight))
  # multiply by real return to obtain the annual return of RP portfolio
  annual_return <- opt_weight * RealRet[i,1:14]
  temp <- sum(annual_return)
  annual_return <- as.vector(cbind(annual_return,temp))
  RP_annnual_return <- rbind(RP_annnual_return, (annual_return))
}

colnames(weight) <- colnames(ExpectedRet)[1:14]
colnames(RP_annnual_return) <- c(colnames(weight),"totalreturn")


write.csv(weight,"F:\\大四下\\AWMC\\风险平价\\RP_weight_monthly.csv")
write.csv(RP_annnual_return,"F:\\大四下\\AWMC\\风险平价\\RP_return_monthly.csv")


