<template>
  <div
    class="flex flex-col md:flex-row justify-between gap-6 p-6 border border-gray-300 rounded-2xl bg-white shadow-md"
  >
    <div class="flex flex-col md:w-fit">
      <div class="mb-3">
        <UUser
          :to="`/vendors/${vendor.id}`"
          :name="vendor.user?.company_name"
          :description="vendor.user?.full_name"
          :avatar="{
            src: vendor.user?.logo_url || undefined,
            icon: 'i-lucide-camera',
          }"
          :ui="{ avatar: 'rounded-lg border border-black' }"
          size="3xl"
          class="text-start"
        />
      </div>

      <div v-if="vendor.rating" class="flex items-center gap-1 mb-3">
        <span class="font-semibold">{{ vendor.rating }}</span>
        <StarRating :rating="vendor.rating" />
        <span class="text-sm text-muted">({{ vendor.reviewsCount }})</span>
      </div>
      <div v-else class="flex items-center gap-1 mb-3">
        <span class="font-semibold">No rating yet</span>
      </div>

      <div class="flex flex-wrap max-w-[16rem] gap-2 mb-4">
        <span
          v-for="tag in vendor.services"
          :key="tag.id"
          class="bg-gray-200 px-3 py-1 rounded-full text-sm font-medium"
        >
          {{ tag.label }}
        </span>
      </div>

      <hr />

      <div class="space-y-2 w-full border-gray-400 pt-3">
        <UTooltip :delay-duration="0" text="Minimum Project Price">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-tag" />
            <span>${{ vendor.min_project_size }}</span>
          </div>
        </UTooltip>
        <UTooltip :delay-duration="0" text="Avarage Hourly Rate">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-clock" />
            <span>${{ vendor.avg_hourly_rate }}</span>
          </div>
        </UTooltip>
        <UTooltip :delay-duration="0" text="Number of Employees">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-users" />
            <span>{{ vendor.employee_count }} people</span>
          </div>
        </UTooltip>
        <div class="flex items-center gap-2 pb-3">
          <UIcon name="i-lucide-map-pin" />
          <span>{{ vendor.user?.location }}</span>
        </div>
      </div>

      <hr v-if="!incoming" />

      <UButton
        v-if="!incoming"
        class="w-fit mt-2 px-0"
        variant="link"
        :leading-icon="
          isShortlisted ? 'i-lucide-bookmark-check' : 'i-lucide-bookmark'
        "
        size="sm"
        @click="toggleShortlist"
      >
        {{ isShortlisted ? 'Shortlisted' : 'Add to Shortlist' }}
      </UButton>
    </div>

    <div class="flex-1 flex flex-col justify-between text-start">
      <div v-if="reviews.length > 0">
        <h4 class="font-semibold mb-2">What clients have said</h4>

        <div class="grid xl:grid-cols-2 gap-3">
          <div
            v-for="review in displayedReviews"
            :key="review.id"
            class="border border-gray-300 rounded-lg p-3 bg-gray-50"
          >
            <ReviewCard :review="review" />
          </div>
        </div>
      </div>

      <UEmpty
        v-else
        icon="i-lucide-star"
        title="No reviews yet"
        description="This vendor has not received any reviews yet."
        class="h-full"
      />

      <div class="flex justify-end mt-4">
        <UButton
          v-if="!incoming"
          :disabled="alreadySent"
          @click="handleVendorSelect(vendor.id)"
        >
          {{ alreadySent ? 'Sent!' : 'Request a quote' }}
        </UButton>

        <div v-else-if="!alreadyProcessed" class="flex gap-2">
          <UButton variant="solid" size="lg" @click="handleVendorAccept">
            Accept
          </UButton>
          <UButton size="lg" @click="handleVendorDeny"> Deny </UButton>
        </div>

        <div v-else>
          <UButton disabled>
            {{ alreadyProcessed }}
          </UButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VendorProfilePublic, ReviewPublic } from '~/generated/api';

import {
  projectsSendProjectRequestCompany,
  requestsAcceptProject,
  requestsDeclineProject,
  reviewsGetReviewsForVendor,
  shortlistAddVendorToShortlist,
  shortlistRemoveVendorFromShortlist,
} from '~/generated/api';

const emit = defineEmits(['select', 'add-shortlist', 'shortlist-changed']);

const {
  vendor,
  currentProjectId,
  requestId,
  initiallyShortlisted = false,
  incoming,
} = defineProps<{
  vendor: VendorProfilePublic;
  currentProjectId: string;
  requestId: string;
  initiallyShortlisted?: boolean;
  incoming?: boolean;
}>();

const isShortlisted = ref(initiallyShortlisted);
const alreadySent = ref(false);
const alreadyProcessed = ref();
const toast = useToast();

async function handleVendorSelect(vendorId: string) {
  const res = await projectsSendProjectRequestCompany({
    path: {
      project_id: currentProjectId,
      vendor_profile_id: vendorId,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to send request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Request sent',
    description: 'The vendor has been notified.',
    color: 'success',
  });
  alreadySent.value = true;
}

async function handleVendorAccept() {
  const res = await requestsAcceptProject({
    path: {
      request_id: requestId,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to accept request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Request accepted!',
    description: 'The vendor has been notified.',
    color: 'success',
  });
  alreadyProcessed.value = 'Accepted';
}

async function handleVendorDeny() {
  const res = await requestsDeclineProject({
    path: {
      request_id: requestId,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to decline request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Request declined',
    description: 'The vendor has been notified.',
    color: 'success',
  });
  alreadyProcessed.value = 'Denied';
}

async function toggleShortlist() {
  const res = isShortlisted.value
    ? await shortlistRemoveVendorFromShortlist({
        path: {
          project_id: currentProjectId,
          vendor_profile_id: vendor.id,
        },
      })
    : await shortlistAddVendorToShortlist({
        path: {
          project_id: currentProjectId,
          vendor_profile_id: vendor.id,
        },
      });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(
        res.error,
        isShortlisted.value
          ? 'Failed to remove from shortlist'
          : 'Failed to add to shortlist',
      ),
      color: 'error',
    });
    return;
  }

  isShortlisted.value = !isShortlisted.value;
  toast.add({
    title: 'Success',
    description: isShortlisted.value
      ? 'Added to shortlist'
      : 'Removed from shortlist',
    color: 'success',
  });
  emit('shortlist-changed', isShortlisted.value);
}

const reviews = ref<ReviewPublic[]>([]);

const displayedReviews = computed(() => reviews.value.slice(0, 4));

async function loadReviews() {
  const res = await reviewsGetReviewsForVendor({
    path: {
      vendor_profile_id: vendor.id,
    },
    query: {
      limit: 4,
    },
  });

  if (res.error) {
    console.error('Failed to load reviews:', res.error);
    return;
  }

  reviews.value = res.data.result || [];
}

onMounted(() => {
  loadReviews();
});
</script>
