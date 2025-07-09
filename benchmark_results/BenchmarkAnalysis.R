rm(list=ls())

library(tidyverse)

# Getting the data
data_1000 <- read.csv("results_1000.csv")
data_1000_warm <- data_1000 %>% filter(count!=0)

data_1000_delete <- data_1000 %>% filter(operation==' insert')
data_1000_delete_warm <- data_1000_delete %>% filter(count!=0)

# Plotting the data
data_1000 %>% ggplot(aes(time, driver)) + geom_boxplot() + facet_grid(~operation)
data_1000_warm %>% ggplot(aes(time, driver)) + geom_boxplot() + facet_grid(~operation)

data_1000_delete %>% ggplot(aes(time, driver)) + geom_boxplot()
data_1000_delete_warm %>% ggplot(aes(time, driver)) + geom_boxplot()

# Means

del_med <- data_1000 %>% filter(operation==' delete' & driver=='AsyncpgDriver')

del_med_med <- del_med %>% summarise(median = median(time, na.rm=TRUE))

data_1000 %>% ggplot(aes(x=driver, y=median(time))) + geom_dotplot() + facet_grid(~operation)