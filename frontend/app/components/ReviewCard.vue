<template>
  <div class="flex items-start justify-between mb-2">
    <div>
      <p class="font-semibold text-sm">
        {{
          review.author?.full_name || review.author?.company_name || 'Anonymous'
        }}
      </p>
      <p class="text-xs text-muted">
        {{ formatDateReview(review.created_at) }}
      </p>
    </div>
    <div class="flex items-center gap-1 text-yellow-500">
      <StarRating :rating="review.rating" />
    </div>
  </div>
  <p class="text-sm leading-relaxed">
    {{ review.text }}
  </p>
</template>

<script setup lang="ts">
import type { ReviewPublic } from '~/generated/api';

const { review } = defineProps<{
  review: ReviewPublic;
}>();
</script>
