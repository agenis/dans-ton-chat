library(rjson)
library(RJSONIO)
library(jsonlite)
setwd("C:/Users/user/Desktop/dtc")
library(tidyverse)
source("mes_fonctions_utiles.R")
# importer le fichier traité en python
result <- jsonlite::fromJSON(readLines("result_traite.json"))
result <- rjson::fromJSON("result_traite.json")


# csv
result = read.csv("result_traite.csv", stringsAsFactors = FALSE)

# export format iramuteq


result %>% sample_n(200) %>% select(comments, nb_lignes, score_neg, score_pos, nb_speak) %>% ggPCA



# si importation avec le menu dans R:il faut mettre ? blanc la case indicateure de donn?es manquantes 


# ajotu de colonnes fun
result = result %>% mutate(qualite = ifelse(score_neg > score_pos, "mauvaise", "bonne"))
result$comments_factor = cut(result$comments, breaks=c(-1, 5, 30, 1000), labels=c("few", "average", "many"), include.lowest = TRUE)




varcomm <-" *Comment_"
varqual <- " *Qualite_"
varspeak <- " *Speak_"
set.seed(123)
res = sample_n(result, 25000) %>% arrange(id_quote)
to.exclude = which(sapply(str_locate_all(res$rtue, "T|???"), function(x) dim(x)[1]>=1))
myheaders<-paste0(sprintf("%05d",res$id_quote), varcomm, res$comments_factor, varqual, res$qualite, varspeak, res$nb_speak_factor)
sink("_test.txt")
for (i in setdiff(seq_along(res$X), to.exclude)){
  cat(myheaders[i]); cat("\n")
  cat(result$rtue[i])
  cat("\n"); cat("\n")
}
sink()
# corpus zola:
http://athena.unige.ch/athena/admin/ath_txt.html


