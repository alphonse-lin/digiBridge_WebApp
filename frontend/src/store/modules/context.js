import { defineStore } from 'pinia'

export const useContextStore = defineStore(
  'context', {
    state: () => ({
      clicks: null,
      image: null,
      maskImg: null
    }),
    actions: {
      setClicks (clicks) {
        this.clicks = clicks
      },
      setImage (image) {
        this.image = image
      },
      setMaskImg (maskImg) {
        this.maskImg = maskImg
      }
    }
  })
