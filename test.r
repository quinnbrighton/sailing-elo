library(PlackettLuce)

print(getwd())
# Read the CSV file into a DataFrame
df <- read.csv("data/testrdata.csv")
sailors <- read.csv("data/testrdataskipper.csv")
#newdata <- read.csv("data/plackett_luce_input.csv")
# Print the first few rows of the DataFrame
head(df)
head(sailors)
head(newdata)
race_matrix <- as.matrix(df)
head(race_matrix)
sailorrankings <- as.rankings(race_matrix, input = "orderings")

print(sailorrankings)

connectivity(sailorrankings, verbose = TRUE)
# Fit the Plackett-Luce model
model <- PlackettLuce(sailorrankings, 
                    model = "iterative scaling",
                    npseudo = 0.1,
                    normal = NULL,
                    gamma = NULL,
                    adherence = NULL,
                    weights = freq(rankings),
                    na.action = getOption("na.action"),
                    start = NULL,
                    method = c("iterative scaling", "BFGS", "L-BFGS"),
                    epsilon = 1e-05,
                    steffensen = 0.1,
                    maxit = c(5000, 100),
                    trace = FALSE,
                    verbose = TRUE
                    )

# Print the model summary
#summary(model)
coefs <- coef(model)

#avRank <- apply(model, 2, function(x) mean(x[x > 0]))
#coefs <- round(coef(mod)[order(avRank[keep])], 2)
head(coefs, 3)
tail(coefs, 100)


model_df <- as.data.frame(coef(model))


write.csv(coefs, "data/coefsoutput2.csv", row.names = TRUE)
