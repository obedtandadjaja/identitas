# identitas
Using OpenCV and image recognition to parse data and validate Indonesian identification cards

There are multiple challenges in achieving the desired result:

1. Detect where the card is
1. Crop the original picture to just the card
1. If the card is slanted in the picture, make the card up right
1. Detect the text inside the card
1. Calculate confidence level in the text detection, if it is below a certain threshold, have the user to reupload or position the camera correctly. Might need to also turn on/off the camera's flash

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

## Future Work

1. Figure out pattern in KTP cards and predict where information will be (i.e. where will name, address, dob be in the picture)
1. Use text recognition to parse text from the picture
1. Figure out how to do confidence metrics/calculation
1. Convert to microservice
