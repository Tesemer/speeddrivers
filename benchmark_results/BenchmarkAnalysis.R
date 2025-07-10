rm(list=ls())

library(tidyverse)
library(foreach)

# Getting the data
data_1000 <- read.csv("results_1000.csv")
#data_100000 <- read.csv("results_100000.csv")

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
  del <- input_data %>% filter(operation=='delete')
  del %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_delete_", text, ".png"))
  
  # Insert
  ins <- input_data %>% filter(operation=='insert')
  ins %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_insert_", text, ".png"))
  
  # Read
  rea <- input_data %>% filter(operation=='read')
  rea %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_read_", text, ".png"))
  
  # Update
  upd <- input_data %>% filter(operation=='update')
  upd %>% ggplot(aes(time, driver)) + geom_boxplot()
  ggsave(file=paste0(getwd(), "/plots/bp_update_", text, ".png"))
  
}

make_median <- function(input_data, mode) {
  
  ops <- c('insert', 'update', 'delete', 'read')
  dri <- c('AsyncpgDriver', 'Psycopg2Driver', 'Pg8000', 'SqlalchemyDriver')
  
  foreach(operat = ops) %do% {
    
    # Filter out only the correct operation
    driver_data <- input_data %>% filter(operation==operat)
    head(driver_data)
    
    # Calculate the medians 
    median_tibble <- NULL
    foreach(driv = dri) %do% { # Create data for every driver
      
      # Filter the driver
      median_data <- driver_data %>% filter(driver==driv)
      med <- median_data %>% summarise(median = median(time, na.rm=TRUE))
      
      if (is.null(median_tibble)) { # Check if the tibble exists or not
        median_tibble = tibble(driver=driv, med)
      } else {
        median_tibble <- median_tibble %>% add_row(tibble_row(driver=driv, med[1]))
      }
      
    }
    
    # Plotting the median
    median_tibble %>% ggplot(aes(x=median, y=driver)) + geom_dotplot()
    ggsave(file=paste0(getwd(), "/plots/median_", operat, "_", mode, ".png"))
    
  }
  
  tibble(ops, b=1)
  
}

plotting_data <- function(input_data) {
  
  # BOXPLOTS
  
  # Without warmup
  make_boxplots(input_data, "cold")
  
  # With warmup
  input_data_warm = input_data %>% filter(count!=0)
  make_boxplots(input_data_warm, "warm")
  
  # MEDIAN
  
  # Without warmup
  make_median(input_data, "cold")
  
  # With warmup
  make_median(input_data_warm, "warm")
  
}

plotting_data(data_1000)