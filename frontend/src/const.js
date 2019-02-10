const RESP_STATUS = {
  OK: 'OK',
  ERR: 'ERROR'
};

const emotion2num = {
  sadness: 0,
  neutral: 1,
  disgust: 2,
  anger: 3,
  surprise: 4,
  fear: 5,
  happiness: 6
};

const num2emotion = {
  0: 'sadness',
  1: 'neutral',
  2: 'disgust',
  3: 'anger',
  4: 'surprise',
  5: 'fear',
  6: 'happiness',
};

const IMAGES_PER_REQ = 8;

export default {
  RESP_STATUS: RESP_STATUS,
  emotionIds: emotion2num,
  num2emotion: num2emotion,
  IMAGES_PER_REQ: IMAGES_PER_REQ
}
