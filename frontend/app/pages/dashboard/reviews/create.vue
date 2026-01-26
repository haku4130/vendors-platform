<template>
  <UContainer>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      class="mb-4"
      @click="navigateTo('/dashboard/reviews')"
    >
      Back to Reviews
    </UButton>

    <div class="max-w-2xl mx-auto">
      <div v-if="loading" class="text-center py-12">
        <UIcon name="i-lucide-loader-2" class="w-8 h-8 animate-spin mx-auto" />
      </div>

      <div v-else-if="!reviewedUser" class="text-center py-12">
        <UEmpty
          icon="i-lucide-alert-circle"
          title="User not found"
          description="The user you're trying to review doesn't exist."
        />
      </div>

      <div v-else class="bg-white rounded-2xl p-6 shadow-sm space-y-6">
        <h1 class="text-2xl font-semibold">Write a Review</h1>

        <UUser
          :name="reviewedUser.company_name"
          :description="
            reviewedUser.full_name +
            ' • ' +
            (reviewedUser?.role === 'vendor' ? 'Vendor' : 'Company')
          "
          :avatar="{ src: reviewedUser.logo_url || undefined }"
          :to="
            reviewedUser?.role === 'vendor'
              ? `/vendors/${reviewedUser.vendor_profile?.id}`
              : `/companies/${reviewedUser.id}`
          "
          target="_blank"
          :ui="{ avatar: 'rounded-lg border border-black' }"
          size="lg"
        />

        <UForm
          :schema="
            v.object({
              rating: v.pipe(
                v.number(),
                v.integer(),
                v.minValue(1),
                v.maxValue(5),
              ),
              text: v.pipe(
                v.string('Please write your review'),
                v.minLength(10, 'Please write at least 10 characters'),
                v.maxLength(2000, 'Please write at most 2000 characters'),
              ),
            })
          "
          :state="form"
          class="space-y-6"
          @submit="onSubmit"
        >
          <UFormField label="Rating" name="rating">
            <StarRating
              v-model:rating="form.rating"
              clickable
              :star-size="24"
              @update:rating="form.rating = Math.ceil(form.rating)"
            />
          </UFormField>

          <UFormField label="Your Review" name="text">
            <UTextarea
              v-model="form.text"
              placeholder="Share your experience working with this partner..."
              :rows="6"
              autoresize
              class="w-full"
            />
          </UFormField>

          <div class="flex gap-3">
            <UButton type="submit" size="lg" :loading="submitting">
              Submit Review
            </UButton>
            <UButton
              variant="outline"
              size="lg"
              @click="navigateTo('/dashboard/reviews')"
            >
              Cancel
            </UButton>
          </div>
        </UForm>
      </div>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import * as v from 'valibot';
import type { UserPublic } from '~/generated/api';
import { usersReadUserById, reviewsCreateReview } from '~/generated/api';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});

const route = useRoute();
const toast = useToast();

const userId = computed(() => route.query.user_id as string);

const loading = ref(true);
const submitting = ref(false);
const reviewedUser = ref<UserPublic | null>(null);

const form = reactive({
  rating: 5,
  text: '',
});

async function loadUser() {
  if (!userId.value) {
    loading.value = false;
    return;
  }

  loading.value = true;
  const res = await usersReadUserById({
    path: {
      user_id: userId.value,
    },
  });
  loading.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to load user'),
      color: 'error',
    });
    return;
  }

  reviewedUser.value = res.data;
}

async function onSubmit() {
  if (!reviewedUser.value) return;

  submitting.value = true;
  const res = await reviewsCreateReview({
    body: {
      reviewed_user_id: reviewedUser.value.id,
      rating: form.rating,
      text: form.text,
    },
  });
  submitting.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to submit review'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Success',
    description: 'Your review has been submitted!',
    color: 'success',
  });

  navigateTo('/dashboard/reviews');
}

onMounted(() => {
  loadUser();
});
</script>
