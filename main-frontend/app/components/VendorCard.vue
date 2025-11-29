<template>
  <div
    class="flex flex-col md:flex-row justify-between gap-6 p-6 border border-black rounded-2xl bg-white"
  >
    <div class="flex flex-col md:w-fit">
      <div class="flex items-center gap-4 mb-3">
        <UAvatar
          src="https://github.com/haku4130.png"
          icon="i-lucide-camera"
          alt="Vendor logo"
          size="3xl"
        />
        <div>
          <h3 class="text-lg font-semibold">
            {{ data.name }}
          </h3>
        </div>
      </div>

      <div class="flex items-center gap-1 mb-3 px-2.5">
        <span class="font-semibold">{{ data.rating }}</span>
        <StarRating :rating="data.rating" />
        <span class="text-sm text-muted">({{ data.reviewsCount }})</span>
      </div>

      <div class="flex flex-wrap max-w-[16rem] gap-2 mb-4">
        <span
          v-for="tag in displayedTags"
          :key="tag"
          class="bg-gray-200 px-3 py-1 rounded-full text-sm font-medium"
        >
          {{ tag }}
        </span>
        <button
          v-if="extraTagsCount > 0"
          class="text-gray-700 text-sm font-medium hover:underline"
        >
          + {{ extraTagsCount }} more
        </button>
      </div>

      <div class="space-y-2 w-fit border-y border-gray-400 pt-3 pr-10 pl-2.5">
        <UTooltip :delay-duration="0" text="Minimum Project Price">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-tag" />
            <span>{{ data.minProjectSize }}</span>
          </div>
        </UTooltip>
        <UTooltip :delay-duration="0" text="Hourly Rate Range">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-clock" />
            <span>{{ data.rateRange }}</span>
          </div>
        </UTooltip>
        <UTooltip :delay-duration="0" text="Number of Employees">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-users" />
            <span>{{ data.employees }}</span>
          </div>
        </UTooltip>
        <div class="flex items-center gap-2 pb-3">
          <UIcon name="i-lucide-map-pin" />
          <span>{{ data.location }}</span>
        </div>
      </div>

      <UButton
        class="w-fit mt-2"
        variant="link"
        leading-icon="i-lucide-bookmark"
        size="sm"
        @click="$emit('add-shortlist', data.id)"
      >
        Add to Shortlist
      </UButton>
    </div>

    <div class="flex-1 flex flex-col justify-between text-start">
      <div>
        <h4 class="font-semibold mb-2">What clients have said</h4>

        <div class="grid lg:grid-cols-2 gap-3">
          <div
            v-for="review in displayedReviews"
            :key="review.id"
            class="border border-gray-300 rounded-lg p-3 bg-gray-50"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="font-semibold text-sm">{{ review.author }}</span>
              <div class="flex items-center gap-0.5 text-yellow-500 text-xs">
                <StarRating :rating="review.rating" />
              </div>
            </div>
            <p class="text-sm text-gray-700 leading-snug line-clamp-3">
              {{ review.text }}
            </p>
          </div>
        </div>

        <a
          v-if="data.reviewLink"
          :href="data.reviewLink"
          class="inline-block mt-3 text-blue-600 text-sm font-medium hover:underline"
        >
          See all Reviews
        </a>
      </div>

      <div class="flex justify-end mt-4">
        <UButton @click="selectVendor"> Request a quote </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(['select', 'add-shortlist']);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

// показываем только первые 3 тега
const displayedTags = computed(() => props.data.tags?.slice(0, 3) || []);
const extraTagsCount = computed(() =>
  props.data.tags?.length > 3 ? props.data.tags.length - 3 : 0
);

// показываем только 3 последних отзыва
const displayedReviews = computed(() => props.data.reviews?.slice(0, 3) || []);

// при выборе вендора
function selectVendor() {
  emit('select', props.data);
}
</script>
