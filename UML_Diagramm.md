# UML Class Diagram

## RootWidget
+------------------------------------------------+
|                   RootWidget                   | 
+------------------------------------------------+ 
| - distanceRounded: NumericProperty             |
| - distance: NumericProperty                    |
| - heightRounded: NumericProperty               | 
| - step: NumericProperty                        | 
| - label: StringProperty                        | 
| - measureTypeButton: StringProperty            | 
| - camera_initialized: bool                     |
| - capture: object                              | 
| - image_widget: ObjectProperty                 | 
| - orientationHandler: OrientationHandler       | 
| - measurementsHandler: MeasurementHandler      |
+------------------------------------------------+ 
| + start_camera(): None                         | 
| + update_camera(dt): None                      | 
| + on_stop(): None                              | 
| + text_field_person_height_on_text(text): None | 
| + on_measure_button(): None                    | 
| + switchMeasurementType(): None                | 
| + resetMeasurements(): None                    |
+------------------------------------------------+

+----------------------------+
|     OrientationHandler     |
+----------------------------+
| - pitch: float             |
| - azimuth: float           |
| - roll: float              |
| - pitchRounded: float      |
+----------------------------+
| + enable_listener(): None  |
| + disable_listener(): None |
| + get_orientation(dt): None|
+----------------------------+

## MeasurementHandler
+----------------------------------------------------+
|                 MeasurementHandler                 |
+----------------------------------------------------+ 
| - personHeight: float                              | 
| - measureTypeButton: String                        |
+----------------------------------------------------+ 
| + setPersonHeight(height): None                    | 
| + calculateDistance(pitch): (float, float)         | 
| + calculateHeight(distance, pitch): (float, float) | 
| + switchMeasurementType(): String                  | 
+----------------------------------------------------+

+-------------------------+
|          Main           |
+-------------------------+
| + build(): object       |
| + on_start(): None      |
| + on_stop(): None       |
+-------------------------+

## Key Relationships
- **RootWidget** uses **OrientationHandler** and **MeasurementHandler** to handle measurements and orientation data.
- **OrientationHandler** updates the orientation data (pitch, azimuth, roll).
- **MeasurementHandler** calculates the height and distance based on the orientation data and a reference person’s height.
- **Main** initializes and runs the app, managing the camera and orientation listeners.
