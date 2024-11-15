library(PlackettLuce)
library(lbfgs)
print(getwd())
# Read the CSV file into a DataFrame
df <- read.csv("data/testrdata.csv", header = FALSE)
#sailors <- read.csv("data/testrdataskipper.csv")
#newdata <- read.csv("data/plackett_luce_input.csv")
# Print the first few rows of the DataFrame
head(df)
#head(sailors)
#head(newdata)
race_matrix <- as.matrix(df)
head(race_matrix)
num_rows <- nrow(df)
print(num_rows) #0.00025 usually
weights <- exp(0.00005 * (0:(num_rows - 1)))
head(weights)
tail(weights)

sailorrankings <- as.rankings(race_matrix, input = "orderings")

#print(sailorrankings)
anyNA(sailorrankings)
anyNA(weights)

res <- connectivity(sailorrankings, verbose = TRUE)

# Identify the largest cluster size
max_size <- max(res$csize)

# Find the indices of the largest clusters
largest_clusters <- which(res$csize == max_size)

# Extract the rankings from the largest clusters
sailorrankings <- sailorrankings[, res$membership %in% largest_clusters]

#connectivity(sailorrankings, verbose = TRUE)
# Fit the Plackett-Luce model
model <- PlackettLuce(
  sailorrankings,
  method = "BFGS",
  epsilon = 1e-04,  # Larger epsilon for easier convergence
  maxit = c(10000, 500)  # Increase max iterations if needed
)

#model <- PlackettLuce(sailorrankings, method = "L-BFGS",
#npseudo = 0.01, normal = NULL,gamma = TRUE, adherence = NULL, weights = weights, na.action = getOption("na.action"),
#start = NULL, epsilon = 1e-06, steffensen = 0.01, maxit = c(5000, 100), trace = FALSE, verbose = TRUE)


coefs <- summary(model)

#avRank <- apply(model, 2, function(x) mean(x[x > 0]))
#coefs <- round(coef(mod)[order(avRank[keep])], 2)
head(coefs, 3)
tail(coefs, 100)

# Check the structure of the summary object
str(coefs)

# Extract the coefficients, standard errors, t-values, and p-values
coeffs <- coefs$coefficients

# Convert to a data frame
coefs_df <- as.data.frame(coeffs)

# View the first few rows to confirm
head(coefs_df, 3)

# Save to CSV
write.csv(coefs_df, "data/coefs_output2.csv", row.names = TRUE)
