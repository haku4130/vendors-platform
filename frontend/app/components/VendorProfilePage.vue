<template>
  <div class="space-y-8">
    <!-- Header Section -->
    <UCard class="bg-vendor-gradient shadow-lg">
      <div class="flex flex-col md:flex-row gap-6 items-start md:items-center">
        <NuxtImg
          :src="vendor.user?.logo_url || '/placeholder-avatar.png'"
          class="rounded-lg border-2 border-white shadow-md md:w-48 md:h-48 object-cover"
        />

        <div class="flex-1">
          <div class="flex items-center">
            <h1 class="text-3xl font-semibold">
              {{ vendor.user?.company_name }}
            </h1>
          </div>

          <div class="flex mb-4 sm:mb-2">
            <span class="text-sm align-middle text-muted">
              {{ vendor.user?.full_name }}
            </span>
          </div>

          <div class="flex flex-wrap gap-x-4 gap-y-1 text-sm mb-4">
            <div v-if="vendor.user?.location" class="flex items-center gap-1">
              <UIcon name="i-lucide-map-pin" class="w-4 h-4" />
              <span>{{ vendor.user.location }}</span>
            </div>
            <div class="flex items-center gap-1">
              <UIcon name="i-lucide-calendar" class="w-4 h-4" />
              <span>Founded {{ vendor.founded_year }}</span>
            </div>
            <div v-if="vendor.company_website" class="flex items-center gap-1">
              <UButton
                :href="
                  vendor.company_website?.startsWith('http')
                    ? vendor.company_website
                    : `https://${vendor.company_website}`
                "
                target="_blank"
                variant="link"
                leading-icon="i-lucide-globe"
                trailing-icon="i-lucide-external-link"
                :ui="{ leadingIcon: 'w-4 h-4', trailingIcon: 'w-4 h-4' }"
                class="px-0"
              >
                Website
              </UButton>
            </div>
            <div
              v-if="vendor.rating"
              class="w-fit flex items-center gap-2 bg-white/30 px-3 py-1 rounded-full"
            >
              <span class="font-semibold">{{ vendor.rating.toFixed(1) }}</span>
              <StarRating :rating="vendor.rating" />
              <span class="text-sm text-muted"
                >({{ vendor.reviewsCount || 0 }})</span
              >
            </div>
          </div>
        </div>
      </div>
    </UCard>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-6">
        <!-- About Section -->
        <UCard>
          <template #header>
            <h2 class="text-xl font-semibold">About</h2>
          </template>
          <template #default>
            <p class="leading-relaxed whitespace-pre-line">
              {{ vendor.description }}
            </p>
          </template>
        </UCard>

        <!-- Services Section -->
        <UCard>
          <template #header>
            <h2 class="text-xl font-semibold">Services</h2>
          </template>
          <template #default>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="service in vendor.services"
                :key="service.id"
                class="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-full text-sm font-medium transition-colors"
              >
                {{ service.label }}
              </span>
            </div>
          </template>
        </UCard>

        <!-- Reviews Section -->
        <UCard>
          <template #header>
            <div class="flex justify-between items-center">
              <h2 class="text-xl font-semibold">Reviews</h2>
              <span v-if="vendor.reviewsCount" class="text-sm text-muted">
                {{ vendor.reviewsCount }} total review(s)
              </span>
            </div>
          </template>
          <template #default>
            <div v-if="reviews.length > 0" class="space-y-4">
              <div
                v-for="review in reviews"
                :key="review.id"
                class="border border-gray-200 rounded-lg p-4 bg-gray-50"
              >
                <div class="flex items-start justify-between mb-2">
                  <div>
                    <p class="font-semibold text-sm">
                      {{
                        review.author?.full_name ||
                        review.author?.company_name ||
                        'Anonymous'
                      }}
                    </p>
                    <p class="text-xs text-muted">
                      {{ formatDate(review.created_at) }}
                    </p>
                  </div>
                  <div class="flex items-center gap-1 text-yellow-500">
                    <StarRating :rating="review.rating" />
                  </div>
                </div>
                <p class="text-sm leading-relaxed">
                  {{ review.text }}
                </p>
              </div>

              <div v-if="hasMoreReviews" class="text-center pt-4">
                <UButton
                  variant="outline"
                  :loading="loadingMore"
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
              description="This vendor has not received any reviews yet."
            />
          </template>
        </UCard>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Key Information -->
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Key Information</h3>
          </template>
          <template #default>
            <div class="space-y-4">
              <div>
                <p class="text-sm text-muted mb-1">Minimum Project Size</p>
                <p class="text-lg font-semibold">
                  ${{ vendor.min_project_size }}
                </p>
              </div>
              <div>
                <p class="text-sm text-muted mb-1">Average Hourly Rate</p>
                <p class="text-lg font-semibold">
                  ${{ vendor.avg_hourly_rate }}
                </p>
              </div>
              <div>
                <p class="text-sm text-muted mb-1">Employees</p>
                <p class="text-lg font-semibold">
                  {{ vendor.employee_count }} people
                </p>
              </div>
              <div>
                <p class="text-sm text-muted mb-1">Turnover</p>
                <p class="text-lg font-semibold">
                  ${{ formatTurnover(vendor.turnover) }}
                </p>
              </div>
            </div>
          </template>
        </UCard>

        <!-- Contact Information -->
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Contact</h3>
          </template>
          <template #default>
            <div class="space-y-3">
              <div>
                <p class="text-sm text-muted mb-1">Sales Email</p>
                <a
                  :href="`mailto:${vendor.sales_email}`"
                  class="text-blue-600 hover:underline break-all"
                >
                  {{ vendor.sales_email }}
                </a>
              </div>
              <div>
                <p class="text-sm text-muted mb-1">Phone</p>
                <a
                  :href="`tel:${vendor.admin_contact_phone}`"
                  class="text-blue-600 hover:underline"
                >
                  {{ vendor.admin_contact_phone }}
                </a>
              </div>
            </div>
          </template>
        </UCard>

        <!-- Main Goal -->
        <UCard v-if="vendor.main_goal">
          <template #header>
            <h3 class="text-lg font-semibold">Main Goal</h3>
          </template>
          <template #default>
            <p class="">{{ vendor.main_goal }}</p>
          </template>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VendorProfilePublic, ReviewPublic } from '~/generated/api';
import { reviewsGetReviewsForVendor } from '~/generated/api';

const props = defineProps<{
  vendor: VendorProfilePublic;
}>();

const reviews = ref<ReviewPublic[]>([]);
const loadingMore = ref(false);
const skip = ref(0);
const limit = 10;
const totalReviews = ref<number | null>(null);

const hasMoreReviews = computed(() => {
  return (
    totalReviews.value !== null && reviews.value.length < totalReviews.value
  );
});

async function loadReviews() {
  const res = await reviewsGetReviewsForVendor({
    path: {
      vendor_profile_id: props.vendor.id,
    },
    query: {
      skip: 0,
      limit: limit,
    },
  });

  if (res.error) {
    console.error('Failed to load reviews:', res.error);
    return;
  }

  reviews.value = res.data.result || [];
  totalReviews.value = res.data.total;
}

async function loadMoreReviews() {
  if (loadingMore.value || !hasMoreReviews.value) return;

  loadingMore.value = true;
  skip.value = reviews.value.length;

  const res = await reviewsGetReviewsForVendor({
    path: {
      vendor_profile_id: props.vendor.id,
    },
    query: {
      skip: skip.value,
      limit: limit,
    },
  });

  loadingMore.value = false;

  if (res.error) {
    console.error('Failed to load more reviews:', res.error);
    return;
  }

  reviews.value.push(...(res.data.result || []));
}

function formatDate(dateString?: string): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function formatTurnover(turnover: number): string {
  if (turnover >= 1000000) {
    return `${(turnover / 1000000).toFixed(1)}M`;
  }
  if (turnover >= 1000) {
    return `${(turnover / 1000).toFixed(1)}K`;
  }
  return turnover.toString();
}

onMounted(() => {
  loadReviews();
});
</script>
