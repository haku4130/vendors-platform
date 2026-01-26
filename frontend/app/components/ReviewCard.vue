<template>
  <div class="border border-gray-300 rounded-lg p-3 bg-gray-50">
    <div class="flex items-start justify-between mb-2">
      <div class="flex items-center gap-3">
        <UUser
          :name="displayName"
          :description="displayRole"
          :avatar="avatar"
          :to="toUrl"
          :ui="{ avatar: 'rounded-lg border border-black' }"
        />
      </div>
      <StarRating :rating="review.rating" />
    </div>

    <p class="mb-2">{{ review.text }}</p>

    <p v-if="review.created_at" class="text-xs text-muted">
      {{ formatDateReview(review.created_at) }}
    </p>
  </div>
</template>

<script setup lang="ts">
import type { ReviewPublic } from '~/generated/api';

const { review, showAuthor } = defineProps<{
  review: ReviewPublic;
  showAuthor?: boolean; // If true, show author; otherwise show reviewed user
}>();

const reviewedUser = computed(() => {
  return showAuthor ? review.author : review.reviewed_user;
});

const displayName = computed(() => {
  return reviewedUser.value.company_name;
});

const displayRole = computed(() => {
  return (
    reviewedUser.value.full_name +
    ' • ' +
    (reviewedUser.value.role === 'vendor' ? 'Vendor' : 'Company')
  );
});

const avatar = computed(() => {
  return {
    src: reviewedUser.value.logo_url || undefined,
  };
});

const toUrl = computed(() => {
  return reviewedUser.value.role === 'vendor'
    ? `/vendors/${reviewedUser.value.vendor_profile?.id}`
    : `/companies/${reviewedUser.value.id}`;
});
</script>
