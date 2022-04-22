#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(rsconnect)

library(shiny)
library("readr")
library(ggplot2)

r<-read.csv("winequality-red.csv", sep=";", header=TRUE)
w<-read.csv("winequality-white.csv", sep=";", header=TRUE)


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Linearity in Wine datasets"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            radioButtons("x","Wine type:", 
                         list("White"="w","Red"="r")),
            radioButtons("y","Physiochemical test:", 
                    list("fixed acidity"="fa", "volatile acidity"="va",  "citric acid"="ca", "residual sugar"="rs", "chlorides" ="cl", "free sulfur dioxide"="fs02" ,"total sulfur dioxide"="ts02", "density"="d", "pH"="p", "sulphates"="s", "alcohol" ="a")
        )),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)



# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
        
        if(input$x=='w'){       i<-w     }     
        if(input$x=='r'){       i<-r     }     
        if(input$y=='fa'){       j<-i$fixed.acidity    }     
        if(input$y=='va'){       j<- i$volatile.acidity  }     
        if(input$y=='ca'){       j<- i$citric.acid  }     
        if(input$y=='rs'){       j<- i$residual.sugar    }     
        if(input$y=='cl'){       j<- i$chlorides    }     
        if(input$y=='fs02'){       j<- i$free.sulfur.dioxide    }
        if(input$y=='ts02'){       j<-  i$total.sulfur.dioxide   }     
        if(input$y=='d'){       j<- i$density    }     
        if(input$y=='p'){       j<- i$pH     }     
        if(input$y=='s'){       j<-i$sulphates    } 
        if(input$y=='a'){j<-i$alcohol}
        
  

        ggplot(i, aes(x = j, y = i$quality)) +
            geom_point(alpha = 0.2, position = "jitter", fill=i$quality) + geom_smooth(method = "lm", se = F) +labs(title="Scatter plot between Quality and physiochemical tests")+xlab("Phsyiochemical test")+ylab("Quality") 
    })
}



# Run the application 
shinyApp(ui = ui, server = server)
