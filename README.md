# The Vault
 A Safe vault with RFID+Facial Recognition based security. The idea is to build and develop a simple Safe based on a 2-factor authentication system. The first stage incorporates RFID technology to verify user credentials, followed by the second stage utilizing facial recognition for a secondary authentication which unlocks the safe. 
 This dual-layered approach synergistically enhances overall security, mitigating the risk of unauthorized access or impersonation scenarios, thus safeguarding physical assets effectively.

# Sequence of operation:
 - Upon user interaction, the RF code is tapped for initial stage validation, confirming user credentials. Upon successful validation, indicated by a green light and a specific buzzer sound, the user is granted access. In the event of validation failure, signified by a red light and distinct buzzer sound, access is denied.
 - Subsequently, if the RF identification is validated successfully, the user proceeds to undergo facial recognition for the second authentication process where the Raspberry Pi and camera-based system is used to recognize the face of the person based on user-specific pre-trained data.
 - Upon successful facial authentication, denoted by a green light, a custom-designed safe lock using servo motors will unlock the door. Conversely, if facial authentication fails, indicated by a red light, access is restricted.

# Hardware Used:
 ## Arduino:
 - Interfacing with RC522 RFID reader through SPI communication.
 - Interfacing servo/servos for unlocking the Safe.
 ## Raspberrypi 4:
 - Interfacing the Raspberry Pi camera and using it for facial recognition
 - Connection to Arduino through I2C.
 ## The SAFE:
 - Custom Designed and 3D printed safe with housing for a servo-based lock for unlocking.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8660d96d-2b03-4dc4-b372-0658b1fa81a2" width="400" style="margin-right: 70px;"  />
  <img src="https://github.com/user-attachments/assets/8a809553-37c8-4708-a3d8-09e294b981f6" width="320" />
</p>

# Demo Video:
 Access the demo video using the following link: https://drive.google.com/file/d/1c1BBhBYi_ez_1aJ91xZJ7nyviKOWjDaa/view?usp=sharing
