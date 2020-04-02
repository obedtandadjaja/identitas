# identitas
Using OpenCV and image recognition to parse data and validate Indonesian identification cards

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

## Future Work

1. Flatten picture to a 2D to take care of cases where the KTP card is slanted
1. Figure out pattern in KTP cards and predict where information will be (i.e. where will name, address, dob be in the picture)
1. Use text recognition to parse text from the picture
1. Figure out how to do confidence metrics/calculation
1. Convert to microservice
