
library(PlackettLuce)

print(getwd())
# Read the CSV file into a DataFrame
df <- read.csv("sailing-elo/data/testrdata.csv")
sailors <- read.csv("sailing-elo/data/testrdatasailor.csv")
newdata <- read.csv("sailing-elo/data/testrdata2.csv")
# Print the first few rows of the DataFrame
head(df)
head(sailors)
head(newdata)
sailorrankings <- rankings(newdata, id = "race", item = "id", rank = "ranking")

#print(sailorrankings)

#connectivity(sailorrankings, verbose = TRUE)
# Fit the Plackett-Luce model
model <- PlackettLuce(sailorrankings, model = "iterative scaling", npseudo = 0.1)

# Print the model summary
summary(model)
coefs <- coef(model)

#avRank <- apply(model, 2, function(x) mean(x[x > 0]))
#coefs <- round(coef(mod)[order(avRank[keep])], 2)
#head(coefs, 3)
#tail(coefs, 3)'''


model_df <- as.data.frame(coef(summary(model)))

write.csv(coefs, "sailing-elo/data/coefsoutput2.csv", row.names = TRUE)

