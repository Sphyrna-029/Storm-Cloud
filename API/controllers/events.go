// controllers/events.go

package controllers

import (
	    "net/http"
        "github.com/gin-gonic/gin"
        "github.com/BuckarewBanzai/storm-cloud/models"
)

type CreateEventInput struct {
	StationID  string `json:"stationid" binding:"required"`
	Temperature string `json:"temperature" binding:"required"`
	Pressure string `json:"pressure" binding:"required"`
	Humidity string `json:"humidity" binding:"required"`
	BusVoltage string `json:"busvoltage" binding:"required"`
	BusCurrent string `json:"buscurrent" binding:"required"`
	SupplyVoltage string `json:"supplyvoltage" binding:"required"`
	ShuntVoltage string `json:"shuntvoltage" binding:"required"`
	Power string `json:"power" binding:"required"`
}

// GET /events
// Get all events
func FindEvents(c *gin.Context) {
  var events []models.Event
  models.DB.Find(&events)

  c.JSON(http.StatusOK, gin.H{"data": events})
}

// POST /events
// Create new weather event
func CreateEvent(c *gin.Context) {
	// Validate input
	var input CreateEventInput
	if err := c.ShouldBindJSON(&input); err != nil {
	  c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	  return
	}
  
	// Create event
	events := models.Event{StationID: input.StationID, Temperature: input.Temperature, Pressure: input.Pressure, Humidity: input.Humidity, BusVoltage: input.BusVoltage, BusCurrent: input.BusCurrent, SupplyVoltage: input.SupplyVoltage, ShuntVoltage: input.ShuntVoltage, Power: input.Power}
	models.DB.Create(&events)
  
	c.JSON(http.StatusOK, gin.H{"data": events})
  }
