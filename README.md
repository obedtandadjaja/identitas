# identitas

Using OpenCV and image recognition to parse data and validate Indonesian identification cards

There are multiple challenges in achieving the desired result:

1. Detect where the card is
1. Crop the original picture to just the card
1. If the card is slanted in the picture, make the card up right
1. Detect the text inside the card
1. Calculate confidence level in the text detection, if it is below a certain threshold, have the user to reupload or position the camera correctly. Might need to also turn on/off the camera's flash

## External factors that may affect result

1. Image/sensor noise. Sensor noise from a handheld camera is typically higher than that of a traditional scanner.
2. Viewing angles. The scene might not have a viewing angle that is parallel to the text.
3. Blurring.
4. Lighting condition. We cannot control if the camera has flash on, or if the sun is shining brightly.
5. Resolution. Differences in camera quality might affect the amount of noise in the scene.
6. Non-paper objects. Paper is not reflective, but text that appear on a reflective object makes it harder to detect.

## Examples

<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-1.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-1.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-2.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-2.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-3.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-3.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-4.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-4.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-5.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-5.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-6.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-6.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-7.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-7.png" width="400" />
</div>
<div style="display:inline-block">
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/training_images/ktp-8.png" width="400" />
  <img src="https://raw.githubusercontent.com/obedtandadjaja/identitas/master/results/ktp-8.png" width="400" />
</div>

## Project Scope

The project is still using some external libraries to process the text, however, it will be restricted from using any paid services like Google Cloud Vision API which basically does everything for you.

Although yes in a production environment using some machine learning model maintained by Google will yield better results, the goal of this project is to learn what Google Cloud Vision API is doing under the hood.

## Future Work

1. Figure out pattern in KTP cards and predict where information will be (i.e. where will name, address, dob be in the picture)
1. Use text recognition to parse text from the picture
1. Figure out how to do confidence metrics/calculation
1. Convert to microservice

## Running

Running the migration: `alembic upgread head`
