#include <WiFi.h>
#include <esp_wifi.h> // Include ESP WiFi header for esp_wifi_set_mac

// Define your custom MAC address (must be 6 bytes long)
uint8_t newMACAddress[6] = {0x01, 0x01, 0xFA, 0xCA, 0xDE, 0x01};

void setup() {
  Serial.begin(115200);

  // Print the default MAC address
  Serial.print("Default MAC Address: ");
  Serial.println(WiFi.macAddress());

  // Set the new MAC address for the WiFi STA interface
  if (esp_wifi_set_mac(WIFI_IF_STA, newMACAddress) == ESP_OK) {
    Serial.println("MAC address changed successfully!");
  } else {
    Serial.println("Failed to change MAC address.");
  }

  // Initialize WiFi to apply the new MAC address
  WiFi.begin();

  // Print the new MAC address
  Serial.print("New MAC Address: ");
  Serial.println(WiFi.macAddress());
}

void loop() {
  // Add your main code here
}
