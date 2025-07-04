rm(list=ls())

library(tidyverse)

# Getting the data
simple_data <- read.csv("results_2849d0da-9026-4298-aad6-ac046754f1f9_100.csv")

# Plotting the data
simple_data %>% ggplot(aes(x=count, y=time, color=driver)) + geom_line() +  facet_grid(~operation)