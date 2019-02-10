<template>
  <div id="app" style="width: 1024px; margin-left: calc(50% - 512px);">

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

    <div>
      <gallery
        :images="images.map(img => img.url)"
        :index="index"
        @close="index = null"
      >
      </gallery>

      <div
        class="image"
        v-for="(image, imageIndex) in images"
        :key="imageIndex"
        @click="index = imageIndex"
        :style="{ backgroundImage: 'url(' + image.url + ')', width: '240px', height: '200px' }"
      >
      </div>
    </div>

    <div style="text-align: center; padding-top: 1%;">
      <a-button @click="getPhotos"> More </a-button>
    </div>

    <div>
      <a-back-top />
    </div>

  </div>
</template>

<script>
  import VueGallery from 'vue-gallery';
  import { Select, BackTop, Button } from 'ant-design-vue'

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

  function set2Array(set) {
    return Array.from(set)
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
    }
  },

  methods: {
    getPhotos() {
      let emotions = this.isFilterPressed ? this.nextEmotions : this.currentEmotions;
      this.isFilterPressed = false;
      console.log('next emotions: ' + set2Array(this.nextEmotions) + '\n');
      console.log('currentEmotions: ' + set2Array(this.currentEmotions) + '\n');
      let jsonEmotionsList = JSON.stringify(set2Array(emotions));
      let queryParams = formQueryParams(jsonEmotionsList, this.offset, CONST.IMAGES_PER_REQ);
      let path = '/api/get_photos';

      axios.get(path, { params: queryParams }).then(response =>
          response.data
      )
        .then(resp => {
          if (resp.status === CONST.RESP_STATUS.ERR) {
            console.log('Unexpected response code: ' + resp.status);
          } else {
            this.images = this.images.concat(resp.photos_info);
            console.log(this.images);
            let lastImg = this.images[this.images.length - 1];
            this.offset = lastImg.id;
          }
        })
        .catch(function (reason) {
          console.log('Error ocurred while performing request: ' + reason);
        })
    },

    onFilterPressed() {
      this.images = [];
      this.getPhotos();
      this.currentEmotions = this.nextEmotions;
      this.isFilterPressed = true;
    },

    onSelect(value) {
      console.log(`selected ${value}`);
      this.nextEmotions = new Set(Object.values(value));
    },
  },

  beforeMount() {
    this.getPhotos();
  },

  components: {
    'gallery': VueGallery,
    'a-select': Select,
    'a-select-option': Select,
    'a-back-top': BackTop,
    'a-button': Button
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
</style>
