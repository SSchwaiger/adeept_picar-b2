<template>
  <ButtonsChild :buttons="buttons" :cols="cols"/>
</template>

<script>
import ButtonsChild from '@/components/controll/child/ButtonsChild.vue'

export default ({
  name: 'ArmControlMod',
  components: {
    ButtonsChild
  },
  data: () => ({
    buttons: [
      [false, 'Left', 'lookleft', 74, 'LRstop'],
      [false, 'Up', 'up', 73, 'UDstop'],
      [false, 'Down', 'down', 75, 'UDstop'],
      [false, 'Right', 'lookright', 76, 'LRstop']
    ],
    cols: 4
  })
})
</script>

<style lang="stylus" scoped>
</style>
