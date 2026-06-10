<template>
  <div class="max-w-5xl mx-auto space-y-6">
    <!-- Hero -->
    <div
      class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden"
    >
      <div class="h-24 bg-gradient-to-r from-blue-500 to-blue-400" />
      <div class="px-8 pb-8">
        <div class="flex items-end gap-5 -mt-10 mb-5">
          <div
            class="w-20 h-20 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shrink-0 border-4 border-white shadow-md"
            :style="{
              backgroundColor: avatarColor(vendor.user?.company_name ?? ''),
            }"
          >
            {{ initials(vendor.user?.company_name ?? "") }}
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4"
        >
          <div class="min-w-0">
            <h1 class="text-2xl font-bold text-gray-900">
              {{ vendor.user?.company_name }}
            </h1>
            <p class="text-sm text-gray-500 mt-0.5">
              {{ vendor.user?.full_name }}
            </p>

            <div class="flex flex-wrap items-center gap-3 mt-3">
              <div
                v-if="vendor.user?.location"
                class="flex items-center gap-1.5 text-sm text-gray-500"
              >
                <UIcon name="i-lucide-map-pin" class="w-4 h-4 shrink-0" />
                <span>{{ vendor.user.location }}</span>
              </div>
              <div
                v-if="vendor.founded_year"
                class="flex items-center gap-1.5 text-sm text-gray-500"
              >
                <UIcon name="i-lucide-calendar" class="w-4 h-4 shrink-0" />
                <span>{{
                  t("vendorProfile.foundedIn", { year: vendor.founded_year })
                }}</span>
              </div>
              <a
                v-if="vendor.company_website"
                :href="
                  vendor.company_website.startsWith('http')
                    ? vendor.company_website
                    : `https://${vendor.company_website}`
                "
                target="_blank"
                class="flex items-center gap-1.5 text-sm text-blue-600 hover:underline"
              >
                <UIcon name="i-lucide-globe" class="w-4 h-4 shrink-0" />
                <span>{{ t("common.website") }}</span>
                <UIcon name="i-lucide-external-link" class="w-3 h-3" />
              </a>

              <div
                v-if="vendor.rating"
                class="flex items-center gap-1.5 px-3 py-1 bg-amber-50 border border-amber-100 rounded-full"
              >
                <UIcon
                  name="i-lucide-star"
                  class="w-3.5 h-3.5 text-amber-400 fill-amber-400"
                />
                <span class="text-sm font-semibold text-amber-700">{{
                  vendor.rating.toFixed(1)
                }}</span>
                <span class="text-xs text-amber-600"
                  >· {{ vendor.reviewsCount }}
                  {{ reviewsLabel(vendor.reviewsCount ?? 0) }}</span
                >
              </div>
              <div
                v-else
                class="flex items-center gap-1.5 px-3 py-1 bg-gray-50 border border-gray-200 rounded-full"
              >
                <UIcon name="i-lucide-star" class="w-3.5 h-3.5 text-gray-400" />
                <span class="text-sm text-gray-500">{{
                  t("common.noRatings")
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Body: main + sidebar -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main -->
      <div class="lg:col-span-2 space-y-6">
        <!-- About -->
        <div
          v-if="vendor.description"
          class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6"
        >
          <h2 class="text-base font-semibold mb-3">
            {{ t("vendorProfile.about") }}
          </h2>
          <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
            {{ vendor.description }}
          </p>
        </div>

        <!-- Main goal -->
        <div
          v-if="vendor.main_goal"
          class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6"
        >
          <h2 class="text-base font-semibold mb-3">
            {{ t("vendorProfile.mainGoal") }}
          </h2>
          <p class="text-sm text-gray-700 leading-relaxed">
            {{ vendor.main_goal }}
          </p>
        </div>

        <!-- Services -->
        <div
          v-if="vendor.services.length"
          class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6"
        >
          <h2 class="text-base font-semibold mb-3">
            {{ t("vendorProfile.specialization") }}
          </h2>
          <div>
            <span
              v-for="(svc, i) in vendor.services"
              :key="svc.id"
              :class="[
                'inline-block mr-1.5 mb-1.5 px-3 py-1 rounded-full text-sm font-medium border',
                i === 0
                  ? 'bg-blue-500 text-white border-blue-500'
                  : 'bg-white text-gray-700 border-gray-300',
              ]"
            >
              {{ svc.label }}
            </span>
          </div>
        </div>

        <!-- Reviews -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <div class="flex items-center justify-between mb-5">
            <h2 class="text-base font-semibold">{{ t("common.reviews") }}</h2>
            <span v-if="totalReviews" class="text-sm text-gray-400">
              {{ totalReviews }} {{ reviewsLabel(totalReviews) }}
            </span>
          </div>

          <div v-if="reviews.length > 0" class="space-y-4">
            <div class="grid lg:grid-cols-2 gap-3">
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
                :loading="loadingMore"
                @click="loadMoreReviews"
              >
                {{ t("common.loadMore") }}
              </UButton>
            </div>
          </div>
          <UEmpty
            v-else
            icon="i-lucide-star"
            :title="t('vendorProfile.noReviews')"
            :description="t('vendorProfile.noReviewsDesc')"
            class="py-6"
          />
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Stats -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <h3 class="text-base font-semibold mb-4">
            {{ t("vendorProfile.stats") }}
          </h3>
          <div class="space-y-4">
            <div class="flex items-start gap-3">
              <div
                class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-tag" class="w-4 h-4 text-blue-500" />
              </div>
              <div>
                <p class="text-xs text-gray-400">
                  {{ t("vendorProfile.minProject") }}
                </p>
                <p class="font-semibold text-sm">
                  ${{ formatNumber(vendor.min_project_size) }}
                </p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div
                class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-clock" class="w-4 h-4 text-blue-500" />
              </div>
              <div>
                <p class="text-xs text-gray-400">
                  {{ t("vendorProfile.hourlyRate") }}
                </p>
                <p class="font-semibold text-sm">
                  ${{ formatNumber(vendor.avg_hourly_rate) }}
                </p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div
                class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-users" class="w-4 h-4 text-blue-500" />
              </div>
              <div>
                <p class="text-xs text-gray-400">
                  {{ t("vendorProfile.team") }}
                </p>
                <p class="font-semibold text-sm">
                  {{
                    t("vendorProfile.employees", {
                      count: vendor.employee_count,
                    })
                  }}
                </p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div
                class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0"
              >
                <UIcon
                  name="i-lucide-trending-up"
                  class="w-4 h-4 text-blue-500"
                />
              </div>
              <div>
                <p class="text-xs text-gray-400">
                  {{ t("vendorProfile.turnover") }}
                </p>
                <p class="font-semibold text-sm">
                  ${{ formatTurnover(vendor.turnover) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <h3 class="text-base font-semibold mb-4">
            {{ t("common.contacts") }}
          </h3>
          <div class="space-y-3">
            <div v-if="vendor.sales_email" class="flex items-start gap-3">
              <div
                class="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-mail" class="w-4 h-4 text-gray-500" />
              </div>
              <div class="min-w-0">
                <p class="text-xs text-gray-400">Email</p>
                <a
                  :href="`mailto:${vendor.sales_email}`"
                  class="text-sm text-blue-600 hover:underline break-all"
                >
                  {{ vendor.sales_email }}
                </a>
              </div>
            </div>
            <div
              v-if="vendor.admin_contact_phone"
              class="flex items-start gap-3"
            >
              <div
                class="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center shrink-0"
              >
                <UIcon name="i-lucide-phone" class="w-4 h-4 text-gray-500" />
              </div>
              <div>
                <p class="text-xs text-gray-400">{{ t("common.phone") }}</p>
                <a
                  :href="`tel:${vendor.admin_contact_phone}`"
                  class="text-sm text-blue-600 hover:underline"
                >
                  {{ vendor.admin_contact_phone }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VendorProfilePublic, ReviewPublic } from "~/generated/api";
import { reviewsGetReviewsForVendor } from "~/generated/api";

const props = defineProps<{
  vendor: VendorProfilePublic;
}>();

const { t } = useI18n();

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
  if (n === 1) return t("common.reviewCount.singular");
  if (n >= 2 && n <= 4) return t("common.reviewCount.few");
  return t("common.reviewCount.many");
}

function formatNumber(n: number): string {
  return n.toLocaleString("ru-RU");
}

function formatTurnover(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + "M";
  if (n >= 1_000) return (n / 1_000).toFixed(1) + "K";
  return n.toString();
}

const reviews = ref<ReviewPublic[]>([]);
const loadingMore = ref(false);
const totalReviews = ref<number>(0);

const hasMoreReviews = computed(
  () => reviews.value.length < totalReviews.value,
);

async function loadReviews() {
  const res = await reviewsGetReviewsForVendor({
    path: { vendor_profile_id: props.vendor.id },
    query: { skip: 0, limit: 6 },
  });
  if (res.error) return;
  reviews.value = res.data.result || [];
  totalReviews.value = res.data.total;
}

async function loadMoreReviews() {
  if (loadingMore.value || !hasMoreReviews.value) return;
  loadingMore.value = true;
  const res = await reviewsGetReviewsForVendor({
    path: { vendor_profile_id: props.vendor.id },
    query: { skip: reviews.value.length, limit: 6 },
  });
  loadingMore.value = false;
  if (res.error) return;
  reviews.value.push(...(res.data.result || []));
}

onMounted(() => {
  loadReviews();
});
</script>
