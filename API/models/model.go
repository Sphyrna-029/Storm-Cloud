package models

type Event struct {
  ID             uint   `json:"id" gorm:"primary_key"`
  StationID      string `json:"stationid"`
  Temperature    string `json:"temperature"`
  Pressure       string `json:"pressure"`
  Humidity       string `json:"humidity"`
  BusVoltage     string `json:"busvoltage"`
  BusCurrent     string `json:"buscurrent"`
  SupplyVoltage  string `json:"supplyvoltage"`
  ShuntVoltage   string `json:"shuntvoltage"`
  Power          string `json:"power"`
}
