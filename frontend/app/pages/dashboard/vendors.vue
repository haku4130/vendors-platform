<template>
  <div>
    <UContainer
      class="bg-vendor-gradient shadow-sm p-6 mb-6 rounded-2xl flex flex-col items-stretch gap-6"
    >
      <div class="flex items-center">
        <h1 class="text-xl font-semibold text-gray-900 leading-snug">
          Find the perfect partner for your project
        </h1>
      </div>

      <div class="bg-white rounded-xl flex flex-col gap-4 min-w-fit w-full p-6">
        <div class="flex flex-col gap-3 w-full">
          <UInputMenu
            v-model="searchServices"
            icon="i-lucide-search"
            placeholder="Search for Web Design, Web App Development, etc."
            :items="searchServicesMenuItems"
            value-key="value"
            multiple
            :disabled="searchServices.length >= 10 || !categories"
            :ui="{ base: 'rounded-lg', tagsItem: 'hidden' }"
            class="w-full"
          >
            <template v-if="!categories" #empty>
              <div class="text-center py-2 text-muted">
                Failed to load services
              </div>
            </template>
          </UInputMenu>

          <template v-if="searchServices.length > 0">
            <USeparator
              :label="`Selected Services (${searchServices.length}/10)`"
              class="my-2"
            />
            <div
              class="flex flex-wrap gap-2 border border-gray-300 rounded-lg p-3 min-h-[56px]"
            >
              <div
                v-for="service in searchServices"
                :key="service.id"
                class="px-3 py-1.5 rounded-sm inline-flex items-center gap-1.5 ring ring-inset ring-accented bg-elevated text-default text-xs"
              >
                <span class="truncate">{{ service.label }}</span>
                <button
                  class="inline-flex items-center rounded-xs text-dimmed hover:text-default hover:bg-accented/75 transition-colors"
                  @click="removeService(service)"
                >
                  <UIcon name="i-lucide-x" class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </template>

          <LocationSelector
            v-model="location"
            class="w-full"
            :ui="{ base: 'rounded-lg' }"
          />
        </div>

        <div class="flex gap-2">
          <UButton
            size="xl"
            :loading="isSearching"
            :disabled="searchServices.length === 0"
            class="w-full justify-center"
            @click="handleSearch"
          >
            Search
          </UButton>
          <UButton
            v-if="hasSearched"
            size="xl"
            variant="ghost"
            @click="handleClear"
          >
            Clear
          </UButton>
        </div>
      </div>
    </UContainer>

    <section v-if="hasSearched" class="bg-white rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">
          Search Results
          <span
            v-if="searchResults && !isSearching"
            class="text-muted font-normal"
          >
            ({{ searchResults.total }} found)
          </span>
        </h3>
      </div>

      <div
        v-if="isSearching"
        class="flex flex-col justify-center items-center py-12"
      >
        <UIcon
          name="i-lucide-loader-2"
          class="animate-spin text-4xl text-primary mb-4"
        />
        <p class="text-muted">Searching for vendors...</p>
      </div>

      <div
        v-else-if="searchResults && searchResults.result.length > 0"
        class="space-y-4"
      >
        <VendorCard
          v-for="vendor in searchResults.result"
          :key="vendor.id"
          :vendor="vendor"
        />
      </div>

      <div v-else class="text-center py-12">
        <UIcon name="i-lucide-search-x" class="text-6xl text-gray-300 mb-4" />
        <h4 class="text-xl font-semibold text-gray-700">No vendors found</h4>
        <p class="mt-2 text-muted mb-4">
          Try adjusting your search criteria or selecting different services.
        </p>
        <UButton variant="outline" @click="handleClear"> Clear Search </UButton>
      </div>
    </section>

    <!-- Empty state when no search performed yet -->
    <section
      v-else
      class="bg-white rounded-2xl p-12 shadow-sm text-center space-y-4"
    >
      <UIcon
        name="i-lucide-search"
        class="text-6xl text-gray-300 mx-auto mb-4"
      />
      <h3 class="text-xl font-semibold text-gray-700">
        Start searching for vendors
      </h3>
      <p class="text-muted max-w-md mx-auto">
        Select the services you need and optionally a location to find the
        perfect vendors for your project.
      </p>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { InputMenuItem } from '@nuxt/ui';
import { catalogListCategories, vendorsSearchVendors } from '~/generated/api';
import type {
  CategoryPublic,
  ServicePublicShort,
  VendorProfilePublic,
} from '~/generated/api';

definePageMeta({
  middleware: ['auth', 'company-only'],
  layout: 'dashboard',
});

const route = useRoute();
const router = useRouter();
const toast = useToast();

const location = ref<string | undefined>(undefined);
const searchServices = ref<ServicePublicShort[]>([]);
const isSearching = ref(false);
const hasSearched = ref(false);
const searchResults = ref<{
  result: VendorProfilePublic[];
  total: number;
} | null>(null);

// Load categories with error handling
const { data: categories, error: categoriesError } =
  await catalogListCategories();

if (categoriesError) {
  console.error('Failed to load categories:', categoriesError);
  toast.add({
    title: 'Failed to load services',
    description: 'Please refresh the page to try again',
    color: 'error',
  });
}

const searchServicesMenuItems = ref<InputMenuItem[]>(
  buildInputMenuItems(categories),
);

function buildInputMenuItems(
  categories: CategoryPublic[] | undefined,
): InputMenuItem[] {
  if (!categories) {
    return [];
  }

  const items: InputMenuItem[] = [];

  categories.forEach((cat) => {
    items.push({ type: 'label', label: cat.label });
    cat.services.forEach((service) => {
      items.push({
        label: service.label,
        value: service,
      });
    });
    items.push({ type: 'separator' });
  });

  // Remove the last separator
  if (items.length > 0) {
    items.pop();
  }

  return items;
}

// Initialize from query parameters if present
onMounted(async () => {
  try {
    const serviceIdsParam = route.query.service_ids;
    const locationParam = route.query.location;

    if (!categories) {
      console.warn(
        'Categories not loaded, skipping initialization from query params',
      );
      return;
    }

    // Load location from query if present
    if (locationParam && typeof locationParam === 'string') {
      location.value = locationParam;
    }

    // Load services from query if present
    if (serviceIdsParam && typeof serviceIdsParam === 'string') {
      const serviceIds = serviceIdsParam.split(',').filter((id) => id.trim());

      if (serviceIds.length === 0) {
        return;
      }

      // Find services that match the IDs
      const selectedServices: ServicePublicShort[] = [];
      categories.forEach((category) => {
        category.services.forEach((service) => {
          if (serviceIds.includes(service.id)) {
            selectedServices.push(service);
          }
        });
      });

      if (selectedServices.length > 0) {
        searchServices.value = selectedServices;
        // Automatically search if services were provided
        await handleSearch();
      } else {
        console.warn('No matching services found for IDs:', serviceIds);
        toast.add({
          title: 'Invalid search parameters',
          description: 'Some services could not be loaded',
          color: 'warning',
        });
      }
    }
  } catch (error) {
    console.error('Failed to initialize from query params:', error);
    toast.add({
      title: 'Initialization error',
      description: 'Failed to load search parameters',
      color: 'error',
    });
  }
});

function removeService(service: ServicePublicShort) {
  searchServices.value = searchServices.value.filter(
    (s) => s.id !== service.id,
  );
}

function handleClear() {
  searchServices.value = [];
  location.value = undefined;
  searchResults.value = null;
  hasSearched.value = false;
  // Clear query params
  router.replace({ query: {} });
}

async function handleSearch() {
  // Validation
  if (searchServices.value.length === 0) {
    toast.add({
      title: 'Please select services',
      description: 'Select at least one service to search for vendors',
      color: 'warning',
    });
    return;
  }

  if (!categories) {
    toast.add({
      title: 'Services not loaded',
      description: 'Please refresh the page and try again',
      color: 'error',
    });
    return;
  }

  isSearching.value = true;
  hasSearched.value = true;

  try {
    // Extract service IDs from selected services
    const serviceIds = searchServices.value.map((s) => s.id);

    // Validate service IDs
    if (serviceIds.some((id) => !id)) {
      throw new Error('Invalid service selected');
    }

    // Update URL with search params
    await router.replace({
      query: {
        service_ids: serviceIds.join(','),
        ...(location.value && { location: location.value }),
      },
    });

    // Call the API to search vendors
    const response = await vendorsSearchVendors({
      query: {
        service_ids: serviceIds,
        location: location.value || undefined,
        limit: 100,
      },
    });

    if (response.error) {
      const errorMessage = extractErrorMessage(
        response.error,
        'Failed to search vendors',
      );
      throw new Error(errorMessage);
    }

    if (!response.data) {
      throw new Error('No data received from server');
    }

    searchResults.value = response.data;

    if (searchResults.value.total === 0) {
      toast.add({
        title: 'No vendors found',
        description:
          'Try selecting different services or changing the location',
        color: 'info',
      });
    }
  } catch (error) {
    console.error('Search failed:', error);

    let errorDescription = 'An error occurred while searching for vendors';

    if (error instanceof Error) {
      errorDescription = error.message;
    } else if (typeof error === 'string') {
      errorDescription = error;
    }

    toast.add({
      title: 'Search failed',
      description: errorDescription,
      color: 'error',
    });

    searchResults.value = { result: [], total: 0 };
  } finally {
    isSearching.value = false;
  }
}
</script>
