<template>
  <div class="space-y-4">
    <!-- Top block -->
    <section class="bg-vendor-gradient p-6 rounded-2xl">
      <h2 class="text-xl font-semibold text-white">
        {{ $t('dashboard.reviews.banner') }}
      </h2>
    </section>

    <!-- Tabs for reviews -->
    <UTabs :items="tabs" class="w-full" :ui="{ content: 'my-4' }">
      <!-- My Reviews -->
      <template #written class="space-y-4">
        <div v-if="loadingWritten" class="text-center py-8">
          <UIcon
            name="i-lucide-loader-2"
            class="w-6 h-6 animate-spin mx-auto"
          />
        </div>

        <UEmpty
          v-else-if="!writtenReviews.length"
          icon="i-lucide-pen-line"
          :title="$t('dashboard.reviews.empty.writtenTitle')"
          :description="$t('dashboard.reviews.empty.writtenDescription')"
          class="w-fit mx-auto py-8"
        />

        <div v-else class="space-y-4">
          <ReviewCard
            v-for="review in writtenReviews"
            :key="review.id"
            :review="review"
            :show-author="false"
          />
        </div>
      </template>

      <!-- Reviews About Me -->
      <template #received class="space-y-4">
        <div v-if="loadingReceived" class="text-center py-8">
          <UIcon
            name="i-lucide-loader-2"
            class="w-6 h-6 animate-spin mx-auto"
          />
        </div>

        <UEmpty
          v-else-if="!receivedReviews.length"
          icon="i-lucide-star"
          :title="$t('dashboard.reviews.empty.receivedTitle')"
          :description="$t('dashboard.reviews.empty.receivedDescription')"
          class="w-fit mx-auto py-8"
        />

        <div v-else class="space-y-4">
          <ReviewCard
            v-for="review in receivedReviews"
            :key="review.id"
            :review="review"
            :show-author="true"
          />
        </div>
      </template>

      <!-- Users to Review -->
      <template #to-review class="space-y-4">
        <div v-if="loadingToReview" class="text-center py-8">
          <UIcon
            name="i-lucide-loader-2"
            class="w-6 h-6 animate-spin mx-auto"
          />
        </div>

        <UEmpty
          v-else-if="!usersToReview.length"
          icon="i-lucide-users"
          :title="$t('dashboard.reviews.empty.toReviewTitle')"
          :description="$t('dashboard.reviews.empty.toReviewDescription')"
          class="w-fit mx-auto py-8"
        />

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div
            v-for="user in usersToReview"
            :key="user.id"
            class="rounded-lg p-3 border border-gray-200 bg-gray-50 flex items-center justify-between"
          >
            <UUser
              :name="user.company_name"
              :description="
                user.full_name +
                ' • ' +
                (user?.role === 'vendor' ? 'Vendor' : 'Company')
              "
              :avatar="{ src: user.logo_url || undefined }"
              :to="
                user?.role === 'vendor'
                  ? `/vendors/${user.vendor_profile?.id}`
                  : `/companies/${user.id}`
              "
              target="_blank"
              :ui="{ avatar: 'rounded-lg border border-black' }"
            />
            <UButton
              :to="`/dashboard/reviews/create?user_id=${user.id}`"
              size="sm"
              icon="i-lucide-pen-line"
              class="bg-white"
            >
              {{ $t('dashboard.reviews.writeButton') }}
            </UButton>
          </div>
        </div>
      </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import { useBreakpoints } from '@vueuse/core';
import type { ReviewPublic, UserPublic } from '~/generated/api';
import {
  reviewsGetMyReviews,
  reviewsGetReviewsReceivedByMe,
  reviewsGetUsersToReview,
} from '~/generated/api';

const { t } = useI18n();

const breakpoints = useBreakpoints({
  sm: 640,
});

const tabs = computed(() => {
  const isSmallScreen = !breakpoints.sm.value;
  return [
    {
      slot: 'written',
      label: isSmallScreen ? t('dashboard.reviews.tabs.writtenShort') : t('dashboard.reviews.tabs.written'),
      icon: 'i-lucide-pen-line',
    },
    {
      slot: 'received',
      label: isSmallScreen ? t('dashboard.reviews.tabs.receivedShort') : t('dashboard.reviews.tabs.received'),
      icon: 'i-lucide-star',
    },
    {
      slot: 'to-review',
      label: isSmallScreen ? t('dashboard.reviews.tabs.toReviewShort') : t('dashboard.reviews.tabs.toReview'),
      icon: 'i-lucide-users',
    },
  ];
});

const loadingWritten = ref(false);
const loadingReceived = ref(false);
const loadingToReview = ref(false);

const writtenReviews = ref<ReviewPublic[]>([]);
const receivedReviews = ref<ReviewPublic[]>([]);
const usersToReview = ref<UserPublic[]>([]);

const toast = useToast();

async function loadWrittenReviews() {
  loadingWritten.value = true;
  const res = await reviewsGetMyReviews();
  loadingWritten.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to load reviews'),
      color: 'error',
    });
    return;
  }

  writtenReviews.value = res.data?.result || [];
}

async function loadReceivedReviews() {
  loadingReceived.value = true;
  const res = await reviewsGetReviewsReceivedByMe();
  loadingReceived.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to load reviews'),
      color: 'error',
    });
    return;
  }

  receivedReviews.value = res.data?.result || [];
}

async function loadUsersToReview() {
  loadingToReview.value = true;
  const res = await reviewsGetUsersToReview();
  loadingToReview.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to load users'),
      color: 'error',
    });
    return;
  }

  usersToReview.value = res.data || [];
}

onMounted(() => {
  loadWrittenReviews();
  loadReceivedReviews();
  loadUsersToReview();
});
</script>
