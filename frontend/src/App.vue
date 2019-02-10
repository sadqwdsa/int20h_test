<template>
  <div id="app">
    <div style="width: 1024px; margin-left: calc(50% - 512px);">
      <div style="text-align: center; padding-top: 1%; width: 100%">
        <a-select
          mode="multiple"
          :defaultValue="[]"
          style="width: 35%;"
          @change="onSelect"
          placeholder="Please select emotions"
        >

          <a-select-option
            v-for="emotionId in emotionsConst"
            :key="emotionId"
          >{{num2emotion[emotionId]}}
          </a-select-option>

        </a-select>

        <a-button style="margin-left: 1%" @click="onFilterPressed"> Filter </a-button>
      </div>

      <div style="margin: 10px">
        <gallery
          :images="images.map(img => img.origin_url)"
          :index="index"
          @close="index = null"
        >
        </gallery>

        <div
          class="image"
          v-for="(image, imageIndex) in images"
          :key="imageIndex"
          @click="index = imageIndex"
          :style="{ backgroundImage: 'url(' + image.min_url + ')', width: '240px', height: '200px' }"
        >
        </div>
      </div>

      <div style="text-align: center">
        <a-spin style="margin: 15px" v-if="displaySpin" size="large" />
      </div>

      <div style="text-align: center;">
        <a-button :disabled="disableMore" style="margin-top: 10px; margin-bottom: 50px" @click="getPhotos"> More </a-button>
      </div>

      <div>
        <a-back-top />
      </div>
    </div>

    <div class="footer">Developed by <b>sadqwdsa</b> int20h team</div>
  </div>
</template>

<script>
  import VueGallery from 'vue-gallery';
  import { Select, BackTop, Button, Spin} from 'ant-design-vue'

  import CONST from './const';
  import axios from 'axios';

  import 'ant-design-vue/dist/antd.css';

  function formQueryParams(emotions,
                           fromId,
                           count) {
    return {
      emotions: emotions,
      from_id: fromId,
      count: count
    }
  }

export default {
  name: 'app',

  data: function () {
    return {
      images: [], // array contains elements of the following schema { id, url }
      index: null,
      offset: 0,
      num2emotion: CONST.num2emotion,
      nextEmotions: new Set() /*new Set(Object.values(CONST.EMOTIONS))*/,
      currentEmotions: new Set(),
      isFilterPressed: false,
      emotionsConst: Object.values(CONST.EMOTIONS), //should not be changed
      disableMore: false,
      displaySpin: true
    }
  },

  methods: {
    getPhotos() {
      this.displaySpin = true;
      let emotions = this.isFilterPressed ? this.nextEmotions : this.currentEmotions;
      this.isFilterPressed = false;
      let jsonEmotionsList = JSON.stringify(Array.from(emotions));
      let queryParams = formQueryParams(jsonEmotionsList, this.offset, CONST.IMAGES_PER_REQ);
      let path = '/api/get_photos';

      axios.get(path, { params: queryParams })
        .then(resp => resp.data)
        .then(payload => {
          if (payload.status === CONST.RESP_STATUS.ERR) {
            console.log('Unexpected response code: ' + payload.status);
          } else {
            if (payload.photos_info.length < CONST.IMAGES_PER_REQ) {
              this.disableMore = true;
            }

            this.displaySpin = false;
            this.images = this.images.concat(payload.photos_info);
            let lastImg = this.images[this.images.length - 1];
            this.offset = lastImg.id;
          }
        })
        .catch(function (reason) {
          console.log('Error occurred while performing request: ' + reason);
        })
    },

    onFilterPressed() {
      this.images = [];
      this.offset = 0;
      this.currentEmotions = this.nextEmotions;
      this.isFilterPressed = true;
      this.disableMore = false;
      this.getPhotos();
    },

    onSelect(value) {
      this.nextEmotions = new Set(Object.values(value));
    },
  },

  updated() {
    window.scrollTo(0, document.body.scrollHeight);
  },

  beforeMount() {
    this.getPhotos();
  },

  components: {
    'gallery': VueGallery,
    'a-select': Select,
    'a-select-option': Select,
    'a-back-top': BackTop,
    'a-button': Button,
    'a-spin': Spin
  },
}
</script>

<style lang="scss">
  .image {
    float: left;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    border: 1px solid #ebebeb;
    margin: 5px;
  }

  .footer {
    font-size: 14px;
    font-family:
            "Chinese Quote",
            -apple-system,
            BlinkMacSystemFont;

    position: fixed;
    bottom: 0;
    background-color: #c7c8d0;
    width: 100%;
    height: 40px;
    display: block;
    text-align: center;
    padding-top: 10px;
  }
</style>
