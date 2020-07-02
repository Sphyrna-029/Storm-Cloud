// controllers/events.go

package controllers

import (
        "net/http"
        "time"
        "github.com/gin-gonic/gin"
        "github.com/BuckarewBanzai/storm-cloud/models"
)

type CreateEventInput struct {
        StationID  string `json:"stationid" binding:"required"`
        DateTime time.Time `json:"datetime" binding:"required"`
        Temperature float32 `json:"temperature" binding:"required"`
        Pressure float32 `json:"pressure" binding:"required"`
        Humidity float32 `json:"humidity" binding:"required"`
        BusVoltage float32 `json:"busvoltage" binding:"required"`
        BusCurrent float32 `json:"buscurrent" binding:"required"`
        SupplyVoltage float32 `json:"supplyvoltage" binding:"required"`
        ShuntVoltage float32 `json:"shuntvoltage" binding:"required"`
        Power float32 `json:"power" binding:"required"`
}

// GET /events
// Get all events
func FindEvents(c *gin.Context) {
  var events []models.Event
  models.DB.Find(&events)

  c.JSON(http.StatusOK, gin.H{"data": events})
}

// GET /event/:stationid
// Find events by stationid
func FindStation(c *gin.Context) {
        // Get model if exist
        var events []models.Event
        if err := models.DB.Where("station_id = ?", c.Param("id")).Find(&events).Error; err != nil {
                c.JSON(http.StatusBadRequest, gin.H{"error": "Station ID not found!"})
                return
        }

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
        events := models.Event{
                                    StationID: input.StationID,
                                    DateTime: input.DateTime,
                                    Temperature: input.Temperature,
                                    Pressure: input.Pressure,
                                    Humidity: input.Humidity,
                                    BusVoltage: input.BusVoltage,
                                    BusCurrent: input.BusCurrent,
                                    SupplyVoltage: input.SupplyVoltage,
                                    ShuntVoltage: input.ShuntVoltage,
                                    Power: input.Power }

        models.DB.Create(&events)

        c.JSON(http.StatusOK, gin.H{"data": events})
  }
