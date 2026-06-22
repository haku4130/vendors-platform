<template>
  <div
    class="flex flex-col md:flex-row border border-gray-200 rounded-2xl bg-white shadow-sm overflow-hidden"
  >
    <!-- Left panel -->
    <div
      class="flex flex-col p-6 md:w-72 shrink-0 border-b md:border-b-0 md:border-r border-gray-200"
    >
      <!-- Logo + name + contact -->
      <div class="mb-4">
        <UUser
          :to="`/vendors/${vendor.id}`"
          :name="vendor.user?.company_name"
          :description="vendor.user?.full_name"
          :avatar="{
            src: vendor.user?.logo_url || undefined,
            icon: 'i-lucide-building-2',
          }"
          :ui="{ avatar: 'rounded-xl border border-gray-200' }"
          size="3xl"
          class="text-start"
        />
      </div>

      <!-- Rating -->
      <div v-if="vendor.rating" class="flex items-center gap-2 mb-4">
        <span class="text-xl font-bold">{{ vendor.rating.toFixed(1) }}</span>
        <span class="text-gray-400">·</span>
        <span class="text-sm text-gray-500"
          >{{ vendor.reviewsCount }} {{ reviewsLabel }}</span
        >
      </div>
      <div v-else class="text-sm text-gray-400 mb-4">
        {{ $t("vendorCard.noReviews") }}
      </div>

      <hr class="border-gray-200 mb-4" />

      <!-- Специализация -->
      <p
        class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3"
      >
        {{ $t("vendorCard.specialization") }}
      </p>
      <div class="mb-2">
        <span
          v-for="(tag, index) in vendor.services"
          :key="tag.id"
          :class="[
            'inline-block mr-1.5 mb-1.5 px-3 py-1 rounded-full text-sm font-medium border',
            index === 0
              ? 'bg-blue-500 text-white border-sky-500'
              : 'bg-white text-gray-700 border-gray-300',
          ]"
        >
          {{ tag.label }}
        </span>
      </div>

      <hr class="border-gray-200 mb-4" />

      <!-- Stats -->
      <div class="space-y-3 mb-6">
        <div class="flex items-start gap-3">
          <UIcon name="i-lucide-tag" class="mt-0.5 text-gray-400 shrink-0" />
          <div>
            <p class="text-xs text-gray-400">
              {{ $t("vendorCard.minProject") }}
            </p>
            <p class="font-semibold">
              ${{ formatNumber(vendor.min_project_size) }}
            </p>
          </div>
        </div>
        <div v-if="vendor.user?.location" class="flex items-start gap-3">
          <UIcon
            name="i-lucide-map-pin"
            class="mt-0.5 text-gray-400 shrink-0"
          />
          <div>
            <p class="text-xs text-gray-400">{{ $t("vendorCard.location") }}</p>
            <p class="font-semibold">{{ vendor.user.location }}</p>
          </div>
        </div>
      </div>

      <div class="flex-1"></div>

      <!-- Buttons -->
      <div v-if="!incoming && currentProjectId" class="space-y-2">
        <UButton
          block
          color="neutral"
          variant="outline"
          :leading-icon="
            isShortlisted ? 'i-lucide-bookmark-check' : 'i-lucide-bookmark'
          "
          @click="toggleShortlist"
        >
          {{
            isShortlisted
              ? $t("vendorCard.inShortlist")
              : $t("vendorCard.addToShortlist")
          }}
        </UButton>
        <UButton
          block
          :disabled="alreadySent"
          trailing-icon="i-lucide-arrow-right"
          @click="handleVendorSelect(vendor.id)"
        >
          {{
            alreadySent
              ? $t("vendorCard.requestSent")
              : $t("vendorCard.requestProposal")
          }}
        </UButton>
      </div>

      <div v-else-if="incoming && currentProjectId">
        <UButton
          block
          trailing-icon="i-lucide-arrow-right"
          :to="`/dashboard/projects/${currentProjectId}/incoming-request/${requestId}`"
        >
          {{ $t("vendorCard.viewProposal") }}
        </UButton>
      </div>
    </div>

    <!-- Right panel -->
    <div class="flex-1 flex flex-col p-6 gap-5 min-w-0">
      <!-- Reviews -->
      <div>
        <p
          class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3"
        >
          {{ $t("vendorCard.clientReviews") }}
        </p>

        <div v-if="reviews.length > 0" class="space-y-3">
          <div
            v-for="review in displayedReviews"
            :key="review.id"
            class="border border-gray-200 rounded-xl p-4 bg-gray-50"
          >
            <div class="flex items-center gap-3 mb-3">
              <div
                class="w-9 h-9 rounded-lg flex items-center justify-center text-white text-xs font-bold shrink-0"
                :style="{
                  backgroundColor: avatarColor(review.author.company_name),
                }"
              >
                {{ initials(review.author.company_name) }}
              </div>
              <div>
                <p class="font-semibold text-sm leading-tight">
                  {{ review.author.company_name }}
                </p>
                <p class="text-xs text-gray-400">
                  {{ review.author.full_name }} ·
                  {{ review.author.role === "vendor" ? "Vendor" : "Company" }}
                </p>
              </div>
            </div>
            <p class="text-sm mb-2">{{ review.text }}</p>
            <p v-if="review.created_at" class="text-xs text-gray-400">
              {{ formatDateReview(review.created_at) }}
            </p>
          </div>
        </div>

        <UEmpty
          v-else
          icon="i-lucide-star"
          :title="$t('vendorCard.noClientReviews')"
          :description="$t('vendorCard.noClientReviewsDesc')"
          class="py-4"
        />
      </div>

      <!-- Why choose -->
      <div
        v-if="highlights.length > 0"
        class="border border-gray-200 rounded-xl p-4 bg-gray-50 shrink-0 mt-auto"
      >
        <p
          class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3"
        >
          {{ $t("vendorCard.whyChoose") }}
        </p>
        <ul class="space-y-2">
          <li
            v-for="point in highlights"
            :key="point"
            class="flex items-start gap-2 text-sm"
          >
            <UIcon
              name="i-lucide-check"
              class="text-green-500 mt-0.5 shrink-0"
            />
            <span>{{ point }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VendorProfilePublic, ReviewPublic } from "~/generated/api";

import {
  projectsSendProjectRequestCompany,
  requestsAcceptProject,
  requestsDeclineProject,
  reviewsGetReviewsForVendor,
  shortlistAddVendorToShortlist,
  shortlistRemoveVendorFromShortlist,
} from "~/generated/api";

const emit = defineEmits(["select", "add-shortlist", "shortlist-changed"]);

const {
  vendor,
  currentProjectId = null,
  requestId = null,
  initiallyShortlisted = false,
  incoming,
  onShortlistChanged = undefined,
} = defineProps<{
  vendor: VendorProfilePublic;
  currentProjectId?: string | null;
  requestId?: string | null;
  initiallyShortlisted?: boolean;
  incoming?: boolean;
  onShortlistChanged?: () => void;
}>();

const { t } = useI18n();

const isShortlisted = ref(initiallyShortlisted);
const alreadySent = ref(false);
const alreadyProcessed = ref();
const toast = useToast();

const reviewsLabel = computed(() => {
  const n = vendor.reviewsCount ?? 0;
  if (n === 1) return t("common.reviewCount.singular");
  if (n >= 2 && n <= 4) return t("common.reviewCount.few");
  return t("common.reviewCount.many");
});

function formatNumber(n: number): string {
  return n.toLocaleString("ru-RU");
}

function initials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

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
  const index = Math.abs(hash) % AVATAR_COLORS.length;
  return AVATAR_COLORS[index] ?? AVATAR_COLORS[0] ?? "#2563eb";
}

const highlights = computed(() => {
  const items: string[] = [];
  if (vendor.services.length > 0)
    items.push(
      t("vendorCard.specializationHighlight", {
        services: vendor.services
          .slice(0, 2)
          .map((s) => s.label)
          .join(", "),
      }),
    );
  if (vendor.user?.location)
    items.push(
      t("vendorCard.locationHighlight", { location: vendor.user.location }),
    );
  if (vendor.min_project_size)
    items.push(
      t("vendorCard.minProjectHighlight", {
        amount: formatNumber(vendor.min_project_size),
      }),
    );
  return items;
});

async function handleVendorSelect(vendorId: string) {
  if (!currentProjectId) {
    toast.add({
      title: "Проект не выбран",
      description: "Сначала создайте проект, чтобы отправить запрос.",
      color: "warning",
    });
    return;
  }

  const res = await projectsSendProjectRequestCompany({
    path: { project_id: currentProjectId, vendor_profile_id: vendorId },
  });

  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(
        res.error,
        "Не удалось отправить запрос",
      ),
      color: "error",
    });
    return;
  }

  toast.add({
    title: "Запрос отправлен",
    description: "Вендор получил уведомление.",
    color: "success",
  });
  alreadySent.value = true;
}

async function handleVendorAccept() {
  if (!requestId) {
    toast.add({
      title: "Ошибка",
      description: "Отсутствует ID запроса",
      color: "error",
    });
    return;
  }

  const res = await requestsAcceptProject({ path: { request_id: requestId } });

  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error, "Не удалось принять запрос"),
      color: "error",
    });
    return;
  }

  toast.add({
    title: "Запрос принят!",
    description: "Вендор получил уведомление.",
    color: "success",
  });
  alreadyProcessed.value = "Принято";
}

async function handleVendorDeny() {
  if (!requestId) {
    toast.add({
      title: "Ошибка",
      description: "Отсутствует ID запроса",
      color: "error",
    });
    return;
  }

  const res = await requestsDeclineProject({ path: { request_id: requestId } });

  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(
        res.error,
        "Не удалось отклонить запрос",
      ),
      color: "error",
    });
    return;
  }

  toast.add({
    title: "Запрос отклонён",
    description: "Вендор получил уведомление.",
    color: "success",
  });
  alreadyProcessed.value = "Отклонено";
}

async function toggleShortlist() {
  if (!currentProjectId) {
    toast.add({
      title: "Проект не выбран",
      description: "Сначала создайте проект, чтобы добавить в шорт-лист.",
      color: "warning",
    });
    return;
  }

  const wasShortlisted = isShortlisted.value;

  const res = wasShortlisted
    ? await shortlistRemoveVendorFromShortlist({
        path: { project_id: currentProjectId, vendor_profile_id: vendor.id },
      })
    : await shortlistAddVendorToShortlist({
        path: { project_id: currentProjectId, vendor_profile_id: vendor.id },
      });

  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(
        res.error,
        wasShortlisted
          ? "Не удалось удалить из шорт-листа"
          : "Не удалось добавить в шорт-лист",
      ),
      color: "error",
    });
    return;
  }

  isShortlisted.value = !wasShortlisted;

  if (wasShortlisted) {
    toast.add({
      title: "Удалено из шорт-листа",
      description: "Вендор удалён из вашего шорт-листа",
      color: "success",
      actions: [
        {
          label: "Отменить",
          color: "primary",
          onClick: async () => {
            await undoShortlistRemoval();
          },
        },
      ],
    });
  } else {
    toast.add({
      title: "Добавлено в шорт-лист",
      description: "Вендор добавлен в ваш шорт-лист",
      color: "success",
    });
  }

  emit("shortlist-changed", isShortlisted.value);
}

async function undoShortlistRemoval() {
  if (!currentProjectId) return;

  const res = await shortlistAddVendorToShortlist({
    path: { project_id: currentProjectId, vendor_profile_id: vendor.id },
  });

  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(
        res.error,
        "Не удалось восстановить вендора в шорт-листе",
      ),
      color: "error",
    });
    return;
  }

  isShortlisted.value = true;
  toast.add({
    title: "Восстановлено",
    description: "Вендор снова в шорт-листе",
    color: "success",
  });

  if (onShortlistChanged) onShortlistChanged();
  emit("shortlist-changed", isShortlisted.value);
}

const reviews = ref<ReviewPublic[]>([]);
const displayedReviews = computed(() => reviews.value.slice(0, 4));

async function loadReviews() {
  const res = await reviewsGetReviewsForVendor({
    path: { vendor_profile_id: vendor.id },
    query: { limit: 4 },
  });

  if (res.error) {
    console.error("Failed to load reviews:", res.error);
    return;
  }

  reviews.value = res.data.result || [];
}

onMounted(() => {
  loadReviews();
});
</script>
