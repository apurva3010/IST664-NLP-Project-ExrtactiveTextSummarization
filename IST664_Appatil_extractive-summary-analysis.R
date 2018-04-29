# author: appatil
metrics <- read.csv(file="metrics.csv", header=TRUE, sep=",")

bleu1_density <- density(as.numeric(metrics$bleu1))
bleu4_density <- density(as.numeric(metrics$bleu4))
bleu1ws_density <- density(as.numeric(metrics$bleu1ws))
bleu4ws_density <- density(as.numeric(metrics$bleu4ws))

par(mar=c(4.1, 3.5, 3.5, 1.5), mgp=c(2, 1, 0), las=0)

plot(bleu1_density,type="l", col="red", xlab="Scores" ,ylab="Density", main="Cumulative BLEU-1 Scores Distribution", lwd = 2)
lines(bleu1ws_density, type="l", col="blue", lwd = 2)
cat(sprintf("BLEU-1\n---\nWith Stopwords\nMean = %0.5f\nStd. Dev = %0.5f\nWithout Stopwords\nMean = %0.5f\nStd. Dev = %0.5f\n",
        mean(metrics$bleu1), sd(metrics$bleu1), mean(metrics$bleu1ws), sd(metrics$bleu1ws)))

plot(bleu4_density,type="l", col="red", xlab="Scores" ,ylab="Density", main="Cumulative BLEU-4 Scores Distribution", lwd = 2)
lines(bleu4ws_density, type="l", col="blue", lwd = 2)
cat(sprintf("BLEU-4\n---\nWith Stopwords\nMean = %0.5f\nStd. Dev = %0.5f\nWithout Stopwords\nMean = %0.5f\nStd. Dev = %0.5f\n",
            mean(metrics$bleu4), sd(metrics$bleu4), mean(metrics$bleu4ws), sd(metrics$bleu4ws)))
