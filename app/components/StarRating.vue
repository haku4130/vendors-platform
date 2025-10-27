<template>
  <vue3StarRatings
    :model-value="rating"
    :custom-svg="CustomRatingStar"
    disable-click
    star-color="oklch(79.5% 0.184 86.047)"
    :star-size="16"
    inactive-color="#E5E7EF"
  />
</template>

<script lang="ts" setup>
import vue3StarRatings from 'vue3-star-ratings';
import CustomRatingStar from '~/components/CustomRatingStar.vue';

defineProps<{
  rating: number;
}>();
</script>
