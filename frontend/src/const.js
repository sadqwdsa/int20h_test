const RESP_STATUS = {
  OK: 'OK',
  ERR: 'ERROR'
};

const EMOTIONS = {
  SADNESS: 0,
  NEUTRAL: 1,
  DISGUST: 2,
  ANGER: 3,
  SURPRISE: 4,
  FEAR: 5,
  HAPPINESS: 6
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
  EMOTIONS: EMOTIONS,
  num2emotion: num2emotion,
  IMAGES_PER_REQ: IMAGES_PER_REQ
}
