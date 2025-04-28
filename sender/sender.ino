#include <esp_now.h>
#include <WiFi.h>

// Peer MAC Address - replace this with the MAC address of the other ESP32
uint8_t peerAddress[] = {0x44, 0x17, 0x93, 0x7C, 0x39, 0x1C}; // Example MAC, replace with actual peer's MAC 44:17:93:7C:39:1C

typedef struct struct_message {
  char message[100];
} struct_message;

struct_message myData;

// Callback when data is received
void OnDataRecv(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("");
  Serial.println(myData.message);
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  // Serial.println("MAC Address: ");
  // Serial.println(WiFi.macAddress());
  
  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register receive callback
  esp_now_register_recv_cb(OnDataRecv);

  // Register peer
  esp_now_peer_info_t peerInfo;
  memset(&peerInfo, 0, sizeof(peerInfo)); // Clear peerInfo structure
  memcpy(peerInfo.peer_addr, peerAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;

  // Add peer
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  // Check if data is available on the serial monitor
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n'); // Read the input from the serial monitor
    message.toCharArray(myData.message, 100);

    // Send message via ESP-NOW
    esp_err_t result = esp_now_send(peerAddress, (uint8_t *) &myData, sizeof(myData));

    if (result != ESP_OK) {
      Serial.println("Error sending the data");
    }
  }

  delay(1000);
}
