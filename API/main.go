package main

import (
  "github.com/gin-gonic/gin"
  "github.com/BuckarewBanzai/storm-cloud/models"
  "github.com/BuckarewBanzai/storm-cloud/controllers"
)

func main() {
  r := gin.Default()

  models.ConnectDatabase()

  r.GET("/events", controllers.FindEvents)
  r.GET("/events/:id", controllers.FindStation)
  r.POST("/events", controllers.CreateEvent)
  r.GET("/strike", controllers.FindStrikes)
  r.POST("/strike", controllers.CreateStrike)

  r.Run(":8081")
}
