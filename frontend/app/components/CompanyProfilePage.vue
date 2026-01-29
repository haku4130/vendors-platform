<template>
  <div class="space-y-8">
    <!-- Header Section -->
    <UCard class="bg-vendor-gradient shadow-lg">
      <div class="flex flex-col md:flex-row gap-6 items-start md:items-center">
        <NuxtImg
          :src="company.logo_url || '/placeholder-avatar.png'"
          :alt="company.company_name"
          class="rounded-lg border-2 border-white shadow-md w-full h-full md:w-48 md:h-48 object-cover"
        />

        <div class="flex-1 text-black">
          <div class="flex items-center">
            <h1 class="text-3xl font-semibold">
              {{ company.company_name }}
            </h1>
          </div>

          <div class="flex mb-4 sm:mb-2">
            <span class="text-sm align-middle">
              {{ company.full_name }}
            </span>
          </div>

          <div class="flex flex-wrap gap-x-4 gap-y-1 text-sm mb-4">
            <div v-if="company.location" class="flex items-center gap-1">
              <UIcon name="i-lucide-map-pin" class="w-4 h-4" />
              <span>{{ company.location }}</span>
            </div>
            <div
              v-if="company.rating"
              class="w-fit flex items-center gap-2 bg-white/30 px-3 py-1 rounded-full"
            >
              <span class="font-semibold">{{ company.rating.toFixed(1) }}</span>
              <StarRating :rating="company.rating" />
              <span class="text-sm text-muted"
                >({{ company.ratingCount || 0 }})</span
              >
            </div>
            <div
              v-else
              class="w-fit flex items-center gap-2 bg-white/30 px-3 py-1 rounded-full"
            >
              <span class="font-semibold">No rating yet</span>
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Reviews Section -->
    <UCard>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">Reviews</h2>
          <span v-if="company.ratingCount" class="text-sm text-muted">
            {{ company.ratingCount }} total review(s)
          </span>
        </div>
      </template>
      <template #default>
        <div v-if="loadingReviews" class="flex justify-center py-8">
          <UIcon name="i-lucide-loader-2" class="w-6 h-6 animate-spin" />
        </div>

        <div v-else-if="reviews.length > 0">
          <div class="grid lg:grid-cols-2 xl:grid-cols-3 gap-3">
            <ReviewCard
              v-for="review in reviews"
              :key="review.id"
              :review="review"
              show-author
            />
          </div>

          <div v-if="hasMoreReviews" class="text-center pt-4">
            <UButton
              variant="outline"
              :loading="loadingMoreReviews"
              @click="loadMoreReviews"
            >
              Load More Reviews
            </UButton>
          </div>
        </div>

        <UEmpty
          v-else
          icon="i-lucide-star"
          title="No reviews yet"
          description="This company hasn't received any reviews yet."
        />
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import type { UserPublic, ReviewPublic } from '~/generated/api';
import { reviewsGetReviewsForUser } from '~/generated/api';

const { company } = defineProps<{
  company: UserPublic;
}>();

const reviews = ref<ReviewPublic[]>([]);
const loadingReviews = ref(true);
const loadingMoreReviews = ref(false);
const reviewsPerPage = 5;
const totalReviews = ref(0);

const hasMoreReviews = computed(
  () => reviews.value.length < totalReviews.value,
);

async function loadReviews() {
  const res = await reviewsGetReviewsForUser({
    path: {
      user_id: company.id,
    },
    query: {
      skip: 0,
      limit: reviewsPerPage,
    },
  });

  loadingReviews.value = false;

  if (res.error) {
    console.error('Failed to load reviews:', res.error);
    return;
  }

  reviews.value = res.data?.result || [];
  totalReviews.value = res.data?.total || 0;
}

async function loadMoreReviews() {
  loadingMoreReviews.value = true;

  const res = await reviewsGetReviewsForUser({
    path: {
      user_id: company.id,
    },
    query: {
      skip: reviews.value.length,
      limit: reviewsPerPage,
    },
  });

  loadingMoreReviews.value = false;

  if (res.error) {
    console.error('Failed to load more reviews:', res.error);
    return;
  }

  reviews.value.push(...(res.data?.result || []));
}

onMounted(() => {
  loadReviews();
});
</script>
