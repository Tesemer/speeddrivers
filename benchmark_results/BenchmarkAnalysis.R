rm(list=ls())

library(tidyverse)
library(foreach)

# Getting the data
data_100 <- read.csv("results_100.csv")
data_1000 <- read.csv("results_1000.csv")
data_10000 <- read.csv("results_10000.csv")

data_all <- 


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

make_violinplots <- function(input_data, text) {
  
  # Delete
  del <- input_data %>% filter(operation=='delete')
  del %>% ggplot(aes(time, driver)) + geom_violin()
  ggsave(file=paste0(getwd(), "/plots/vp_delete_", text, ".png"))
  
  # Insert
  ins <- input_data %>% filter(operation=='insert')
  ins %>% ggplot(aes(time, driver)) + geom_violin()
  ggsave(file=paste0(getwd(), "/plots/vp_insert_", text, ".png"))
  
  # Read
  rea <- input_data %>% filter(operation=='read')
  rea %>% ggplot(aes(time, driver)) + geom_violin()
  ggsave(file=paste0(getwd(), "/plots/vp_read_", text, ".png"))
  
  # Update
  upd <- input_data %>% filter(operation=='update')
  upd %>% ggplot(aes(time, driver)) + geom_violin()
  ggsave(file=paste0(getwd(), "/plots/vp_update_", text, ".png"))
  
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

plotting_data <- function(input_data, size) {
  
  # BOXPLOTS
  
  # Without warmup
  make_boxplots(input_data, paste0("cold", size))
  
  # With warmup
  input_data_warm = input_data %>% filter(count!=0)
  make_boxplots(input_data_warm, paste0("warm", size))
  
  # MEDIAN
  
  # Without warmup
  make_median(input_data, paste0("cold", size))
  
  # With warmup
  make_median(input_data_warm, paste0("warm", size))
  
  # VIOLIN PLOTS
  
  # Without warmup
  make_violinplots(input_data, paste0("cold", size))
  
  # With warmup
  make_violinplots(input_data_warm, paste0("warm", size))
  
}



plotting_data(data_100, "100")
plotting_data(data_1000, "1000")
plotting_data(data_10000, "10000")