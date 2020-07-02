package models

import("time")

type Event struct {
  ID             uint   `json:"id" gorm:"primary_key"`
  StationID      string `json:"stationid"`
  DateTime       time.Time  `json:"datetime"`
  Temperature    float32 `json:"temperature"`
  Pressure       float32 `json:"pressure"`
  Humidity       float32 `json:"humidity"`
  BusVoltage     float32 `json:"busvoltage"`
  BusCurrent     float32 `json:"buscurrent"`
  SupplyVoltage  float32 `json:"supplyvoltage"`
  ShuntVoltage   float32 `json:"shuntvoltage"`
  Power          float32 `json:"power"`
}
