<template>
  <div
    class="flex flex-col bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow overflow-hidden"
  >
    <div class="p-5 pb-4">
      <div class="flex items-start justify-between gap-2 mb-3">
        <div class="flex items-center gap-3 min-w-0">
          <div
            class="w-10 h-10 rounded-xl flex items-center justify-center text-white text-sm font-bold shrink-0"
            :style="{
              backgroundColor: avatarColor(proposal.project.owner.company_name),
            }"
          >
            {{ initials(proposal.project.owner.company_name) }}
          </div>
          <div class="min-w-0">
            <p class="font-semibold text-sm truncate">
              {{ proposal.project.owner.company_name }}
            </p>
            <p class="text-xs text-gray-400 truncate">
              {{ proposal.project.owner.full_name }}
            </p>
          </div>
        </div>

        <span
          :class="[
            'shrink-0 px-2.5 py-1 rounded-full text-xs font-semibold',
            statusStyle.bg,
            statusStyle.text,
          ]"
        >
          {{ statusStyle.label }}
        </span>
      </div>

      <h3 class="font-semibold text-base leading-snug line-clamp-2 mb-3">
        {{ proposal.project.title }}
      </h3>

      <div v-if="proposal.project.services?.length" class="mb-3">
        <span
          v-for="svc in proposal.project.services.slice(0, 3)"
          :key="svc.id"
          class="inline-block mr-1.5 mb-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100"
        >
          {{ svc.label }}
        </span>
        <span
          v-if="proposal.project.services.length > 3"
          class="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-500"
        >
          +{{ proposal.project.services.length - 3 }}
        </span>
      </div>
    </div>

    <div class="px-5 pb-4 space-y-2">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UIcon
          name="i-lucide-banknote"
          class="w-4 h-4 text-gray-400 shrink-0"
        />
        <span class="font-medium"
          >${{ formatBudget(proposal.project.budget) }}</span
        >
      </div>
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UIcon
          name="i-lucide-calendar"
          class="w-4 h-4 text-gray-400 shrink-0"
        />
        <span>{{ proposal.project.start_date }}</span>
      </div>
      <div
        v-if="proposal.project.location"
        class="flex items-center gap-2 text-sm text-gray-600"
      >
        <UIcon name="i-lucide-map-pin" class="w-4 h-4 text-gray-400 shrink-0" />
        <span>{{ proposal.project.location }}</span>
      </div>
    </div>

    <div class="mt-auto px-5 pb-5 pt-3 border-t border-gray-100 space-y-2">
      <p class="text-xs text-gray-400">
        {{
          $t("proposalCard.sentAt", {
            date: formatDateReview(proposal.created_at),
          })
        }}
      </p>
      <UButton
        block
        variant="outline"
        color="primary"
        trailing-icon="i-lucide-arrow-right"
        :to="`/dashboard/proposals/${proposal.id}`"
      >
        {{ $t("proposalCard.viewBrief") }}
      </UButton>
      <UButton
        v-if="proposal.status === 'accepted'"
        block
        variant="outline"
        color="neutral"
        trailing-icon="i-lucide-mail"
        :to="`mailto:${proposal.project.owner.email}`"
        target="_blank"
      >
        {{ $t("proposalCard.contactClient") }}
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProjectRequestPublicProjectFull } from "~/generated/api";

const { proposal } = defineProps<{
  proposal: ProjectRequestPublicProjectFull;
}>();

const { t } = useI18n();

const STATUS_STYLES = computed(() => ({
  sent: {
    label: t("proposalCard.statusSent"),
    bg: "bg-amber-50",
    text: "text-amber-700",
  },
  accepted: {
    label: t("proposalCard.statusAccepted"),
    bg: "bg-green-50",
    text: "text-green-700",
  },
  declined: {
    label: t("proposalCard.statusDeclined"),
    bg: "bg-red-50",
    text: "text-red-600",
  },
}));

const statusStyle = computed(
  () => STATUS_STYLES.value[proposal.status] ?? STATUS_STYLES.value.sent,
);

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
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
}

function initials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

function formatBudget(n: number): string {
  if (n >= 1_000_000)
    return (n / 1_000_000).toFixed(n % 1_000_000 === 0 ? 0 : 1) + "M";
  if (n >= 1_000) return (n / 1_000).toFixed(n % 1_000 === 0 ? 0 : 1) + "K";
  return n.toLocaleString("ru-RU");
}
</script>
