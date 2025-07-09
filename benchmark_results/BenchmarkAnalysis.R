rm(list=ls())

library(tidyverse)

# Getting the data
data_1000 <- read.csv("results_1000.csv")

#data_1000_delete <- data_1000 %>% filter(operation==' insert')
#data_1000_delete_warm <- data_1000_delete %>% filter(count!=0)

# Plotting the data
#data_1000 %>% ggplot(aes(time, driver)) + geom_boxplot() + facet_grid(~operation)
#data_1000_warm %>% ggplot(aes(time, driver)) + geom_boxplot() + facet_grid(~operation)

#data_1000_delete %>% ggplot(aes(time, driver)) + geom_boxplot()
#data_1000_delete_warm %>% ggplot(aes(time, driver)) + geom_boxplot()

# Means

#del_med <- data_1000 %>% filter(operation==' delete' & driver=='AsyncpgDriver')

#del_med_med <- del_med %>% summarise(median = median(time, na.rm=TRUE))

#data_1000 %>% ggplot(aes(x=driver, y=median(time))) + geom_dotplot() + facet_grid(~operation)

make_boxplots <- function(input_data, text) {
  
  # Delete
  del <- input_data %>% filter(operation==' delete')
  del %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_delete_", text, ".png"))
  
  # Insert
  ins <- input_data %>% filter(operation==' insert')
  ins %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_insert_", text, ".png"))
  
  # Read
  rea <- input_data %>% filter(operation==' read')
  rea %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_read_", text, ".png"))
  
  # Update
  upd <- input_data %>% filter(operation==' update')
  upd %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_update_", text, ".png"))
  
}

plotting_data <- function(input_data) {
  
  # Without warmup
  make_boxplots(input_data, "cold")
  
  # With warmup
  input_data_warm = input_data %>% filter(count!=0)
  make_boxplots(input_data_warm, "warm")
  
}

plotting_data(data_1000)