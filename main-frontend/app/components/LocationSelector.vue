<template>
  <UInputMenu
    v-model="model"
    placeholder="Select city"
    :icon="icon ?? undefined"
    :items="locations"
    :loading="isFetchingLocations"
    class="w-full"
    size="lg"
    :ui="{ trailingIcon: 'text-normal', leadingIcon: 'text-muted' }"
    @update:search-term="query = $event"
  >
    <template #empty>Search for location</template>
  </UInputMenu>
</template>

<script setup lang="ts">
import { useDebounceFn } from '@vueuse/core';

interface NominatimResult {
  display_name: string;
  name: string;
  address?: {
    city?: string;
    town?: string;
    village?: string;
    country?: string;
  };
}

const model = defineModel<string>();
const { icon = 'i-lucide-map-pin' } = defineProps<{
  icon?: string | null;
}>();

const query = ref('');
const locations = ref<string[]>([]);
const isFetchingLocations = ref(false);

const MIN_QUERY_LENGTH = 1;
const LOCATION_FETCH_DEBOUNCE = 100;

let locationAbortController: AbortController | null = null;
let lastFetchedLocationTerm = '';

async function fetchLocations(searchTerm: string) {
  const normalizedTerm = searchTerm.trim();
  if (normalizedTerm.length < MIN_QUERY_LENGTH) {
    locations.value = [];
    isFetchingLocations.value = false;
    return;
  }

  if (locationAbortController) {
    locationAbortController.abort();
    locationAbortController = null;
  }

  if (normalizedTerm === lastFetchedLocationTerm) {
    isFetchingLocations.value = false;
    return;
  }

  isFetchingLocations.value = true;
  const controller = new AbortController();
  locationAbortController = controller;

  try {
    const data = await $fetch<NominatimResult[]>(
      'https://nominatim.openstreetmap.org/search',
      {
        signal: controller.signal,
        query: {
          format: 'json',
          q: normalizedTerm,
          limit: 5,
          addressdetails: 1,
        },
        headers: {
          'Accept-Language': 'en',
          'User-Agent': 'VendorPlatform/1.0 (vendor-platform.local)',
        },
      }
    );

    if (query.value.trim() !== normalizedTerm) {
      return;
    }

    locations.value = Array.from(
      new Set(
        data.map((loc) => {
          const address = loc.address || {};
          const city =
            address.city || address.town || address.village || loc.name || '';
          const country = address.country || '';
          return city && country ? `${city}, ${country}` : loc.display_name;
        })
      )
    );

    lastFetchedLocationTerm = normalizedTerm;
  } catch (error) {
    if (!controller.signal.aborted) {
      console.warn('Failed to fetch locations', error);
      locations.value = [];
    }
  } finally {
    if (locationAbortController === controller) {
      locationAbortController = null;
    }

    if (query.value.trim() === normalizedTerm) {
      isFetchingLocations.value = false;
    }
  }
}

const debouncedFetch = useDebounceFn(fetchLocations, LOCATION_FETCH_DEBOUNCE);

watch(query, debouncedFetch);
</script>
