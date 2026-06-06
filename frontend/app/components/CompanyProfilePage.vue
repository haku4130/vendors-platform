<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- Hero -->
    <div
      class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden"
    >
      <div class="h-24 bg-gradient-to-r from-blue-500 to-blue-400" />
      <div class="px-8 pb-8">
        <div class="flex items-end gap-5 -mt-10 mb-5">
          <div
            class="w-20 h-20 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shrink-0 border-4 border-white shadow-md"
            :style="{ backgroundColor: avatarColor(company.company_name) }"
          >
            {{ initials(company.company_name) }}
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4"
        >
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ company.company_name }}
            </h1>
            <p class="text-sm text-gray-500 mt-0.5">{{ company.full_name }}</p>

            <div class="flex flex-wrap items-center gap-3 mt-3">
              <div
                v-if="company.location"
                class="flex items-center gap-1.5 text-sm text-gray-500"
              >
                <UIcon name="i-lucide-map-pin" class="w-4 h-4 shrink-0" />
                <span>{{ company.location }}</span>
              </div>

              <div
                v-if="company.rating"
                class="flex items-center gap-1.5 px-3 py-1 bg-amber-50 border border-amber-100 rounded-full"
              >
                <UIcon
                  name="i-lucide-star"
                  class="w-3.5 h-3.5 text-amber-400 fill-amber-400"
                />
                <span class="text-sm font-semibold text-amber-700">{{
                  company.rating.toFixed(1)
                }}</span>
                <span class="text-xs text-amber-600"
                  >· {{ company.ratingCount }}
                  {{ reviewsLabel(company.ratingCount ?? 0) }}</span
                >
              </div>
              <div
                v-else
                class="flex items-center gap-1.5 px-3 py-1 bg-gray-50 border border-gray-200 rounded-full"
              >
                <UIcon name="i-lucide-star" class="w-3.5 h-3.5 text-gray-400" />
                <span class="text-sm text-gray-500">Нет оценок</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reviews -->
    <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
      <div class="flex items-center justify-between mb-5">
        <h2 class="text-lg font-semibold">Отзывы</h2>
        <span v-if="totalReviews > 0" class="text-sm text-gray-400"
          >{{ totalReviews }} {{ reviewsLabel(totalReviews) }}</span
        >
      </div>

      <div v-if="loadingReviews" class="flex justify-center py-10">
        <UIcon
          name="i-lucide-loader-2"
          class="w-6 h-6 animate-spin text-muted"
        />
      </div>

      <div v-else-if="reviews.length > 0" class="space-y-4">
        <div class="grid lg:grid-cols-2 xl:grid-cols-3 gap-3">
          <ReviewCard
            v-for="review in reviews"
            :key="review.id"
            :review="review"
            show-author
          />
        </div>
        <div v-if="hasMoreReviews" class="text-center pt-2">
          <UButton
            variant="outline"
            color="neutral"
            :loading="loadingMoreReviews"
            @click="loadMoreReviews"
          >
            Загрузить ещё
          </UButton>
        </div>
      </div>

      <UEmpty
        v-else
        icon="i-lucide-star"
        title="Отзывов пока нет"
        description="Эта компания ещё не получила отзывов."
        class="py-6"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { UserPublic, ReviewPublic } from "~/generated/api";
import { reviewsGetReviewsForUser } from "~/generated/api";

const { company } = defineProps<{
  company: UserPublic;
}>();

const AVATAR_COLORS = [
  "#2563eb",
  "#16a34a",
  "#9333ea",
  "#db2777",
  "#d97706",
  "#0891b2",
  "#dc2626",
  "#059669",
  "#7c3aed",
  "#0284c7",
];

function avatarColor(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++)
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]!;
}

function initials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

function reviewsLabel(n: number): string {
  if (n === 1) return "отзыв";
  if (n >= 2 && n <= 4) return "отзыва";
  return "отзывов";
}

const reviews = ref<ReviewPublic[]>([]);
const loadingReviews = ref(true);
const loadingMoreReviews = ref(false);
const reviewsPerPage = 6;
const totalReviews = ref(0);

const hasMoreReviews = computed(
  () => reviews.value.length < totalReviews.value,
);

async function loadReviews() {
  const res = await reviewsGetReviewsForUser({
    path: { user_id: company.id },
    query: { skip: 0, limit: reviewsPerPage },
  });
  loadingReviews.value = false;
  if (res.error) return;
  reviews.value = res.data?.result || [];
  totalReviews.value = res.data?.total || 0;
}

async function loadMoreReviews() {
  loadingMoreReviews.value = true;
  const res = await reviewsGetReviewsForUser({
    path: { user_id: company.id },
    query: { skip: reviews.value.length, limit: reviewsPerPage },
  });
  loadingMoreReviews.value = false;
  if (res.error) return;
  reviews.value.push(...(res.data?.result || []));
}

onMounted(() => {
  loadReviews();
});
</script>
