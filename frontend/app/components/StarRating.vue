<template>
  <vue3StarRatings
    v-model="rating"
    :custom-svg="CustomRatingStar"
    :disable-click="!clickable"
    star-color="oklch(79.5% 0.184 86.047)"
    :star-size="starSize"
    inactive-color="#E5E7EF"
  />
</template>

<script lang="ts" setup>
import vue3StarRatings from 'vue3-star-ratings';
import CustomRatingStar from '~/components/CustomRatingStar.vue';

const rating = defineModel<number>('rating', { required: true });

const { clickable = false, starSize = 16 } = defineProps<{
  clickable?: boolean;
  starSize?: number;
}>();
</script>
