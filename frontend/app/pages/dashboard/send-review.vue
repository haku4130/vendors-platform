<template>
  <UContainer class="max-w-2xl space-y-6">
    <div class="text-center">
      <h1 class="text-2xl font-semibold">Give Feedback</h1>
      <p class="text-muted mt-1">
        Tell us what you like and what we should improve about the vendor
        platform.
      </p>
    </div>

    <UCard class="shadow-sm">
      <template #default>
        <UForm :state="form" class="space-y-5" @submit="submit">
          <UFormField label="Rate your experience" name="rating" class="w-fit">
            <StarRating
              v-model:rating="form.rating"
              clickable
              :star-size="24"
              @update:rating="form.rating = Math.ceil(form.rating)"
            />
          </UFormField>

          <UFormField
            label="Feedback"
            name="message"
            help="Please be specific (min 10 chars)."
          >
            <UTextarea
              v-model="form.message"
              :rows="6"
              placeholder="What worked well? What didn't? Any missing features?"
              autoresize
              class="w-full"
            />
          </UFormField>

          <div class="flex items-center justify-end gap-2 pt-2">
            <UButton variant="ghost" type="button" @click="resetForm">
              Reset
            </UButton>
            <UButton :loading="submitting" type="submit">
              Send feedback
            </UButton>
          </div>
        </UForm>
      </template>
    </UCard>
  </UContainer>
</template>

<script setup lang="ts">
import type { HttpValidationError } from '~/generated/api';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});

const toast = useToast();
const route = useRoute();
const submitting = ref(false);

const form = reactive({
  rating: 5 as number,
  message: '' as string,
});

function resetForm() {
  form.rating = 5 as number;
  form.message = '';
}

async function submit() {
  const rating =
    form.rating === null || form.rating === undefined
      ? null
      : Number(form.rating);

  if (
    rating !== null &&
    (!Number.isFinite(rating) || rating < 1 || rating > 5)
  ) {
    toast.add({
      title: 'Invalid rating',
      description: 'Rating must be between 1 and 5.',
      color: 'error',
    });
    return;
  }

  if ((form.message ?? '').trim().length < 10) {
    toast.add({
      title: 'Feedback is too short',
      description: 'Please write at least 10 characters.',
      color: 'error',
    });
    return;
  }

  submitting.value = true;

  try {
    const config = useRuntimeConfig();
    const token = useCookie('access_token');

    const resp = await fetch(
      `${config.public.backendApiUrl}/api/v1/feedback/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: token.value ? `Bearer ${token.value}` : '',
        },
        body: JSON.stringify({
          rating,
          message: form.message.trim(),
          page_url: route.fullPath,
        }),
      },
    );

    if (!resp.ok) {
      let detail: unknown = null;
      try {
        detail = await resp.json();
      } catch {
        // ignore
      }
      toast.add({
        title: 'Error',
        description:
          typeof detail === 'object' && detail !== null && 'detail' in detail
            ? extractErrorMessage(detail as HttpValidationError)
            : 'Failed to send feedback',
        color: 'error',
      });
      return;
    }

    toast.add({
      title: 'Thank you!',
      description: 'Your feedback has been sent.',
      color: 'success',
    });
    resetForm();
  } catch (e) {
    console.error('Failed to send feedback', e);
    toast.add({
      title: 'Error',
      description: 'Failed to send feedback',
      color: 'error',
    });
  } finally {
    submitting.value = false;
  }
}
</script>
